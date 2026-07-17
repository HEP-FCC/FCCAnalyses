import os
import sys
import logging
import argparse
import subprocess
import shutil
import glob  # <--- Added for tracking output ROOT files

LOGGER = logging.getLogger('FCCAnalyses.fit')

def run_fit(parser: argparse.ArgumentParser) -> None:
    """Sub-command entry point for object-oriented fitting configurations."""
    
    args, tool_args = parser.parse_known_args()

    anapath = os.path.abspath(args.script_path)
    output_path = args.output
    backend = args.backend.lower()

    LOGGER.info('Steering fit configuration towards the "%s" backend...', backend)
    
    output_dir = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(output_dir, exist_ok=True)

    if backend == 'combine':
        from combine import generate_datacard
        generate_datacard(anapath, output_path)

        if args.execute:
            if shutil.which('combine') is None:
                LOGGER.error('The "combine" command-line tool cannot be found...')
                sys.exit(6)

            LOGGER.info('Launching Combine statistical engine execution on: %s', output_path)
            try:
                # 1. Strip the '--' separator if present
                if tool_args and tool_args[0] == '--':
                    tool_args = tool_args[1:]

                # 2. Check if the user explicitly provided a custom method
                if '-M' in tool_args or '--method' in tool_args:
                    base_command = ['combine', output_path]
                else:
                    base_command = ['combine', '-M', 'AsymptoticLimits', output_path]
                
                # 3. Execute Combine from the current directory (resolves relative shape files)
                full_command = base_command + tool_args
                subprocess.run(full_command, check=True)
                
                # 4. Resolve the output directory and move generated output files there
                output_dir = os.path.dirname(os.path.abspath(output_path))
                os.makedirs(output_dir, exist_ok=True)
                
                output_patterns = ['higgsCombine*.root', 'fitDiagnostics*.root', 'combine_logger.out']
                moved_count = 0
                
                for pattern in output_patterns:
                    for filepath in glob.glob(pattern):
                        dest_path = os.path.join(output_dir, os.path.basename(filepath))
                        if os.path.exists(dest_path):
                            os.remove(dest_path)
                        shutil.move(filepath, output_dir)
                        moved_count += 1
                
                if moved_count > 0:
                    # Convert absolute path to a clean relative path for the CLI output
                    rel_output_dir = os.path.relpath(output_dir)
                    LOGGER.info("Successfully organized %d fit artifact(s) in: %s/", moved_count, rel_output_dir)

            except subprocess.CalledProcessError as e:
                LOGGER.error('Combine statistical fitting execution failed!')
                sys.exit(7)
                
            except KeyboardInterrupt:
                LOGGER.info('Fit execution interrupted by user (Ctrl+C). Terminating cleanly...')
                sys.exit(0)
