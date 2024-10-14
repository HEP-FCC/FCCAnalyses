'''
Analysis example for FCC-hh, using gg->HH->bbyy di-Higgs production events 
'''
from argparse import ArgumentParser


# Mandatory: Analysis class where the user defines the operations on the
# dataframe.
class Analysis():
    '''
    Di-Higgs analysis in bbyy.
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
            'pwp8_pp_hh_5f_hhbbyy_split_HF_tau_tags': {},
            # 'pwp8_pp_hh_5f_hhbbyy': {},
        }

        # Mandatory: Input directory where to find the samples, or a production tag when running over the centrally produced
        # samples (this points to the yaml files for getting sample statistics)
        self.input_dir = '/eos/experiment/fcc/hh/tutorials/lhe_unpacked_tester/'
        # self.input_dir = '/eos/experiment/fcc/hh/tutorials/edm4hep_tutorial_data/'
        # self.prod_tag = 'FCCee/spring2021/IDEA/'

        # Optional: output directory, default is local running directory
        self.output_dir = 'outputs/FCChh/ggHH_bbyy/presel/'

        # Optional: analysisName, default is ''
        # self.analysis_name = 'My Analysis'

        # Optional: number of threads to run on, default is 'all available'
        # self.n_threads = 4

        # Optional: running on HTCondor, default is False
        # self.run_batch = False

        # Optional: Use weighted events
        self.do_weighted = True 

        # Optional: test file that is used if you run with the --test argument (fccanalysis run ./examples/FCChh/ggHH_bbyy/analysis_stage1.py --test)
        self.test_file = 'root://eospublic.cern.ch//eos/experiment/fcc/hh/' \
                         'tutorials/edm4hep_tutorial_data/' \
                         'p8_ee_ZH_ecm240.root'


    # Mandatory: analyzers function to define the analysis graph, please make
    # sure you return the dataframe, in this example it is dframe2
    def analyzers(self, dframe):
        '''
        Analysis graph.
        '''

        dframe2 = (
            dframe

            .Define("weight",  "EventHeader.weight")

            ########################################### PHOTONS ########################################### 

            .Define("gamma",  "FCCAnalyses::ReconstructedParticle::get(Photon_objIdx.index, ReconstructedParticles)")
            .Define("selpt_gamma", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(gamma)")
            .Define("sel_gamma_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_gamma)")
            .Define("sel_gamma", "AnalysisFCChh::SortParticleCollection(sel_gamma_unsort)") #sort by pT

            .Define("ngamma",  "FCCAnalyses::ReconstructedParticle::get_n(sel_gamma)") 
            .Define("g1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_gamma)[0]")
            .Define("g1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_gamma)[0]")
            .Define("g1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_gamma)[0]")
            .Define("g1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_gamma)[0]")
            .Define("g2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_gamma)[1]")
            .Define("g2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_gamma)[1]")
            .Define("g2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_gamma)[1]")
            .Define("g2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_gamma)[1]")

            #H(yy) if it exists, if there are no 2 selected photons, doesnt get filled 
            .Define("yy_pairs_unmerged", "AnalysisFCChh::getPairs(sel_gamma)") # retrieves the leading pT pair of all possible 
            .Define("yy_pairs", "AnalysisFCChh::merge_pairs(yy_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_yy", "FCCAnalyses::ReconstructedParticle::get_mass(yy_pairs)")


            ########################################### JETS ########################################### 

            # selected jets above a pT threshold of 30 GeV, eta < 4
            .Define("selpt_jets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(Jet)")
            .Define("sel_jets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_jets)")
            .Define("sel_jets", "AnalysisFCChh::SortParticleCollection(sel_jets_unsort)") 
            .Define("njets",  "FCCAnalyses::ReconstructedParticle::get_n(sel_jets)")
            .Define("j1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_jets)[0]")
            .Define("j1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_jets)[0]")
            .Define("j1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_jets)[0]")
            .Define("j1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_jets)[0]")

            .Define("j2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_jets)[1]")
            .Define("j2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_jets)[1]")
            .Define("j2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_jets)[1]")
            .Define("j2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_jets)[1]")

            #b-tagged jets:
            #b tagged jets
            .Define("bjets", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)") #bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            .Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(bjets)")
            .Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
            .Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)")
            .Define("nbjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")
            .Define("b1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_bjets)[0]")
            .Define("b1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)[0]")
            .Define("b1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_bjets)[0]")
            .Define("b1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_bjets)[0]")
            .Define("b2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_bjets)[1]")
            .Define("b2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)[1]")
            .Define("b2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_bjets)[1]")
            .Define("b2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_bjets)[1]")

            #H(bb) system - using the medium WP jets - if there are no 2 b-tagged jets these variable don't get filled
            .Define("bb_pairs_unmerged", "AnalysisFCChh::getPairs(sel_bjets)") # retrieves the leading pT pair of all possible 
            .Define("bb_pairs", "AnalysisFCChh::merge_pairs(bb_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_bb", "FCCAnalyses::ReconstructedParticle::get_mass(bb_pairs)")

            ########################################### APPLY PRE-SELECTION ########################################### 

            #require at least two b-jets and two photons, both with invariant masses compatible with the Higgs mass
            .Filter("sel_bjets.size()>1")
            .Filter("sel_gamma.size()>1") 
            .Filter("m_bb[0] < 200.") 
            .Filter("m_bb[0] > 80.") 
            .Filter("m_yy[0] < 180.") 
            .Filter("m_yy[0] > 100.")   

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
            # Photons and H(yy) system:
            'ngamma', 'g1_pt', 'g2_pt', 'g1_eta', 'g2_eta', 'm_yy',
            # b-jets and H(bb) system:
            'nbjets', 'b1_pt', 'b2_pt', 'b1_eta', 'b2_eta', 'm_bb',
        ]
        return branch_list
