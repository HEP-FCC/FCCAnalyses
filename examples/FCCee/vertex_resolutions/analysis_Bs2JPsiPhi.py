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

#
#	This is used to process a file in which the Bs and the Bsbar are forced
#	to decay into Jpsi ( -> mu mu) + Phi ( -> K K )
#	We reconstruct the secondary vertex from the 2 muon and 2 kaon tracks.
#       The example also shows how to retrieve the MC and reco'ed Bs legs,
#       as well as the MC Bs, JP]psi and Phis, with their kinematics.
#
#	Example file : /eos/fcc/users/e/eperez/vertexing/Bs2JpsiPhi_evtgen.root
# 	Note: these events were generated at (0,0,0), i.e.no smearing of the
#	primary vertex.
#

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

               # number of tracks in the event
               .Define("ntracks","getTK_n(EFlowTrack_1)")

               # Retrieve the decay vertex of all MC particles
               #.Define("MC_DecayVertices",  "MCParticle::get_endPoint( Particle, Particle1)" )


               # MC indices of the decay Bs (PDG = 531) -> mu+ (PDG = -13) mu- (PDG = 13) K+ (PDG = 321) K- (PDG = -321)
               # Retrieves a vector of int's which correspond to indices in the Particle block
               # vector[0] = the mother, and then the daughters in the order specified, i.e. here
               #       [1] = the mu+, [2] = the mu-, [3] = the K+, [4] = the K-
               # The first boolean below: when set to true, the dsughters specified in the list are looked
               # for among the final, stable particles that come out from the mother, i.e. the decay tree is
	       # explored recursively if needed.
               # The second boolean: when set to true, the charge conjugate decays are included too.
               # If the event contains more than one such decays,only the first one is kept.
	       # get_indices_ExclusiveDecay looks for an exclusive decay: if a mother is found, that decays 
               # into the particles specified in the list plus other particle(s), this decay is not selected.
               .Define("Bs2MuMuKK_indices",  "MCParticle::get_indices_ExclusiveDecay( 531, {-13,13,321,-321}, true, true) ( Particle, Particle1)" )

                # the MC Bs : the Bs is the first particle in the Bs2MuMuKK_indices vector
               .Define("Bs",  "selMC_leg(0) ( Bs2MuMuKK_indices, Particle )")

                # and the MC legs of the Bs : the mu+ is the second particle in the vector, etc.
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

	       # Kinematics of the mother Bs (MC)
               .Define("Bs_theta",   "MCParticle::get_theta( Bs )")
               .Define("Bs_phi",   "MCParticle::get_phi( Bs )")
               .Define("Bs_e",   "MCParticle::get_e( Bs )")

               
               # Decay vertex of the Bs (MC)
               # Careful with getMC_decayVertex: if Bs -> Bsbar, this returns the prod vertex of the Bsbar !
               #.Define("BsDecayVertex",   "getMC_decayVertex(531, false)( Particle, Particle1)")
               # Hence, use instead a custom method in Bs2JPsiPhi :
               .Define("BsMCDecayVertex",   "BsMCDecayVertex( Bs2MuMuKK_indices, Particle )")

               # Returns the RecoParticles associated with the four  Bs decay products.
               # The size of this collection is always 4 provided that Bs2MuMuKK_indices is not empty,
               # possibly including "dummy" particles in case one of the legs did not make a RecoParticle.
               # This is done on purpose, in order to maintain the mapping with the indices - i.e. the 1st particle in 
               # the list BsRecoParticles is the mu+, then the mu-, etc.
               # (selRP_matched_to_list ignores the unstable MC particles that are in the input list of indices
 	       # hence the mother particle, which is the [0] element of the Bs2MuMuKK_indices vector).
               .Define("BsRecoParticles",  "selRP_matched_to_list( Bs2MuMuKK_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")

               # the corresponding tracks - here, dummy particles, if any, are removed, i.e. one may have < 4 tracks,
               # e.g. if one muon or kaon was emitted outside of the acceptance
               .Define("BsTracks",   "getRP2TRK( BsRecoParticles, EFlowTrack_1)" )

               # number of tracks in this BsTracks collection ( = the #tracks used to reconstruct the Bs vertex)
               .Define("n_BsTracks", "getTK_n( BsTracks )")

               # Now we reconstruct the Bs decay vertex using the reco'ed tracks.
               # First the full object, of type Vertexing::FCCAnalysesVertex
               .Define("BsVertexObject",   "Vertexing::VertexFitter_Tk( 2, BsTracks)" )
               # from which we extract the edm4hep::VertexData object, which contains the vertex positiob in mm
               .Define("BsVertex",  "Vertexing::get_VertexData( BsVertexObject )")


	       # We may want to look at the reco'ed Bs legs: in the BsRecoParticles vector, 
               # the first particle (vector[0]) is the mu+, etc :
               .Define("RecoMuplus",   "selRP_leg(0)( BsRecoParticles )")
               .Define("RecoMuminus",  "selRP_leg(1)( BsRecoParticles )")
               .Define("RecoKplus",    "selRP_leg(2)( BsRecoParticles )")
               .Define("RecoKminus",   "selRP_leg(3)( BsRecoParticles )")
               # and their kinematics :
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

	       # Looks at the angular separation (3D angles) between the Bs daughters: among
               # all the pairs of particles in BsRecoParticles, retrieve the minimal angular distance,
               # the maximal distance, and the average distance
               .Define("deltaAlpha_max","angular_separation(0)( BsRecoParticles )")
               .Define("deltaAlpha_min","angular_separation(1)( BsRecoParticles )")
               .Define("deltaAlpha_ave","angular_separation(2)( BsRecoParticles )")

	       # To look at the angular separation between the MC Jpsi and the Phi :

	       # First retrieve the indices of the JPsi and the phi :
               # MC indices of the decay Bs (PDG = 531)  -> JPsi (PDG = 443) Phi (PDG = 333)
               # Retrieves a vector of int's which correspond to indices in the Particle block
               # vector[0] = the mother, and then the daughters in the order specified, i.e. here
               #       [1] = the Jpsi, [2] = the phi
               # The first boolean below (here set to false) means that we look for a JPsi and a Phi
               # among the direct daughters of the mother, i.e. the decay tree is not explored down
               # to the final, stable particles.
               # The second boolean (true) means that the charge conjugate decay isincluded too.
               # If the event contains more than one such decays,only the first one is kept.
               # get_indices_ExclusiveDecay looks for an exclusive decay: if a mother is found, that decays 
               # into the particles specified in the list plus other particle(s), this decay is not selected.
               .Define("Bs2JPsiPhi_indices",   "MCParticle::get_indices_ExclusiveDecay( 531, {443,333}, false, true) ( Particle, Particle1)" )

               # This extracts the MC Jpsi. In list of indices determined above, Bs2JPsiPhi_indices,
               # 1 is the position of the Jpsi in the Bs2JPsiPhi_indices vector.
               .Define("JPsi",   "selMC_leg( 1) ( Bs2JPsiPhi_indices , Particle )")
               # Idem: extract the MC Phi. 2 is the position of the Phi in the Bs2JPsiPhi_indices vector.
               .Define("Phi",   "selMC_leg( 2) ( Bs2JPsiPhi_indices , Particle )")

               # From these two MC particles, determine their angular separation
               .Define("Angle_JpsiPhi",  "MCParticle::AngleBetweenTwoMCParticles( JPsi, Phi)" )



               # the reco'ed legs, with the momenta at the Bs decay vertex - instead of at their
	       # point of dca
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

               # not so useful here, but for completeness : Bs to JPsi decay ?
               # Returns booleans. e.g. the first one means that the event contains a Bs that decayed to a JPsi (443) + X, 
               # not counting the cases where Bs -> Bsbar -> JPsi + X
               .Define("Bsdecay",  "MCParticle::get_decay(531, 443, false)(Particle, Particle1)")
               .Define("Bsbardecay",  "MCParticle::get_decay(-531, 443, false)(Particle, Particle1)")


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

                # MC Bs decay vertex :
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
