import sys
import ROOT

#choose to run Bc2TauNu or Bu2TauNu depending on the PDGIG
PDGID=541 #Bc
#PDGID=521 #B

Filter=""
if PDGID==541:
    #very small BR so filter to be more efficient in CPU
    Filter="FCCAnalyses::MCParticle::filter_pdgID(541, true)(Particle)==true"
elif PDGID==521:
    #Complex filter not to have two B in the event that would decay exclusively
    Filter="(FCCAnalyses::MCParticle::filter_pdgID(521, false)(Particle)==true && FCCAnalyses::MCParticle::filter_pdgID(-521, false)(Particle)==false) || (FCCAnalyses::MCParticle::filter_pdgID(521, false)(Particle)==false && FCCAnalyses::MCParticle::filter_pdgID(-521, false)(Particle)==true)"

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gSystem.Load("libFCCAnalysesFlavour")

ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader
_bs  = ROOT.dummyLoaderFlavour


print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

ROOT.gInterpreter.Declare("""
edm4hep::Vector3d MyMCDecayVertex(ROOT::VecOps::RVec<edm4hep::Vector3d> in1, ROOT::VecOps::RVec<edm4hep::Vector3d> in2) {

   edm4hep::Vector3d vertex(1e12, 1e12, 1e12);
   if ( in1.size() == 0 && in2.size()==0) {
      std::cout <<"no vtx " <<std::endl;
      return vertex;
   }

   if ( in1.size() == 1 && in2.size()==0) vertex=in1[0];
   else if ( in1.size() == 0 && in2.size()==1) vertex=in2[0];
   else{
std::cout << "in1.size() " << in1.size() << "  in2.size() " <<in1.size()<< std::endl;
   }
   return vertex;
}

""")

ROOT.gInterpreter.Declare("""
float MyMinEnergy(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {

   float min=999999.;
   for (auto & p: in) {
    if (p.energy<min && p.energy>0) min=p.energy;
  }
  return min;
}

""")

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
        #df2 = (self.df.Range(10)
        df2 = (self.df
               #.Filter(Filter)

               .Alias("Particle1", "Particle#1.index")
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

               # MC event primary vertex
               .Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(21)( Particle )" )

               # number of tracks
               .Define("ntracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")

               # Retrieve the decay vertex of all MC particles
               .Define("MC_DecayVertices",  "FCCAnalyses::MCParticle::get_endPoint( Particle, Particle1)" )

               # MC indices of the decay Bc/Bu -> nu nu pi+ pi- pi+
               #     - if the event contains > 1 such decays, the first one is kept
               #     - the cases Bs -> Bsbar -> mu mu K K are included here
               #   first boolean: if true, look at the stable daughters, otherwise at the intermediate daughters
               #   second boolean: if true, include the charge conjugate decays
               .Define("B2NuNuPiPiPi_indices",   "FCCAnalyses::MCParticle::get_indices_ExclusiveDecay( %s, { 16, -16, 211, -211, 211 }, true, false)( Particle, Particle1)"%(PDGID))
               .Define("Bbar2NuNuPiPiPi_indices","FCCAnalyses::MCParticle::get_indices_ExclusiveDecay( -%s, { -16, 16, -211, 211, -211 }, true, false)( Particle, Particle1)"%(PDGID))

               .Define("Piminus", "selMC_leg(4) ( B2NuNuPiPiPi_indices , Particle)" )
               .Define("Piplus",  "selMC_leg(4) ( Bbar2NuNuPiPiPi_indices , Particle)" )
               .Define("TauMCDecayVertex",  "MyMCDecayVertex(FCCAnalyses::MCParticle::get_vertex(Piminus),FCCAnalyses::MCParticle::get_vertex(Piplus))")

               # the MC Bc or Bcbar:
               .Define("B",  "if (B2NuNuPiPiPi_indices.size()>0) return selMC_leg(0) (B2NuNuPiPiPi_indices , Particle ); else return selMC_leg(0) (Bbar2NuNuPiPiPi_indices , Particle );")

                # Kinematics of the B :
               .Define("B_theta", "FCCAnalyses::MCParticle::get_theta( B )")
               .Define("B_phi",   "FCCAnalyses::MCParticle::get_phi( B )")
               .Define("B_e",     "FCCAnalyses::MCParticle::get_e( B )")
               .Define("B_charge","FCCAnalyses::MCParticle::get_charge( B )")

                # and the MC legs of the B :
               .Define("Nu1_vec",  "if (B2NuNuPiPiPi_indices.size()>0) return selMC_leg(1) (B2NuNuPiPiPi_indices , Particle ); else return selMC_leg(1) (Bbar2NuNuPiPiPi_indices , Particle );")
               .Define("Nu2_vec",  "if (B2NuNuPiPiPi_indices.size()>0) return selMC_leg(2) (B2NuNuPiPiPi_indices , Particle ); else return selMC_leg(2) (Bbar2NuNuPiPiPi_indices , Particle );")
               .Define("Pion1_vec",  "if (B2NuNuPiPiPi_indices.size()>0) return selMC_leg(3) (B2NuNuPiPiPi_indices , Particle ); else return selMC_leg(3) (Bbar2NuNuPiPiPi_indices , Particle );")
               .Define("Pion2_vec",  "if (B2NuNuPiPiPi_indices.size()>0) return selMC_leg(4) (B2NuNuPiPiPi_indices , Particle ); else return selMC_leg(4) (Bbar2NuNuPiPiPi_indices , Particle );")
               .Define("Pion3_vec",  "if (B2NuNuPiPiPi_indices.size()>0) return selMC_leg(5) (B2NuNuPiPiPi_indices , Particle ); else return selMC_leg(5) (Bbar2NuNuPiPiPi_indices , Particle );")

               .Define("Nu1e_vec",     "FCCAnalyses::MCParticle::get_e( Nu1_vec )")
               .Define("Nu2e_vec",     "FCCAnalyses::MCParticle::get_e( Nu2_vec )")
               .Define("Pion1e_vec",   "FCCAnalyses::MCParticle::get_e( Pion1_vec )")
               .Define("Pion2e_vec",   "FCCAnalyses::MCParticle::get_e( Pion2_vec )")
               .Define("Pion3e_vec",   "FCCAnalyses::MCParticle::get_e( Pion3_vec )")


               # as the size can be 0, need to do this trick to avoid crashes
               .Define("Nu1",  "if (Nu1e_vec.size()>0 && Nu2e_vec.size()>0 && Nu1e_vec[0] > Nu2e_vec[0]) return Nu1_vec; else return Nu2_vec;")
               .Define("Nu2",  "if (Nu1e_vec.size()>0 && Nu2e_vec.size()>0 && Nu1e_vec[0] < Nu2e_vec[0]) return Nu1_vec; else return Nu2_vec;")
               .Define("Pion1", "if (Pion1e_vec.size()>0 && Pion2e_vec.size()>0 && Pion3e_vec.size()>0 && Pion1e_vec[0] > Pion2e_vec[0] && Pion1e_vec[0] > Pion3e_vec[0]) return Pion1_vec; else if (Pion1e_vec.size()>0 && Pion2e_vec.size()>0 && Pion3e_vec.size()>0 && Pion2e_vec[0]>Pion1e_vec[0] && Pion2e_vec[0]>Pion3e_vec[0]) return Pion2_vec; else return Pion3_vec;")
               .Define("Pion2", "if (Pion1e_vec.size()>0 && Pion2e_vec.size()>0 && Pion3e_vec.size()>0 && Pion1e_vec[0] < Pion2e_vec[0] && Pion1e_vec[0] > Pion3e_vec[0]) return Pion1_vec; else if (Pion1e_vec.size()>0 && Pion2e_vec.size()>0 && Pion3e_vec.size()>0 && Pion2e_vec[0]<Pion1e_vec[0] && Pion2e_vec[0]>Pion3e_vec[0]) return Pion2_vec; else return Pion3_vec;")
               .Define("Pion3", "if (Pion1e_vec.size()>0 && Pion2e_vec.size()>0 && Pion3e_vec.size()>0 && Pion1e_vec[0] < Pion2e_vec[0] && Pion1e_vec[0] < Pion3e_vec[0]) return Pion1_vec; else if (Pion1e_vec.size()>0 && Pion2e_vec.size()>0 && Pion3e_vec.size()>0 && Pion2e_vec[0]<Pion1e_vec[0] && Pion2e_vec[0]<Pion3e_vec[0]) return Pion2_vec; else return Pion3_vec;")


               # Kinematics of the B decay:
               .Define("Nu1_theta", "FCCAnalyses::MCParticle::get_theta( Nu1 )")
               .Define("Nu1_phi",   "FCCAnalyses::MCParticle::get_phi( Nu1 )")
               .Define("Nu1_e",     "FCCAnalyses::MCParticle::get_e( Nu1 )")
               .Define("Nu1_charge","FCCAnalyses::MCParticle::get_charge( Nu1 )")

               .Define("Nu2_theta", "FCCAnalyses::MCParticle::get_theta( Nu2 )")
               .Define("Nu2_phi",   "FCCAnalyses::MCParticle::get_phi( Nu2 )")
               .Define("Nu2_e",     "FCCAnalyses::MCParticle::get_e( Nu2 )")
               .Define("Nu2_charge","FCCAnalyses::MCParticle::get_charge( Nu2 )")

               .Define("Pion1_theta", "FCCAnalyses::MCParticle::get_theta( Pion1 )")
               .Define("Pion1_phi",   "FCCAnalyses::MCParticle::get_phi( Pion1 )")
               .Define("Pion1_e",     "FCCAnalyses::MCParticle::get_e( Pion1 )")
               .Define("Pion1_charge","FCCAnalyses::MCParticle::get_charge( Pion1 )")

               .Define("Pion2_theta", "FCCAnalyses::MCParticle::get_theta( Pion2 )")
               .Define("Pion2_phi",   "FCCAnalyses::MCParticle::get_phi( Pion2 )")
               .Define("Pion2_e",     "FCCAnalyses::MCParticle::get_e( Pion2 )")
               .Define("Pion2_charge","FCCAnalyses::MCParticle::get_charge( Pion2 )")

               .Define("Pion3_theta", "FCCAnalyses::MCParticle::get_theta( Pion3 )")
               .Define("Pion3_phi",   "FCCAnalyses::MCParticle::get_phi( Pion3 )")
               .Define("Pion3_e",     "FCCAnalyses::MCParticle::get_e( Pion3 )")
               .Define("Pion3_charge","FCCAnalyses::MCParticle::get_charge( Pion3 )")

               # Returns the RecoParticles associated with the 5 Bc decay products.
               # The size of this collection is always 5 provided that Bc2TauNuNuPiPiPi_indices is not empty,
               # possibly including "dummy" particles in case one of the leg did not make a RecoParticle.
               # This is on purpose, to maintain the mapping with the indices - i.e. the 1st particle in
               # the list is the Nu_taubar, then the Nu_tau, etc.
               .Define("BRecoParticles",  "if (B2NuNuPiPiPi_indices.size()>0) return ReconstructedParticle2MC::selRP_matched_to_list( B2NuNuPiPiPi_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle); else return ReconstructedParticle2MC::selRP_matched_to_list( Bbar2NuNuPiPiPi_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle);")

               #Returns the pion with minimum energy
               .Define("minPionE", "MyMinEnergy(BRecoParticles)")

               # the corresponding tracks - here, dummy particles, if any, are removed
               .Define("BTracks",   "ReconstructedParticle2Track::getRP2TRK( BRecoParticles, EFlowTrack_1)" )

               # number of tracks used to reconstruct the Bc vertex
               .Define("n_BTracks", "ReconstructedParticle2Track::getTK_n( BTracks )")

               # the reco'ed vertex :
               .Define("BVertexObject",   "VertexFitterSimple::VertexFitter_Tk( 2, BTracks)" )
               .Define("BVertex",  "VertexingUtils::get_VertexData( BVertexObject )")

               # Angular separation between the tracks from the Bc decays
               .Define("deltaAlpha_max","ReconstructedParticle::angular_separationBuilder(0)( BRecoParticles )")
               .Define("deltaAlpha_min","ReconstructedParticle::angular_separationBuilder(1)( BRecoParticles )")
               .Define("deltaAlpha_ave","ReconstructedParticle::angular_separationBuilder(2)( BRecoParticles )")

        )


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [

                "ntracks",
                "BVertex",
                "TauMCDecayVertex",
                "n_BTracks",
                "deltaAlpha_max","deltaAlpha_min","deltaAlpha_ave",
                "minPionE",
                "B_theta","B_phi","B_e","B_charge",

                "Nu1_theta","Nu1_phi","Nu1_e","Nu1_charge",

                "Nu2_theta","Nu2_phi","Nu2_e","Nu2_charge",

                "Pion1_theta","Pion1_phi","Pion1_e","Pion1_charge",

                "Pion2_theta","Pion2_phi","Pion2_e","Pion2_charge",

                "Pion3_theta","Pion3_phi","Pion3_e","Pion3_charge",

                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)

# python examples/FCCee/flavour/Bc2TauNu/analysis_B2TauNu_truth.py "/eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp_v03/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/events_1*" events_Bc2TauNuTAUHADNU_truth.root
# python examples/FCCee/flavour/Bc2TauNu/analysis_B2TauNu_truth.py "/eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp_v03/p8_ee_Zbb_ecm91_EvtGen_Bu2TauNuTAUHADNU/events_1*" events_Bu2TauNuTAUHADNU_truth.root


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

    outfile = outDir+'events.root'
    if len(sys.argv)==3:outfile=sys.argv[2]

    ncpus = 8
    analysis = analysis(fileListRoot, outfile, ncpus)
    analysis.run()
