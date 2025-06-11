'''
Example of standalone FCCAnalyses script using podio::DataSource.
'''

import os
import ROOT
ROOT.gROOT.SetBatch(True)


def main():
    '''
    Main entry point for the standalone analysis.
    '''

    ###########################################################################
    # Not part of the example (needed for the CI tests)
    k4h_stack_env = os.environ['KEY4HEP_STACK']
    k4h_os_stack_type = ""
    if 'almalinux9' in k4h_stack_env:
        k4h_os_stack_type += 'alma9'
    elif 'ubuntu22' in k4h_stack_env:
        k4h_os_stack_type += 'ubuntu22'
    elif 'ubuntu24' in k4h_stack_env:
        k4h_os_stack_type += 'ubuntu24'

    k4h_os_stack_type += '/'

    if 'sw-nightlies.hsf.org' in k4h_stack_env:
        k4h_os_stack_type += 'nightlies'
    elif 'sw.hsf.org' in k4h_stack_env:
        k4h_os_stack_type += 'release'
    ###########################################################################

    input_list = [
        'https://fccsw.web.cern.ch/fccsw/analysis/test-samples/edm4hep099/' +
        k4h_os_stack_type + '/p8_ee_WW_ecm240_edm4hep.root'
    ]

    ROOT.gSystem.Load('libFCCAnalyses')
    if ROOT.dummyLoader:
        print('----> DEBUG: Found FCCAnalyses library.')
        ROOT.gInterpreter.Declare("using namespace FCCAnalyses::PodioSource;")
    print('----> INFO: Loading analyzers from libFCCAnalyses... ',)

    if ROOT.podio.DataSource:
        print('----> DEBUG: Found Podio ROOT DataSource.')
    print('----> INFO: Loading events through podio::DataSource...')

    try:
        dframe = ROOT.podio.CreateDataFrame(input_list)
    except TypeError as excp:
        print('----> ERROR: Unable to build dataframe!')
        print(excp)

    dframe2 = dframe.Define(
        'electron_truth',
        'ReconstructedParticle::selPDG(11)(RecoMCLink)')

    dframe3 = dframe2.Define(
        'electron_truth_pt',
        'ReconstructedParticle::getPt(electron_truth)')

    dframe4 = dframe3.Filter('electron_truth_pt.size() < 3')

    count = dframe4.Count()
    dframe4.Snapshot('events', 'data-source-standalone-output.root',
                     ['electron_truth_pt'])

    print('---------------------')
    print('Number of events: ', count.GetValue())


if __name__ == '__main__':
    main()
