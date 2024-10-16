'''
Analysis example for FCC-hh, using gg->HH->bbyy di-Higgs production events to check the Delphes b-tagging efficiencies
'''
from argparse import ArgumentParser

# Mandatory: Analysis class where the user defines the operations on the
# dataframe.
class Analysis():
    '''
    Validation of Delphes b-tagging efficiencies in HH->bbyy events.
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
        self.output_dir = 'outputs/FCChh/ggHH_bbyy/nosel/'

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
                         'pwp8_pp_hh_5f_hhbbyy.root'


    # Mandatory: analyzers function to define the analysis graph, please make
    # sure you return the dataframe, in this example it is dframe2
    def analyzers(self, dframe):
        '''
        Analysis graph.
        '''

        dframe2 = (
            dframe

            .Define("weight",  "EventHeader.weight")

            ########################################### JETS ########################################### 

            #LOOSE WP
            .Define("b_tagged_jets_loose", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 0)") #bit 0 = loose WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            .Define("n_b_jets_loose", "FCCAnalyses::ReconstructedParticle::get_n(b_tagged_jets_loose)")
            .Define("px_b_jets_loose",  "FCCAnalyses::ReconstructedParticle::get_px(b_tagged_jets_loose)")
            .Define("py_b_jets_loose",  "FCCAnalyses::ReconstructedParticle::get_py(b_tagged_jets_loose)")
            .Define("pz_b_jets_loose",  "FCCAnalyses::ReconstructedParticle::get_pz(b_tagged_jets_loose)")
            .Define("E_b_jets_loose",  "FCCAnalyses::ReconstructedParticle::get_e(b_tagged_jets_loose)")
            .Define("pT_b_jets_loose",  "FCCAnalyses::ReconstructedParticle::get_pt(b_tagged_jets_loose)")
            .Define("eta_b_jets_loose",  "FCCAnalyses::ReconstructedParticle::get_eta(b_tagged_jets_loose)")

            #MEDIUM WP
            .Define("b_tagged_jets_medium", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 1)") #bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            .Define("n_b_jets_medium", "FCCAnalyses::ReconstructedParticle::get_n(b_tagged_jets_medium)")
            .Define("px_b_jets_medium",  "FCCAnalyses::ReconstructedParticle::get_px(b_tagged_jets_medium)")
            .Define("py_b_jets_medium",  "FCCAnalyses::ReconstructedParticle::get_py(b_tagged_jets_medium)")
            .Define("pz_b_jets_medium",  "FCCAnalyses::ReconstructedParticle::get_pz(b_tagged_jets_medium)")
            .Define("E_b_jets_medium",  "FCCAnalyses::ReconstructedParticle::get_e(b_tagged_jets_medium)")
            .Define("pT_b_jets_medium",  "FCCAnalyses::ReconstructedParticle::get_pt(b_tagged_jets_medium)")
            .Define("eta_b_jets_medium",  "FCCAnalyses::ReconstructedParticle::get_eta(b_tagged_jets_medium)")

            #TIGHT WP
            .Define("b_tagged_jets_tight", "AnalysisFCChh::get_tagged_jets(Jet, Jet_HF_tags, _Jet_HF_tags_particle, _Jet_HF_tags_parameters, 2)") #bit 2 = tight WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            .Define("n_b_jets_tight", "FCCAnalyses::ReconstructedParticle::get_n(b_tagged_jets_tight)")
            .Define("px_b_jets_tight",  "FCCAnalyses::ReconstructedParticle::get_px(b_tagged_jets_tight)")
            .Define("py_b_jets_tight",  "FCCAnalyses::ReconstructedParticle::get_py(b_tagged_jets_tight)")
            .Define("pz_b_jets_tight",  "FCCAnalyses::ReconstructedParticle::get_pz(b_tagged_jets_tight)")
            .Define("E_b_jets_tight",  "FCCAnalyses::ReconstructedParticle::get_e(b_tagged_jets_tight)")
            .Define("pT_b_jets_tight",  "FCCAnalyses::ReconstructedParticle::get_pt(b_tagged_jets_tight)")
            .Define("eta_b_jets_tight",  "FCCAnalyses::ReconstructedParticle::get_eta(b_tagged_jets_tight)")

            ########################################### MC PARTICLES ########################################### 

            #all MC particles
            .Define("mc_particles", "Particle")
            .Alias("mc_parents", "_Particle_parents.index")
            .Alias("mc_daughters", "_Particle_daughters.index")


            ################################# Gen matched b-jets for b-tag eff study ########################################### 
            .Define("MC_b", "AnalysisFCChh::getBhadron(mc_particles,mc_parents)")
            .Define("jets_genmatched_b", "AnalysisFCChh::find_reco_matches(MC_b, Jet, 0.4)")

            .Define("bjets_loose_genmatched_b", "AnalysisFCChh::find_reco_matches(MC_b, b_tagged_jets_loose, 0.4)")
            .Define("bjets_medium_genmatched_b", "AnalysisFCChh::find_reco_matches(MC_b, b_tagged_jets_medium, 0.4)")
            .Define("bjets_tight_genmatched_b", "AnalysisFCChh::find_reco_matches(MC_b, b_tagged_jets_tight, 0.4)")

            #all genmatched
            .Define("n_jets_genmatched_b", "FCCAnalyses::ReconstructedParticle::get_n(jets_genmatched_b)")
            .Define("pT_jets_genmatched_b", "FCCAnalyses::ReconstructedParticle::get_pt(jets_genmatched_b)")
            .Define("eta_jets_genmatched_b", "FCCAnalyses::ReconstructedParticle::get_eta(jets_genmatched_b)")

            #loose btag
            .Define("n_bjets_loose_genmatched_b", "FCCAnalyses::ReconstructedParticle::get_n(bjets_loose_genmatched_b)")
            .Define("pT_bjets_loose_genmatched_b", "FCCAnalyses::ReconstructedParticle::get_pt(bjets_loose_genmatched_b)")
            .Define("eta_bjets_loose_genmatched_b", "FCCAnalyses::ReconstructedParticle::get_eta(bjets_loose_genmatched_b)")

            #medium btag
            .Define("n_bjets_medium_genmatched_b", "FCCAnalyses::ReconstructedParticle::get_n(bjets_medium_genmatched_b)")
            .Define("pT_bjets_medium_genmatched_b", "FCCAnalyses::ReconstructedParticle::get_pt(bjets_medium_genmatched_b)")
            .Define("eta_bjets_medium_genmatched_b", "FCCAnalyses::ReconstructedParticle::get_eta(bjets_medium_genmatched_b)")

            #tight btag
            .Define("n_bjets_tight_genmatched_b", "FCCAnalyses::ReconstructedParticle::get_n(bjets_tight_genmatched_b)")
            .Define("pT_bjets_tight_genmatched_b", "FCCAnalyses::ReconstructedParticle::get_pt(bjets_tight_genmatched_b)")
            .Define("eta_bjets_tight_genmatched_b", "FCCAnalyses::ReconstructedParticle::get_eta(bjets_tight_genmatched_b)")

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
            #gen-matched b-jets to check efficiencies
            'n_b_jets_loose', 'n_b_jets_medium', 'n_b_jets_tight',
            'n_jets_genmatched_b', 'pT_jets_genmatched_b', 'eta_jets_genmatched_b',
            'n_bjets_loose_genmatched_b', 'pT_bjets_loose_genmatched_b', 'eta_bjets_loose_genmatched_b',
            'n_bjets_medium_genmatched_b', 'pT_bjets_medium_genmatched_b', 'eta_bjets_medium_genmatched_b',
            'n_bjets_tight_genmatched_b', 'pT_bjets_tight_genmatched_b', 'eta_bjets_tight_genmatched_b',
        ]
        return branch_list
