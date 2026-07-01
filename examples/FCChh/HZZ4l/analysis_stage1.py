'''
Single Higgs @FCC-hh : HZZ4l analysis
'''
from argparse import ArgumentParser


# Mandatory: Analysis class where the user defines the operations on the
# dataframe.
class Analysis():
    '''
    H(ZZ->4l) analysis
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

        # Mandatory: Input directory where to find the samples, or a production tag when running over the centrally produced
        # samples (this points to the yaml files for getting sample statistics)
        self.input_dir = '/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/{}/'.format(self.ana_args.detector)

        # Optional: output directory, default is local running directory
        self.output_dir = '/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/{}/H4l_analysis/'.format(self.ana_args.detector)

        # Mandatory: List of processes to run over
        if self.ana_args.energy == "100TeV":
            self.process_list = {
                 #FULL @ 100 TeV
                # 'mgp8_pp_h012j_5f_hllll/events_000000564': {}, #signal 
                # 'mgp8_pp_h012j_5f_hllll': {'fraction':0.001}, # LOCAL TESTER! 

                'mgp8_pp_h012j_5f_hllll': {'chunks':50}, #signal 
                'mgp8_pp_tth01j_5f_hllll': {'chunks':50},  
                'mgp8_pp_vbf_h01j_5f_hllll': {'chunks':50},  
                'mgp8_pp_vh012j_5f_hllll': {'chunks':50},  
                'mgp8_pp_llll01j_mhcut_5f_HT_0_200': {'chunks':50}, #4l cont. bkg
                'mgp8_pp_llll01j_mhcut_5f_HT_200_500': {'chunks':50},
                'mgp8_pp_llll01j_mhcut_5f_HT_500_1100': {'chunks':50}, 
                'mgp8_pp_llll01j_mhcut_5f_HT_1100_100000': {'chunks':50}, 
            }
             
            self.output_dir = self.output_dir+"/100TeV/"

        elif self.ana_args.energy == "84TeV" or self.ana_args.energy == "72TeV" or self.ana_args.energy == "120TeV":
            self.process_list =  {
                'mgp8_pp_h012j_5f_{}_hllll'.format(self.ana_args.energy):{'chunks':50}, 
                'mgp8_pp_vbf_h01j_5f_{}_hllll'.format(self.ana_args.energy):{'chunks':50}, 
                'mgp8_pp_tth01j_5f_{}_hllll'.format(self.ana_args.energy):{'chunks':50}, 
                'mgp8_pp_vh012j_5f_{}_hllll'.format(self.ana_args.energy):{'chunks':50}, 
                'mgp8_pp_llll01j_mhcut_5f_HT_0_200_{}'.format(self.ana_args.energy):{'chunks':50}, 
                'mgp8_pp_llll01j_mhcut_5f_HT_200_500_{}'.format(self.ana_args.energy):{'chunks':50}, 
                'mgp8_pp_llll01j_mhcut_5f_HT_500_1100_{}'.format(self.ana_args.energy):{'chunks':50}, 
                'mgp8_pp_llll01j_mhcut_5f_HT_1100_100000_{}'.format(self.ana_args.energy):{'chunks':50}, 
            }

            self.output_dir = self.output_dir+"/{}/".format(self.ana_args.energy)

        else:
            raise Exception("Unsupported argumente for energy! Currently only support 100TeV, 84TeV, 72TeV and 120TeV!")

        # Optional: analysisName, default is ''
        self.analysis_name = 'FCC-hh H4mu analysis'

        # Optional: number of threads to run on, default is 'all available'
        self.n_threads = 4

        # Optional: running on HTCondor, default is False
        self.run_batch = True
        # self.run_batch = False

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

                # apply selection to the muons
                .Define("selpt_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(5.)(muons)")
                .Define("sel_muons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_muons)")
                .Define("sel_muons", "AnalysisFCChh::SortParticleCollection(sel_muons_unsort)") #sort by pT
                .Define("n_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_muons)") 
                .Define("pT_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_muons)") 
                .Define("eta_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_muons)") 
                .Define("phi_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_muons)") 

                ########################################### ELECTRONS ########################################### 
                .Define("electrons",  "FCCAnalyses::ReconstructedParticle::get(Electron_objIdx.index, ReconstructedParticles)")
                .Define("n_electrons",  "FCCAnalyses::ReconstructedParticle::get_n(electrons)")
                .Define("E_electrons",  "FCCAnalyses::ReconstructedParticle::get_e(electrons)")
                .Define("pT_electrons",  "FCCAnalyses::ReconstructedParticle::get_pt(electrons)")
                .Define("eta_electrons",  "FCCAnalyses::ReconstructedParticle::get_eta(electrons)")
                .Define("phi_electrons",  "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")

                # apply selection to the electrons
                .Define("selpt_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(5.)(electrons)")
                .Define("sel_electrons_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_electrons)")
                .Define("sel_electrons", "AnalysisFCChh::SortParticleCollection(sel_electrons_unsort)") #sort by pT
                .Define("n_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_n(sel_electrons)") 
                .Define("pT_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_electrons)") 
                .Define("eta_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_electrons)") 
                .Define("phi_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_electrons)") 

                ########################################### JETS ########################################### 

                # all reconstructed jets
                .Define("n_jets",  "FCCAnalyses::ReconstructedParticle::get_n(Jet)")
                .Define("E_jets",  "FCCAnalyses::ReconstructedParticle::get_e(Jet)")
                .Define("pT_jets",  "FCCAnalyses::ReconstructedParticle::get_pt(Jet)")
                .Define("eta_jets",  "FCCAnalyses::ReconstructedParticle::get_eta(Jet)")
                .Define("phi_jets",  "FCCAnalyses::ReconstructedParticle::get_phi(Jet)")

                ########################################### MET & HT ########################################### 
                .Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)")
                .Define("MET_phi", "FCCAnalyses::ReconstructedParticle::get_phi(MissingET)")
                # .Define("HT", "FCCAnalyses::ReconstructedParticle::get_pt(ScalarHT)") 

                .Define("recoHT", "ScalarHT")

                ########################################### MC PARTICLES ########################################### 

                # #all MC particles
                .Alias("mc_particles", "Particle")
                .Alias("mc_parents", "_Particle_parents.index")
                .Alias("mc_daughters", "_Particle_daughters.index")

                #THIS ONLY WORKS ON SIGNAL SAMPLES!
                .Define("truth_ZZ_llll_flavour", "AnalysisFCChh::getTruthZ4lFlavourFlag(mc_particles, mc_parents, mc_daughters)")

                # .Define("genHT", "FCCAnalyses::MCParticle::scalarHT(mc_particles)")

                # .Define("mc_muons", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(mc_particles)")
                # .Define("n_mc_muons", "FCCAnalyses::MCParticle::get_n(mc_muons)")

                ########################################### LEPTON PAIRS ########################################### 
                .Define("OS_ll_pairs", "AnalysisFCChh::build_Zll_pairs(sel_muons, sel_electrons)")
                .Define("n_OS_ll_pairs", "AnalysisFCChh::get_n_pairs(OS_ll_pairs)")

        )

        # dframe3 = dframe2

        dframe_sel = dframe2.Filter("n_OS_ll_pairs > 1")  
        
        dframe3 =  (dframe_sel
                #require at least 2 pairs found to continue!
                .Define("Zll_pair_leading_unmerged", "OS_ll_pairs.at(0)")
                .Define("Zll_pair_subleading_unmerged", "OS_ll_pairs.at(1)")

                #split the pairs:
                .Define("tlv_leading_pair_lep1", "AnalysisFCChh::getTLV_reco(Zll_pair_leading_unmerged.particle_1)") 
                .Define("tlv_leading_pair_lep2", "AnalysisFCChh::getTLV_reco(Zll_pair_leading_unmerged.particle_2)") 
                .Define("leading_pair_lep1_e",  "tlv_leading_pair_lep1.E()")
                .Define("leading_pair_lep1_pt",  "tlv_leading_pair_lep1.Pt()")
                .Define("leading_pair_lep1_eta",  "tlv_leading_pair_lep1.Eta()")
                .Define("leading_pair_lep1_phi",  "tlv_leading_pair_lep1.Phi()")
                .Define("leading_pair_lep2_e",  "tlv_leading_pair_lep2.E()")
                .Define("leading_pair_lep2_pt",  "tlv_leading_pair_lep2.Pt()")
                .Define("leading_pair_lep2_eta",  "tlv_leading_pair_lep2.Eta()")
                .Define("leading_pair_lep2_phi",  "tlv_leading_pair_lep2.Phi()")

                .Define("tlv_subleading_pair_lep1", "AnalysisFCChh::getTLV_reco(Zll_pair_subleading_unmerged.particle_1)") 
                .Define("tlv_subleading_pair_lep2", "AnalysisFCChh::getTLV_reco(Zll_pair_subleading_unmerged.particle_2)") 
                .Define("subleading_pair_lep1_e",  "tlv_subleading_pair_lep1.E()")
                .Define("subleading_pair_lep1_pt",  "tlv_subleading_pair_lep1.Pt()")
                .Define("subleading_pair_lep1_eta",  "tlv_subleading_pair_lep1.Eta()")
                .Define("subleading_pair_lep1_phi",  "tlv_subleading_pair_lep1.Phi()")
                .Define("subleading_pair_lep2_e",  "tlv_subleading_pair_lep2.E()")
                .Define("subleading_pair_lep2_pt",  "tlv_subleading_pair_lep2.Pt()")
                .Define("subleading_pair_lep2_eta",  "tlv_subleading_pair_lep2.Eta()")
                .Define("subleading_pair_lep2_phi",  "tlv_subleading_pair_lep2.Phi()")

                .Define("Zll_pair_leading", "AnalysisFCChh::merge_pair(Zll_pair_leading_unmerged)")
                .Define("Zll_pair_subleading", "AnalysisFCChh::merge_pair(Zll_pair_subleading_unmerged)")

                .Define("m_ll_leading", "FCCAnalyses::ReconstructedParticle::get_mass(Zll_pair_leading)")
                .Define("pT_ll_leading", "FCCAnalyses::ReconstructedParticle::get_pt(Zll_pair_leading)")
                .Define("eta_ll_leading", "FCCAnalyses::ReconstructedParticle::get_eta(Zll_pair_leading)")

                .Define("m_ll_subleading", "FCCAnalyses::ReconstructedParticle::get_mass(Zll_pair_subleading)")
                .Define("pT_ll_subleading", "FCCAnalyses::ReconstructedParticle::get_pt(Zll_pair_subleading)")
                .Define("eta_ll_subleading", "FCCAnalyses::ReconstructedParticle::get_eta(Zll_pair_subleading)")

                .Define("ZZ_llll_system", "AnalysisFCChh::merge_parts_TLVs(Zll_pair_leading, Zll_pair_subleading)")
                .Define("pT_llll", "FCCAnalyses::ReconstructedParticle::get_pt(ZZ_llll_system)")
                .Define("m_llll", "FCCAnalyses::ReconstructedParticle::get_mass(ZZ_llll_system)")
                .Define("eta_llll", "FCCAnalyses::ReconstructedParticle::get_eta(ZZ_llll_system)")

                .Define("ZZ_llll_flavour", "AnalysisFCChh::get_4l_flavour_flag(Zll_pair_leading_unmerged, Zll_pair_subleading_unmerged)")
        )
            
        return dframe3

    # Mandatory: output function, please make sure you return the branch list
    # as a python list
    def output(self):
        '''
        Output variables which will be saved to output root file.
        '''
        branch_list = [
            'weight',
            # leptons:
            'n_muons', 'n_muons_sel', 'pT_muons_sel', 'eta_muons_sel', 'phi_muons_sel',
            'n_electrons', 'n_electrons_sel', 'pT_electrons_sel', 'eta_electrons_sel', 'phi_electrons_sel',
            # building the H4l system 
            'n_OS_ll_pairs',
            'leading_pair_lep1_e', 'leading_pair_lep1_pt', 'leading_pair_lep1_eta', 'leading_pair_lep1_phi',
            'leading_pair_lep2_e', 'leading_pair_lep2_pt', 'leading_pair_lep2_eta', 'leading_pair_lep2_phi',
            'subleading_pair_lep1_e', 'subleading_pair_lep1_pt', 'subleading_pair_lep1_eta', 'subleading_pair_lep1_phi',
            'subleading_pair_lep2_e', 'subleading_pair_lep2_pt', 'subleading_pair_lep2_eta', 'subleading_pair_lep2_phi',
            'm_ll_leading', 'pT_ll_leading', 'eta_ll_leading', 
            'm_ll_subleading', 'pT_ll_subleading', 'eta_ll_subleading', 
            'pT_llll', 'm_llll', 'eta_llll',
            'ZZ_llll_flavour',
            # all jets
            'n_jets', 'E_jets', 'pT_jets', 'eta_jets', 'phi_jets',
            # MET & HT 
            'MET', 'MET_phi', 'recoHT',
            #gen level muons for validation
            # 'n_mc_muons', "genHT",

            #ONLY FOR SIGNALS:
            "truth_ZZ_llll_flavour",

        ]
        return branch_list