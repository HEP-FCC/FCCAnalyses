'''
Standalone test of EDM4hep RDataSource in Python.
'''

import ROOT
ROOT.gROOT.SetBatch(True)


def main():
    '''
    Main entry point for the standalone analysis.
    '''
    input_list = ['https://fccsw.web.cern.ch/fccsw/testsamples/edm4hep1/'
                  'p8_ee_WW_ecm240_edm4hep.root']

    ROOT.gSystem.Load("libFCCAnalyses")
    if ROOT.dummyLoader:
        print('----> Debug: Found FCCAnalyses library.')
    print("----> Info: Loading analyzers from libFCCAnalyses... ",)

    if ROOT.podio.DataSource:
        print('----> Debug: Found Podio ROOT DataSource.')
    print('----> Info: Loading events through podio::DataSource...')

    try:
        dframe = ROOT.podio.CreateDataFrame(input_list)
    except TypeError as excp:
        print('----> Error: Unable to build dataframe!')
        print(excp)

    dframe2 = dframe.Define(
        "electron_truth",
        "recoParticle::selPDG(11)(MCRecoAssociations)")

    dframe3 = dframe2.Define(
        "electron_truth_pt",
        "recoParticle::getPt(electron_truth)")

    dframe4 = dframe3.Filter("electron_truth_pt.size() < 3")

    count = dframe4.Count()
    dframe4.Snapshot("events", "output.root", {"electron_truth_pt"})
    # dframe4.Snapshot("events", "output.root", {"electron_truth",
    #                                            "electron_truth_pt"})

    print("---------------------")
    print("Nuber of events: ", count.GetValue())


if __name__ == "__main__":
    main()
