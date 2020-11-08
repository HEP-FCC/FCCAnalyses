import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.getMC_px
_fcc2  = ROOT.getRP2MC_p

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)
print ('fccana2  ',_fcc2)


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
        match=ROOT.getRP2MC_p_func()
        string_vec = ROOT.std.vector('string')()
        string_vec.push_back('MCRecoAssociations#0.index')
        string_vec.push_back('MCRecoAssociations#1.index')
        string_vec.push_back('ReconstructedParticles')
        string_vec.push_back('Particle')

        df2 = (self.df
               .Define("MC_px",         "getMC_px(Particle)")
               .Define("MC_py",         "getMC_py(Particle)")
               .Define("MC_pz",         "getMC_pz(Particle)")
               .Define("MC_p",          "getMC_p(Particle)")
               .Define("MC_pdg",        "getMC_pdg(Particle)")
               .Define("MC_charge",     "getMC_charge(Particle)")
               .Define("MC_mass",       "getMC_mass(Particle)")
               .Define("MC_status",     "getMC_genStatus(Particle)")
               .Define("MC_vertex_x",   "getMC_vertex_x(Particle)")
               .Define("MC_vertex_y",   "getMC_vertex_y(Particle)")
               .Define("MC_vertex_z",   "getMC_vertex_z(Particle)")

               .Define("RP_p",          "getRP_p(ReconstructedParticles)")
               .Define("RP_px",         "getRP_px(ReconstructedParticles)")
               .Define("RP_py",         "getRP_py(ReconstructedParticles)")
               .Define("RP_pz",         "getRP_pz(ReconstructedParticles)")
               .Define("RP_charge",     "getRP_charge(ReconstructedParticles)")
               .Define("RP_mass",       "getRP_mass(ReconstructedParticles)")

               .Define("RP_TRK_D0",      "getRP2TRK_D0(ReconstructedParticles, EFlowTrack_1)")
               .Define("RP_TRK_Z0",      "getRP2TRK_D0(ReconstructedParticles, EFlowTrack_1)")

               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Alias("Particle0", "Particle#0.index")

               .Define('RP_MC_index',    "getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_p',        "getRP2MC_p(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_px',       "getRP2MC_px(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_py',       "getRP2MC_py(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_pz',       "getRP2MC_pz(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_pdg',      "getRP2MC_pdg(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_charge',   "getRP2MC_charge(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_mass',     "getRP2MC_mass(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
               .Define('RP_MC_parentindex', "getRP2MC_parentid(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle, Particle0)")
               
               #.Define('RPMC_p',        match,string_vec)
               )

        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "MC_px",
                "MC_py",
                "MC_pz",
                "MC_p",
                "MC_pdg",
                "MC_charge",
                "MC_mass",
                "MC_status",
                "MC_vertex_x",
                "MC_vertex_y",
                "MC_vertex_z",

                "RP_p",
                "RP_px",
                "RP_py",
                "RP_pz",
                "RP_charge",
                "RP_mass",

                "RP_TRK_D0",
                "RP_TRK_Z0",

                "RP_MC_p",
                "RP_MC_px",
                "RP_MC_py",
                "RP_MC_pz",
                "RP_MC_pdg",
                "RP_MC_charge",
                "RP_MC_index",
                "RP_MC_parentindex",


                
                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)

# example call for standalone file
# python FCCeeAnalyses/Z_Zbb_Flavor/dataframe/analysis.py /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp/p8_ee_Ztautau_ecm91/events_012154460.root

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
