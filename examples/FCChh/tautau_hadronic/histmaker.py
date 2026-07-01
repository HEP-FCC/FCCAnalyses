import ROOT
import array

intLumi = 3e7

fraction = 0.01
debug = False


processList = {

        'pwp8_pp_hh_lambda100_5f_hhbbtata': {"fraction": fraction},

}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag = "FCChh/fcc_v07/II/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "/eos/experiment/fcc/hh/utils/FCCDicts/FCChh_procDict_fcc_v07_II.json"

# Define the input dir (optional)
# inputDir    = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/II/"

# Optional: output directory, default is local running directory
outputDir = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/II/tautau_hadronic/"

# optional: ncpus, default is 4, -1 uses all cores available
nCPUS = -1

# scale the histograms with the cross-section and integrated luminosity
# doScale = True

# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):

    results = []
    selections = []

    df = df.Define("weight", "EventHeader.weight")
    weightsum = df.Sum("weight")

    # cut 0 : all events
    df = df.Define(f"cut{len(selections)}", f"{len(selections)}")
    results.append(df.Histo1D(("cutFlow", "", 5, 0, 5), f"cut{len(selections)}"))
    selections.append("All events")

    # select muons 
    df = df.Define("muons",  "FCCAnalyses::ReconstructedParticle::get(Muon_objIdx.index, ReconstructedParticles)") 
    df = df.Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(muons)")
    df = df.Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_muons)")
    df = df.Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)") #sort by pT
    df = df.Define("n_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_muons)") 
    df = df.Define("pT_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_muons)")

    # select electrons
    df = df.Define("electrons",  "FCCAnalyses::ReconstructedParticle::get(Electron_objIdx.index, ReconstructedParticles)")
    df = df.Define("selpt_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(electrons)")
    df = df.Define("sel_electrons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_electrons)")
    df = df.Define("sel_electrons", "AnalysisFCChh::SortParticleCollection(sel_electrons_unsort)") #sort by pT
    df = df.Define("n_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_electrons)")
    df = df.Define("pT_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_electrons)")

    # select jets
    df = df.Define(
        "b_tagged_jets_medium", "AnalysisFCChh::get_tagged_jets(Jet, Jet_tau_tags, _Jet_tau_tags_particle, _Jet_tau_tags_parameters, 1)"
    )  # bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_II.tcl
    # select medium b-jets with pT > 30 GeV, |eta| < 4
    df = df.Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(b_tagged_jets_medium)")
    df = df.Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
    df = df.Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)")  # sort by pT
    df = df.Define("sel_bjets_pt", "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)")
    df = df.Define("n_bjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")

    #select hadronic taus
    df = df.Define(
        "tau_tagged_jets_medium", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)"
    )  # bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_II.tcl
    # select medium tauswith pT > 30 GeV, |eta| < 4
    df = df.Define("selpt_taujets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(tau_tagged_jets_medium)")
    df = df.Define("sel_taujets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_taujets)")
    df = df.Define("sel_taujets", "AnalysisFCChh::SortParticleCollection(sel_taujets_unsort)")  # sort by pT
    df = df.Define("sel_taujets_pt", "FCCAnalyses::ReconstructedParticle::get_pt(sel_taujets)")
    df = df.Define("n_taujets", "FCCAnalyses::ReconstructedParticle::get_n(sel_taujets)")

    # select jets
    df = df.Define("selpt_jets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(Jet)")
    df = df.Define("sel_jets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_jets)")
    df = df.Define("sel_jets", "AnalysisFCChh::SortParticleCollection(sel_jets_unsort)") 
    df = df.Define("n_jets", "FCCAnalyses::ReconstructedParticle::get_n(sel_jets)")
    # missing ET
    df = df.Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)")

    results.append(df.Histo1D(("n_bjets_pre", "", 10, 0, 10), "n_bjets"))
    results.append(df.Histo1D(("n_jets_pre", "", 10, 0, 10), "n_jets"))
    results.append(df.Histo1D(("n_taujets_pre", "", 10, 0, 10), "n_taujets"))

    # calculate HT
    df = df.Define("HT","ScalarHT")

    df = df.Define("ht_tev", "HT/1000.")

    results.append(df.Histo1D(("HT_pre", "", 20, 0, 2000), "ht_tev"))
    results.append(df.Histo1D(("MET_pre", "", 20, 0, 2000), "MET"))

    # store selection labels dynamically in the ROOT file
    from ROOT import TObjString

    selection_str = "\n".join(selections)
    selection_obj = TObjString(selection_str)

    # Identify the cutFlow histogram and attach the object
    for obj in results:
        h = obj.GetValue()  # returns the TH1
        if h.GetName() == "cutFlow":
            h.GetListOfFunctions().Add(selection_obj)
            break

    return results, weightsum
