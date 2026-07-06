import os
import sys
import logging
import argparse
import subprocess
import shutil

LOGGER = logging.getLogger('FCCAnalyses.fit')

def run_fit(parser: argparse.ArgumentParser) -> None:
    """Sub-command entry point for object-oriented fitting configurations."""
    
    # parse_known_args splits recognized flags from extra forwarding flags
    args, tool_args = parser.parse_known_args()

    anapath = os.path.abspath(args.script_path)
    output_path = args.output
    backend = args.backend.lower()

    LOGGER.info('Steering fit configuration towards the "%s" backend...', backend)

    if backend == 'combine':
        from combine import generate_datacard
        generate_datacard(anapath, output_path)

        if args.execute:
            if shutil.which('combine') is None:
                LOGGER.error('The "combine" command-line tool cannot be found...')
                sys.exit(6)

            LOGGER.info('Launching Combine statistical engine execution on: %s', output_path)
            try:
                # 1. Start with the clean, default framework command
                base_command = ['combine', '-M', 'AsymptoticLimits', output_path]
                
                # 2. Append whatever the user passed after the '--'
                full_command = base_command + tool_args

                subprocess.run(full_command, check=True)
                
            except subprocess.CalledProcessError as e:
                LOGGER.error('Combine statistical fitting execution failed!')
                sys.exit(7)
