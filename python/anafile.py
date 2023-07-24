'''
Handle the attributes from the analysis file.
Used only in managed mode.
'''

import sys

def getElement(rdfModule, element, isFinal=False):
    '''
    Pick up the attribute from the analysis file.
    '''
    try:
        return getattr(rdfModule, element)
    except AttributeError:

        #return default values or crash if mandatory
        if element == 'processList':
            print('----> Error: The variable <{}> is mandatory in your analysis file!'.format(element))
            print('             Aborting...')
            sys.exit(3)

        elif element=='analysers':
            print('The function <{}> is mandatory in your analysis.py file, will exit'.format(element))
            if isFinal: print('The function <{}> is not part of final analysis'.format(element))
            sys.exit(3)

        elif element=='output':
            print('The function <{}> is mandatory in your analysis.py file, will exit'.format(element))
            if isFinal: print('The function <{}> is not part of final analysis'.format(element))
            sys.exit(3)

        elif element=='analysisName':
            print('The variable <analysisName> is optional in your analysis.py file, return default value ""')
            return ""

        elif element=='nCPUS':
            print('The variable <{}> is optional in your analysis.py file, return default value 4'.format(element))
            return 4

        elif element=='runBatch':
            print('----> Info: The variable <{}> is optional in your analysis file.'.format(element))
            print('            Returning default value: False')
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return False

        elif element=='outputDir':
            print('The variable <{}> is optional in your analysis.py file, return default value running dir'.format(element))
            return ""

        elif element=='batchQueue':
            print('The variable <{}> is optional in your analysis.py file, return default value workday'.format(element))
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return "workday"

        elif element=='compGroup':
             print('The variable <{}> is optional in your analysis.py file, return default value group_u_FCC.local_gen'.format(element))
             if isFinal: print('The option <{}> is not available in final analysis'.format(element))
             return "group_u_FCC.local_gen"

        elif element=='outputDirEos':
            print('The variable <{}> is optional in your analysis.py file, return default empty string'.format(element))
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return ""

        elif element=='eosType':
            print('The variable <{}> is optional in your analysis.py file, return default eospublic'.format(element))
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return "eospublic"

        elif element=='userBatchConfig':
            print('The variable <{}> is optional in your analysis.py file, return default empty string'.format(element))
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return ""

        elif element=='testFile':
            print('The variable <{}> is optional in your analysis.py file, return default file'.format(element))
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/events_131527278.root"

        elif element=='procDict':
            if isFinal:
                print('The variable <{}> is mandatory in your analysis_final.py file, exit'.format(element))
                sys.exit(3)
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='cutList':
            if isFinal:
                print('The variable <{}> is optional in your analysis_final.py file, return empty dictonary'.format(element))
                return {}
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='defineList':
            if isFinal:
                print('The variable <{}> is optional in your analysis_final.py file, return empty dictonary'.format(element))
                return {}
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='histoList':
            if isFinal:
                print('The variable <{}> is mandatory in your analysis_final.py file, exit'.format(element))
                sys.exit(3)
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='doTree':
            if isFinal:
                print('The variable <{}> is optional in your analysis_final.py file return default value False'.format(element))
                return False
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='procDictAdd':
            if isFinal:
                print('The variable <{}> is optional in your analysis_final.py file return empty dictionary'.format(element))
                return {}
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='doScale':
            if isFinal:
                print('The variable <{}> is optional in the final step/histmaker. By default no scaling is applied.'.format(element))
                return False
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='intLumi':
            if isFinal:
                print('The variable <{}> is optional in the final step/histmaker. Use the default value of 1'.format(element))
                return 1.
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='saveTabular':
            if isFinal:
                print('The variable <{}> is optional in your analysis_final.py file return empty dictionary'.format(element))
                return {}
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='cutLabels':
            if isFinal:
                print('The variable <{}> is optional in your analysis_final.py file return empty dictionary'.format(element))
                return {}
            else: print('The option <{}> is not available in presel analysis'.format(element))

        elif element=='geometryFile':
            print('The variable <{}> is optional in your analysis.py file, return default value empty string'.format(element))
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return ""

        elif element=='readoutName':
            print('The variable <{}> is optional in your analysis.py file, return default value empty string'.format(element))
            if isFinal: print('The option <{}> is not available in final analysis'.format(element))
            return ""

        return None


#__________________________________________________________
def getElementDict(d, element):
    try:
        value=d[element]
        return value
    except KeyError:
#        print (element, "does not exist using default value")
        return None
