import os
import sys
import logging
from combine import generate_datacard

LOGGER = logging.getLogger('FCCAnalyses.fit')

def run_fit(parser):
    """
    Entry point for the 'fccanalysis fit' sub-command.
    """
    args, _ = parser.parse_known_args()

    if args.command != 'fit':
        LOGGER.error('Wrong sub-command!\nAborting...')
        sys.exit(3)

    if not os.path.isfile(args.script_path):
        LOGGER.error('Fit script "%s" not found!\nAborting...', args.script_path)
        sys.exit(3)

    # Convert to absolute path and pass to Combine engine
    anapath = os.path.abspath(args.script_path)
    output_path = args.output
    
    generate_datacard(anapath, output_path)
