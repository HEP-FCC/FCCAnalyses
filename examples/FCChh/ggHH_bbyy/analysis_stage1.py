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
        # self.prod_tag = 'FCCee/spring2021/IDEA/'

        # Optional: output directory, default is local running directory
        self.output_dir = 'outputs/FCChh/ggHH_bbyy/' \
                          # f'stage1_{self.ana_args.muon_pt}'

        # Optional: analysisName, default is ''
        # self.analysis_name = 'My Analysis'

        # Optional: number of threads to run on, default is 'all available'
        # self.n_threads = 4

        # Optional: running on HTCondor, default is False
        # self.run_batch = False

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
            .Define("sel_gamma", "AnalysisFCChh::SortParticleCollection(sel_gamma_unsort)")

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
            .Define("yy_pairs_unmerged", "AnalysisFCChh::getPairs(sel_gamma)")
            .Define("yy_pairs", "AnalysisFCChh::merge_pairs(yy_pairs_unmerged)")
            .Define("m_yy", "FCCAnalyses::ReconstructedParticle::get_mass(yy_pairs)")


            ########################################### JETS ########################################### 

            # jets after overlap removal is performed between jets and isolated electrons, muons and photons

            # selected jets above a pT threshold of 30 GeV, eta < 4, tight ID 
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
            # .Alias("Jet3","Jet#3.index") 
            .Alias("Jet3","_Jet_particles.index")
            #LOOSE WP : bit 1 = medium WP, bit 2 = tight WP
            #b tagged jets
            .Define("bjets", "AnalysisFCChh::get_tagged_jets(ReconstructedParticles, ParticleIDs, _ParticleIDs_particle, _ParticleIDs_parameters, 1)") #bit 0 = loose WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
            # .Define("bjets", "AnalysisFCChh::get_tagged_jets(Jet, Jet3, ParticleIDs, _ParticleIDs_parameters, 1)") #bit 0 = loose WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
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


            # #H(bb) system - using the loose WP b-jets -> if the events has < 2 bjets these variables do not get filled!
            # .Define("bb_pairs_unmerged", "AnalysisFCChh::getPairs(sel_bjets)") #currently gets only leading pT pair, as a RecoParticlePair
            # #then merge the bb pair into one object and get its kinematic properties
            # .Define("bb_pairs", "AnalysisFCChh::merge_pairs(bb_pairs_unmerged)") #merge into one object to access inv masses etc
            # .Define("m_bb", "FCCAnalyses::ReconstructedParticle::get_mass(bb_pairs)")

        )
        return dframe2

    # Mandatory: output function, please make sure you return the branch list
    # as a python list
    def output(self):
        '''
        Output variables which will be saved to output root file.
        '''
        branch_list = [
            'nbjets',
            # 'm_bb',
            'ngamma',
            'm_yy',
            # 'selected_muons_pt',
            # 'selected_muons_y',
            # 'selected_muons_p',
            # 'selected_muons_e',
            # 'zed_leptonic_pt',
            # 'zed_leptonic_m',
            # 'zed_leptonic_charge',
            # 'zed_leptonic_recoil_m'
        ]
        return branch_list
