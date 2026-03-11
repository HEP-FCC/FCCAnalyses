'''
Submitting to the HTCondor batch system.
'''

import os
import sys
import time
import logging
import subprocess
import datetime
import argparse
import string
from typing import Any

from process import get_process_info
from process import get_subfile_list, get_chunk_list

LOGGER = logging.getLogger('FCCAnalyses.batch')

# _____________________________________________________________________________
def determine_os(fccana_dir: str) -> str | None:
    '''
    Determines platform on which FCCAnalyses was compiled
    '''
    if fccana_dir is None:
        try:
            with open('/etc/system-release-cpe', 'r',
                      encoding='utf-8') as os_info_file:
                os_info = os_info_file.read()

            if 'redhat:enterprise_linux:9' in os_info:
                return 'almalinux9'
        except FileNotFoundError:
            # Fallback for non-RHEL systems (Arch, Ubuntu, macOS)
            pass

        return None
# _____________________________________________________________________________

def create_condor_submit(config: dict[str, Any],  batch_dir: str, sample_name: str, subjob_scripts: list[str],output_dir_eos: str | None) -> Any:
    '''
    Creates HTCondor submit object.
    '''
    import htcondor
    
    submit_dict = {
        "executable": "$(scriptfile)",
        "log": f"{batch_dir}/condor_job.{sample_name}.$(ClusterId).log",
        "getenv": "False",
        "max_retries": "3",
        "RequestCpus": str(config["n-threads"]),
        "should_transfer_files": "yes",
        "when_to_transfer_output": "on_exit",
        "transfer_output_files": sample_name,
        "+JobFlavour": f'"{config["batch-queue"]}"',
        "+AccountingGroup": f'"{config["accounting-group"]}"',
    }

    # Handle OS
    build_os = determine_os(config['fccana-dir'])
    if build_os == 'centos7':
        submit_dict['MY.WantOS'] = 'el7'
    elif build_os == 'almalinux9':
        submit_dict['MY.WantOS'] = 'el9'

    # Handle Logs/Output
    if output_dir_eos is None:
        log_base = f"{config['output-dir']}/log/{sample_name}/condor_job.{sample_name}.$(ClusterId).$(ProcId)"
        submit_dict["output"] = f"{log_base}.out"
        submit_dict["error"] = f"{log_base}.error"
        submit_dict["transfer_output_remaps"] = f'"{sample_name}={config["output-dir"]}/{sample_name}"'
    else:
        log_base = f"log/{sample_name}/condor_job.{sample_name}.$(ClusterId).$(ProcId)"
        submit_dict["output"] = f"{log_base}.out"
        submit_dict["error"] = f"{log_base}.error"
        submit_dict["output_destination"] = f"root://{config['eos-type']}.cern.ch/{output_dir_eos}"
        submit_dict["MY.XRDCP_CREATE_DIR"] = "True"

    # Merge user custom config strings if they exist
    sub = htcondor.Submit(submit_dict)
    if config['user-batch-config'] is not None:
        with open(config['user-batch-config'], 'r', encoding='utf-8') as cfile:
            for line in cfile:
                if line.strip() and not line.startswith('#'):
                    sub.append(line.strip())

    sub.set_iterable("scriptfile", subjob_scripts)
    return sub

def create_subjob_script(config: dict[str, Any],
                         sample_name: str,
                         chunk_list: list[list[str]],
                         chunk_num: int) -> str:
    '''
    Creates sub-job script to be run.
    '''
    sample_output_filepath = os.path.join(sample_name,
                                          f'chunk_{chunk_num}.root')

    scr = '#!/bin/bash\n\n'
    scr += f'source {config["key4hep-stack"]}\n'
    if config['fccana-dir'] is not None:
        scr += f'source {config["fccana-dir"]}/setup.sh\n\n'

    scr += f'mkdir -p {sample_name}\n\n'
    scr += f'fccanalysis run {config["full-analysis-path"]}'
    scr += f' --output {sample_output_filepath}'
    scr += f' --n-threads {config["n-threads"]}'
    scr += ' --input'
    for file_path in chunk_list[chunk_num]:
        scr += f' {file_path}'
    if len(config['cli-arguments']['remaining']) > 0:
        scr += ' -- ' + ' '.join(config['cli-arguments']['remaining'])
    scr += '\n'

    return scr

# _____________________________________________________________________________

def submit_job(sub: Any, spool: bool, max_trials: int) -> bool:
    '''
    Submit job to HTCondor using the native Python API.
    '''
    import htcondor
    schedd = htcondor.Schedd()
    for i in range(max_trials):
        try:
            # Native submission returns a ClusterID object
            with schedd.transaction() as txn:
                cluster_id = sub.queue(txn)
            
            # If we are on EOS, we MUST spool the files to the schedd
            if spool:
                schedd.spool(sub.jobs(cluster_id))
                
            LOGGER.info('Submission successful. ClusterId: %s', cluster_id)
            return True
            
        except Exception as e:
            if i < max_trials - 1:
                LOGGER.warning('Submission failed, retrying... Trial: %i / %i. Error: %s', 
                               i + 1, max_trials, e)
                time.sleep(10)
            else:
                LOGGER.error('Critical: Failed submitting after %i trials. Error: %s', 
                             max_trials, e)
    return False

# _____________________________________________________________________________
def merge_config_analysis_class(config: dict[str, Any],
                                args: argparse.Namespace,
                                analysis_module: Any) -> dict[str, Any]:
    '''
    Merge configuration from the analysis script class and the command-line
    arguments.
    '''
    analysis_class = analysis_module.Analysis(vars(args))
    config['analysis-class'] = analysis_class

    if not hasattr(analysis_class, 'process_list'):
        LOGGER.error('Analysis does not define any processes!\nAborting...')
        sys.exit(3)
    config['sample-list'] = analysis_class.process_list
    if not config['sample-list']:
        LOGGER.error('Analysis does not define any processes!\nAborting...')
        sys.exit(3)

    if not hasattr(analysis_class, 'prod_tag') and not hasattr(analysis_class, 'input_dir'):
        LOGGER.error('Analysis does not define production tag or input directory!\nAborting...')
        sys.exit(3)

    if hasattr(analysis_class, 'prod_tag') and hasattr(analysis_class, 'input_dir'):
        LOGGER.error('Analysis defines both production tag and input directory!\nAborting...')
        sys.exit(3)

    if hasattr(analysis_class, 'prod_tag'):
        config['production-tag'] = analysis_class.prod_tag
    else:
        config['production-tag'] = None

    if hasattr(analysis_class, 'input_dir'):
        config['input-directory'] = analysis_class.input_dir
    else:
        config['input-directory'] = None

    if hasattr(analysis_class, 'n_threads'):
        config['n-threads'] = analysis_class.n_threads
    else:
        config['n-threads'] = 1

    if hasattr(analysis_class, 'batch_queue'):
        config['batch-queue'] = analysis_class.batch_queue
    else:
        config['batch-queue'] = 'longlunch'

    if hasattr(analysis_class, 'comp_group'):
        config['accounting-group'] = analysis_class.comp_group
    else:
        config['accounting-group'] = 'group_u_FCC.local_gen'

    config['user-batch-config'] = None
    if hasattr(analysis_class, 'user_batch_config'):
        if not os.path.isfile(analysis_class.user_batch_config):
            LOGGER.warning('Provided file with additional job description parameters can\'t be found!\nFile path: %s\nContinuing...', analysis_class.user_batch_config)
        else:
            config['user-batch-config'] = analysis_class.user_batch_config

    config['output-dir'] = None
    if hasattr(analysis_class, 'output_dir'):
        config['output-dir'] = analysis_class.output_dir
    if os.path.isabs(config['output-dir']):
        LOGGER.error('Provided output directory path is absolute (starts with `/`)!\nPlease, use relative path for the output directory.\nAborting...')
        sys.exit(3)

    config['output-dir-eos'] = None
    if hasattr(analysis_class, 'output_dir_eos'):
        config['output-dir-eos'] = analysis_class.output_dir_eos
    else:
        if config['submission-filesystem-type'] == 'eos':
            LOGGER.error('Submission to CERN\'s HTCondor from EOS requires "output_dir_eos" analysis attribute defined!\nAborting...')
            sys.exit(3)

    config['eos-type'] = None
    if hasattr(analysis_class, 'eos_type'):
        config['eos-type'] = analysis_class.eos_type
    else:
        config['eos-type'] = 'eosuser'

    return config

# _____________________________________________________________________________
def send_sample(config: dict[str, Any], sample_name: str) -> None:
    '''
    Send sample to HTCondor batch system.
    '''
    sample_dict = config['sample-list'][sample_name]
    timestamp = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%Y-%m-%d_%H-%M-%S')

    batch_dir = os.path.join('batch-submission-files', timestamp, sample_name)
    if not os.path.exists(batch_dir):
        os.system(f'mkdir -p {batch_dir}')

    fraction = 1.
    if 'fraction' in sample_dict:
        fraction = sample_dict['fraction']

    chunks = 1
    if 'chunks' in sample_dict:
        chunks = sample_dict['chunks']

    dataset_input_dir = None
    if 'input_dir' in sample_dict:
        dataset_input_dir = sample_dict['input_dir']
    if 'input-dir' in sample_dict:
        dataset_input_dir = sample_dict['input-dir']

    file_list, event_list = get_process_info(sample_name, config['production-tag'], config['input-directory'])

    if len(file_list) <= 0:
        LOGGER.error('No files to process!\nContinuing...')
        return

    if fraction < 1.:
        file_list = get_subfile_list(file_list, event_list, fraction)

    chunk_list = [file_list]
    if chunks > 1:
        chunk_list = get_chunk_list(file_list, chunks)
    else:
        LOGGER.warning('Number of requested output chunks for the sample "%s" is suspiciously low!', sample_name)

    subjob_scripts = []
    for chunk_num in range(len(chunk_list)):
        subjob_script_path = os.path.join(batch_dir, f'job_{sample_name}_chunk_{chunk_num}.sh')
        subjob_scripts.append(subjob_script_path)

        for i in range(3):
            try:
                with open(subjob_script_path, 'w', encoding='utf-8') as ofile:
                    subjob_script = create_subjob_script(config, sample_name, chunk_list, chunk_num)
                    ofile.write(subjob_script)
            except IOError as err:
                if i < 2:
                    LOGGER.warning('I/O error(%i): %s', err.errno, err.strerror)
                else:
                    LOGGER.error('I/O error(%i): %s', err.errno, err.strerror)
                    sys.exit(3)
            else:
                break
            time.sleep(10)
        subprocess.getstatusoutput(f'chmod u+x {subjob_script_path}')

    LOGGER.debug('Sub-job scripts to be run:\n - %s', '\n - '.join(subjob_scripts))

    condor_config_path = f'{batch_dir}/job_desc_{sample_name}.cfg'

    if isinstance(config['output-dir-eos'], string.Template):
        output_dir_eos = config['output-dir-eos'].substitute(timestamp=timestamp)
    else:
        output_dir_eos = config['output-dir-eos']

    if output_dir_eos is not None and not os.path.exists(output_dir_eos):
        os.system(f'mkdir -p {output_dir_eos}')

    sub = create_condor_submit(config, batch_dir, sample_name, subjob_scripts, output_dir_eos)

    spool = (config["submission-filesystem-type"] == "eos")
    if spool:
         LOGGER.warning("To download the log files use \"condor_transfer_data\" command!")

    max_trials = 3
    success = submit_job(sub, spool, max_trials)
    if not success:
        LOGGER.error('Failed submitting after: %i trials!\nAborting...', max_trials)
        sys.exit(3)

# _____________________________________________________________________________
def send_to_batch(args: argparse.Namespace, analysis_module: Any) -> None:
    '''
    Send jobs to HTCondor batch system.
    '''
    config: dict[str, Any] = {}
    config['cli-arguments'] = vars(args)
    config['analysis-path'] = args.anascript_path
    config['full-analysis-path'] = os.path.abspath(args.anascript_path)

    config['fccana-dir'] = None
    if 'FCCANA_LOCAL_DIR' in os.environ:
        config['fccana-dir'] = os.environ['FCCANA_LOCAL_DIR']

    config['key4hep-stack'] = os.environ['KEY4HEP_STACK']
    config['current-working-directory'] = os.getcwd()

    if os.getcwd().startswith('/eos/'):
        config['submission-filesystem-type'] = 'eos'
    elif os.getcwd().startswith('/afs/'):
        config['submission-filesystem-type'] = 'afs'
    else:
        config['submission-filesystem-type'] = 'unknown'

    if config['fccana-dir'] is not None:
        try:
            subprocess.check_output(['make', 'install'], cwd=config['fccana-dir']+'/build', stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            LOGGER.error('The FCCanalyses libraries are not properly build and installed!\nAborting job submission(s)...')
            sys.exit(3)

    if hasattr(analysis_module, "Analysis"):
        config = merge_config_analysis_class(config, args, analysis_module)

    for sample_name in config['sample-list'].keys():
        LOGGER.info('Submitting sample "%s"', sample_name)
        send_sample(config, sample_name)
