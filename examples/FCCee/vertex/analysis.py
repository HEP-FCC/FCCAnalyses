import sys
import ROOT

print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)


#
# Example file :
#    /eos/experiment/fcc/ee/examples/lowerTriangle/p8_ecm91GeV_Zuds_IDEAtrkCov.root
#    ( these events were generated at (0,0,0) i.e. no vertex smearing
#
# Example file from spring2021, with vertex smearing :
#    /eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zuds_ecm91/events_125841058.root


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
        df2 = (self.df.Range(0,1000)
        #df2 = (self.df

               # MC event primary vertex
               .Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(21)( Particle )" )

               # number of tracks
               .Define("ntracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")


               # Select primary tracks based on the matching to MC
		  # This can be used  to select primary tracks when the
		  # gen-level primary vertex  is not  (0,0,0)
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               # the recoParticles corresponding  to the tracks that are primaries, according to MC-matching :
               .Define("MC_PrimaryTracks_RP",  "VertexingUtils::SelPrimaryTracks(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle, MC_PrimaryVertex)" )
               # and the corresponding tracks :
               .Define("MC_PrimaryTracks",  "ReconstructedParticle2Track::getRP2TRK( MC_PrimaryTracks_RP, EFlowTrack_1)" )

               .Define("nPrimaryTracks", "ReconstructedParticle::get_n(MC_PrimaryTracks_RP)")

               # Reconstruct the vertex from these primary tracks :
               .Define("VertexObject_primaryTracks",  "VertexFitterSimple::VertexFitter ( 1, MC_PrimaryTracks_RP, EFlowTrack_1) ")
               .Define("Vertex_primaryTracks",   "VertexingUtils::get_VertexData( VertexObject_primaryTracks )")   # primary vertex, in mm

               # Idem, but adding the beam-spot constraint to the vertex fitter
                  # At the Z peak, the beam-spot size is ( 4.5 mum, 20 nm, 0.3 mm)
		  # The beam-spot dimensions are passed in mum :
               .Define("VertexObject_primaryTracks_BSC",  "VertexFitterSimple::VertexFitter ( 1, MC_PrimaryTracks_RP, EFlowTrack_1, true, 4.5, 20e-3, 300) ")
               .Define("Vertex_primaryTracks_BSC",   "VertexingUtils::get_VertexData( VertexObject_primaryTracks_BSC )")   # primary vertex, in mm


               #Run the Acts AMVF vertex finder
               #.Define("VertexObject_actsFinder","VertexFinderActs::VertexFinderAMVF( EFlowTrack_1)")
               #.Define("Vertex_actsFinder",   "VertexingUtils::get_VertexData( VertexObject_actsFinder )")   # primary vertex, in mm
               #.Define("nPrimaryTracks_actsFinder", "VertexingUtils::get_VertexNtrk(VertexObject_actsFinder)")

               #Run the Acts full Billoir vertex fitter
               #.Define("VertexObject_primaryTracks_actsFitter","VertexFitterActs::VertexFitterFullBilloir(PrimaryTracks, EFlowTrack_1)")
               #.Define("Vertex_primaryTracks_actsFitter", "VertexingUtils::get_VertexData( VertexObject_primaryTracks_actsFitter )")   # primary vertex, in mm


               # --- now, determime the primary (and secondary) tracks without using the MC-matching:

               # First, reconstruct a vertex from all tracks
               #.Define("VertexObject_allTracks",  "VertexFitterSimple::VertexFitter_Tk ( 1, EFlowTrack_1, true, 4.5, 20e-3, 300)")
               # Select the tracks that are reconstructed  as primaries
               .Define("RecoedPrimaryTracks",  "VertexFitterSimple::get_PrimaryTracks( EFlowTrack_1, true, 4.5, 20e-3, 300, 0., 0., 0.)")

               .Define("n_RecoedPrimaryTracks",  "ReconstructedParticle2Track::getTK_n( RecoedPrimaryTracks )")
               # the final primary vertex :
               .Define("FinalVertexObject",   "VertexFitterSimple::VertexFitter_Tk ( 1, RecoedPrimaryTracks, true, 4.5, 20e-3, 300) ")
               .Define("FinalVertex",   "VertexingUtils::get_VertexData( FinalVertexObject )")

               # the secondary tracks
               .Define("SecondaryTracks",   "VertexFitterSimple::get_NonPrimaryTracks( EFlowTrack_1,  RecoedPrimaryTracks )")
               .Define("n_SecondaryTracks",  "ReconstructedParticle2Track::getTK_n( SecondaryTracks )" )

               # which of the tracks are primary according to the reco algprithm
               .Define("IsPrimary_based_on_reco",  "VertexFitterSimple::IsPrimary_forTracks( EFlowTrack_1,  RecoedPrimaryTracks )")
               # which of the tracks are primary according to the MC-matching
               .Define("IsPrimary_based_on_MC",  "VertexFitterSimple::IsPrimary_forTracks( EFlowTrack_1,  MC_PrimaryTracks )")





        )


        # select branches for output file
        branchList = ROOT.vector('string')()
        for branchName in [
                "MC_PrimaryVertex",
                "ntracks",
                "nPrimaryTracks",
		# primary vertex, seeded by the tracks that are MC-matched to MC-primaries
                "Vertex_primaryTracks",
                "Vertex_primaryTracks_BSC",
                "IsPrimary_based_on_MC",

                #"nPrimaryTracks_actsFinder",
		#
                # commented out temporarily, very slow !?
                #
                #"Vertex_actsFinder",     # on Zuds: both track selections lead to very similar results for the vertex
                #"Vertex_primaryTracks_actsFitter",     # on Zuds: both track selections lead to very similar results for the vertex

		#  primary vertex and primary tracks w/o any MC-matching :
		"IsPrimary_based_on_reco",
		"FinalVertex",

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
