import os
import sys
import logging
import argparse
import subprocess
import shutil

LOGGER = logging.getLogger('FCCAnalyses.fit')

def run_fit(parser: argparse.ArgumentParser) -> None:
    """Sub-command entry point for object-oriented fitting configurations."""
    args = parser.parse_args()
    
    anapath = os.path.abspath(args.script_path)
    output_path = args.output
    backend = args.backend.lower()

    LOGGER.info('Steering fit configuration towards the "%s" backend...', backend)

    if backend == 'combine':
        from combine import generate_datacard
        generate_datacard(anapath, output_path)
        
        # If the user requested live execution
        if args.execute:
            if shutil.which('combine') is None:
                LOGGER.error('The "combine" command-line tool cannot be found in your current environment path!\n'
                             'Please ensure you have sourced your Combine workspace before running execution.')
                sys.exit(6)
                
            LOGGER.info('Launching Combine statistical engine execution on: %s', output_path)
            try:
                # Executes the single-line combine limit calculation command
                subprocess.run(['combine', '-M', 'AsymptoticLimits', output_path], check=True)
            except subprocess.CalledProcessError as e:
                LOGGER.error('Combine statistical fitting execution failed! Error code: %s', e.returncode)
                sys.exit(7)
                
    elif backend == 'pyhf':
        LOGGER.error('Backend "pyhf" is planned but not yet implemented! Aborting...')
        sys.exit(5)
