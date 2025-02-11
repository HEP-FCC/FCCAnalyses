'''
Analysis for FCC-hh VBF H->WW
author Elliot Lipeles (lipeles@sas.upenn.edu)
'''
from argparse import ArgumentParser
import vbf_hww.analysis_config as analysis_config

# Mandatory: Analysis class where the user defines the operations on the
# dataframe.
class Analysis():
    '''
    VBF Higgs analysis in H to WW to llvv.
    '''
    def __init__(self, cmdline_args):
        parser = ArgumentParser(
            description='Additional analysis arguments',
            usage='Provide additional arguments after analysis script path')
        # parser.add_argument('--bjet-pt', default='10.', type=float,
        #                     help='Minimal pT of the selected b-jets.')
        # Parse additional arguments not known to the FCCAnalyses parsers
        # All command line arguments know to fccanalysis are provided in the
        # `cmdline_arg` dictionary.
        self.ana_args, _ = parser.parse_known_args(cmdline_args['unknown'])

        self.process_list = analysis_config.process_list
        self.input_dir = analysis_config.input_dir
        self.output_dir = analysis_config.stage1_output
                
        # Optional: analysisName, default is ''
        self.analysis_name = 'FCC-hh VBF HWW analysis'

        # Optional: number of threads to run on, default is 'all available'
        # self.n_threads = 4

        # Optional: running on HTCondor, default is False
        self.run_batch = True
        
        # Optional: Use weighted events
        self.do_weighted = True 

        # Optional: read the input files with podio::DataSource 
        self.use_data_source = False # explicitly use old way in this version 

        # Optional: test file that is used if you run with the --test argument (fccanalysis run ./examples/FCChh/ggHH_bbyy/analysis_stage1.py --test)
        self.test_file = None


    # Mandatory: analyzers function to define the analysis graph, please make
    # sure you return the dataframe, in this example it is dframe2
    def analyzers(self, dframe):
        '''
        Analysis graph.
        '''

        dframe2 = (
            dframe

            ########################################### DEFINITION OF VARIABLES ########################################### 

            # generator event weight
            .Define("weight",  "EventHeader.weight")

            ########################################### Electrons ########################################### 
            .Define("hardMC",          "FCCAnalyses::MCParticle::sel_genStatus(22)(Particle)")
            .Define("n_hardMC",          "FCCAnalyses::MCParticle::get_n(hardMC)")

            .Define("genW",          "FCCAnalyses::MCParticle::sel_pdgID(24, true)(hardMC)")
            .Define("genWp",          "FCCAnalyses::MCParticle::sel_pdgID(24, false)(hardMC)")
            .Define("genWm",          "FCCAnalyses::MCParticle::sel_pdgID(-24, false)(hardMC)")
            .Define("n_genW",        "FCCAnalyses::MCParticle::get_n(genW)")
            .Define("n_genWp",        "FCCAnalyses::MCParticle::get_n(genWp)")
            .Define("n_genWm",        "FCCAnalyses::MCParticle::get_n(genWm)")
            .Define("genZ",          "FCCAnalyses::MCParticle::sel_pdgID(23, true)(hardMC)")
            .Define("n_genZ",        "FCCAnalyses::MCParticle::get_n(genZ)")
            .Define("genb",          "FCCAnalyses::MCParticle::sel_pdgID(5, true)(Particle)")
            .Define("n_genb",        "FCCAnalyses::MCParticle::get_n(genb)")
            .Define("genb_pt",        "FCCAnalyses::MCParticle::get_pt(genb)[0]")
            .Define("genb_eta",       "FCCAnalyses::MCParticle::get_eta(genb)[0]")
            

            .Define("electrons",  "FCCAnalyses::ReconstructedParticle::get(Electron_objIdx.index, ReconstructedParticles)")
            .Define("selpt_el",   "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(electrons)")
            .Define("sel_el_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_el)")
            .Define("sel_el",  "AnalysisFCChh::SortParticleCollection(sel_el_unsort)") #sort by pT

            .Define("n_el",  "FCCAnalyses::ReconstructedParticle::get_n(sel_el)") 
            .Define("el1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_el)[0]")
            .Define("el1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_el)[0]")
            .Define("el1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_el)[0]")
            .Define("el1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_el)[0]")
            .Define("el2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_el)[1]")
            .Define("el2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_el)[1]")
            .Define("el2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_el)[1]")
            .Define("el2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_el)[1]")

            .Define("muons",  "FCCAnalyses::ReconstructedParticle::get(Muon_objIdx.index, ReconstructedParticles)")
            .Define("selpt_mu",   "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(muons)")
            .Define("sel_mu_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_mu)")
            .Define("sel_mu",  "AnalysisFCChh::SortParticleCollection(sel_mu_unsort)") #sort by pT

            .Define("n_mu",  "FCCAnalyses::ReconstructedParticle::get_n(sel_mu)") 
            .Define("mu1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_mu)[0]")
            .Define("mu1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_mu)[0]")
            .Define("mu1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_mu)[0]")
            .Define("mu1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_mu)[0]")
            .Define("mu2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_mu)[1]")
            .Define("mu2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_mu)[1]")
            .Define("mu2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_mu)[1]")
            .Define("mu2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_mu)[1]")

            # # H(yy) if it exists, if there are no 2 selected photons, doesnt get filled 
            #.Define("el_pairs_unmerged", "AnalysisFCChh::getPairs(sel_el)") # retrieves the leading pT pair of all possible 
            #.Define("el_pairs", "AnalysisFCChh::merge_pairs(el_pairs_unmerged)") # merge pair into one object to access inv masses etc
            #.Define("m_ee", "FCCAnalyses::ReconstructedParticle::get_mass(el_pairs)")
            
            #.Define("mu_pairs_unmerged", "AnalysisFCChh::getPairs(sel_mu)") # retrieves the leading pT pair of all possible 
            #.Define("mu_pairs", "AnalysisFCChh::merge_pairs(mu_pairs_unmerged)") # merge pair into one object to access inv masses etc
            #.Define("m_mm", "FCCAnalyses::ReconstructedParticle::get_mass(mu_pairs)")

            .Define("em_pairs_unmerged", "AnalysisFCChh::getDFOSPairs(sel_el,sel_mu)")
            .Define("em_pairs", "AnalysisFCChh::merge_pairs(em_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_em", "FCCAnalyses::ReconstructedParticle::get_mass(em_pairs)")

            #EVENTWIDE VARIABLES: Access quantities that exist only once per event, such as the missing transverse energy
            .Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)") #absolute value of MET
            .Define("MET_x", "FCCAnalyses::ReconstructedParticle::get_px(MissingET)") #x-component of MET
            .Define("MET_y", "FCCAnalyses::ReconstructedParticle::get_py(MissingET)") #y-component of MET
            .Define("MET_phi", "FCCAnalyses::ReconstructedParticle::get_phi(MissingET)") #angle of MET

            # ########################################### JETS ########################################### 

            .Define("selected_jets", "ReconstructedParticle::sel_pt(30.)(Jet)") #select only jets with a pT > 30 GeV
            .Define("sel_jets", "AnalysisFCChh::SortParticleCollection(selected_jets)") #sort by pT
            .Define("n_jets",   "FCCAnalyses::ReconstructedParticle::get_n(sel_jets)")
            .Define("j1_pt",    "FCCAnalyses::ReconstructedParticle::get_pt(sel_jets)[0]")
            .Define("j1_eta",   "FCCAnalyses::ReconstructedParticle::get_eta(sel_jets)[0]")
            .Define("j1_phi",   "FCCAnalyses::ReconstructedParticle::get_phi(sel_jets)[0]")
            .Define("j2_pt",    "FCCAnalyses::ReconstructedParticle::get_pt(sel_jets)[1]")
            .Define("j2_eta",   "FCCAnalyses::ReconstructedParticle::get_eta(sel_jets)[1]")
            .Define("j2_phi",   "FCCAnalyses::ReconstructedParticle::get_phi(sel_jets)[1]")
            
            .Define("centraljets", "FCCAnalyses::ReconstructedParticle::sel_eta(2.5)(selected_jets)")
            .Define("n_centraljets",   "FCCAnalyses::ReconstructedParticle::get_n(centraljets)")

           #.Define("trackstates", "ReconstructedParticle2Track::getRP2TRK(ReconstructedParticles,EFlowTrack)") 
           # .Define("centraltrks", "FCCAnalyses::ReconstructedParticle::sel_eta(2.5)(selected_trks)")
           # .Define("n_centraltrks", "FCCAnalyses::ReconstructedParticle::get_n(centraltrks)")
           .Define("n_RecoTracks","AnalysisFCChh::get_ntrk(EFlowTrack)")
            

            .Define("jj_pairs_unmerged", "AnalysisFCChh::getPairs(sel_jets)") # retrieves the leading pT pair of all possible 
            .Define("jj_pairs", "AnalysisFCChh::merge_pairs(jj_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_jj", "FCCAnalyses::ReconstructedParticle::get_mass(jj_pairs)")
            .Define("pt_jj", "FCCAnalyses::ReconstructedParticle::get_pt(jj_pairs)")

            # HWW identification
            .Define("dphi_em", 'AnalysisFCChh::get_angularDist_pair(em_pairs_unmerged,"dPhiAbs")')
            .Define("deta_em", 'AnalysisFCChh::get_angularDist_pair(em_pairs_unmerged,"dEta")')
            .Define("dphi_jj", 'AnalysisFCChh::get_angularDist_pair(jj_pairs_unmerged,"dPhiAbs")')
            .Define("deta_jj", 'AnalysisFCChh::get_angularDist_pair(jj_pairs_unmerged,"dEta")')
            .Define("dphi_emMET", 'AnalysisFCChh::get_angularDist_MET(em_pairs,MissingET,"dPhiAbs")')
            .Define("lep_cent", "AnalysisFCChh::get_lepton_centrality(em_pairs_unmerged,jj_pairs_unmerged)")
            .Define("MT", "AnalysisFCChh::get_mT_hww(em_pairs,MissingET)")


            # b-tagged jets at medium working point
            .Define("b_tagged_jets_medium", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)") #bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            # select medium b-jets with pT > 30 GeV, |eta| < 4
            .Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(b_tagged_jets_medium)")
            .Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
            .Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)") #sort by pT
            .Define("n_bjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")
            
            .Define("b_tagged_jets_loose", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 0)") 
            .Define("selpt_bjets_loose", "FCCAnalyses::ReconstructedParticle::sel_pt(20.)(b_tagged_jets_loose)")
            .Define("sel_bjets_loose_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets_loose)")
            .Define("sel_bjets_loose", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)") #sort by pT
            .Define("n_bjets_loose", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets_loose)")
           


            # ########################################### APPLY PRE-SELECTION ########################################### 
            # # require at least electrons and two jets
            .Filter("n_hardMC>0")
            .Filter("((n_genWp>=1)&&(n_genWm>=1))||((n_genZ==1)&&(n_genW==0))")
            .Filter("n_el == 1")
            .Filter("n_mu == 1")
            .Filter("n_jets > 1")
            #.Filter("n_bjets==0") # just remove all bjets for now
        )
        return dframe2

    # Mandatory: output function, please make sure you return the branch list
    # as a python list
    def output(self):
        '''
        Output variables which will be saved to output root file.
        '''
        branch_list = [
            'weight',
            'n_el', 'el1_pt', 'el1_eta', 'el1_phi', 'el2_pt', 'el2_eta', 'el2_phi',
            'n_mu', 'mu1_pt', 'mu1_eta', 'mu1_phi', 'mu2_pt', 'mu2_eta', 'mu2_phi',
            'm_em', 'dphi_em',  'deta_em',  
            'MET', 'MET_x', 'MET_y', 'MET_phi',
            'n_jets', 'n_bjets', 'n_bjets_loose' , 'n_centraljets', 
            'n_RecoTracks',
            'j1_pt', 'j1_eta', 'j1_phi', 'j2_pt', 'j2_eta', 'j2_phi',
            'm_jj', 'dphi_jj',  'deta_jj',  'pt_jj',
            'MT', 'lep_cent', 'dphi_emMET',
            'n_genWp' , 'n_genWm' , 'n_genZ'   , 'n_genb'  , 'genb_pt', 'genb_eta'       
        ]
        return branch_list