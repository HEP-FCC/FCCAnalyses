'''
Single Higgs @FCC-hh : Hmumu analysis
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
        parser.add_argument('--energy', default='100TeV',
                            help='Energy point to run at. Options: 100TeV, 84TeV, 72TeV')
        parser.add_argument('--detector', default='II',
                            help='FCC-hh Delphes detector scenario to run with. Options: I and II (default)')
        # Parse additional arguments not known to the FCCAnalyses parsers
        # All command line arguments know to fccanalysis are provided in the
        # `cmdline_arg` dictionary.
        self.ana_args, _ = parser.parse_known_args(cmdline_args['unknown'])

        if not (self.ana_args.detector == "I" or self.ana_args.detector == "II"):
            raise Exception("ERROR! Unsupported detector scenario. Options are I or II only.")

        # Mandatory: Input directory where to find the samples, or a production tag when running over the centrally produced
        # samples (this points to the yaml files for getting sample statistics)
        self.input_dir = '/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/{}/'.format(self.ana_args.detector)

        # Optional: output directory, default is local running directory
        self.output_dir = '/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/{}/Hmumu_analysis/'.format(self.ana_args.detector)

        # Mandatory: List of processes to run over
        if self.ana_args.energy == "100TeV":
            self.process_list = {
                 #FULL @ 100 TeV
                'mgp8_pp_h012j_5f_hmumu': {'chunks':50}, #signal 
                'mgp8_pp_vbf_h01j_5f_hmumu': {'chunks':50}, #signal 
                'mgp8_pp_tth01j_5f_hmumu': {'chunks':50}, #signal 
                'mgp8_pp_vh012j_5f_hmumu': {'chunks':50}, #signal 
                'mgp8_pp_mumu012j_mhcut_5f_HT_0_100': {'chunks':50}, #mumu cont. bkg
                'mgp8_pp_mumu012j_mhcut_5f_HT_100_300': {'chunks':50}, #mumu cont. bkg
                'mgp8_pp_mumu012j_mhcut_5f_HT_300_500': {'chunks':50}, #mumu cont. bkg
                'mgp8_pp_mumu012j_mhcut_5f_HT_500_700': {'chunks':50}, #mumu cont. bkg
                'mgp8_pp_mumu012j_mhcut_5f_HT_700_900': {'chunks':50}, #mumu cont. bkg
                'mgp8_pp_mumu012j_mhcut_5f_HT_900_1100': {'chunks':50}, #mumu cont. bkg
                'mgp8_pp_mumu012j_mhcut_5f_HT_1100_100000': {'chunks':50}, #mumu cont. bkg
            }
             
            self.output_dir = self.output_dir+"/100TeV/"

        # elif self.ana_args.energy == "84TeV":
        #     self.process_list = {
        #          #FULL @ 84 TeV
        #         'mgp8_pp_h012j_5f_84TeV_hmumu': {'chunks':50}, #signal 
        #         'mgp8_pp_vbf_h01j_5f_84TeV_hmumu': {'chunks':50}, #signal 
        #         'mgp8_pp_tth01j_5f_84TeV_hmumu': {'chunks':50}, #signal 
        #         'mgp8_pp_vh012j_5f_84TeV_hmumu': {'chunks':100}, #signal 
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_0_100_84TeV': {'chunks':100}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_100_300_84TeV': {'chunks':100}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_300_500_84TeV': {'chunks':100}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_500_700_84TeV': {'chunks':100}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_700_900_84TeV': {'chunks':100}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_900_1100_84TeV': {'chunks':100}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_1100_100000_84TeV': {'chunks':100}, #mumu cont. bkg
        #     }

        #     self.output_dir = self.output_dir+"/84TeV/"
        
        # elif self.ana_args.energy == "72TeV":
        #     self.process_list = {
        #          #FULL @ 72 TeV
        #         'mgp8_pp_h012j_5f_72TeV_hmumu': {'chunks':50}, #signal 
        #         'mgp8_pp_vbf_h01j_5f_72TeV_hmumu': {'chunks':50}, #signal 
        #         'mgp8_pp_tth01j_5f_72TeV_hmumu': {'chunks':50}, #signal 
        #         'mgp8_pp_vh012j_5f_72TeV_hmumu': {'chunks':50}, #signal 
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_0_100_72TeV': {'chunks':50}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_100_300_72TeV': {'chunks':50}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_300_500_72TeV': {'chunks':50}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_500_700_72TeV': {'chunks':50}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_700_900_72TeV': {'chunks':50}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_900_1100_72TeV': {'chunks':50}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_1100_100000_72TeV': {'chunks':50}, #mumu cont. bkg
        #     }
        
        # elif self.ana_args.energy == "120TeV":
        #     self.process_list = {
        #          #FULL @ 120 TeV
        #         'mgp8_pp_h012j_5f_120TeV_hmumu': {'chunks':50}, #signal 
        #         'mgp8_pp_vbf_h01j_5f_120TeV_hmumu': {'chunks':50}, #signal 
        #         'mgp8_pp_tth01j_5f_120TeV_hmumu': {'chunks':50}, #signal 
        #         'mgp8_pp_vh012j_5f_120TeV_hmumu': {'chunks':50}, #signal 
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_0_100_120TeV': {'chunks':50}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_100_300_120TeV': {'chunks':50}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_300_500_120TeV': {'chunks':50}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_500_700_120TeV': {'chunks':50}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_700_900_120TeV': {'chunks':50}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_900_1100_120TeV': {'chunks':50}, #mumu cont. bkg
        #         'mgp8_pp_mumu012j_mhcut_5f_HT_1100_100000_120TeV': {'chunks':50}, #mumu cont. bkg
        #     }
            
        #     self.output_dir = self.output_dir+"/120TeV/"
        
        elif self.ana_args.energy == "84TeV" or self.ana_args.energy == "72TeV" or self.ana_args.energy == "120TeV":
            self.process_list =  {
                                
                'mgp8_pp_h012j_5f_{}_hmumu'.format(self.ana_args.energy): {'chunks':50}, #signal 
                'mgp8_pp_vbf_h01j_5f_{}_hmumu'.format(self.ana_args.energy): {'chunks':50}, #signal 
                'mgp8_pp_tth01j_5f_{}_hmumu'.format(self.ana_args.energy): {'chunks':50}, #signal 
                'mgp8_pp_vh012j_5f_{}_hmumu'.format(self.ana_args.energy): {'chunks':50}, #signal 
                'mgp8_pp_mumu012j_mhcut_5f_HT_0_100_{}'.format(self.ana_args.energy): {'chunks':50}, #mumu cont. bkg
                'mgp8_pp_mumu012j_mhcut_5f_HT_100_300_{}'.format(self.ana_args.energy): {'chunks':50}, #mumu cont. bkg
                'mgp8_pp_mumu012j_mhcut_5f_HT_300_500_{}'.format(self.ana_args.energy): {'chunks':50}, #mumu cont. bkg
                'mgp8_pp_mumu012j_mhcut_5f_HT_500_700_{}'.format(self.ana_args.energy): {'chunks':50}, #mumu cont. bkg
                'mgp8_pp_mumu012j_mhcut_5f_HT_700_900_{}'.format(self.ana_args.energy): {'chunks':50}, #mumu cont. bkg
                'mgp8_pp_mumu012j_mhcut_5f_HT_900_1100_{}'.format(self.ana_args.energy): {'chunks':50}, #mumu cont. bkg
                'mgp8_pp_mumu012j_mhcut_5f_HT_1100_100000_{}'.format(self.ana_args.energy): {'chunks':50}, #mumu cont. bkg

            }
            self.output_dir = self.output_dir+"/{}/".format(self.ana_args.energy)
        
        else:
            raise Exception("Unsupported argument for energy! Currently only support 100TeV, 84TeV, 72TeV and 120TeV!")

        # Optional: analysisName, default is ''
        self.analysis_name = 'FCC-hh Hmumu analysis'

        # Optional: number of threads to run on, default is 'all available'
        self.n_threads = 4

        # Optional: running on HTCondor, default is False
        # self.run_batch = False
        self.run_batch = True

        # Optional: Use weighted events
        self.do_weighted = False 

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

                # apply selection to the muons, and then build the leading pair
                .Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(20.)(muons)")
                .Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_muons)")
                .Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)") #sort by pT

                .Define("n_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_muons)") 

                #select the pair
                .Define("OS_mumu_pairs", "AnalysisFCChh::getOSPairs(sel_muons)") 
                .Define("n_os_muon_pairs",  "OS_mumu_pairs.size()") 
                .Define("best_OS_mumu_pair", "AnalysisFCChh::get_first_pair(OS_mumu_pairs)") 
                .Define("mu_plus", "AnalysisFCChh::get_first_from_pair(best_OS_mumu_pair)") 
                .Define("mu_minus", "AnalysisFCChh::get_second_from_pair(best_OS_mumu_pair)") 

                .Define("mu_plus_e",  "FCCAnalyses::ReconstructedParticle::get_e(mu_plus)")
                .Define("mu_plus_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(mu_plus)")
                .Define("mu_plus_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(mu_plus)")
                .Define("mu_plus_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(mu_plus)")
                .Define("mu_minus_e",  "FCCAnalyses::ReconstructedParticle::get_e(mu_minus)")
                .Define("mu_minus_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(mu_minus)")
                .Define("mu_minus_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(mu_minus)")
                .Define("mu_minus_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(mu_minus)")

                # # H(mumu) if it exists, if there is not selected pair, doesn't get filled 
                .Define("best_OS_mumu_pair_merged", "AnalysisFCChh::merge_pairs(best_OS_mumu_pair)") # merge pair into one object to access inv masses etc
                .Define("m_mumu", "FCCAnalyses::ReconstructedParticle::get_mass(best_OS_mumu_pair_merged)")
                .Define("pT_mumu", "FCCAnalyses::ReconstructedParticle::get_pt(best_OS_mumu_pair_merged)")
                .Define("eta_mumu", "FCCAnalyses::ReconstructedParticle::get_eta(best_OS_mumu_pair_merged)")

                ########################################### JETS ########################################### 

                # all recnstructed jets
                .Define("n_jets",  "FCCAnalyses::ReconstructedParticle::get_n(Jet)")
                .Define("E_jets",  "FCCAnalyses::ReconstructedParticle::get_e(Jet)")
                .Define("pT_jets",  "FCCAnalyses::ReconstructedParticle::get_pt(Jet)")
                .Define("eta_jets",  "FCCAnalyses::ReconstructedParticle::get_eta(Jet)")
                .Define("phi_jets",  "FCCAnalyses::ReconstructedParticle::get_phi(Jet)")

                ########################################### MET & HT ########################################### 
                .Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)")
                .Define("MET_phi", "FCCAnalyses::ReconstructedParticle::get_phi(MissingET)")
                # .Define("HT", "FCCAnalyses::ReconstructedParticle::get_pt(ScalarHT)") #not yet in k4SimDelphes due to bug

                .Define("recoHT", "ScalarHT")

                ########################################### MC PARTICLES ########################################### 

                #all MC particles
                .Alias("mc_particles", "Particle")
                # .Alias("mc_parents", "_Particle_parents.index")
                # .Alias("mc_daughters", "_Particle_daughters.index")

                .Define("genHT", "FCCAnalyses::MCParticle::scalarHT(mc_particles)")

                .Define("mc_muons", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(mc_particles)")
                .Define("n_mc_muons", "FCCAnalyses::MCParticle::get_n(mc_muons)")



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
            # muons and H(mumu) system:
            'n_muons', 'n_muons_sel', 'n_os_muon_pairs',
            'mu_plus_e', 'mu_plus_pt', 'mu_plus_eta', 'mu_plus_phi',
            'mu_minus_e', 'mu_minus_pt', 'mu_minus_eta', 'mu_minus_phi',
            'm_mumu', 'pT_mumu', 'eta_mumu',
            # all jets
            'n_jets', 'E_jets', 'pT_jets', 'eta_jets', 'phi_jets',
            # MET & HT 
            'MET', 'MET_phi', 'recoHT',
            #gen level muons for validation
            'n_mc_muons', "genHT",
        ]
        return branch_list