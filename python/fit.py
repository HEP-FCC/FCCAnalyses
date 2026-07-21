import os
import sys
import logging
import argparse
import subprocess
import shutil
import glob

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
        import shlex
        
        # 1. Capture the combine_args returned from the Fit class
        class_combine_args = generate_datacard(anapath, output_path)

        if args.execute:
            if shutil.which('combine') is None:
                LOGGER.error('The "combine" command-line tool cannot be found...')
                sys.exit(6)

            LOGGER.info('Launching Combine statistical engine execution on: %s', output_path)
            try:
                full_command = []
                # 1. Strip the '--' separator if present
                if tool_args and tool_args[0] == '--':
                    tool_args = tool_args[1:]

                cleaned_args = [arg for arg in tool_args if arg != output_path]

                # 2. Merge Class arguments and CLI arguments
                class_args = shlex.split(class_combine_args) if class_combine_args else []
                
                # Deduplicate the Method argument: CLI takes precedence over the Python class
                has_cli_method = '-M' in cleaned_args or '--method' in cleaned_args
                if has_cli_method:
                    for flag in ['-M', '--method']:
                        if flag in class_args:
                            idx = class_args.index(flag)
                            del class_args[idx:idx+2] # Remove the flag and its value from class_args

                combined_args = class_args + cleaned_args

                # Check if the user explicitly provided a custom method
                if '-M' in combined_args or '--method' in combined_args:
                    full_command = ['combine'] + combined_args + [output_path]
                else:
                    full_command = ['combine', '-M', 'AsymptoticLimits'] + combined_args + [output_path]
                
                # 3. Add the --out flag
                output_dir = os.path.dirname(os.path.abspath(output_path))
                full_command.extend(['--out', output_dir])

                LOGGER.info("Executing command: %s", " ".join(full_command))
                subprocess.run(full_command, check=True)

            except subprocess.CalledProcessError as e:
                LOGGER.error('Combine statistical fitting execution failed!')
                sys.exit(7)
                
            except KeyboardInterrupt:
                LOGGER.info('Fit execution interrupted by user (Ctrl+C). Terminating cleanly...')
                sys.exit(0)
        else:
            LOGGER.error('Backend "%s" is not implemented yet. Supported backends: combine.', backend)
            sys.exit(4)
