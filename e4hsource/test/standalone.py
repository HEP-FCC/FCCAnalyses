'''
Standalone test of EDM4hep RDataSource in Python.
'''

import ROOT
ROOT.gROOT.SetBatch(True)

def main():
    input_list = ['https://fccsw.web.cern.ch/fccsw/testsamples/edm4hep1/'
                  'p8_ee_WW_ecm240_edm4hep.root']

    print("----> Info: Loading analyzers from libFCCAnalyses... ",)
    ROOT.gSystem.Load("libFCCAnalyses")
    _fcc = ROOT.dummyLoader

    print('----> Info: Loading events through EDM4hep RDataSource...')
    ROOT.gSystem.Load("libe4hsource")
    if ROOT.loadEDM4hepDataSource():
        print('----> Debug: EDM4hep RDataSource loaded')
    try:
        dframe = ROOT.FCCAnalyses.FromEDM4hep(input_list)
    except TypeError as excp:
        print('----> Error: Unable to build dataframe!')
        print(excp)

    dframe2 = dframe.Define(
        "electron_truth",
        "FCCAnalyses::ReconstructedParticle::selPDG(11)(MCRecoAssociations)")

    dframe3 = dframe2.Define(
        "electron_truth_pt",
        "FCCAnalyses::ReconstructedParticle::getPt(electron_truth)")

    dframe4 = dframe3.Filter("electron_truth_pt.size() < 3")

    count = dframe4.Count()
    dframe4.Snapshot("events", "output.root", {"electron_truth_pt"})
    # dframe4.Snapshot("events", "output.root", {"electron_truth", "electron_truth_pt"})

    print("---------------------")
    print("Nuber of events: ", count.GetValue())

if __name__ == "__main__":
    main()
