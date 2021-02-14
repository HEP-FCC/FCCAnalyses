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
        #df2 = (self.df.Range(100000)
        df2 = (self.df

               .Alias("Particle1", "Particle#1.index")
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

               # MC event primary vertex
               .Define("MC_PrimaryVertex",  "MCParticle::get_EventPrimaryVertex(21)( Particle )" )

               # number of tracks
               .Define("ntracks","getTK_n(EFlowTrack_1)")


               # MC indices of the decay Bs -> Ds+ K-
               # In the file I process, only the Bs0 (not the Bsbar) has been forced to decay into Ds+ K-
               # Look for (Ds+ K-) in the list of unstable decays of a Bs - hence oscillations are
               # not accounted for. So there should be at most one such decay per event. In any case,
               # would there be > 1, the method gives the first one encountered.
               # Returns the indices of : mother Bs, Ds+, K-

               .Define("Bs2DsK_indices", "MCParticle::get_indices_ExclusiveDecay( 531, {431, -321}, false, false) ( Particle, Particle1)" )

               # MC indices of (this) Ds+ -> K+ K- Pi+
               # Do not want *any* Ds here, hence use custom code in Bs2DsK.cc
               # Returns the indices of:  mother Ds+, K+ K- Pi+
               .Define("Ds2KKPi_indices",  "getMC_indices_Ds2KKPi( Bs2DsK_indices, Particle, Particle1) ")

               # MC indices of Bs -> ( K+ K- Pi+ ) K-
               # Return the indices of:  mother Bs, ( K+ K- Pi+ ) K-
               .Define("Bs2KKPiK_indices",  "getMC_indices_Bs2KKPiK( Bs2DsK_indices,  Ds2KKPi_indices)" )

               # the MC Bs :
               .Define("Bs",  "selMC_leg(0) ( Bs2DsK_indices, Particle )")
               # the MC Ds :
               .Define("Ds",  "selMC_leg(1) ( Bs2DsK_indices, Particle )")
               # the MC bachelor K- from the Bs decay :
               .Define("BachelorK",  "selMC_leg(2) ( Bs2DsK_indices, Particle )")

	       # the angle between the MC Ds and the MC K
               .Define("Angle_DsK",  "MCParticle::AngleBetweenTwoMCParticles( Ds, BachelorK ) ")

               # The MC legs from the Ds decay
               .Define("Kplus",   "selMC_leg(1) ( Bs2KKPiK_indices, Particle )")
               .Define("Kminus",   "selMC_leg(2) ( Bs2KKPiK_indices, Particle )")
               .Define("Piplus",   "selMC_leg(3) ( Bs2KKPiK_indices, Particle )")

	       # their energies
               .Define("Kplus_E",  "MCParticle::get_e( Kplus )")
               .Define("Kminus_E",  "MCParticle::get_e( Kminus )")
	       .Define("Piplus_E",   "MCParticle::get_e( Piplus )")


               # the Ds kinematics 
               .Define("Ds_E",  "MCParticle::get_e( Ds )")
               .Define("Ds_pt", "MCParticle::get_pt( Ds ) ")
               .Define("Ds_theta", "MCParticle::get_theta( Ds )")
               .Define("Ds_phi", "MCParticle::get_phi( Ds )")

               # the bachelor K kinematics
               .Define("BachelorK_E",  "MCParticle::get_e( BachelorK )")
               .Define("BachelorK_theta",  "MCParticle::get_theta( BachelorK )")
               .Define("BachelorK_phi",  "MCParticle::get_phi( BachelorK )")

               # Decay vertex of the Ds
               # This takes the production vertex of the 1st non mother particle in Bs2KKPiK_indices, i.e.
               # of the K+ from the Ds, that's what we want. Need to change the name of this method, give it a more general name !
               .Define("DsMCDecayVertex",  "BsMCDecayVertex( Ds2KKPi_indices, Particle ) ")

               # Decay vertex of the Bs :
               # Use the BsMCDecayVertex coded for Bs2JPsiPhi: take the production vertex of the Ds. 
               .Define("BsMCDecayVertex",  "BsMCDecayVertex( Bs2DsK_indices, Particle ) ")


               # RecoParticles associated with the Ds decay
               # the size of this collection is always 3 provided that Ds2KKPi_indices is not empty.
               # In case one of the Ds legs did not make a RecoParticle, a "dummy" particle is inserted in the liat.
               # This is done on purpose, to maintain the mapping with the indices.
               .Define("DsRecoParticles",   " selRP_matched_to_list( Ds2KKPi_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")

               # the corresponding tracks - here, dummy particles, if any, are removed
               .Define("DsTracks",  "getRP2TRK( DsRecoParticles, EFlowTrack_1)" )

               # number of tracks used to reconstruct the Ds vertex
               .Define("n_DsTracks", "getTK_n( DsTracks )")

               # the RecoParticles associated with the K+, K- and Pi+ of teh Ds decay
               .Define("RecoKplus",  "selRP_leg(0)( DsRecoParticles )" )
               .Define("RecoKminus", "selRP_leg(1)( DsRecoParticles )" )
               .Define("RecoPiplus", "selRP_leg(2)( DsRecoParticles )" )

               # Reco'ed vertex of the Ds
               .Define("DsVertexObject",  "Vertexing::VertexFitter_Tk( 3, DsTracks)" )
               .Define("DsVertex",  "Vertexing::get_VertexData( DsVertexObject )")


	       # -------------------------------------------------------------------------------------------------------

               # ----------  Reconstruction of the Bs vertex 

               # the reco'ed legs of the Ds, with the momenta at the Ds decay vertex
               .Define("RecoKplus_atVertex",  "selRP_leg_atVertex(0)( DsRecoParticles, DsVertexObject, EFlowTrack_1)")
               .Define("RecoKminus_atVertex",  "selRP_leg_atVertex(1)( DsRecoParticles, DsVertexObject, EFlowTrack_1)")
               .Define("RecoPiplus_atVertex",  "selRP_leg_atVertex(2)( DsRecoParticles, DsVertexObject, EFlowTrack_1)")

               # the  RecoParticle associated with  the bachelor K
                .Define("BsRecoParticles", "selRP_matched_to_list( Bs2KKPiK_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
                .Define("RecoBachelorK",  "selRP_leg(3)( BsRecoParticles )")
               # and the corresponding track
                .Define("BachelorKTrack",  "getRP2TRK(  RecoBachelorK, EFlowTrack_1)" )

               # Reconstructed Ds
                .Define("RecoDs", " ReconstructedDs( RecoKplus, RecoKminus, RecoPiplus ) ")
                .Define("RecoDs_atVertex",  " ReconstructedDs( RecoKplus_atVertex, RecoKminus_atVertex, RecoPiplus_atVertex) ")

                .Define("RecoDs_pt",  "getRP_pt( RecoDs )")
                .Define("RecoDs_theta",  "getRP_theta( RecoDs ) ")
                .Define("RecoDs_phi",   "getRP_phi( RecoDs )")
                .Define("RecoDs_mass",  "getRP_mass( RecoDs )")

                .Define("RecoDs_atVertex_pt",  "getRP_pt( RecoDs_atVertex )")
                .Define("RecoDs_atVertex_theta",  "getRP_theta( RecoDs_atVertex )")
                .Define("RecoDs_atVertex_phi",   "getRP_phi( RecoDs_atVertex )")
                .Define("RecoDs_atVertex_mass",  "getRP_mass( RecoDs_atVertex )")

               # the list of tracks to reconstruct the Bs vertex
	       # here, a TrackState is built from the RecoDs_atVertex, but the elements of the covariance matrix are
               # set arbitrarily - use a relative uncertainty of 5% for the parameters.
               # See below for a better way to do it.
               .Define("BsTracks",  "tracks_for_fitting_the_Bs_vertex( RecoDs_atVertex, BachelorKTrack, Ds, DsMCDecayVertex )" )
               .Define("n_BsTracks", "getTK_n( BsTracks )")

               # Reco'ed Bs vertex
               .Define("BsVertexObject",  "Vertexing::VertexFitter_Tk( 2, BsTracks)" )
               .Define("BsVertex",  "Vertexing::get_VertexData( BsVertexObject )")


	       # Try to better account for the covariance matrix of the Ds pseudo-track
               .Define("ReconstructedDs_atVertex_TrackState", "ReconstructedDs_atVertex_TrackState( RecoDs_atVertex, Ds, DsMCDecayVertex )" )
               .Define("RecoDs_atVertex_TrackState_Cov",  "ReconstructedDs_atVertex_TrackState_withCovariance( DsTracks, ReconstructedDs_atVertex_TrackState, DsVertexObject) ")
               .Define("BsTracks_Cov",  "tracks_for_fitting_the_Bs_vertex( RecoDs_atVertex_TrackState_Cov, BachelorKTrack) ")
               .Define("BsVertexObject_Cov",  "Vertexing::VertexFitter_Tk( 2, BsTracks_Cov)" )
               # This is the final Bs vertex
               .Define("BsVertex_Cov",  "Vertexing::get_VertexData( BsVertexObject_Cov )")

               .Define("Kplus_phi",  "MCParticle::get_phi( Kplus )")
               .Define("RecoKplus_phi",  "getRP_phi( RecoKplus ) " )
               .Define("RecoKplus_atVertex_phi", "getRP_phi( RecoKplus_atVertex ) ")
               


        )


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                #"MC_PrimaryVertex",
                #"ntracks",
                "Bs",
                #"Ds",
                #"BachelorK",
                "Ds_E",
                "Ds_pt",
                "Ds_theta",
                "Ds_phi",
                "BachelorK_E",
                "BachelorK_theta",
	        "BachelorK_phi",
                #"Kplus",
                #"Kminus",
                #"Piplus",
                "DsMCDecayVertex",
                "BsMCDecayVertex",
                #"DsTracks",
                "n_DsTracks",
                #"RecoKplus",
                #"RecoKminus",
                #"RecoPiplus",
                "DsVertex",
                "RecoDs",
                #"RecoDs_atVertex",
                "RecoDs_pt",
                "RecoDs_theta",
                "RecoDs_phi",
                "RecoDs_mass",
                #"RecoDs_atVertex_pt",
                "RecoDs_atVertex_theta",
                "RecoDs_atVertex_phi",
                "RecoDs_atVertex_mass",
                #"RecoBachelorK",
                "BsVertex",
                "n_BsTracks",
                #"RecoDs_atVertex_TrackState_Cov"

                "BsVertex_Cov",
                "Kplus_phi",
                "RecoKplus_phi",
                "RecoKplus_atVertex_phi",
	        "Angle_DsK",
		"Kplus_E",
		"Kminus_E",
		"Piplus_E"
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
