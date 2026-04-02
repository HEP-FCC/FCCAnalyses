'''
Handle the attributes from the analysis script.
Used only in managed mode.
'''

import sys
import logging
from typing import Any


LOGGER: logging.Logger = logging.getLogger('FCCAnalyses.run')


def get_element(rdf_module, element: str, is_final: bool = False):
    '''
    Pick up the attribute from the analysis file.
    '''
    try:
        return getattr(rdf_module, element)
    except AttributeError:

        # return default values or crash if mandatory
        if element == 'processList':
            LOGGER.error('The variable <%s> is mandatory in your analysis '
                         'script!\nAborting...', element)
            sys.exit(3)

        elif element == 'analysers':
            LOGGER.error('The function <%s> is mandatory in your analysis '
                         'script!\nAborting...', element)
            if is_final:
                LOGGER.error('The function <%s> is not part of the final '
                             'stage of the analysis!', element)
            sys.exit(3)

        elif element == 'output':
            LOGGER.error('The function <%s> is mandatory in your analysis '
                         'script.\nAborting...', element)
            if is_final:
                LOGGER.error('The function <%s> is not part of the final '
                             'stage of the analysis!', element)
            sys.exit(3)

        elif element == 'analysisName':
            LOGGER.debug('The variable <%s> is optional in your analysis '
                         'script.\nReturning empty string.', element)
            return ''

        elif element == 'nCPUS':
            LOGGER.debug('The variable <%s> is optional in your analysis '
                         'script.\nReturning default value: 4', element)
            return 4

        elif element == 'runBatch':
            LOGGER.debug('The variable <%s> is optional in your analysis '
                         'script.\nReturning default value: False')
            if is_final:
                LOGGER.debug('The option <%s> is not available in the final '
                             'stage of the analysis.', element)
            return False

        elif element == 'outputDir':
            LOGGER.debug('The variable <%s> is optional in your analysis '
                         'script.\nOutput will be save to the current work '
                         'directory.', element)
            return ""

        elif element == 'batchQueue':
            LOGGER.debug('The variable <%s> is optional in your analysis '
                         'script.\nReturning default value: "workday"',
                         element)
            if is_final:
                LOGGER.debug('The option <%s> is not available in the final '
                             'stage of the analysis.', element)
            return 'workday'

        elif element == 'compGroup':
            LOGGER.debug('The variable <%s> is optional in your analysis '
                         'script.\nReturning default value: '
                         '"group_u_FCC.local_gen"', element)
            if is_final:
                LOGGER.debug('The option <%s> is not available in the final '
                             'stage of the analysis.', element)
            return 'group_u_FCC.local_gen'

        elif element == 'outputDirEos':
            LOGGER.debug('The variable <%s> is optional in your analysis '
                         'script.\nReturning empty string.', element)
            if is_final:
                LOGGER.debug('The option <%s> is not available in the final '
                             'stage of the analysis.', element)
            return ''

        elif element == 'eosType':
            LOGGER.debug('The variable <%s> is optional in your analysis '
                         'script.\nReturning default value: "eospublic"',
                         element)
            if is_final:
                LOGGER.debug('The option <%s> is not available in the final '
                             'stage of the analysis.', element)
            return 'eospublic'

        elif element == 'userBatchConfig':
            LOGGER.debug('The variable <%s> is optional in your your analysis '
                         'script.\nReturning empty string.', element)
            if is_final:
                LOGGER.debug('The option <%s> is not available in the final '
                             'stage of the analysis.', element)
            return ''

        elif element == 'testFile':
            test_file_path = 'root://eospublic.cern.ch//eos/experiment/fcc' \
                             'ee/generation/DelphesEvents/spring2021/IDEA/' \
                             'p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/' \
                             'events_131527278.root'
            LOGGER.debug('The variable <%s> is optional in your analysis '
                         'script.\nReturning default test file:\n\t%s',
                         element, test_file_path)
            if is_final:
                LOGGER.debug('The option <%s> is not available in the final '
                             'stage of the analysis.', element)
            return test_file_path

        elif element == 'procDict':
            if is_final:
                LOGGER.error('The variable <%s> is mandatory in the final '
                             'stage of the analysis.\nAborting...', element)
                sys.exit(3)
            LOGGER.debug('The option <%s> is not available in the presel. '
                         'stages of the analysis', element)

        elif element == 'cutList':
            if is_final:
                LOGGER.debug('The variable <%s> is optional in your final '
                             'analysis script.\nReturning empty dictionary.',
                             element)
                return {}
            LOGGER.debug('The option <%s> is not available in the presel. '
                         'stages of the analysis', element)

        elif element == 'defineList':
            if is_final:
                LOGGER.debug('The variable <%s> is optional in your final '
                             'analysis script.\nReturning empty dictionary.',
                             element)
                return {}
            LOGGER.debug('The option <%s> is not available in the presel. '
                         'stages of the analysis', element)

        elif element == 'histoList':
            if is_final:
                LOGGER.error('The variable <%s> is mandatory in the final '
                             'stage of the analysis.\nAborting...', element)
                sys.exit(3)
            LOGGER.debug('The option <%s> is not available in the presel. '
                         'stages of the analysis', element)

        elif element == 'doTree':
            if is_final:
                LOGGER.debug('The variable <%s> is optional in your final '
                             'analysis script.\nReturning default value: '
                             'False',
                             element)
                return False
            LOGGER.debug('The option <%s> is not available in the presel. '
                         'stages of the analysis', element)

        elif element == 'procDictAdd':
            if is_final:
                LOGGER.debug('The variable <%s> is optional in your final '
                             'analysis script.\nReturning empty dictionary.',
                             element)
                return {}
            LOGGER.debug('The option <%s> is not available in the presel. '
                         'stages of the analysis', element)

        elif element == 'doScale':
            if is_final:
                LOGGER.debug('The variable <%s> is optional in the analysis '
                             'final step/histmaker.\nBy default no scaling is '
                             'applied.', element)
                return True
            LOGGER.debug('The option <%s> is not available in the presel. '
                         'stages of the analysis', element)

        elif element == 'intLumi':
            if is_final:
                LOGGER.debug('The variable <%s> is optional in the analysis '
                             'final step/histmaker.\nUsing the default value: '
                             '1', element)
                return 1.
            LOGGER.debug('The option <%s> is not available in the presel. '
                         'stages of the analysis', element)

        elif element == 'saveTabular':
            if is_final:
                LOGGER.debug('The variable <%s> is optional in your final '
                             'analysis script.\nReturning empty dictionary.',
                             element)
                return {}
            LOGGER.debug('The option <%s> is not available in the presel. '
                         'stages of the analysis', element)

        elif element == 'cutLabels':
            if is_final:
                LOGGER.debug('The variable <%s> is optional in your final '
                             'analysis script.\nReturning empty dictionary.',
                             element)
                return {}
            LOGGER.debug('The option <%s> is not available in the presel. '
                         'stages of the analysis', element)

        elif element == 'geometryFile':
            LOGGER.debug('The variable <%s> is optional in your analysis '
                         'script.\nReturning empty string.', element)
            if is_final:
                LOGGER.debug('The option <%s> is not available in the final '
                             'stage of the analysis.', element)
            return ''

        elif element == 'readoutName':
            LOGGER.debug('The variable <%s> is optional in your analysis '
                         'script.\nReturning empty string.', element)
            if is_final:
                LOGGER.debug('The option <%s> is not available in the final '
                             'stage of the analysis.', element)
            return ''

        elif element == 'graph':
            return False

        elif element == 'graphPath':
            return ''

        return None


def get_element_dict(_dict, element: str):
    '''
    Returns None if the key is not found in the dictionary.
    '''
    try:
        value = _dict[element]
        return value
    except KeyError:
        LOGGER.debug('Element "%s" not present in the dictionary!',
                     element)
        return None


def get_attribute(obj: object, attr_name: str, default_val=None) -> Any:
    '''
    Returns requested attribute value or default value.
    '''
    try:
        val = getattr(obj, attr_name)
    except AttributeError:
        val = default_val

    return val


# _____________________________________________________________________________
def is_valid_string(variable: str) -> bool:
    '''
    Checks if the variable contains "valid" string:
        - value is not None
        - value is of string type
        - value is not empty
    '''
    if variable is None:
        return False

    if not isinstance(variable, str):
        return False

    if variable:
        return True

    return False


# _____________________________________________________________________________
def has_valid_string(dictionary: dict[str, Any], key: str) -> bool:
    '''
    Checks if the dictionary contains a "valid" string value:
        - key exists in dictionary
        - value is not None
        - value is of string type
        - value is not empty
    '''
    if key not in dictionary:
        return False

    return is_valid_string(dictionary[key])


# _____________________________________________________________________________
def has_valid_float(dictionary: dict[str, Any], key: str) -> bool:
    '''
    Checks if the dictionary contains a "valid" float value:
        - key exists in dictionary
        - value is not None
        - value is of float type
    '''
    if key not in dictionary:
        return False

    if dictionary[key] is None:
        return False

    if isinstance(dictionary[key], float):
        return True

    return False


# _____________________________________________________________________________
def has_valid_int(dictionary: dict[str, Any], key: str) -> bool:
    '''
    Checks if the dictionary contains a "valid" int value:
        - key exists in dictionary
        - value is not None
        - value is of int type
    '''
    if key not in dictionary:
        return False

    if dictionary[key] is None:
        return False

    if isinstance(dictionary[key], int):
        return True

    return False


# _____________________________________________________________________________
def has_valid_2int(dictionary: dict[str, Any], key: str) -> bool:
    '''
    Checks if the dictionary contains a "valid" two int value:
        - key exists in dictionary
        - value is not None
        - values are of type [int, int]
    '''
    if key not in dictionary:
        return False

    if dictionary[key] is None:
        return False

    if isinstance(dictionary[key], tuple) and \
            list(map(type, dictionary[key])) == [int, int]:
        return True

    if isinstance(dictionary[key], list) and \
            map(type, dictionary[key]) == [int, int]:
        return True

    return False


# _____________________________________________________________________________
def validate_sample_list(provided_sample_list: dict[str, dict[str, Any]]):
    '''
    Validate and reshape the provided sample list.
    '''
    sample_list: dict[str, dict[str, Any]] = {}

    for sample_name, provided_sample_dict in provided_sample_list.items():
        if not is_valid_string(sample_name):
            LOGGER.error('Provided sample list contains sample with invalid '
                         'name!\nAborting...')
            sys.exit(3)

        # Deprecations
        # input_dir
        if 'input_dir' in provided_sample_list:
            LOGGER.error('Please use "input-dir" for sample "%s" instead of '
                         '"input_dir"!\nAborting...', sample_name)
            sys.exit(3)
        # output
        if 'output' in provided_sample_list:
            LOGGER.error('Please use "output-stem" for sample "%s" instead of '
                         '"output"!\nAborting...', sample_name)
            sys.exit(3)

        sample_dict: dict[str, Any] = {}

        # Check input dir
        if has_valid_string(provided_sample_list, 'input-dir'):
            sample_dict['input-dir'] = provided_sample_dict['input-dir']
        else:
            sample_dict['input-dir'] = None

        # Check output stem
        if has_valid_string(provided_sample_dict, 'output-stem'):
            sample_dict['output-stem'] = provided_sample_dict['output-stem']
        else:
            sample_dict['output-stem'] = sample_name

        # Check reduction fraction
        if has_valid_float(provided_sample_list, 'fraction'):
            sample_dict['fraction'] = provided_sample_dict['fraction']
        else:
            sample_dict['fraction'] = 1.0

        # Check number of chunks
        if has_valid_int(provided_sample_dict, 'chunks'):
            sample_dict['chunks'] = provided_sample_dict['chunks']
        else:
            sample_dict['chunks'] = 1

        # Check if to stride through the events
        if has_valid_2int(provided_sample_dict, 'stride'):
            sample_dict['scan'] = provided_sample_dict['stride']
        else:
            sample_dict['scan'] = None

        sample_list[sample_name] = sample_dict

    return sample_list


def validate_analysis_class(analysis_class: Any) -> dict[str, Any]:
    '''
    Validate an instance of the Analysis class.
    Returning configuration dictionary for reading clarity.
    '''

    config: dict[str, Any] = {}

    # Save the full analysis class
    config['analysis-class'] = analysis_class

    # Deprecations
    if hasattr(analysis_class, 'run_batch'):
        if analysis_class.run_batch:
            LOGGER.error('run_batch analysis attribute is no longer '
                         'supported, use "fccanalysis submit" instead!\n'
                         'Aborting...')
            sys.exit(3)

    # Check if the analysis chain is provided
    if hasattr(analysis_class, 'analyzers'):
        config['analysis-chain'] = analysis_class.analyzers
    else:
        LOGGER.error('Analysis chain not provided!\nAborting...')
        sys.exit(3)

    # Check the output variables
    if hasattr(analysis_class, 'output'):
        config['output-variables'] = analysis_class.output
    else:
        LOGGER.error('Analysis output variables not provided!\nAborting...')
        sys.exit(3)

    return config
