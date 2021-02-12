import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
#Not in Namespace (works)
_fcc  = ROOT.dummyloader
#In namespace MCParticle (does not work)
#_fcc  = ROOT.MCParticle.get_px

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

#ROOT.ROOT.EnableThreadSafety()
#ROOT.ROOT.EnableImplicitMT(1)
#ROOT.TTree.SetMaxTreeSize(100000000000)

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
        
        #df2 = (self.df.Range(500)
        df2 = (self.df

               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Alias("Particle0", "Particle#0.index")
               
#               .Filter("filter_pdgID(541, true)(Particle)==true")
#               .Filter("filter_pdgID(541, true)(Particle)==false")
#               .Filter("(filter_pdgID(521, false)(Particle)==true && filter_pdgID(-521, false)(Particle)==false) || (filter_pdgID(521, false)(Particle)==false && filter_pdgID(-521, false)(Particle)==true)")
               
               .Define("MC_px",         "MCParticle::get_px(Particle)")
               .Define("MC_py",         "MCParticle::get_py(Particle)")
               .Define("MC_pz",         "MCParticle::get_pz(Particle)")
               .Define("MC_p",          "MCParticle::get_p(Particle)")
               .Define("MC_e",          "MCParticle::get_e(Particle)")
               .Define("MC_pdg",        "MCParticle::get_pdg(Particle)")
               .Define("MC_charge",     "MCParticle::get_charge(Particle)")
               .Define("MC_mass",       "MCParticle::get_mass(Particle)")
               .Define("MC_status",     "MCParticle::get_genStatus(Particle)")
               .Define("MC_vertex_x",   "MCParticle::get_vertex_x(Particle)")
               .Define("MC_vertex_y",   "MCParticle::get_vertex_y(Particle)")
               .Define("MC_vertex_z",   "MCParticle::get_vertex_z(Particle)")

               
               .Define("RP_p",          "getRP_p(ReconstructedParticles)")
               .Define("RP_e",          "getRP_e(ReconstructedParticles)")
               .Define("RP_px",         "getRP_px(ReconstructedParticles)")
               .Define("RP_py",         "getRP_py(ReconstructedParticles)")
               .Define("RP_pz",         "getRP_pz(ReconstructedParticles)")
               .Define("RP_charge",     "getRP_charge(ReconstructedParticles)")
               .Define("RP_mass",       "getRP_mass(ReconstructedParticles)")

               #.Define("RP_TRK_D0",      "getRP2TRK_D0(ReconstructedParticles, EFlowTrack_1)")
               #.Define("RP_TRK_Z0",      "getRP2TRK_Z0(ReconstructedParticles, EFlowTrack_1)")

               .Define('RP_MC_index',            "getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles)") 
               .Define('RP_MC_parentindex',      "MCParticle::get_parentid(RP_MC_index,Particle, Particle0)")
               .Define('RP_MC_grandparentindex', "MCParticle::get_parentid(RP_MC_parentindex,Particle, Particle0)")

               .Define('EVT_thrust',      'minimize_thrust("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
               .Define('EVT_thrust_val',  'EVT_thrust.at(0)')
               .Define('EVT_thrust_x',    'EVT_thrust.at(1)')
               .Define('EVT_thrust_x_err','EVT_thrust.at(2)')
               .Define('EVT_thrust_y',    'EVT_thrust.at(3)')
               .Define('EVT_thrust_y_err','EVT_thrust.at(4)')
               .Define('EVT_thrust_z',    'EVT_thrust.at(5)')
               .Define('EVT_thrust_z_err','EVT_thrust.at(6)')
               
               .Define('EVT_sphericity',      'minimize_sphericity("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
               .Define('EVT_sphericity_val',  'EVT_sphericity.at(0)')
               .Define('EVT_sphericity_x',    'EVT_sphericity.at(1)')
               .Define('EVT_sphericity_x_err','EVT_sphericity.at(2)')
               .Define('EVT_sphericity_y',    'EVT_sphericity.at(3)')
               .Define('EVT_sphericity_y_err','EVT_sphericity.at(4)')
               .Define('EVT_sphericity_z',    'EVT_sphericity.at(5)')
               .Define('EVT_sphericity_z_err','EVT_sphericity.at(6)')

               .Define('RP_thrustangle',      'axisCosTheta(EVT_thrust, RP_px, RP_py, RP_pz)')
               .Define('RP_sphericityangle',  'axisCosTheta(EVT_sphericity, RP_px, RP_py, RP_pz)')

               .Define('EVT_thrusthemis0_q_kappa1',  'getAxisCharge(0, 1)(RP_thrustangle, RP_charge, RP_px, RP_py, RP_pz)')
               .Define('EVT_thrusthemis1_q_kappa1',  'getAxisCharge(1, 1)(RP_thrustangle, RP_charge, RP_px, RP_py, RP_pz)')
               .Define('EVT_thrusthemis0_n',         'getAxisN(0)(RP_thrustangle, RP_charge)')
               .Define('EVT_thrusthemis1_n',         'getAxisN(1)(RP_thrustangle, RP_charge)')
               .Define('EVT_thrusthemis0_e',         'getAxisEnergy(0)(RP_thrustangle, RP_charge, RP_e)')
               .Define('EVT_thrusthemis1_e',         'getAxisEnergy(1)(RP_thrustangle, RP_charge, RP_e)')
               .Define('EVT_thrutshemis0_ncharged',  'EVT_thrusthemis0_n.at(1)')
               .Define('EVT_thrutshemis0_nneutral',  'EVT_thrusthemis0_n.at(2)')
               .Define('EVT_thrutshemis0_echarged',  'EVT_thrusthemis0_e.at(1)')
               .Define('EVT_thrutshemis0_eneutral',  'EVT_thrusthemis0_e.at(2)')
               .Define('EVT_thrutshemis1_ncharged',  'EVT_thrusthemis1_n.at(1)')
               .Define('EVT_thrutshemis1_nneutral',  'EVT_thrusthemis1_n.at(2)')
               .Define('EVT_thrutshemis1_echarged',  'EVT_thrusthemis1_e.at(1)')
               .Define('EVT_thrutshemis1_eneutral',  'EVT_thrusthemis1_e.at(2)')

               .Define('EVT_thrutshemis_emax',  'if (EVT_thrusthemis0_e.at(0)>EVT_thrusthemis1_e.at(0)) return EVT_thrusthemis0_e.at(0); else return EVT_thrusthemis1_e.at(0);')
               .Define('EVT_thrutshemis_emin',  'if (EVT_thrusthemis0_e.at(0)>EVT_thrusthemis1_e.at(0)) return EVT_thrusthemis1_e.at(0); else return EVT_thrusthemis0_e.at(0);')

               .Define('EVT_Echarged_max', 'if (EVT_thrutshemis0_echarged>EVT_thrutshemis1_echarged) return EVT_thrutshemis0_echarged; else return EVT_thrutshemis1_echarged')
               .Define('EVT_Echarged_min', 'if (EVT_thrutshemis0_echarged>EVT_thrutshemis1_echarged) return EVT_thrutshemis1_echarged; else return EVT_thrutshemis0_echarged')
               .Define('EVT_Eneutral_max', 'if (EVT_thrutshemis0_eneutral>EVT_thrutshemis1_eneutral) return EVT_thrutshemis0_eneutral; else return EVT_thrutshemis1_eneutral')
               .Define('EVT_Eneutral_min', 'if (EVT_thrutshemis0_eneutral>EVT_thrutshemis1_eneutral) return EVT_thrutshemis1_eneutral; else return EVT_thrutshemis0_eneutral')

               .Define('EVT_Ncharged_max','if (EVT_thrutshemis0_ncharged>EVT_thrutshemis1_ncharged) return EVT_thrutshemis0_ncharged; else return EVT_thrutshemis1_ncharged')
               .Define('EVT_Ncharged_min','if (EVT_thrutshemis0_ncharged>EVT_thrutshemis1_ncharged) return EVT_thrutshemis1_ncharged; else return EVT_thrutshemis0_ncharged')
               .Define('EVT_Nneutral_max','if (EVT_thrutshemis0_nneutral>EVT_thrutshemis1_nneutral) return EVT_thrutshemis0_nneutral; else return EVT_thrutshemis1_nneutral')
               .Define('EVT_Nneutral_min','if (EVT_thrutshemis0_nneutral>EVT_thrutshemis1_nneutral) return EVT_thrutshemis1_nneutral; else return EVT_thrutshemis0_nneutral')



               #.Define("SelTracks","selTracks(0.,3.,0.,3.)( ReconstructedParticles, EFlowTrack_1)")
               #.Define("nSeltracks",  "getRP_n(SelTracks)")
               # Reconstruct the vertex from these tracks :
               .Define("RP_thrusthemis0", "getAxisRP(0)(RP_thrustangle, ReconstructedParticles)")
               .Define("RP_thrusthemis1", "getAxisRP(1)(RP_thrustangle, ReconstructedParticles)")
               .Define("RP_thrusthemis_emax", "if (EVT_thrusthemis0_e.at(0)>EVT_thrusthemis1_e.at(0)) return RP_thrusthemis0; else return RP_thrusthemis1;")
               .Define("RP_thrusthemis_emin", "if (EVT_thrusthemis0_e.at(0)<EVT_thrusthemis1_e.at(0)) return RP_thrusthemis0; else return RP_thrusthemis1;")
               
               #.Define("Vertex_thrusthemis_emin",  "VertexFB( 1, RP_thrusthemis_emin, EFlowTrack_1 )") # primary vertex
               #.Define("Ntrack_thrusthemis_emin",  "getRP_n(RP_thrusthemis_emin)")

               )

        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [

                "MC_px","MC_py","MC_pz","MC_p","MC_e","MC_pdg","MC_charge","MC_mass","MC_status","MC_vertex_x","MC_vertex_y","MC_vertex_z",

                "EVT_thrust_x","EVT_thrust_y","EVT_thrust_z","EVT_thrust_val","EVT_thrusthemis0_q_kappa1","EVT_thrusthemis1_q_kappa1",
                "EVT_thrutshemis0_ncharged","EVT_thrutshemis1_ncharged","EVT_thrutshemis0_nneutral","EVT_thrutshemis1_nneutral",
                "EVT_thrutshemis0_echarged","EVT_thrutshemis1_echarged","EVT_thrutshemis0_eneutral","EVT_thrutshemis1_eneutral",
                "EVT_thrutshemis_emax","EVT_thrutshemis_emin",

                "EVT_Echarged_max","EVT_Echarged_min","EVT_Eneutral_max","EVT_Eneutral_min","EVT_Ncharged_max","EVT_Ncharged_min","EVT_Nneutral_max","EVT_Nneutral_min",



                "EVT_sphericity_x","EVT_sphericity_y","EVT_sphericity_z","EVT_sphericity_val",

                "RP_thrustangle","RP_sphericityangle","RP_p","RP_px","RP_py","RP_pz","RP_charge","RP_mass",

                "RP_MC_index","RP_MC_parentindex","RP_MC_grandparentindex",
                
                ]:
            branchList.push_back(branchName)

        #opts = ROOT.RDF.RSnapshotOptions()
        #opts.fCompressionAlgorithm = ROOT.ROOT.kLZ4
        #opts.fCompressionLevel = 3
        #opts.fAutoFlush = -1024*1024*branchList.size()
        #df2.Snapshot("events", self.outname, branchList, opts)
        df2.Snapshot("events", self.outname, branchList)

# example call for standalone file
# python examples/FCCee/flavour/generic-analysis/analysis.py /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp_v02/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/events_103989732.root


if __name__ == "__main__":

    if len(sys.argv)==1:
        print ("usage:")
        print ("python ",sys.argv[0]," file.root")
        print ("python ",sys.argv[0]," dir/*.root")
        sys.exit(3)


    import glob
    filelist = glob.glob(sys.argv[1])
    
    print ("Create dataframe object from ", )
    fileListRoot = ROOT.vector('string')()
    for fileName in filelist:
        fileListRoot.push_back(fileName)
        print (fileName, " ",)
        print (" ...")
        
    outDir = sys.argv[0].replace(sys.argv[0].split('/')[0],'outputs/').replace('analysis_Bc2TauNu.py','')+'/'
    import os
    os.system("mkdir -p {}".format(outDir))
    outfile = outDir+sys.argv[1].split('/')[-1]
    ncpus = 8
    analysis = analysis(fileListRoot, outfile, ncpus)
    analysis.run()

    #tf = ROOT.TFile(infile)
    #entries = tf.events.GetEntries()
    #p = ROOT.TParameter(int)( "eventsProcessed", entries)
    #outf=ROOT.TFile(outfile,"UPDATE")
    #p.Write()


