#Optional test file
testFile=" /eos/experiment/fcc/ee/examples/lowerTriangle/p8_ecm91GeV_Zbb_EvtGen_Bs2JpsiPhi_IDEAtrkCov.root"

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

               # MC indices of the decay Bs (PDG = 531) -> mu+ (PDG = -13) mu- (PDG = 13) K+ (PDG = 321) K- (PDG = -321)
               # Retrieves a vector of int's which correspond to indices in the Particle block
               # vector[0] = the mother, and then the daughters in the order specified, i.e. here
               #       [1] = the mu+, [2] = the mu-, [3] = the K+, [4] = the K-
               # Boolean arguments :
               #	1st: stableDaughters. when set to true, the dsughters specified in the list are looked
               #             for among the final, stable particles that come out from the mother, i.e. the decay tree is
               #             explored recursively if needed.
               #        2nd: chargeConjugateMother
               #        3rd: chargeConjugateDaughters
               #        4th: inclusiveDecay: when set to false, if a mother is found, that decays
               #             into the particles specified in the list plus other particle(s), this decay is not selected.
               # If the event contains more than one such decays,only the first one is kept.
               .Define("Bs2MuMuKK_indices",  "MCParticle::get_indices( 531, {-13,13,321,-321}, true, true, true, false) ( Particle, Particle1)" )

               # select events for which the requested decay chain has been found:
               .Filter("Bs2MuMuKK_indices.size() > 0")

               # the mu+ (MCParticle) that comes from the Bs decay :
               .Define("MC_Muplus",  "return Particle.at(  Bs2MuMuKK_indices[1] ) ;")
               # Decay vertex (an edm4hep::Vector3d) of the Bs (MC) = production vertex of the muplus :
               .Define("BsMCDecayVertex",   " return  MC_Muplus.vertex ; ")

               # Returns the RecoParticles associated with the four  Bs decay products.
               # The size of this collection is always 4 provided that Bs2MuMuKK_indices is not empty,
               # possibly including "dummy" particles in case one of the legs did not make a RecoParticle
               # (e.g. because it is outsice the tracker acceptance).
               # This is done on purpose, in order to maintain the mapping with the indices - i.e. the 1st particle in
               # the list BsRecoParticles is the mu+, then the mu-, etc.
               # (selRP_matched_to_list ignores the unstable MC particles that are in the input list of indices
 	       # hence the mother particle, which is the [0] element of the Bs2MuMuKK_indices vector).
               #
               # The matching between RecoParticles and MCParticles requires 4 collections. For more
               # detail, see https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/basics
               .Define("BsRecoParticles",  "ReconstructedParticle2MC::selRP_matched_to_list( Bs2MuMuKK_indices, MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")

               # the corresponding tracks - here, dummy particles, if any, are removed, i.e. one may have < 4 tracks,
               # e.g. if one muon or kaon was emitted outside of the acceptance
               .Define("BsTracks",   "ReconstructedParticle2Track::getRP2TRK( BsRecoParticles, EFlowTrack_1)" )

               # number of tracks in this BsTracks collection ( = the #tracks used to reconstruct the Bs vertex)
               .Define("n_BsTracks", "ReconstructedParticle2Track::getTK_n( BsTracks )")

               # Fit the tracks to a common vertex. That would be a secondary vertex, hence we put
               # a "2" as the first argument of VertexFitter_Tk :
               # 	First the full object, of type Vertexing::FCCAnalysesVertex
               .Define("BsVertexObject",   "VertexFitterSimple::VertexFitter_Tk( 2, BsTracks)" )
               # 	from which we extract the edm4hep::VertexData object, which contains the vertex positiob in mm
               .Define("BsVertex",  "VertexingUtils::get_VertexData( BsVertexObject )")

        )
        return df2


    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
        "MC_Muplus",
        "n_BsTracks",
        "BsMCDecayVertex",
        "BsVertex",
        ]
        return branchList
