import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyloader


print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

class analysis():

    #__________________________________________________________
    def __init__(self, inputlist, outname, ncpu):
        self.outname = outname
        if ".root" not in outname:
            self.outname+=".root"

        #ROOT.ROOT.EnableImplicitMT(ncpu)

        self.df = ROOT.RDataFrame("events", inputlist)
        print (" done")
    #__________________________________________________________
    def run(self):
        #df2 = (self.df.Range(1000)
        df2 = (self.df

               .Alias("Particle1", "Particle#1.index")
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")


               # MC event primary vertex
               .Define("MC_PrimaryVertex",  "MCParticle::get_EventPrimaryVertex(21)( Particle )" )

               # number of tracks
               .Define("ntracks","getTK_n(EFlowTrack_1)")

               # Retrieve the decay vertex of all MC particles
               .Define("MC_DecayVertices",  "MCParticle::get_endPoint( Particle, Particle1)" )

               # MC indices of the decay Bs -> JPsi Phi
               .Define("Bs2JPsiPhi_indices",   "MCParticle::get_indices_ExclusiveDecay( 531, {443,333}, false, true) ( Particle, Particle1)" )
	       .Define("JPsi",   "selMC_leg( 1) ( Bs2JPsiPhi_indices , Particle )")
               .Define("Phi",   "selMC_leg( 2) ( Bs2JPsiPhi_indices , Particle )")
	       .Define("Angle_JpsiPhi",  "MCParticle::AngleBetweenTwoMCParticles( JPsi, Phi)" )


               # MC indices of the decay Bs -> mu+ mu- K+ K-
               #     - if the event contains > 1 such decays, the first one is kept
               #     - the cases Bs -> Bsbar -> mu mu K K are included here
               #   first boolean: if true, look at the stable daughters, otherwise at the intermediate daughters
               #   second boolean: if true, include the charge conjugate decays 
               .Define("Bs2MuMuKK_indices",  "MCParticle::get_indices_ExclusiveDecay( 531, {-13,13,321,-321}, true, true) ( Particle, Particle1)" )

               # Bs to JPsi decay ?
               # Returns booleans. e.g. the first one means that the event contains a Bs that decayed to a JPsi (443) + X, 
               # not counting the cases where Bs -> Bsbar -> JPsi + X
               # NB: not useful actually, since in the files I process, the decay mode 
               # Bs -> JPsi(mumu) Phi(KK) was forced, both for Bs anf for Bsbar
               .Define("Bsdecay",  "MCParticle::get_decay(531, 443, false)(Particle, Particle1)")
               .Define("Bsbardecay",  "MCParticle::get_decay(-531, 443, false)(Particle, Particle1)")

                # the MC Bs :
               .Define("Bs",  "selMC_leg(0) ( Bs2MuMuKK_indices, Particle )")

                # and the MC legs of the Bs :
               .Define("Muplus",  " selMC_leg(1)( Bs2MuMuKK_indices, Particle )")
               .Define("Muminus",  " selMC_leg(2)( Bs2MuMuKK_indices, Particle )")
               .Define("Kplus",  " selMC_leg(3)( Bs2MuMuKK_indices, Particle )")
               .Define("Kminus",  " selMC_leg(4)( Bs2MuMuKK_indices, Particle )")

                # Kinematics of the Bs legs (MC) :
               .Define("Muplus_theta",  "MCParticle::get_theta( Muplus )")
               .Define("Muplus_phi",  "MCParticle::get_phi( Muplus )")
               .Define("Muplus_e",  "MCParticle::get_e( Muplus )")
               .Define("Muminus_theta",  "MCParticle::get_theta( Muminus )")
               .Define("Muminus_phi",  "MCParticle::get_phi( Muminus )")
               .Define("Muminus_e",  "MCParticle::get_e( Muminus )")
               .Define("Kplus_theta",  "MCParticle::get_theta( Kplus )")
               .Define("Kplus_phi",  "MCParticle::get_phi( Kplus )")
               .Define("Kplus_e",  "MCParticle::get_e( Kplus )")
               .Define("Kminus_theta",  "MCParticle::get_theta( Kminus )")
               .Define("Kminus_phi",  "MCParticle::get_phi( Kminus )")
               .Define("Kminus_e",  "MCParticle::get_e( Kminus )")

               .Define("Bs_theta",   "MCParticle::get_theta( Bs )")
               .Define("Bs_phi",   "MCParticle::get_phi( Bs )")
               .Define("Bs_e",   "MCParticle::get_e( Bs )")

               
               # Decay vertex of theBs
		# does not work...  the endpoint is not filled in the files
               #.Define("BsDecayVertex",  "MCParticle::get_endPoint( Bs )")

               # Careful with the following: if Bs -> Bsbar, this returns the prod vertex of the Bsbar !
               #.Define("BsDecayVertex",   "getMC_decayVertex(531, false)( Particle, Particle1)")

               # Better use a custom method in Bs2JPsiPhi :
               .Define("BsMCDecayVertex",   "BsMCDecayVertex( Bs2MuMuKK_indices, Particle )")

               # Returns the RecoParticles associated with the 4 Bs decay products.
               # The size of this collection is always 4 provided that Bs2MuMuKK_indices is not empty,
               # possibly including "dummy" particles in case one of the leg did not make a RecoParticle.
               # This is on purpose, to maintain the mapping with the indices - i.e. the 1st particle in 
               # the list is the mu+, then the mu-, etc.
               .Define("BsRecoParticles",  "selRP_matched_to_list( Bs2MuMuKK_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")

               # the corresponding tracks - here, dummy particles, if any, are removed
               .Define("BsTracks",   "getRP2TRK( BsRecoParticles, EFlowTrack_1)" )

               # number of tracks used to reconstruct the Bs vertex 
               .Define("n_BsTracks", "getTK_n( BsTracks )")

               # the reco'ed vertex :
               .Define("BsVertexObject",   "Vertexing::VertexFitter_Tk( 2, BsTracks)" )
               .Define("BsVertex",  "Vertexing::get_VertexData( BsVertexObject )")

               # Angular separation between the tracks from the Bs decays
               .Define("deltaAlpha_max","angular_separation(0)( BsRecoParticles )")
               .Define("deltaAlpha_min","angular_separation(1)( BsRecoParticles )")
               .Define("deltaAlpha_ave","angular_separation(2)( BsRecoParticles )")

               # the reco'ed Bs legs
               .Define("RecoMuplus",   "selRP_leg(0)( BsRecoParticles )")
               .Define("RecoMuminus",  "selRP_leg(1)( BsRecoParticles )")
               .Define("RecoKplus",    "selRP_leg(2)( BsRecoParticles )")
               .Define("RecoKminus",   "selRP_leg(3)( BsRecoParticles )")
               # and the kinematics :
               .Define("RecoMuplus_theta",  "getRP_theta( RecoMuplus )")
               .Define("RecoMuplus_phi",  "getRP_phi( RecoMuplus )")
               .Define("RecoMuplus_e",  "getRP_e( RecoMuplus )")
               .Define("RecoMuminus_theta",  "getRP_theta( RecoMuminus )")
               .Define("RecoMuminus_phi",  "getRP_phi( RecoMuminus )")
               .Define("RecoMuminus_e",  "getRP_e( RecoMuminus )")
               .Define("RecoKplus_theta",  "getRP_theta( RecoKplus )")
               .Define("RecoKplus_phi",  "getRP_phi( RecoKplus )")
               .Define("RecoKplus_e",  "getRP_e( RecoKplus )")
               .Define("RecoKminus_theta",  "getRP_theta( RecoKminus )")
               .Define("RecoKminus_phi",  "getRP_phi( RecoKminus )")
               .Define("RecoKminus_e",  "getRP_e( RecoKminus )")

               # the reco'ed legs, with the momenta at the Bs decay vertex
	       # This is not needed for the vertexing here. This was mostly to check
     	       # my propagation of the tracks from their point of dca to the Bs vertex.
               .Define("RecoMuplus_atVertex",  "selRP_leg_atVertex(0) ( BsRecoParticles, BsVertexObject, EFlowTrack_1 )")
               .Define("RecoMuplus_atVertex_theta",   "getRP_theta( RecoMuplus_atVertex )")
               .Define("RecoMuplus_atVertex_phi",   "getRP_phi( RecoMuplus_atVertex )")
               .Define("RecoMuminus_atVertex",  "selRP_leg_atVertex(1) ( BsRecoParticles, BsVertexObject, EFlowTrack_1 )")
               .Define("RecoMuminus_atVertex_theta",   "getRP_theta( RecoMuminus_atVertex )")
               .Define("RecoMuminus_atVertex_phi",   "getRP_phi( RecoMuminus_atVertex )")
               .Define("RecoKplus_atVertex",  "selRP_leg_atVertex(2) ( BsRecoParticles, BsVertexObject, EFlowTrack_1 )")
               .Define("RecoKplus_atVertex_theta",   "getRP_theta( RecoKplus_atVertex )")
               .Define("RecoKplus_atVertex_phi",   "getRP_phi( RecoKplus_atVertex )")
               .Define("RecoKminus_atVertex",  "selRP_leg_atVertex(3) ( BsRecoParticles, BsVertexObject, EFlowTrack_1 )")
               .Define("RecoKminus_atVertex_theta",   "getRP_theta( RecoKminus_atVertex )")
               .Define("RecoKminus_atVertex_phi",   "getRP_phi( RecoKminus_atVertex )")


        )


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "MC_PrimaryVertex",
                "ntracks",
                #"Bs2JPsiPhi_indices",
                #"Bs2MuMuKK_indices",
                #"Muplus",
                #"Muminus",
                #"Kplus",
                #"Kminus",

	        # Kinematics of the MC particles:
                "Muplus_theta",
                "Muplus_phi",
                "Muplus_e",
                "Muminus_theta",
                "Muminus_phi",
                "Muminus_e",
                "Kplus_theta",
                "Kplus_phi",
                "Kplus_e",
                "Kminus_theta",
                "Kminus_phi",
                "Kminus_e",
                "Bs_theta",
                "Bs_phi",
                "Bs_e",

                "Bsdecay",
                "Bsbardecay",
                "BsMCDecayVertex",

		# Reco'ed Bs vertex :
                "BsVertex",
                #"BsTracks",
                "n_BsTracks",
                "deltaAlpha_max",
                "deltaAlpha_min",
                "deltaAlpha_ave",
                #"BsRecoParticles",

	        # Kinematics of the Reco'ed particles:
                "RecoMuplus_theta",
                "RecoMuplus_phi",
                "RecoMuplus_e",
                "RecoMuminus_theta",
                "RecoMuminus_phi",
                "RecoMuminus_e",
                "RecoKplus_theta",
                "RecoKplus_phi",
                "RecoKplus_e",
                "RecoKminus_theta",
                "RecoKminus_phi",
                "RecoKminus_e",

                "RecoMuplus_atVertex_theta",
                "RecoMuplus_atVertex_phi",
                "RecoMuminus_atVertex_theta",
                "RecoMuminus_atVertex_phi",
                "RecoKplus_atVertex_theta",
                "RecoKplus_atVertex_phi",
                "RecoKminus_atVertex_theta",
                "RecoKminus_atVertex_phi",

                "Angle_JpsiPhi"


                ]:
            branchList.push_back(branchName)
        df2.Snapshot("events", self.outname, branchList)



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
