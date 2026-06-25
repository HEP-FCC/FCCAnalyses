import os
import sys
import logging
import argparse
import importlib.util

# Use the standard FCCAnalyses logger
LOGGER = logging.getLogger('FCCAnalyses.combine')

def generate_datacard(parser: argparse.ArgumentParser) -> None:
    """
    Sub-command entry point for Combine datacard generation.
    """
    args = parser.parse_args()
    anapath = os.path.abspath(args.fit_script)
    
    LOGGER.info('Loading Combine fit script from:\\n  %s', anapath)
    
    if not os.path.isfile(anapath):
        LOGGER.error('Fit script not found!\\nAborting...')
        sys.exit(3)
        
    # Dynamically load the user's python file
    try:
        spec = importlib.util.spec_from_file_location('user_fit', anapath)
        user_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_module)
    except SyntaxError as err:
        LOGGER.error('Syntax error encountered in the fit script:\\n%s', err)
        sys.exit(3)
        
    # Instantiate the user's class and validate
    if not hasattr(user_module, "Datacard"):
        LOGGER.error('Fit script must define a class named "Datacard"!\\nAborting...')
        sys.exit(3)
        
    user_datacard = user_module.Datacard()
    
    # Check for minimal required members
    if not hasattr(user_datacard, 'processes') or not hasattr(user_datacard, 'channels'):
        LOGGER.error('Datacard class must have "processes" and "channels" defined!\\nAborting...')
        sys.exit(3)
        
    LOGGER.info('Successfully validated user Datacard.')
    LOGGER.info('Channels found: %s', user_datacard.channels)
    LOGGER.info('Processes found: %s', list(user_datacard.processes.keys()))
    
    # TODO: In the next commit, insert Phase 1 text alignment and parsing engine here
    # to loop over the user_datacard members and output the .txt file.
    
    LOGGER.info('Datacard generation skeleton complete.')
