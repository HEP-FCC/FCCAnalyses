'''
Submitting to the HTCondor batch system.
'''

import os
import sys
import time
import logging
import subprocess
import datetime
from typing import Any

from anascript import get_element, get_attribute
from process import get_process_info
from process import get_subfile_list, get_chunk_list


LOGGER = logging.getLogger('FCCAnalyses.batch')


# _____________________________________________________________________________
def determine_os(local_dir: str) -> str | None:
    '''
    Determines platform on which FCCAnalyses was compiled
    '''
    cmake_config_path = local_dir + '/build/CMakeFiles/CMakeConfigureLog.yaml'
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
                         process_name: str,
                         build_os: str | None,
                         rdf_module,
                         subjob_scripts: list[str]) -> str:
    '''
    Creates contents of HTCondor submit description file.
    '''
    cfg = 'executable       = $(scriptfile)\n'

    cfg += f'log              = {log_dir}/condor_job.{process_name}.'
    cfg += '$(ClusterId).log\n'

    cfg += f'output           = {log_dir}/condor_job.{process_name}.'
    cfg += '$(ClusterId).$(ProcId).out\n'

    cfg += f'error            = {log_dir}/condor_job.{process_name}.'
    cfg += '$(ClusterId).$(ProcId).error\n'

    cfg += 'getenv           = False\n'

    cfg += f'environment      = "LS_SUBCWD={log_dir}"\n'  # not sure

    cfg += 'requirements     = ( '
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

    cfg += '+JobFlavour      = "%s"\n' % get_element(rdf_module, 'batch_queue')

    cfg += '+AccountingGroup = "%s"\n' % get_element(rdf_module, 'comp_group')

    cfg += f'RequestCpus      = {config["n-threads"]}\n'

    cfg += 'should_transfer_files = yes\n'
    cfg += 'when_to_transfer_output = on_exit\n'

    cfg += 'transfer_output_files = $(outfile)\n\n'

    # add user batch configuration if any
    user_batch_config = get_attribute(rdf_module, 'user_batch_config', None)
    if user_batch_config is not None:
        if not os.path.isfile(user_batch_config):
            LOGGER.warning('userBatchConfig file can\'t be found! Will not '
                           'add it to the default config.')
        else:
            with open(user_batch_config, 'r', encoding='utf-8') as cfgfile:
                for line in cfgfile:
                    cfg += line + '\n'
        cfg += '\n\n'

    output_dir = get_attribute(rdf_module, 'output_dir', None)
    output_path = os.path.join(output_dir, process_name)
    cfg += 'queue scriptfile, outfile from (\n'
    for idx, scriptfile in enumerate(subjob_scripts):
        cfg += f'    {scriptfile}, {output_path}/chunk_{idx}.root\n'
    cfg += ')\n'

    return cfg


# _____________________________________________________________________________
def create_subjob_script(config: dict[str, Any],
                         local_dir: str,
                         analysis,
                         process_name: str,
                         chunk_num: int,
                         chunk_list: list[list[str]],
                         anapath: str,
                         cmd_args) -> str:
    '''
    Creates sub-job script to be run.
    '''

    output_dir = get_attribute(analysis, 'output_dir', None)

    scr = '#!/bin/bash\n\n'
    scr += 'source ' + local_dir + '/setup.sh\n\n'

    # scr += f'mkdir job_{process_name}_chunk_{chunk_num}\n'
    # scr += f'cd job_{process_name}_chunk_{chunk_num}\n\n'

    output_path = os.path.join(output_dir, process_name,
                               f'chunk_{chunk_num}.root')

    scr += 'which fccanalysis\n'
    # scr += local_dir
    scr += f'fccanalysis run {anapath}'
    scr += f' --output {output_path}'
    if hasattr(analysis, 'n_threads'):
        scr += f' --n-threads {config["n-threads"]}'
    if len(cmd_args.remaining) > 0:
        scr += ' ' + ' '.join(cmd_args.unknown)
    scr += ' --files-list'
    for file_path in chunk_list[chunk_num]:
        scr += f' {file_path}'
    scr += '\n\n'

    # output_dir_eos = get_attribute(analysis, 'output_dir_eos', None)
    # if not os.path.isabs(output_dir) and output_dir_eos is None:
    #     final_dest = os.path.join(local_dir, output_dir, process_name,
    #                               f'chunk_{chunk_num}.root')
    #     scr += f'cp {output_path} {final_dest}\n'

    # if output_dir_eos is not None:
    #     eos_type = get_attribute(analysis, 'eos_type', 'eospublic')

    #     final_dest = os.path.join(output_dir_eos,
    #                               process_name,
    #                               f'chunk_{chunk_num}.root')
    #     final_dest = f'root://{eos_type}.cern.ch/' + final_dest
    #     scr += f'xrdcp {output_path} {final_dest}\n'

    scr += f'ls -alh {output_path}\n'
    scr += 'pwd\n'
    scr += f'find "$PWD" -name *.root\n'

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
def send_to_batch(config: dict[str, Any],
                  args, analysis,
                  sample_name: str) -> None:
    '''
    Send jobs to HTCondor batch system.
    '''
    sample_dict = config['process-list'][sample_name]

    local_dir = os.environ['LOCAL_DIR']
    current_date = datetime.datetime.fromtimestamp(
        datetime.datetime.now().timestamp()).strftime('%Y-%m-%d_%H-%M-%S')
    log_dir = os.path.join('BatchOutputs', current_date, sample_name)
    if not os.path.exists(log_dir):
        os.system(f'mkdir -p {log_dir}')

    # Making sure the FCCAnalyses libraries are compiled and installed
    try:
        subprocess.check_output(['make', 'install'],
                                cwd=local_dir+'/build',
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
    for ch_num in range(len(chunk_list)):
        subjob_script_path = os.path.join(
            log_dir,
            f'job_{sample_name}_chunk_{ch_num}.sh')
        subjob_scripts.append(subjob_script_path)

        for i in range(3):
            try:
                with open(subjob_script_path, 'w', encoding='utf-8') as ofile:
                    subjob_script = create_subjob_script(config,
                                                         local_dir,
                                                         analysis,
                                                         sample_name,
                                                         ch_num,
                                                         chunk_list,
                                                         config['analysis-path'],
                                                         args)
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
                                                     determine_os(local_dir),
                                                     analysis,
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

    batch_cmd = f'condor_submit -spool {condor_config_path}'
    LOGGER.info('Batch command:\n  %s', batch_cmd)
    # success = submit_job(batch_cmd, 10)
    # if not success:
    #     sys.exit(3)
