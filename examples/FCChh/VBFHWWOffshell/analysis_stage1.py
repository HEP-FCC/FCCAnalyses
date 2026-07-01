'''
Off-shell Higgs @FCC-hh : VBF HWW analysis
'''
from argparse import ArgumentParser


# Mandatory: Analysis class where the user defines the operations on the
# dataframe.
class Analysis():
    '''
    H(mumu) analysis
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

        # Mandatory: List of processes to run over
        self.process_list = {
            # # Add your processes like this: 
            ## '<name of process>':{'fraction':<fraction of events to run over>, 'chunks':<number of chunks to split the output into>, 'output':<name of the output file> }, 
            # # - <name of process> needs to correspond either the name of the input .root file, or the name of a directory containing root files 
            # # If you want to process only part of the events, split the output into chunks or give a different name to the output use the optional arguments
            # # or leave blank to use defaults = run the full statistics in one output file named the same as the process:
            # #TESTING
            # 'mgp8_pp_vbf_ww_lvlv_5f_100TeV/events_113865885': {'chunks':1}, #signal
            # FULL
            'mgp8_pp_vbf_ww_lvlv_5f_100TeV':{'chunks':1},
            'mgp8_pp_vbf_h_jjlvlv_5f_100TeV':{'chunks':1},
            'mgp8_pp_vbf_ww_lvlv_SBI_offshell_5f_100TeV':{'chunks':1},
        }

        # Mandatory: Input directory where to find the samples, or a production tag when running over the centrally produced
        # samples (this points to the yaml files for getting sample statistics)
        self.input_dir = '/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v06/II/'

        # Optional: output directory, default is local running directory
        self.output_dir = '/eos/experiment/fcc/hh/analysis_ntuples/fcc_v06/II/Offshell_HWW_Analysis/'

        # Optional: analysisName, default is ''
        self.analysis_name = 'FCC-hh off-shell HWW analysis'

        # Optional: number of threads to run on, default is 'all available'
        self.n_threads = 4

        # Optional: running on HTCondor, default is False
        self.run_batch = False
        # self.run_batch = True

        # Optional: Use weighted events
        self.do_weighted = True 

        # Optional: read the input files with podio::DataSource 
        self.use_data_source = False # explicitly use old way in this version 

        # Optional: test file that is used if you run with the --test argument (fccanalysis run ./examples/FCChh/ggHH_bbyy/analysis_stage1.py --test)
        self.test_file = 'root://eospublic.cern.ch//eos/experiment/fcc/hh/' \
                         'DelphesEvents/fcc_v06/II/mgp8_pp_h012j_5f_hmumu/' \
                         'events_000000599.root'


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

                ########################################### MUONS ########################################### 

                .Define("muons",  "FCCAnalyses::ReconstructedParticle::get(Muon_objIdx.index, ReconstructedParticles)") 
                .Define("n_muons",  "FCCAnalyses::ReconstructedParticle::get_n(muons)")
                .Define("E_muons",  "FCCAnalyses::ReconstructedParticle::get_e(muons)")
                .Define("pT_muons",  "FCCAnalyses::ReconstructedParticle::get_pt(muons)")
                .Define("eta_muons",  "FCCAnalyses::ReconstructedParticle::get_eta(muons)")
                .Define("phi_muons",  "FCCAnalyses::ReconstructedParticle::get_phi(muons)")

                ########################################### JETS ########################################### 

                # all recnstructed jets
                .Define("n_jets",  "FCCAnalyses::ReconstructedParticle::get_n(Jet)")
                .Define("E_jets",  "FCCAnalyses::ReconstructedParticle::get_e(Jet)")
                .Define("pT_jets",  "FCCAnalyses::ReconstructedParticle::get_pt(Jet)")
                .Define("eta_jets",  "FCCAnalyses::ReconstructedParticle::get_eta(Jet)")
                .Define("phi_jets",  "FCCAnalyses::ReconstructedParticle::get_phi(Jet)")

                ########################################### MET ########################################### 
                .Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)")
                .Define("MET_phi", "FCCAnalyses::ReconstructedParticle::get_phi(MissingET)")
                # .Define("HT", "FCCAnalyses::ReconstructedParticle::get_pt(ScalarHT)") #not yet in k4SimDelphes due to bug

                ########################################### MC PARTICLES ########################################### 

                #all MC particles
                .Define("mc_particles", "Particle")
                .Alias("mc_parents", "_Particle_parents.index")
                .Alias("mc_daughters", "_Particle_daughters.index")

                .Define("mc_higgses", "FCCAnalyses::MCParticle::sel_pdgID(25, true)(mc_particles)")
                .Define("n_mc_higgses", "FCCAnalyses::MCParticle::get_n(mc_higgses)")
                .Define("m_mc_higgses", "FCCAnalyses::MCParticle::get_mass(mc_higgses)")

                .Define("mc_Ws", "FCCAnalyses::MCParticle::sel_pdgID(24, true)(mc_particles)")
                .Define("n_mc_Ws", "FCCAnalyses::MCParticle::get_n(mc_Ws)")
                # .Define("m_mc_higgses", "FCCAnalyses::MCParticle::get_mass(mc_higgses)")
                # make pairs of Ws with zero total charge:
                .Define("W_pairs", "AnalysisFCChh::getOSPairs(mc_Ws)")
                .Define("n_W_pairs", "W_pairs.size()")
                .Define("first_W_pair", "AnalysisFCChh::get_first_pair(W_pairs)")
                .Define("first_W_pair_merged", "AnalysisFCChh::merge_pairs(first_W_pair)")
                .Define("m_WW_from_pairs", "FCCAnalyses::MCParticle::get_mass(first_W_pair_merged)")
                

                #Ws directly from the Higgs decay
                .Define("Ws_from_Higgs", "AnalysisFCChh::getWFromH(mc_particles, mc_parents)")
                .Define("n_Ws_from_Higgs", "FCCAnalyses::MCParticle::get_n(Ws_from_Higgs)")

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
            'n_muons', 
            # all jets
            'n_jets', 'E_jets', 'pT_jets', 'eta_jets', 'phi_jets',
            # MET & HT 
            'MET', 'MET_phi', #'HT',
            #gen level higges and Ws for validation
            'n_mc_higgses', 'm_mc_higgses',
            'n_Ws_from_Higgs', 'n_mc_Ws', 'n_W_pairs', 
            'm_WW_from_pairs',

        ]
        return branch_list