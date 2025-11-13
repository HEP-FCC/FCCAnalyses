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
            'pwp8_pp_hh_5f_hhbbyy': {},
        }

        # Mandatory: Input directory where to find the samples, or a production tag when running over the centrally produced
        # samples (this points to the yaml files for getting sample statistics)
        self.input_dir = '/eos/experiment/fcc/hh/tutorials/edm4hep_tutorial_data/'

        # Optional: output directory, default is local running directory
        self.output_dir = 'outputs/FCChh/ggHH_bbyy/presel/'

        # Optional: analysisName, default is ''
        self.analysis_name = 'FCC-hh bbyy analysis'

        # Optional: number of threads to run on, default is 1
        # self.n_threads = 4

        # Optional: running on HTCondor, default is False
        # self.run_batch = False

        # Optional: Use weighted events
        self.do_weighted = True 

        # Optional: read the input files with podio::DataSource 
        self.use_data_source = False # explicitly use old way in this version 

        # Optional: test file that is used if you run with the --test argument (fccanalysis run ./examples/FCChh/ggHH_bbyy/analysis_stage1.py --test)
        self.test_file = 'root://eospublic.cern.ch//eos/experiment/fcc/hh/' \
                         'tutorials/edm4hep_tutorial_data/' \
                         'pwp8_pp_hh_5f_hhbbyy.root'


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

            ########################################### PHOTONS ########################################### 

            .Define("gamma",  "FCCAnalyses::ReconstructedParticle::get(Photon_objIdx.index, ReconstructedParticles)")
            .Define("selpt_gamma", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(gamma)")
            .Define("sel_gamma_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_gamma)")
            .Define("sel_gamma", "AnalysisFCChh::SortParticleCollection(sel_gamma_unsort)") #sort by pT

            .Define("n_gamma",  "FCCAnalyses::ReconstructedParticle::get_n(sel_gamma)") 
            .Define("g1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_gamma)[0]")
            .Define("g1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_gamma)[0]")
            .Define("g1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_gamma)[0]")
            .Define("g1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_gamma)[0]")
            .Define("g2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_gamma)[1]")
            .Define("g2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_gamma)[1]")
            .Define("g2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_gamma)[1]")
            .Define("g2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_gamma)[1]")

            # H(yy) if it exists, if there are no 2 selected photons, doesnt get filled 
            .Define("yy_pairs_unmerged", "AnalysisFCChh::getPairs(sel_gamma)") # retrieves the leading pT pair of all possible 
            .Define("yy_pairs", "AnalysisFCChh::merge_pairs(yy_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_yy", "FCCAnalyses::ReconstructedParticle::get_mass(yy_pairs)")

            ########################################### JETS ########################################### 

            # b-tagged jets at medium working point
            .Define("b_tagged_jets_medium", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)") #bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            # select medium b-jets with pT > 30 GeV, |eta| < 4
            .Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(b_tagged_jets_medium)")
            .Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
            .Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)") #sort by pT
            .Define("n_bjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")
            .Define("b1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_bjets)[0]")
            .Define("b1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)[0]")
            .Define("b1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_bjets)[0]")
            .Define("b1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_bjets)[0]")
            .Define("b2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_bjets)[1]")
            .Define("b2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)[1]")
            .Define("b2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_bjets)[1]")
            .Define("b2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_bjets)[1]")

            # H(bb) system - using the medium WP jets - if there are no 2 b-tagged jets these variable don't get filled
            .Define("bb_pairs_unmerged", "AnalysisFCChh::getPairs(sel_bjets)") # retrieves the leading pT pair of all possible 
            .Define("bb_pairs", "AnalysisFCChh::merge_pairs(bb_pairs_unmerged)") # merge pair into one object to access inv masses etc
            .Define("m_bb", "FCCAnalyses::ReconstructedParticle::get_mass(bb_pairs)")

            ########################################### APPLY PRE-SELECTION ########################################### 
            # require at least two b-jets and two photons
            .Filter("n_gamma > 1")
            .Filter("n_bjets > 1")

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
            'n_gamma', 'g1_pt', 'g2_pt', 'g1_eta', 'g2_eta', 'm_yy',
            # b-jets and H(bb) system:
            'n_bjets', 'b1_pt', 'b2_pt', 'b1_eta', 'b2_eta', 'm_bb',
        ]
        return branch_list
