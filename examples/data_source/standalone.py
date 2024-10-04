'''
Example of standalone FCCAnalyses script using podio::DataSource.
'''

import ROOT
ROOT.gROOT.SetBatch(True)


def main():
    '''
    Main entry point for the standalone analysis.
    '''
    input_list = ['https://fccsw.web.cern.ch/fccsw/testsamples/edm4hep1/'
                  'p8_ee_WW_ecm240_edm4hep.root']

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
        'ReconstructedParticle::selPDG(11)(MCRecoAssociations)')

    dframe3 = dframe2.Define(
        'electron_truth_pt',
        'ReconstructedParticle::getPt(electron_truth)')

    dframe4 = dframe3.Filter('electron_truth_pt.size() < 3')

    count = dframe4.Count()
    dframe4.Snapshot('events', 'output.root', ['electron_truth_pt'])

    print('---------------------')
    print('Number of events: ', count.GetValue())


if __name__ == '__main__':
    main()
