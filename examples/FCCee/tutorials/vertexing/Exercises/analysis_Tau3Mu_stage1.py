import ROOT

analysesList = ['myAnalysis']


#Mandatory: List of processes
processList = {
    'p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2MuMuMu':{},#Run the full statistics in one output file named <outputDir>/xxx.root
    'p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2PiPiPinu':{}
    }

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local running directory
outputDir    = "Tau3Mu"

#Optional test file
testFile= "/eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_noBES_ee_Ztautau_ecm91_EvtGen_TauMinus2PiPiPinu/events_179808277.root"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df

            # Use the "AllMuons" collection, which contains also non-isolated muons (in contrast to the "Muons" collection)
            #    Actually, "Muon" or ("AllMuon") just contain pointers (indices) to the RecoParticle collections,
            #    hence one needs to first retrieve the RecoParticles corresponding to these muons.
            #    ( for more detail about the collections, see https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/basics  )
            .Alias("Muon0", "AllMuon#0.index")
            .Define("muons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
            .Define("n_muons",  "ReconstructedParticle::get_n( muons ) ")

            # -----------------------------------------
            # Add fake muons from pi -> mu

            # This selects the charged hadrons :
            .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
            .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
            .Define("ChargedHadrons", "ReconstructedParticle2MC::selRP_ChargedHadrons( MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
            # Only the ones with  p > 2 GeV could be selected as muons :
            .Define("ChargedHadrons_pgt2",  "ReconstructedParticle::sel_p(2.) ( ChargedHadrons )")
            # Build fake muons based on a flat fake rate (random selection) :
            .Define("fakeMuons_5em2", "myAnalysis::selRP_Fakes( 5e-2, 0.106)(ChargedHadrons_pgt2)" )

            # Now we marge the collection of fake muons with the genuine muons :
            .Define("muons_with_fakes",  "ReconstructedParticle::merge( muons, fakeMuons_5em2 )")
            # and we use this collection later on, instead of "muons" :
            .Alias("theMuons", "muons_with_fakes")
            .Define("n_muons_withFakes",  "ReconstructedParticle::get_n( theMuons )")

            # -----------------------------------------


            # Build triplets of muons.
            # We are interested in tau- -> mu- mu- mu+ (the MC files produced for this tutorial
            # only forced the decay of the tau- , not the tau+ ).
            # Hence we look for triples of total charge = -1 :
            .Define("triplets_m",  "myAnalysis::build_triplets( theMuons, -1. )")   # returns a vector of triplets, i.e. of vectors of 3 RecoParticles
            .Define("n_triplets_m",  "return triplets_m.size() ; " )

             # ----------------------------------------------------
             # Simple: consider only the 1st triplet :

             #  .Define("the_muons_candidate_0",  "return triplets_m[0] ; ")  # the_muons_candidates = a vector of 3 RecoParticles

             # get the corresponding tracks:
             #   .Define("the_muontracks_candidate_0",  "ReconstructedParticle2Track::getRP2TRK( the_muons_candidate_0, EFlowTrack_1)")
             # and fit them to a common vertex :
             #   .Define("TauVertexObject_candidate_0",   "VertexFitterSimple::VertexFitter_Tk( 2, the_muontracks_candidate_0)" )
             # Now we can get the mass of this candidate, as before :
             #   .Define("TauMass_candidate_0",   "myAnalysis::tau3mu_vertex_mass( TauVertexObject_candidate_0 )" )


             # ----------------------------------------------------
             # Now consider all triplets :

              .Define("TauVertexObject_allCandidates",  "myAnalysis::build_AllTauVertexObject( triplets_m , EFlowTrack_1 ) ")
              .Define("TauMass_allCandidates",   "myAnalysis::build_AllTauMasses( TauVertexObject_allCandidates )" )


             # Total visible energy in the event :
             .Define("RecoPartEnergies",  "ReconstructedParticle::get_e( ReconstructedParticles )")
             .Define("visible_energy",  "Sum( RecoPartEnergies )")

        )
        return df2


    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
		"n_muons",
		"n_triplets_m",
		#"TauMass_candidate_0",
		"TauMass_allCandidates",
		"visible_energy"

        ]
        return branchList
