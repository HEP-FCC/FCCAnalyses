import sys
import ROOT

print ("Load cxx analyzers ... ")
ROOT.gSystem.Load("libdatamodel")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal

_p = ROOT.fcc.ParticleData()
_s = ROOT.selectParticlesPtIso

class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):
        df2 = self.df.Define("selected_muons", "selectParticlesPtIso(10, 0.4)(muons, muonITags)") \
                     .Define("selected_muons_pt", "get_pt(selected_muons)") \
                     .Define("selected_muons_y", "get_y(selected_muons)") \
                     .Define("selected_muons_p", "get_p(selected_muons)") \
                     .Define("selected_muons_e", "get_e(selected_muons)") \
                     .Define("jets_10_bs", "selectJets(10, true)(efjets, efbTags)") \
                     .Define("jets_10_lights", "selectJets(10, false)(efjets, efbTags)") \
                     .Define("selected_bs", "noMatchJets(0.2)(jets_10_bs, selected_muons)") \
                     .Define("selected_lights", "noMatchJets(0.2)(jets_10_lights, selected_muons)") \
                     .Define("nbjets", "get_njets(selected_bs)") \
                     .Define("njets", "get_njets2(selected_bs, selected_lights)") \
                     .Define("weight"," id_float(mcEventWeights)") \
                     .Define("zed_leptonic","ResonanceBuilder(23, 91)(selected_muons)") \
                     .Define("zed_leptonic_m", "get_mass(zed_leptonic)") \
                     .Define("zed_leptonic_pt","get_pt(zed_leptonic)") \
                     .Define("zed_hadronic_light","JetResonanceBuilder(23, 91)(jets_10_lights)") \
                     .Define("zed_hadronic_light_m", "get_mass(zed_hadronic_light)") \
                     .Define("zed_hadronic_light_pt","get_pt(zed_hadronic_light)") \
                     .Define("zed_hadronic_b","JetResonanceBuilder(23, 91)(jets_10_bs)") \
                     .Define("zed_hadronic_b_m", "get_mass(zed_hadronic_b)") \
                     .Define("zed_hadronic_b_pt","get_pt(zed_hadronic_b)") \
                     .Define("zed_leptonic_recoil","recoil(240)(zed_leptonic)") \
                     .Define("zed_leptonic_recoil_m","get_mass(zed_leptonic_recoil)") \

        


        branchList = ROOT.vector('string')()
        for branchName in [
                "selected_muons_pt",
                "selected_muons_y",
                "selected_muons_p",
                "selected_muons_e",
                "zed_leptonic_pt",
                "zed_leptonic_m",
                "zed_hadronic_light_pt",
                "zed_hadronic_light_m",
                "zed_hadronic_b_pt",
                "zed_hadronic_b_m",
                "zed_leptonic_recoil_m",
                "nbjets",
                "njets",
                "weight",
        ]:
            branchList.push_back(branchName)
            df2.Snapshot("events", self.outname, branchList)


# example call
# python FCCeeAnalyses/ZH_Zmumu/dataframe/analysis.py root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/fcc_v01/p8_ee_ZZ_ecm240/events_058759855.root
if __name__ == "__main__":

    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        sys.exit(3)
    infile = sys.argv[1]
    outDir = 'FCCee/'+sys.argv[0].split('/')[1]+'/'
    import os
    os.system("mkdir -p {}".format(outDir))
    outfile = outDir+infile.split('/')[-1]
    ncpus = 0
    analysis = analysis(infile, outfile, ncpus)
    analysis.run()

    tf = ROOT.TFile(infile)
    entries = tf.events.GetEntries()
    p = ROOT.TParameter(int)( "eventsProcessed", entries)
    outf=ROOT.TFile(outfile,"UPDATE")
    p.Write()
