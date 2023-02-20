analysesList = ['myAnalysis']

#Mandatory: List of processes
processList = {
    'p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2MuMuMu':{},#Run the full statistics in one output file named <outputDir>/xxx.root
    'p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2PiPiPinu':{}
    #'p8_ee_WW_ecm240':{'fraction':0.5, 'chunks':2}, #Run 50% of the statistics in two files named <outputDir>/p8_ee_WW_ecm240/chunk<N>.root
    #'p8_ee_ZH_ecm240':{'fraction':0.2, 'output':'p8_ee_ZH_ecm240_out'} #Run 20% of the statistics in one file named <outputDir>/p8_ee_ZH_ecm240_out.root (example on how to change the output name)
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"


#Optional test file
testFile= "/eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2MuMuMu/events_189205650.root"


#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df

               .Alias("Particle1", "Particle#1.index")
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

               # MC indices of the decay Tau- (PDG = 15) -> mu+ (PDG = -13) mu- (PDG = 13) mu- (PDG = 13)
               # Retrieves a vector of int's which correspond to indices in the Particle block
               # vector[0] = the mother, and then the daughters in the order specified, i.e. here
               #       [1] = the mu+, [2] = the mu-, [3] = the other mu-
               # Boolean arguments :
               #	1st: stableDaughters. when set to true, the dsughters specified in the list are looked
               #             for among the final, stable particles that come out from the mother, i.e. the decay tree is
               #             explored recursively if needed.
               #        2nd: chargeConjugateMother
               #        3rd: chargeConjugateDaughters
               #        4th: inclusiveDecay: when set to false, if a mother is found, that decays
               #             into the particles specified in the list plus other particle(s), this decay is not selected.
               # If the event contains more than one such decays,only the first one is kept.
               .Define("indices",  "MCParticle::get_indices( 15, {-13,13,13}, true, true, true, false) ( Particle, Particle1)" )

               # select events for which the requested decay chain has been found:
               .Filter("indices.size() > 0")


               # the mu+ (MCParticle) that comes from the tau decay :
               .Define("MC_Muplus",  "return Particle.at(  indices[1] ) ;")
               # Decay vertex (an edm4hep::Vector3d) of the Tau (MC) = production vertex of the muplus :
               .Define("TauMCDecayVertex",   " return  MC_Muplus.vertex ; ")

               # Returns the RecoParticles associated with the four  Tau  decay products.
               # The size of this collection is always 4 provided that indices is not empty,
               # possibly including "dummy" particles in case one of the legs did not make a RecoParticle
               # (e.g. because it is outsice the tracker acceptance).
               # This is done on purpose, in order to maintain the mapping with the indices - i.e. the 1st particle in
               # the list TauRecoParticles is the mu+, then the mu-, etc.
               # (selRP_matched_to_list ignores the unstable MC particles that are in the input list of indices
 	       # hence the mother particle, which is the [0] element of the indices vector).
               #
               # The matching between RecoParticles and MCParticles requires 4 collections. For more
               # detail, see https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/basics
               .Define("TauRecoParticles",  "ReconstructedParticle2MC::selRP_matched_to_list( indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")

               # the corresponding tracks - here, dummy particles, if any, are removed, i.e. one may have < 4 tracks,
               # e.g. if one muon or kaon was emitted outside of the acceptance
               .Define("TauTracks",   "ReconstructedParticle2Track::getRP2TRK( TauRecoParticles, EFlowTrack_1)" )

               # number of tracks in this Tracks collection ( = the #tracks used to reconstruct the Tau vertex)
               .Define("n_TauTracks", "ReconstructedParticle2Track::getTK_n( TauTracks )")

               # Fit the tracks to a common vertex. That would be a secondary vertex, hence we put
               # a "2" as the first argument of VertexFitter_Tk :
               #              First the full object, of type Vertexing::FCCAnalysesVertex
               .Define("TauVertexObject",   "VertexFitterSimple::VertexFitter_Tk( 2, TauTracks)" )
               #              from which we extract the edm4hep::VertexData object, which contains the vertex positiob in mm
               .Define("TauVertex",  "VertexingUtils::get_VertexData( TauVertexObject )")

               # The reco'ed tau mass - from the post-VertxFit momenta, at the tau decay vertex :
               .Define("TauMass",   "myAnalysis::tau3mu_vertex_mass( TauVertexObject ) ")

               # The "raw" mass - using the track  momenta at their dca :
               .Define("RawMass",  "myAnalysis::tau3mu_raw_mass( TauRecoParticles ) ")


               # test MC kinem:
	       # note : for 95% of the events, the three muons have | cos theta | < 0.98
               #        but demanding in addition that they all have E or p > 2 GeV,
               #        the efficiency falls down to 75%
               #.Define("MC_Muminus1",  "return Particle.at(  indices[2] ) ;")
               #.Define("MC_Muminus2",  "return Particle.at(  indices[3] ) ;")
#
#               .Define("MC_Muplus_p", "myAnalysis::get_p( MC_Muplus )")
#               .Define("MC_Muplus_e", "myAnalysis::get_e( MC_Muplus )")
#               .Define("MC_Muplus_theta",  "myAnalysis::get_theta( MC_Muplus ) ")
#
#               .Define("MC_Muminus1_p", "myAnalysis::get_p( MC_Muminus1 )")
#               .Define("MC_Muminus1_e", "myAnalysis::get_e( MC_Muminus1 )")
#               .Define("MC_Muminus1_theta",  "myAnalysis::get_theta( MC_Muminus1 ) ")
#
#               .Define("MC_Muminus2_p", "myAnalysis::get_p( MC_Muminus2 )")
#               .Define("MC_Muminus2_e", "myAnalysis::get_e( MC_Muminus2 )")
#               .Define("MC_Muminus2_theta",  "myAnalysis::get_theta( MC_Muminus2 ) ")





        )
        return df2


    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
		"MC_Muplus",
                "n_TauTracks",
                "TauMCDecayVertex",
                "TauVertex",
                "TauMass",
		"RawMass",

		#"MC_Muplus_p", "MC_Muplus_e", "MC_Muplus_theta",
		#"MC_Muminus1_p", "MC_Muminus1_e", "MC_Muminus1_theta",
		#"MC_Muminus2_p", "MC_Muminus2_e", "MC_Muminus2_theta",
        ]
        return branchList
