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
from typing import Any

from process import get_process_info
from process import get_subfile_list, get_chunk_list


LOGGER = logging.getLogger('FCCAnalyses.batch')


# _____________________________________________________________________________
def determine_os(fccana_dir: str) -> str | None:
    '''
    Determines platform on which FCCAnalyses was compiled
    '''
    cmake_config_path = fccana_dir + '/build/CMakeFiles/CMakeConfigureLog.yaml'
    if not os.path.isfile(cmake_config_path):
        LOGGER.warning('CMake configuration file was not found!\n'
                       'Was FCCAnalyses properly build?')
        return None

    with open(cmake_config_path, 'r', encoding='utf-8') as cmake_config_file:
        cmake_config = cmake_config_file.read()
        if 'centos7' in cmake_config:
            return 'centos7'
        if 'almalinux9' in cmake_config:
            return 'almalinux9'

    return None


# _____________________________________________________________________________
def create_condor_config(config: dict[str, Any],
                         log_dir: str,
                         sample_name: str,
                         subjob_scripts: list[str]) -> str:
    '''
    Creates contents of HTCondor submit description file.
    '''
    cfg = 'executable       = $(scriptfile)\n'

    cfg += f'log              = {log_dir}/condor_job.{sample_name}.'
    cfg += '$(ClusterId).log\n'

    cfg += f'output           = {log_dir}/condor_job.{sample_name}.'
    cfg += '$(ClusterId).$(ProcId).out\n'

    cfg += f'error            = {log_dir}/condor_job.{sample_name}.'
    cfg += '$(ClusterId).$(ProcId).error\n'

    cfg += 'getenv           = False\n'

    cfg += f'environment      = "LS_SUBCWD={log_dir}"\n'  # not sure

    cfg += 'requirements     = ( '
    build_os = determine_os(config['fccana-dir'])
    if build_os == 'centos7':
        cfg += '(OpSysAndVer =?= "CentOS7") && '
    if build_os == 'almalinux9':
        cfg += '(OpSysAndVer =?= "AlmaLinux9") && '
    if build_os is None:
        LOGGER.warning('Submitting jobs to default operating system. There '
                       'may be compatibility issues.')
    cfg += '(Machine =!= LastRemoteHost) && (TARGET.has_avx2 =?= True) )\n'

    cfg += 'on_exit_remove   = (ExitBySignal == False) && (ExitCode == 0)\n'

    cfg += 'max_retries      = 3\n'

    cfg += f'+JobFlavour      = "{config["batch_queue"]}"\n'

    cfg += f'+AccountingGroup = "{config["accounting-group"]}"\n'

    cfg += f'RequestCpus      = {config["n-threads"]}\n'

    cfg += 'should_transfer_files = yes\n'
    cfg += 'when_to_transfer_output = on_exit\n'

    cfg += 'transfer_output_files = $(outfile)\n\n'

    # Add user batch configuration if any.
    if config['user-batch-config'] is not None:
        with open(config['user-batch-config'], 'r', encoding='utf-8') as cfile:
            for line in cfile:
                cfg += line + '\n'
        cfg += '\n\n'

    sample_output_dir = os.path.join(config['output-dir'], sample_name)
    cfg += 'queue scriptfile, outfile from (\n'
    for idx, scriptfile in enumerate(subjob_scripts):
        cfg += f'    {scriptfile}, {sample_output_dir}/chunk_{idx}.root\n'
    cfg += ')\n'

    return cfg


# _____________________________________________________________________________
def create_subjob_script(config: dict[str, Any],
                         sample_name: str,
                         chunk_list: list[list[str]],
                         chunk_num: int) -> str:
    '''
    Creates sub-job script to be run.
    '''

    sample_output_filepath = os.path.join(config['output-dir'],
                                          sample_name,
                                          f'chunk_{chunk_num}.root')

    scr = '#!/bin/bash\n\n'

    scr += f'source {config["fccana-dir"]}/setup.sh\n\n'

    scr += 'which fccanalysis\n\n'

    scr += f'fccanalysis run {config["analysis-path"]}'
    scr += f' --output {sample_output_filepath}'
    scr += f' --n-threads {config["n-threads"]}'
    scr += ' --files-list'
    for file_path in chunk_list[chunk_num]:
        scr += f' {file_path}'
    if len(config['cli-arguments']['remaining']) > 0:
        scr += ' -- ' + ' '.join(config['cli-arguments']['remaining'])
    scr += '\n\n'

    # output_dir_eos = get_attribute(analysis, 'output_dir_eos', None)
    # if not os.path.isabs(output_dir) and output_dir_eos is None:
    #     final_dest = os.path.join(fccana_dir, output_dir, sample_name,
    #                               f'chunk_{chunk_num}.root')
    #     scr += f'cp {output_path} {final_dest}\n'

    # if output_dir_eos is not None:
    #     eos_type = get_attribute(analysis, 'eos_type', 'eospublic')

    #     final_dest = os.path.join(output_dir_eos,
    #                               sample_name,
    #                               f'chunk_{chunk_num}.root')
    #     final_dest = f'root://{eos_type}.cern.ch/' + final_dest
    #     scr += f'xrdcp {output_path} {final_dest}\n'

    scr += f'ls -alh {sample_output_filepath}\n'
    scr += 'pwd\n'
    scr += 'find "$PWD" -name *.root\n'

    return scr


# _____________________________________________________________________________
def submit_job(cmd: str, max_trials: int) -> bool:
    '''
    Submit job to condor, retry `max_trials` times.
    '''
    for i in range(max_trials):
        with subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True) as proc:
            (stdout, stderr) = proc.communicate()

            if proc.returncode == 0 and len(stderr) == 0:
                LOGGER.info(stdout)
                LOGGER.info('GOOD SUBMISSION')
                return True

            LOGGER.warning('Error while submitting, retrying...\n  '
                           'Trial: %i / %i\n  Error: %s',
                           i, max_trials, stderr)
            time.sleep(10)

    LOGGER.error('Failed submitting after: %i trials!', max_trials)
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

    # Check if there are any processes defined.
    if not hasattr(analysis_class, 'process_list'):
        LOGGER.error('Analysis does not define any processes!\n'
                     'Aborting...')
        sys.exit(3)
    config['sample-list'] = analysis_class.process_list

    # Check if there is production tag or input directory defined.
    if not hasattr(analysis_class, 'prod_tag') and \
       not hasattr(analysis_class, 'input_dir'):
        LOGGER.error('Analysis does not define production tag or input '
                     'directory!\nAborting...')
        sys.exit(3)

    if hasattr(analysis_class, 'prod_tag') and \
       hasattr(analysis_class, 'input_dir'):
        LOGGER.error('Analysis defines both production tag and input '
                     'directory!\nAborting...')
        sys.exit(3)

    # Determine input.
    if hasattr(analysis_class, 'prod_tag'):
        config['production-tag'] = analysis_class.prod_tag
    else:
        config['production-tag'] = None

    if hasattr(analysis_class, 'input_dir'):
        config['input-directory'] = analysis_class.input_dir
    else:
        config['input-directory'] = None

    # Determine number of threads to run in.
    if hasattr(analysis_class, 'n_threads'):
        config['n-threads'] = analysis_class.n_threads
    else:
        config['n-threads'] = 1

    # Determine batch queue.
    if hasattr(analysis_class, 'batch_queue'):
        config['batch-queue'] = analysis_class.batch_queue
    else:
        config['batch_queue'] = 'longlunch'

    # Determine accounting group.
    if hasattr(analysis_class, 'comp_group'):
        config['accounting-group'] = analysis_class.comp_group
    else:
        config['accounting-group'] = 'group_u_FCC.local_gen'

    # Check if user provided additional job description parameters.
    config['user-batch-config'] = None
    if hasattr(analysis_class, 'user_batch_config'):
        if not os.path.isfile(analysis_class.user_batch_config):
            LOGGER.warning('Provided file with additional job description '
                           'parameters can\'t be found!\nFile path: %s\n'
                           'Continuing...', analysis_class.user_batch_config)
        else:
            config['user-batch-config'] = analysis_class.user_batch_config

    # Check for global output directory.
    config['output-dir'] = None
    if hasattr(analysis_class, 'output_dir'):
        config['output-dir'] = analysis_class.output_dir
        os.system(f'mkdir -p {config["output-dir"]}')

    # Check if EOS output dir is defined.
    config['output-dir-eos'] = None
    if hasattr(analysis_class, 'output_dir_eos'):
        config['output-dir-eos'] = analysis_class.output_dir_eos
    else:
        if config['submission-filesystem-type'] == 'eos':
            LOGGER.error('Submission to CERN\'s HTCondor from requires that '
                         '"output_dir_eos" analysis attribute is defined!\n'
                         'Aborting...')
            sys.exit(3)

    return config


# _____________________________________________________________________________
def send_sample(config: dict[str, Any],
                sample_name: str) -> None:
    '''
    Send sample to HTCondor batch system.
    '''
    sample_dict = config['sample-list'][sample_name]

    # Create log directory
    current_date = datetime.datetime.fromtimestamp(
        datetime.datetime.now().timestamp()).strftime('%Y-%m-%d_%H-%M-%S')
    log_dir = os.path.join('BatchOutputs', current_date, sample_name)
    if not os.path.exists(log_dir):
        os.system(f'mkdir -p {log_dir}')

    # Making sure the FCCAnalyses libraries are compiled and installed
    try:
        subprocess.check_output(['make', 'install'],
                                cwd=config['fccana-dir']+'/build',
                                stderr=subprocess.DEVNULL
                                )
    except subprocess.CalledProcessError:
        LOGGER.error('The FCCanalyses libraries are not properly build and '
                     'installed!\nAborting job submission...')
        sys.exit(3)

    # Determine the fraction of the input to be processed
    fraction = 1.
    if 'fraction' in sample_dict:
        fraction = sample_dict['fraction']

    # Determine the number of chunks the output will be split into
    chunks = 1
    if 'chunks' in sample_dict:
        chunks = sample_dict['chunks']

    file_list, event_list = get_process_info(sample_name,
                                             config['production-tag'],
                                             config['input-directory'])

    if len(file_list) <= 0:
        LOGGER.error('No files to process!\nContinuing...')
        return

    # Adjust number of input files according to the fraction requirement
    if fraction < 1.:
        file_list = get_subfile_list(file_list, event_list, fraction)

    # Adjust number of output files according to the chunk requirement
    chunk_list = [file_list]
    if chunks > 1:
        chunk_list = get_chunk_list(file_list, chunks)
    else:
        LOGGER.warning('Number of requested output chunks for the sample '
                       '"%s" is suspiciously low!', sample_name)

    subjob_scripts = []
    for chunk_num in range(len(chunk_list)):
        subjob_script_path = os.path.join(
            log_dir,
            f'job_{sample_name}_chunk_{chunk_num}.sh')
        subjob_scripts.append(subjob_script_path)

        for i in range(3):
            try:
                with open(subjob_script_path, 'w', encoding='utf-8') as ofile:
                    subjob_script = create_subjob_script(config,
                                                         sample_name,
                                                         chunk_list,
                                                         chunk_num)
                    ofile.write(subjob_script)
            except IOError as err:
                if i < 2:
                    LOGGER.warning('I/O error(%i): %s',
                                   err.errno, err.strerror)
                else:
                    LOGGER.error('I/O error(%i): %s', err.errno, err.strerror)
                    sys.exit(3)
            else:
                break
            time.sleep(10)
        subprocess.getstatusoutput(f'chmod u+x {subjob_script_path}')

    LOGGER.debug('Sub-job scripts to be run:\n - %s',
                 '\n - '.join(subjob_scripts))

    condor_config_path = f'{log_dir}/job_desc_{sample_name}.cfg'

    for i in range(3):
        try:
            with open(condor_config_path, 'w', encoding='utf-8') as cfgfile:
                condor_config = create_condor_config(config,
                                                     log_dir,
                                                     sample_name,
                                                     subjob_scripts)
                cfgfile.write(condor_config)
        except IOError as err:
            LOGGER.warning('I/O error(%i): %s', err.errno, err.strerror)
            if i == 2:
                sys.exit(3)
        else:
            break
        time.sleep(10)
    # subprocess.getstatusoutput(f'chmod u+x {condor_config_path}')

    if config['submission-filesystem-type'] == 'eos':
        batch_cmd = f'condor_submit -spool {condor_config_path}'
    else:
        batch_cmd = f'condor_submit {condor_config_path}'
    LOGGER.info('Batch command:\n  %s', batch_cmd)
    success = submit_job(batch_cmd, 10)
    if not success:
        sys.exit(3)


# _____________________________________________________________________________
def send_to_batch(args: argparse.Namespace,
                  analysis_module: Any) -> None:
    '''
    Send jobs to HTCondor batch system.
    '''

    config: dict[str, Any] = {}
    config['cli-arguments'] = vars(args)
    config['analysis-path'] = args.anascript_path
    config['full-analysis-path'] = os.path.abspath(args.anascript_path)

    # Find location of the FCCanalyses directory
    # TODO: Rename LOCAL_DIR to FCCANA_DIR
    config['fccana-dir'] = os.environ['LOCAL_DIR']

    # Get current working directory
    config['current-working-directory'] = os.getcwd()

    # Determine type of filesystem the submission is made from
    if os.getcwd().startswith('/eos/'):
        config['submission-filesystem-type'] = 'eos'
    elif os.getcwd().startswith('/afs/'):
        config['submission-filesystem-type'] = 'afs'
    else:
        config['submission-filesystem-type'] = 'unknown'

    if hasattr(analysis_module, "Analysis"):
        config = merge_config_analysis_class(config, args, analysis_module)

    for sample_name in config['sample-list'].keys():
        LOGGER.info('Submitting sample "%s"', sample_name)

        send_sample(config, sample_name)
