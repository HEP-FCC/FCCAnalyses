'''
Submit analysis to be run on remote machine(s).
'''

import os
import sys
import logging
import importlib
import argparse
import shutil
from typing import Any
from batch import send_to_batch


LOGGER = logging.getLogger('FCCAnalyses.submit')


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

    # Check if there are any processes defined
    if not hasattr(analysis_class, 'process_list'):
        LOGGER.error('Analysis does not define any processes!\n'
                     'Aborting...')
        sys.exit(3)
    config['process-list'] = analysis_class.process_list

    # Check if there is production tag or input directory defined
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

    if hasattr(analysis_class, 'prod_tag'):
        config['production-tag'] = analysis_class.prod_tag
    else:
        config['production-tag'] = None

    if hasattr(analysis_class, 'input_dir'):
        config['input-directory'] = analysis_class.input_dir
    else:
        config['input-directory'] = None

    return config


# _____________________________________________________________________________
def submit_analysis(parser: argparse.ArgumentParser) -> None:
    '''
    Sub-command entry point.
    '''

    args = parser.parse_args()

    # Check to where the analysis will be submitted.
    if args.where == 'ht-condor':
        # Check if HTCondor is available
        if shutil.which('condor_q') is None:
            LOGGER.error('HTCondor tools can\'t be found!\nAborting...')
            sys.exit(3)
        LOGGER.info('Submitting analysis to HTCondor...')

    elif args.where == 'slurm':
        LOGGER.error('Submission to the Slurm is not yet implemented!\n'
                     'Aborting...')
        sys.exit(3)
    elif args.where == 'grid':
        LOGGER.error('Submission to the GRID is not yet implemented!\n'
                     'Aborting...')
        sys.exit(3)

    config = {}
    config['cli-arguments'] = vars(args)

    # Work with absolute path of the analysis script.
    anapath = os.path.abspath(args.anascript_path)
    LOGGER.info('Loading analysis script from:\n  %s', anapath)

    # Check that the analysis file exists.
    if not os.path.isfile(anapath):
        LOGGER.error('Analysis script not found!\nAborting...')
        sys.exit(3)
    config['analysis-path'] = anapath

    # Load the analysis script as a module
    try:
        analysis_spec = importlib.util.spec_from_file_location('fccanalysis',
                                                               anapath)
        analysis_module = importlib.util.module_from_spec(analysis_spec)
        analysis_spec.loader.exec_module(analysis_module)
    except SyntaxError as err:
        LOGGER.error('Syntax error encountered in the analysis script:\n%s',
                     err)
        sys.exit(3)

    if hasattr(analysis_module, "Analysis"):
        config = merge_config_analysis_class(config, args, analysis_module)

    for process_name in config['process-list'].keys():
        LOGGER.info('Submitting process "%s"', process_name)

        send_to_batch(config, args, config['analysis-class'], process_name)
