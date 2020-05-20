
import sys
import ROOT

print "Load cxx analyzers ... ",
ROOT.gSystem.Load("libdatamodel")
ROOT.gSystem.Load("libFCCAnalyses")
print ""


print "Create dataframe object from ", 
fileListRoot = ROOT.vector('string')()
for fileName in [sys.argv[1]]:
    fileListRoot.push_back(fileName)
    print fileName, " ",
print " ..."
df = ROOT.RDataFrame("events", fileListRoot)
print " done"

df2 = df.Define("selected_electrons",  "selectParticlesPtIso(10, 0.4)(electrons, electronITags)") \
        .Define("selected_muons",      "selectParticlesPtIso(10, 0.4)(muons, muonITags)") \
        .Define("selected_leptons",    "mergeElectronsAndMuons(selected_electrons, selected_muons)") \
        .Define("zeds",                "LeptonicZBuilder(selected_leptons)") \
        .Define("selected_leptons_pt", "get_pt(selected_leptons)") \
        .Define("zeds_pt",             "get_pt(zeds)") \
        .Define("higgs",               "LeptonicHiggsBuilder(zeds)") \
        .Define("higgs_m",             "get_mass(higgs)") \
        .Define("higgs_pt",            "get_pt(higgs)") \
        .Define("jets_10_bs",          "selectJets(10, true)(pfjets04, pfbTags04)") \
        .Define("jets_10_lights",      "selectJets(10, true)(pfjets04, pfbTags04)") \
        .Define("selected_bs",         "noMatchJets(0.2)(jets_10_bs, selected_leptons)") \
        .Define("selected_lights",     "noMatchJets(0.2)(jets_10_lights, selected_leptons)") \
        .Define("nbjets",              "get_njets(selected_bs)") \
        .Define("njets",               "get_njets2(selected_bs, selected_lights)") \
        .Define("weight",              "id_float_legacy(mcEventWeights)") \
        .Define("n_selected_electrons","get_nparticles(electrons)") \
        
         

branchList = ROOT.vector('string')()
for branchName in [
                    "n_selected_electrons",
                    "higgs_pt",
                    "higgs_m",
                    "nbjets",
                    "njets",
                    "weight",
                  ]:
    branchList.push_back(branchName)
df2.Snapshot("events", "tree.root", branchList)
