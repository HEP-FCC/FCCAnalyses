testFile="/eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zuds_ecm91/events_125841058.root"
#testFile="/eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zbb_ecm91/events_092272862.root"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df

               # MC event primary vertex
               .Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(21)( Particle )" )

               # number of tracks
               .Define("ntracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")

               # Fit all tracks of the events to a common vertex  - here using a beam-spot constraint:

               # VertexObject_allTracks is an object of type VertexingUtils::FCCAnalysesVertex
               # It contains in particular :
               #  - an edm4hep::VertexData :
               # 	std::int32_t primary{}; ///< boolean flag, if vertex is the primary vertex of the event
               # 	float chi2{}; ///< chi-squared of the vertex fit
               # 	::edm4hep::Vector3f position{}; ///< [mm] position of the vertex.
               # 	std::array<float, 6> covMatrix{}; ///< covariance matrix of the position (stored as lower triangle matrix, i.e. cov(xx),cov(y,x),cov(z,x),cov(y,y),... )
               # - ROOT::VecOps::RVec<float> reco_chi2 : the contribution to the chi2 of all tracks used in the fit
               # - ROOT::VecOps::RVec< TVector3 >  updated_track_momentum_at_vertex : the post-fit (px, py, pz ) of the tracks, at the vertex (and not at their d.c.a.)
               .Define("VertexObject_allTracks",  "VertexFitterSimple::VertexFitter_Tk ( 1, EFlowTrack_1, true, 4.5, 20e-3, 300)")

               # EFlowTrack_1 is the collection of all tracks (the fitting method can of course be applied to a subset of tracks (see later)).
               # "true" means that a beam-spot constraint is applied. Default is no BSC. Following args are the BS size and position, in mum :
               #                                   bool BeamSpotConstraint = false,
               #                                   double sigmax=0., double sigmay=0., double sigmaz=0.,
               #                                   double bsc_x=0., double bsc_y=0., double bsc_z=0. )  ;

               # This returns the  edm4hep::VertexData :
               .Define("Vertex_allTracks",  "VertexingUtils::get_VertexData( VertexObject_allTracks )")   # primary vertex, in mm

               # This is not a good estimate of the primary vertex: even in a Z -> uds event, there are displaced tracks (e.g. Ks, Lambdas), which would bias the fit.
               # Below, we determine the "primary tracks" using an iterative algorithm - cf LCFI+.
               .Define("RecoedPrimaryTracks",  "VertexFitterSimple::get_PrimaryTracks( EFlowTrack_1, true, 4.5, 20e-3, 300, 0., 0., 0.)")

               # Now we run again the vertex fit, but only on the primary tracks :
               .Define("PrimaryVertexObject",   "VertexFitterSimple::VertexFitter_Tk ( 1, RecoedPrimaryTracks, true, 4.5, 20e-3, 300) ")
               .Define("PrimaryVertex",   "VertexingUtils::get_VertexData( PrimaryVertexObject )")

               # It is often useful to retrieve the secondary (i.e. non-primary) tracks, for example to search for secondary vertices.
               # The method below simply "subtracts" the primary tracks from the full collection :
               .Define("SecondaryTracks",   "VertexFitterSimple::get_NonPrimaryTracks( EFlowTrack_1,  RecoedPrimaryTracks )")

               #Needed to display the vertex in the event display tutorial
               .Define("tracks", "EFlowTrack_1")
               .Define("PV_vec", "ROOT::VecOps::RVec<edm4hep::VertexData> v; v.push_back(Vertex_allTracks); return v;")
        )
        return df2


    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
        "MC_PrimaryVertex",
        "ntracks",
        "Vertex_allTracks",
        "PrimaryVertex",
        "tracks",
        "PV_vec"
        ]
        return branchList
