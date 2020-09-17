
import sys
import ROOT

print "Load cxx analyzers ... ",
ROOT.gSystem.Load("libdatamodel")
ROOT.gSystem.Load("libFCCAnalyses")
print ""

_p = ROOT.fcc.ParticleData()
_s = ROOT.selectParticlesPtIso
print _p

print "Create dataframe object from ", 
fileListRoot = ROOT.vector('string')()
for fileName in [sys.argv[1]]:
    fileListRoot.push_back(fileName)
    print fileName, " ",
print " ..."
df = ROOT.RDataFrame("events", fileListRoot)
print " done"

df2 = df.Define("selected_electrons", "selectParticlesPtIso(10, 0.4)(electrons, electronITags)") \
        .Define("selected_muons", "selectParticlesPtIso(10, 0.4)(muons, muonITags)") \
        .Define("selected_leptons", "mergeElectronsAndMuons(selected_electrons, selected_muons)") \
        .Define("selected_leptons_pt", "get_pt(selected_leptons)") \
        .Define("zeds", "LeptonicZBuilder(selected_leptons)") \
        .Define("zeds_pt", "get_pt(zeds)") \
        .Define("zeds_m", "get_mass(zeds)") \
        .Define("jets_10_bs", "selectJets(10, true)(jets, bTags)") \
        .Define("jets_10_lights", "selectJets(10, false)(jets, bTags)") \
        .Define("selected_bs", "noMatchJets(0.2)(jets_10_bs, selected_leptons)") \
        .Define("selected_lights", "noMatchJets(0.2)(jets_10_lights, selected_leptons)") \
        .Define("nbjets", "get_njets(selected_bs)") \
        .Define("njets", "get_njets2(selected_bs, selected_lights)") \
        .Define("weight"," id_float(mcEventWeights)") \
        .Define("zed_leptonic","ResonanceBuilder(23, 91)(selected_leptons)") \
        .Define("zed_leptonic_m", "get_mass(zed_leptonic)") \
        .Define("zed_leptonic_pt","get_pt(zed_leptonic)") \
        .Define("zed_hadronic_light","JetResonanceBuilder(23, 91)(jets_10_lights)") \
        .Define("zed_hadronic_light_m", "get_mass(zed_hadronic_light)") \
        .Define("zed_hadronic_light_pt","get_pt(zed_hadronic_light)") \
        .Define("zed_hadronic_b","JetResonanceBuilder(23, 91)(jets_10_bs)") \
        .Define("zed_hadronic_b_m", "get_mass(zed_hadronic_b)") \
        .Define("zed_hadronic_b_pt","get_pt(zed_hadronic_b)") \


branchList = ROOT.vector('string')()
for branchName in [
                    "selected_leptons_pt",
                    "zeds_pt",
                    "zeds_m",
                    "zed_leptonic_pt",
                    "zed_leptonic_m",
                    "zed_hadronic_light_pt",
                    "zed_hadronic_light_m",
                    "zed_hadronic_b_pt",
                    "zed_hadronic_b_m",
                    "nbjets",
                    "njets",
                    "weight",
                  ]:
    branchList.push_back(branchName)
df2.Snapshot("events", "tree.root", branchList)

# example call for standalone file
# python FCCeeAnalyses/ZH_Zmumu/dataframe/analysis.py root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/fcc_v01/p8_ee_ZZ_ecm240/events_058759855.root
if __name__ == "__main__":

    if len(sys.argv)==1:
        print "usage:"
        print "python ",sys.argv[0]," file.root"
        sys.exit(3)
    infile = sys.argv[1]
    outDir = 'FCCee/'+sys.argv[0].split('/')[1]+'/'
    import os
    os.system("mkdir -p {}".format(outDir))
    outfile = outDir+infile.split('/')[-1]
    ncpus = 0
    analysis = analysis(infile, outfile, ncpus)
    analysis.run()

