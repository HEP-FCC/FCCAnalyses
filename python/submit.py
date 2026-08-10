'''
Submit analysis to be run on remote machine(s).
'''

import os
import sys
import logging
import importlib
import argparse
import shutil
from batch import send_to_batch
from grid_submission import GridSubmissionError, submit_grid_submission


LOGGER = logging.getLogger('FCCAnalyses.submit')


# _____________________________________________________________________________
def _parse_submit_arguments(parser: argparse.ArgumentParser) -> argparse.Namespace:
    '''Parse submission arguments and preserve grid worker arguments after --.'''
    preliminary_args, _ = parser.parse_known_args()
    if preliminary_args.where != 'grid' or '--' not in sys.argv:
        args = parser.parse_args()
        if args.where == 'grid':
            args.remaining = []
        return args

    separator_index = sys.argv.index('--')
    args = parser.parse_args(sys.argv[1:separator_index])
    args.remaining = sys.argv[separator_index + 1:]
    return args


# _____________________________________________________________________________
def submit_analysis(parser: argparse.ArgumentParser) -> None:
    '''
    Sub-command entry point.
    '''

    args = _parse_submit_arguments(parser)

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
        try:
            submit_grid_submission(args)
        except GridSubmissionError as error:
            LOGGER.error('%s\nAborting...', error)
            sys.exit(3)
        return

    # Work with absolute path of the analysis script.
    anapath = os.path.abspath(args.anascript_path)
    LOGGER.info('Loading analysis script from:\n  %s', anapath)

    # Check that the analysis file exists.
    if not os.path.isfile(anapath):
        LOGGER.error('Analysis script not found!\nAborting...')
        sys.exit(3)

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

    if args.where == 'ht-condor':
        send_to_batch(args, analysis_module)
