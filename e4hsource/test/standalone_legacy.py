'''
Standalone test of legacy EDM4hep RDataSource in Python.
'''

import ROOT
ROOT.gROOT.SetBatch(True)

def main():
    input_list = [
        '/eos/user/g/gasadows/Output/TrackingPerformance/'
        'LCIO/FCCee_o1_v04/REC/resVXD_3mic/'
        'RECTest_FCCee_o1_v04_resVXD_3mic_mu_89_deg_100_GeV_10000_evts_edm4hep'
        '.root'
    ]

    print ("----> Info: Loading analyzers from libFCCAnalyses... ",)
    ROOT.gSystem.Load("libFCCAnalyses")
    _fcc = ROOT.dummyLoader

    print('----> Info: Loading events through legacy EDM4hep RDataSource...')
    ROOT.gSystem.Load("libe4hlegacysource")
    if ROOT.loadEDM4hepLegacySource():
        print('----> Debug: Legacy EDM4hep RDataSource loaded')
    try:
        dframe = ROOT.FCCAnalyses.FromEDM4hepLegacy(input_list)
    except TypeError as excp:
        print('----> Error: Unable to build dataframe!')
        print(excp)

    dframe2 = dframe.Define(
        "electron_truth",
        "FCCAnalyses::ReconstructedParticle::selPDG(11, false)(RecoMCTruthLink)"
    )

    dframe3 = dframe2.Define(
        "electron_truth_pt",
        "FCCAnalyses::ReconstructedParticle::getPt(electron_truth)")

    dframe4 = dframe3.Filter("electron_truth_pt.size() > 0")

    count = dframe4.Count()
    dframe4.Snapshot("events", "output.root", {"electron_truth_pt"})
    # dframe4.Snapshot("events", "output.root", {"electron_truth",
    #                                            "electron_truth_pt"})

    print("---------------------")
    print("Nuber of events: ", count.GetValue())

if __name__ == "__main__":
    main()
