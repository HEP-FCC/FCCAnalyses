'''
Handle the attributes from the analysis script.
Used only in managed mode.
'''

import sys
import logging


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
                         'script!.\nAborting...', element)
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


def get_attribute(obj, attr_name: str, default_val=None):
    '''
    Returns requested attribute value or default value.
    '''
    try:
        val = getattr(obj, attr_name)
    except AttributeError:
        val = default_val

    return val
