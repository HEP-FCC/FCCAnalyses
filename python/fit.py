import os
import sys
import logging
import argparse
import subprocess
import shutil
import glob
from extract import extract_fit_results

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
        
        class_combine_args = generate_datacard(anapath, output_path)

        if args.execute:
            if shutil.which('combine') is None:
                LOGGER.error('The "combine" command-line tool cannot be found...')
                sys.exit(6)

            LOGGER.info('Launching Combine statistical engine execution on: %s', output_path)
            try:
                full_command = []
                if tool_args and tool_args[0] == '--':
                    tool_args = tool_args[1:]

                cleaned_args = [arg for arg in tool_args if arg != output_path]
                class_args = shlex.split(class_combine_args) if class_combine_args else []
                
                has_cli_method = '-M' in cleaned_args or '--method' in cleaned_args
                if has_cli_method:
                    for flag in ['-M', '--method']:
                        if flag in class_args:
                            idx = class_args.index(flag)
                            del class_args[idx:idx+2] 

                combined_args = class_args + cleaned_args

                if not any('MINIMIZER_analytic' in arg for arg in combined_args):
                    combined_args = ['--X-rtd', 'MINIMIZER_analytic'] + combined_args

                # Build the command WITHOUT forcing --out
                if '-M' in combined_args or '--method' in combined_args:
                    full_command = ['combine'] + combined_args + [output_path]
                else:
                    full_command = ['combine', '-M', 'MultiDimFit'] + combined_args + [output_path]

                LOGGER.info("Executing command: %s", " ".join(full_command))
                subprocess.run(full_command, check=True)
                
                # --- ROBUST ARTIFACT SHIFTING ---
                # Scoop up any ROOT files Combine dropped in the main directory
                artifacts = glob.glob("higgsCombine*.root") + glob.glob("fitDiagnostics*.root")
                for artifact in artifacts:
                    dest_file = os.path.join(output_dir, os.path.basename(artifact))
                    # Remove old versions if they exist in the target directory
                    if os.path.exists(dest_file):
                        os.remove(dest_file)
                    shutil.move(artifact, output_dir)
                
                # Automatically extract and display results from the correct directory
                extract_fit_results(output_dir)

            except subprocess.CalledProcessError as e:
                LOGGER.error('Combine statistical fitting execution failed!')
                sys.exit(7)
                
            except KeyboardInterrupt:
                LOGGER.info('Fit execution interrupted by user (Ctrl+C). Terminating cleanly...')
                sys.exit(0)
    else:
        LOGGER.error('Backend "%s" is not implemented yet. Supported backends: combine.', backend)
        sys.exit(4)
