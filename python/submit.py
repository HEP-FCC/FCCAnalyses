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


LOGGER = logging.getLogger('FCCAnalyses.submit')


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
