import os
import sys
import logging
import argparse

LOGGER = logging.getLogger('FCCAnalyses.fit')

def run_fit(parser: argparse.ArgumentParser) -> None:
    """Sub-command entry point for object-oriented fitting configurations."""
    args = parser.parse_args()
    
    anapath = os.path.abspath(args.script_path)
    output_path = args.output
    backend = args.backend.lower()

    LOGGER.info('Steering fit configuration towards the "%s" backend...', backend)

    if backend == 'combine':
        # Lazy import to keep dependencies clean
        from combine import generate_datacard
        generate_datacard(anapath, output_path)
        
    elif backend == 'pyhf':
        LOGGER.error('Backend "pyhf" is planned but not yet implemented! Aborting...')
        sys.exit(5)
        
    else:
        LOGGER.error('Unsupported fitting backend: %s. Aborting...', backend)
        sys.exit(4)
