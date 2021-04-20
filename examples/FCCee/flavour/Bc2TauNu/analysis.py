import sys
import ROOT
from array import array

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libawkward")
ROOT.gSystem.Load("libawkward-cpu-kernels")
ROOT.gSystem.Load("libFCCAnalyses")

ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)


ROOT.gInterpreter.ProcessLine('''
TMVA::Experimental::RBDT<> bdt("Bc2TauNu_BDT", "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bc2TauNu/xgb_bdt_vtx.root");

computeModel = TMVA::Experimental::Compute<18, float>(bdt);
''')


class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        ROOT.ROOT.EnableImplicitMT(ncpu)
        ROOT.EnableThreadSafety()
        self.df = ROOT.RDataFrame("events", inputlist)
        print (" init done, about to run")
    #__________________________________________________________
    def run(self):
        #84702
        #df2 = (self.df.Range(1000)
        
        df2 = (self.df
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Alias("Particle0", "Particle#0.index")
               .Alias("Particle1", "Particle#1.index")

               .Define("MC_PDG", "MCParticle::get_pdg(Particle)")
               .Define("MC_n", "int(MC_PDG.size())")
               .Define("MC_M1", "myUtils::get_MCMother1(Particle,Particle0)")
               .Define("MC_M2", "myUtils::get_MCMother2(Particle,Particle0)")
               .Define("MC_D1", "myUtils::get_MCDaughter1(Particle,Particle1)")
               .Define("MC_D2", "myUtils::get_MCDaughter2(Particle,Particle1)")
               
               .Define("RP_e",          "ReconstructedParticle::get_e(ReconstructedParticles)")
               .Define("RP_px",         "ReconstructedParticle::get_px(ReconstructedParticles)")
               .Define("RP_py",         "ReconstructedParticle::get_py(ReconstructedParticles)")
               .Define("RP_pz",         "ReconstructedParticle::get_pz(ReconstructedParticles)")
               .Define("RP_charge",     "ReconstructedParticle::get_charge(ReconstructedParticles)")
              
               .Define('EVT_thrust',          'Algorithms::minimize_thrust("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
               .Define('RP_thrustangle',      'Algorithms::getAxisCosTheta(EVT_thrust, RP_px, RP_py, RP_pz)')

               #hemis0 == negative angle, hemis1 == positive angle
               .Define('EVT_thrusthemis0_n',         'Algorithms::getAxisN(0)(RP_thrustangle, RP_charge)')
               .Define('EVT_thrusthemis1_n',         'Algorithms::getAxisN(1)(RP_thrustangle, RP_charge)')
               .Define('EVT_thrusthemis0_e',         'Algorithms::getAxisEnergy(0)(RP_thrustangle, RP_charge, RP_e)')
               .Define('EVT_thrusthemis1_e',         'Algorithms::getAxisEnergy(1)(RP_thrustangle, RP_charge, RP_e)')
               .Define('EVT_thrutshemis0_ncharged',  'EVT_thrusthemis0_n.at(1)')
               .Define('EVT_thrutshemis0_nneutral',  'EVT_thrusthemis0_n.at(2)')
               .Define('EVT_thrutshemis0_echarged',  'EVT_thrusthemis0_e.at(1)')
               .Define('EVT_thrutshemis0_eneutral',  'EVT_thrusthemis0_e.at(2)')
               .Define('EVT_thrutshemis1_ncharged',  'EVT_thrusthemis1_n.at(1)')
               .Define('EVT_thrutshemis1_nneutral',  'EVT_thrusthemis1_n.at(2)')
               .Define('EVT_thrutshemis1_echarged',  'EVT_thrusthemis1_e.at(1)')
               .Define('EVT_thrutshemis1_eneutral',  'EVT_thrusthemis1_e.at(2)')

               .Define('EVT_thrusthemis_emax','if (EVT_thrusthemis0_e.at(0)>EVT_thrusthemis1_e.at(0)) return EVT_thrusthemis0_e.at(0); else return EVT_thrusthemis1_e.at(0);')
               .Define('EVT_thrusthemis_emin','if (EVT_thrusthemis0_e.at(0)>EVT_thrusthemis1_e.at(0)) return EVT_thrusthemis1_e.at(0); else return EVT_thrusthemis0_e.at(0);')
               
               .Define('EVT_Echarged_max', 'if (EVT_thrutshemis0_echarged>EVT_thrutshemis1_echarged) return EVT_thrutshemis0_echarged; else return EVT_thrutshemis1_echarged')
               .Define('EVT_Echarged_min', 'if (EVT_thrutshemis0_echarged>EVT_thrutshemis1_echarged) return EVT_thrutshemis1_echarged; else return EVT_thrutshemis0_echarged')
               .Define('EVT_Eneutral_max', 'if (EVT_thrutshemis0_eneutral>EVT_thrutshemis1_eneutral) return EVT_thrutshemis0_eneutral; else return EVT_thrutshemis1_eneutral')
               .Define('EVT_Eneutral_min', 'if (EVT_thrutshemis0_eneutral>EVT_thrutshemis1_eneutral) return EVT_thrutshemis1_eneutral; else return EVT_thrutshemis0_eneutral')

               .Define('EVT_Ncharged_max','if (EVT_thrutshemis0_ncharged>EVT_thrutshemis1_ncharged) return float(EVT_thrutshemis0_ncharged); else return float(EVT_thrutshemis1_ncharged)')
               .Define('EVT_Ncharged_min','if (EVT_thrutshemis0_ncharged>EVT_thrutshemis1_ncharged) return float(EVT_thrutshemis1_ncharged); else return float(EVT_thrutshemis0_ncharged)')
               .Define('EVT_Nneutral_max','if (EVT_thrutshemis0_nneutral>EVT_thrutshemis1_nneutral) return float(EVT_thrutshemis0_nneutral); else return float(EVT_thrutshemis1_nneutral)')
               .Define('EVT_Nneutral_min','if (EVT_thrutshemis0_nneutral>EVT_thrutshemis1_nneutral) return float(EVT_thrutshemis1_nneutral); else return float(EVT_thrutshemis0_nneutral)')

               
               #Build MC Vertex
               .Define("MCVertexObject", "myUtils::get_MCVertexObject(Particle, Particle0)")
               .Define("MC_Vertex_x",    "myUtils::get_MCVertex_x(MCVertexObject)")
               .Define("MC_Vertex_y",    "myUtils::get_MCVertex_y(MCVertexObject)")
               .Define("MC_Vertex_z",    "myUtils::get_MCVertex_z(MCVertexObject)")
               .Define("MC_Vertex_ind",  "myUtils::get_MCindMCVertex(MCVertexObject)")
               .Define("MC_Vertex_ntrk", "myUtils::get_NTracksMCVertex(MCVertexObject)")
               .Define("MC_Vertex_n",    "int(MC_Vertex_x.size())")
               .Define("MC_Vertex_PDG",  "myUtils::get_MCpdgMCVertex(MCVertexObject, Particle)")
               .Define("MC_Vertex_PDGmother",  "myUtils::get_MCpdgMotherMCVertex(MCVertexObject, Particle)")
               .Define("MC_Vertex_PDGgmother", "myUtils::get_MCpdgGMotherMCVertex(MCVertexObject, Particle)")
               
               #Build Reco Vertex
               .Define("VertexObject", "myUtils::get_VertexObject(MCVertexObject,ReconstructedParticles,EFlowTrack_1,MCRecoAssociations0,MCRecoAssociations1)")

               #Filter when no PV is reconstructed
               .Define("EVT_hasPV",    "myUtils::hasPV(VertexObject)")
               .Filter("EVT_hasPV==1")
               #
               .Define("EVT_NtracksPV", "float(myUtils::get_PV_ntracks(VertexObject))")
               .Define("EVT_NVertex",   "float(VertexObject.size())")
  
               .Define("Vertex_x",     "myUtils::get_Vertex_x(VertexObject)")
               .Define("Vertex_y",     "myUtils::get_Vertex_y(VertexObject)")
               .Define("Vertex_z",     "myUtils::get_Vertex_z(VertexObject)")
               .Define("Vertex_xErr",  "myUtils::get_Vertex_xErr(VertexObject)")
               .Define("Vertex_yErr",  "myUtils::get_Vertex_yErr(VertexObject)")
               .Define("Vertex_zErr",  "myUtils::get_Vertex_zErr(VertexObject)")

               .Define("Vertex_chi2",  "myUtils::get_Vertex_chi2(VertexObject)")
               .Define("Vertex_mcind", "myUtils::get_Vertex_indMC(VertexObject)")
               .Define("Vertex_ind",   "myUtils::get_Vertex_ind(VertexObject)")
               .Define("Vertex_isPV",  "myUtils::get_Vertex_isPV(VertexObject)")
               .Define("Vertex_ntrk",  "myUtils::get_Vertex_ntracks(VertexObject)")
               .Define("Vertex_n",     "int(Vertex_x.size())")

               .Define("Vertex_d2PV",  "myUtils::get_Vertex_d2PV(VertexObject,-1)")
               .Define("Vertex_d2PVx", "myUtils::get_Vertex_d2PV(VertexObject,0)")
               .Define("Vertex_d2PVy", "myUtils::get_Vertex_d2PV(VertexObject,1)")
               .Define("Vertex_d2PVz", "myUtils::get_Vertex_d2PV(VertexObject,2)")
               
               .Define("Vertex_d2PVErr", "myUtils::get_Vertex_d2PVError(VertexObject,-1)")
               .Define("Vertex_d2PVxErr","myUtils::get_Vertex_d2PVError(VertexObject,0)")
               .Define("Vertex_d2PVyErr","myUtils::get_Vertex_d2PVError(VertexObject,1)")
               .Define("Vertex_d2PVzErr","myUtils::get_Vertex_d2PVError(VertexObject,2)")
               
               .Define("Vertex_d2PVSig",  "Vertex_d2PV/Vertex_d2PVErr")
               .Define("Vertex_d2PVxSig", "Vertex_d2PVx/Vertex_d2PVxErr")
               .Define("Vertex_d2PVySig", "Vertex_d2PVy/Vertex_d2PVyErr")
               .Define("Vertex_d2PVzSig", "Vertex_d2PVz/Vertex_d2PVzErr")

               .Define("Vertex_d2MC",   "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,-1)")
               .Define("Vertex_d2MCx",  "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,0)")
               .Define("Vertex_d2MCy",  "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,1)")
               .Define("Vertex_d2MCz",  "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,2)")

               .Define("RecoPartPID" ,"myUtils::PID(ReconstructedParticles, MCRecoAssociations0,MCRecoAssociations1,Particle)")
               .Define("RecoPartPIDAtVertex" ,"myUtils::get_RP_atVertex(RecoPartPID, VertexObject)")
               
               #build_tau23pi(float arg_masslow, float arg_masshigh, float arg_p, float arg_angle, bool arg_rho)
               .Define("Tau23PiCandidates",         "myUtils::build_tau23pi(VertexObject,RecoPartPIDAtVertex)")
               .Define("EVT_NTau23Pi",              "float(myUtils::getFCCAnalysesComposite_N(Tau23PiCandidates))")
               .Filter("EVT_NTau23Pi>0")

               .Define("Vertex_thrusthemis_angle",   "myUtils::get_Vertex_thrusthemis_angle(VertexObject, RecoPartPIDAtVertex, EVT_thrust)")
               #hemis0 == negative angle, hemis1 == positive angle
               .Define("Vertex_thrusthemis_emin",    "myUtils::get_Vertex_thrusthemis_emin(Vertex_thrusthemis_angle, EVT_thrusthemis0_e.at(0), EVT_thrusthemis1_e.at(0))")
               .Define("EVT_dPV2DVmin", "myUtils::get_dPV2DV_min(Vertex_d2PV)")
               .Define("EVT_dPV2DVmax", "myUtils::get_dPV2DV_max(Vertex_d2PV)")
               .Define("EVT_dPV2DVave", "myUtils::get_dPV2DV_ave(Vertex_d2PV)")
               .Define("EVT_NDV_hemis0", "float(myUtils::get_Npos(Vertex_thrusthemis_angle))")
               .Define("EVT_NDV_hemis1", "float(myUtils::get_Nneg(Vertex_thrusthemis_angle))")

               
               #Build MVA with only thrust info
               .Define("MVAVec", ROOT.computeModel, ("EVT_thrusthemis_emin", "EVT_thrusthemis_emax",
                                                     "EVT_Echarged_min",     "EVT_Echarged_max",
                                                     "EVT_Eneutral_min",     "EVT_Eneutral_max",
                                                     "EVT_Ncharged_min",     "EVT_Ncharged_max",
                                                     "EVT_Nneutral_min",     "EVT_Nneutral_max",
                                                     "EVT_NtracksPV",        "EVT_NVertex",
                                                     "EVT_NTau23Pi",         "EVT_NDV_hemis0",
                                                     "EVT_NDV_hemis1",       "EVT_dPV2DVmin",
                                                     "EVT_dPV2DVmax",        "EVT_dPV2DVave"))
               .Define("MVA", "MVAVec.at(0)")
               .Filter("MVA>0.6")
 
               .Define("Tau23PiCandidates_mass",    "myUtils::getFCCAnalysesComposite_mass(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_q",       "myUtils::getFCCAnalysesComposite_charge(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_vertex",  "myUtils::getFCCAnalysesComposite_vertex(Tau23PiCandidates)")
               .Define("Tau23PiCandidates_mcvertex","myUtils::getFCCAnalysesComposite_mcvertex(Tau23PiCandidates,VertexObject)")
               .Define("Tau23PiCandidates_px",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,0)")
               .Define("Tau23PiCandidates_py",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,1)")
               .Define("Tau23PiCandidates_pz",      "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,2)")
               .Define("Tau23PiCandidates_p",       "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates,-1)")
               .Define("Tau23PiCandidates_B",       "myUtils::getFCCAnalysesComposite_B(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex)")
               
               .Define("Tau23PiCandidates_track",   "myUtils::getFCCAnalysesComposite_track(Tau23PiCandidates, VertexObject)")
               .Define("Tau23PiCandidates_d0",      "myUtils::get_trackd0(Tau23PiCandidates_track)")
               .Define("Tau23PiCandidates_z0",      "myUtils::get_trackz0(Tau23PiCandidates_track)")

               .Define("Tau23PiCandidates_rho",     "myUtils::build_rho(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex)")
               .Define("Tau23PiCandidates_rho1mass","myUtils::get_mass(Tau23PiCandidates_rho, 0)")
               .Define("Tau23PiCandidates_rho2mass","myUtils::get_mass(Tau23PiCandidates_rho, 1)")

               .Define("Tau23PiCandidates_pion1px", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 0)")
               .Define("Tau23PiCandidates_pion1py", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 1)")
               .Define("Tau23PiCandidates_pion1pz", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 2)")
               .Define("Tau23PiCandidates_pion1p",  "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0, -1)")
               .Define("Tau23PiCandidates_pion1q",  "myUtils::getFCCAnalysesComposite_q(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 0)")
               .Define("Tau23PiCandidates_pion1d0", "myUtils::getFCCAnalysesComposite_d0(Tau23PiCandidates, VertexObject, 0)")
               .Define("Tau23PiCandidates_pion1z0", "myUtils::getFCCAnalysesComposite_z0(Tau23PiCandidates, VertexObject, 0)")
               
               .Define("Tau23PiCandidates_pion2px", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 0)")
               .Define("Tau23PiCandidates_pion2py", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 1)")
               .Define("Tau23PiCandidates_pion2pz", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 2)")
               .Define("Tau23PiCandidates_pion2p",  "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1, -1)")
               .Define("Tau23PiCandidates_pion2q",  "myUtils::getFCCAnalysesComposite_q(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 1)")
               .Define("Tau23PiCandidates_pion2d0", "myUtils::getFCCAnalysesComposite_d0(Tau23PiCandidates, VertexObject, 1)")
               .Define("Tau23PiCandidates_pion2z0", "myUtils::getFCCAnalysesComposite_z0(Tau23PiCandidates, VertexObject, 1)")
               
               .Define("Tau23PiCandidates_pion3px", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, 0)")
               .Define("Tau23PiCandidates_pion3py", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, 1)")
               .Define("Tau23PiCandidates_pion3pz", "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, 2)")
               .Define("Tau23PiCandidates_pion3p",  "myUtils::getFCCAnalysesComposite_p(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2, -1)")
               .Define("Tau23PiCandidates_pion3q",  "myUtils::getFCCAnalysesComposite_q(Tau23PiCandidates, VertexObject, RecoPartPIDAtVertex, 2)")
               .Define("Tau23PiCandidates_pion3d0", "myUtils::getFCCAnalysesComposite_d0(Tau23PiCandidates, VertexObject, 2)")
               .Define("Tau23PiCandidates_pion3z0", "myUtils::getFCCAnalysesComposite_z0(Tau23PiCandidates, VertexObject, 2)")

               .Define("TrueTau23Pi_vertex",        "myUtils::get_trueVertex(MCVertexObject,Particle,Particle0, 15, 541)")
               .Define("TrueTau23Pi_track",         "myUtils::get_truetrack(TrueTau23Pi_vertex, MCVertexObject, Particle)")
               .Define("TrueTau23Pi_d0",            "myUtils::get_trackd0(TrueTau23Pi_track)")
               .Define("TrueTau23Pi_z0",            "myUtils::get_trackz0(TrueTau23Pi_track)")

               #.Define("TrueRho", "myUtils::build_truerho(TrueTau23Pi_vertex,MCVertexObject,Particle)")
               #.Define("TrueRho1M", "TrueRho.at(0).mass")
               #.Define("TrueRho2M", "TrueRho.at(1).mass")
               


               
               
           )
        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [

                "MC_PDG","MC_M1","MC_M2","MC_n","MC_D1","MC_D2",
                "EVT_thrusthemis_emin", "EVT_thrusthemis_emax",
                "EVT_Echarged_min", "EVT_Echarged_max",
                "EVT_Eneutral_min", "EVT_Eneutral_max",
                "EVT_Ncharged_min", "EVT_Ncharged_max",
                "EVT_Nneutral_min", "EVT_Nneutral_max",
                "EVT_NtracksPV", "EVT_NVertex", "EVT_NTau23Pi",
                
                "MC_Vertex_x", "MC_Vertex_y", "MC_Vertex_z", 
                "MC_Vertex_ntrk", "MC_Vertex_n",
                
                "MC_Vertex_PDG","MC_Vertex_PDGmother","MC_Vertex_PDGgmother",
                
                "Vertex_x", "Vertex_y", "Vertex_z",
                "Vertex_xErr", "Vertex_yErr", "Vertex_zErr",
                "Vertex_isPV", "Vertex_ntrk", "Vertex_chi2", "Vertex_n",
                "Vertex_thrusthemis_angle", "Vertex_thrusthemis_emin",

                "Vertex_d2PV", "Vertex_d2PVx", "Vertex_d2PVy", "Vertex_d2PVz",
                "Vertex_d2PVErr", "Vertex_d2PVxErr", "Vertex_d2PVyErr", "Vertex_d2PVzErr",
                
                "MVA","EVT_hasPV",

                "TrueTau23Pi_vertex","TrueTau23Pi_d0","TrueTau23Pi_z0",
                
                "Tau23PiCandidates_mass", "Tau23PiCandidates_vertex", "Tau23PiCandidates_mcvertex", "Tau23PiCandidates_B",
                "Tau23PiCandidates_px", "Tau23PiCandidates_py", "Tau23PiCandidates_pz", "Tau23PiCandidates_p", "Tau23PiCandidates_q",  "Tau23PiCandidates_d0",  "Tau23PiCandidates_z0",
                #"Tau23PiCandidates_rho1px", "Tau23PiCandidates_rho1py", "Tau23PiCandidates_rho1pz",
                "Tau23PiCandidates_rho1mass",
                #"Tau23PiCandidates_rho2px", "Tau23PiCandidates_rho2py", "Tau23PiCandidates_rho2pz",
                "Tau23PiCandidates_rho2mass",
                
                "Tau23PiCandidates_pion1px", "Tau23PiCandidates_pion1py", "Tau23PiCandidates_pion1pz", "Tau23PiCandidates_pion1p", "Tau23PiCandidates_pion1q", "Tau23PiCandidates_pion1d0", "Tau23PiCandidates_pion1z0",
                "Tau23PiCandidates_pion2px", "Tau23PiCandidates_pion2py", "Tau23PiCandidates_pion2pz", "Tau23PiCandidates_pion2p", "Tau23PiCandidates_pion2q", "Tau23PiCandidates_pion2d0", "Tau23PiCandidates_pion2z0",
                "Tau23PiCandidates_pion3px", "Tau23PiCandidates_pion3py", "Tau23PiCandidates_pion3pz", "Tau23PiCandidates_pion3p", "Tau23PiCandidates_pion3q", "Tau23PiCandidates_pion3d0", "Tau23PiCandidates_pion3z0",
                
                #"TrueRho1M",
                #"TrueRho2M",
                
                
                ]:
            branchList.push_back(branchName)

        #opts = ROOT.RDF.RSnapshotOptions()
        #opts.fCompressionAlgorithm = ROOT.ROOT.kLZ4
        #opts.fCompressionLevel = 3
        #opts.fAutoFlush = -1024*1024*branchList.size()
        #df2.Snapshot("events", self.outname, branchList, opts)
        df2.Snapshot("events", self.outname, branchList)

# example call for standalone file
# python examples/FCCee/flavour/Bc2TauNu/analysis.py flat_ee_Zbb_Bc2TauNu.root /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp_v03/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/events_003834121.root

# python examples/FCCee/flavour/Bc2TauNu/analysis.py flat_ee_Zbb_Bu2TauNu.root /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp_v03/p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU/events_026079857.root

# python examples/FCCee/flavour/Bc2TauNu/analysis.py  flat_ee_Zbb_Bc2TauNu.root "/eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp_v03/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/events_*"

# python examples/FCCee/flavour/Bc2TauNu/analysis.py flat_ee_Zbb.root  /eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp_v03/p8_ee_Zbb_ecm91/events_026734131.root



if __name__ == "__main__":

    if len(sys.argv)<3:
        print ("usage:")
        print ("python ",sys.argv[0]," output.root input.root")
        print ("python ",sys.argv[0]," output.root \"inputdir/*.root\"")
        print ("python ",sys.argv[0]," output.root file1.root file2.root file3.root <nevents>")
        sys.exit(3)


    print ("Create dataframe object from ", )
    fileListRoot = ROOT.vector('string')()
    nevents=0

    if len(sys.argv)==3 and "*" in sys.argv[2]:
        import glob
        filelist = glob.glob(sys.argv[2])
        for fileName in filelist:
            fileListRoot.push_back(fileName)
            print (fileName, " ",)
            print (" ...")


    elif len(sys.argv)>2:
        for i in range(2,len(sys.argv)):
            try:
                nevents=int(sys.argv[i])
                print ('nevents found (will be in the processed events branch in roo tree):',nevents)
            except ValueError:
                fileListRoot.push_back(sys.argv[i])
                print (sys.argv[i], " ",)
                print (" ...")

                         
    outfile=sys.argv[1]
    print('output file:  ',outfile)
    if len(outfile.split('/'))>1:
        import os
        os.system("mkdir -p {}".format(outfile.replace(outfile.split('/')[-1],'')))

    if nevents==0:
        for f in fileListRoot:
            tf=ROOT.TFile.Open(str(f),"READ")
            tt=tf.Get("events")
            nevents+=tt.GetEntries()
    print ("nevents ", nevents)
    
    import time
    start_time = time.time()
    ncpus = 8
    analysis = analysis(fileListRoot, outfile, ncpus)
    analysis.run()

    elapsed_time = time.time() - start_time
    print  ('==============================SUMMARY==============================')
    print  ('Elapsed time (H:M:S)     :  ',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print  ('Events Processed/Second  :  ',int(nevents/elapsed_time))
    print  ('Total Events Processed   :  ',int(nevents))
    print  ('===================================================================')

    
    outf = ROOT.TFile( outfile, 'update' )
    meta = ROOT.TTree( 'metadata', 'metadata informations' )
    n = array( 'i', [ 0 ] )
    meta.Branch( 'eventsProcessed', n, 'eventsProcessed/I' )
    n[0]=nevents
    meta.Fill()
    p = ROOT.TParameter(int)( "eventsProcessed", n[0])
    p.Write()
    outf.Write()
    outf.Close()

