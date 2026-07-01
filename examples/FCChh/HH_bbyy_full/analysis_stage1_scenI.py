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
            'pwp8_pp_hh_lambda100_5f_hhbbaa': {'chunks':200},
            'pwp8_pp_hh_lambda240_5f_hhbbaa': {'chunks':200},
            'pwp8_pp_hh_lambda300_5f_hhbbaa': {'chunks':200},
            'pwp8_pp_hh_lambda000_5f_hhbbaa': {'chunks':200},
            #single Higgs bkgs
            'mgp8_pp_h012j_5f_haa': {'chunks':100},
            'mgp8_pp_vbf_h01j_5f_haa': {'chunks':100},
            'mgp8_pp_tth01j_5f_haa': {'chunks':200},
            'mgp8_pp_vh012j_5f_haa': {'chunks':100},
            #yy+jets continuum bkg
            'mgp8_pp_jjaa_5f': {'chunks':250},

        }

        # Mandatory: Input directory where to find the samples, or a production tag when running over the centrally produced
        # samples (this points to the yaml files for getting sample statistics)
        self.input_dir = '/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v07/I/'

        # Optional: output directory, default is local running directory
        self.output_dir = '/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/I/'

        # Optional: analysisName, default is ''
        self.analysis_name = 'FCC-hh bbyy analysis, with Delphes scenario I'

        # Optional: number of threads to run on, default is 'all available'
        # self.n_threads = 4

        # Optional: running on HTCondor, default is False
        self.run_batch = True

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

            ########################################### JETS ########################################### 

            # jets after overlap removal is performed between jets and isolated electrons, muons and photons

            #selected jets above a pT threshold of 30 GeV, eta < 4, tight ID 
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

            ########################################### ELECTRONS ########################################### 

            #all isolated 
            .Define("ele",  "FCCAnalyses::ReconstructedParticle::get(Electron_objIdx.index, ReconstructedParticles)")
            .Define("selpt_ele", "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(ele)")
            .Define("sel_ele_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_ele)")
            .Define("sel_ele", "AnalysisFCChh::SortParticleCollection(sel_ele_unsort)")
            .Define("nele",  "FCCAnalyses::ReconstructedParticle::get_n(sel_ele)")
            .Define("e1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_ele)[0]")
            .Define("e1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_ele)[0]")
            .Define("e1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_ele)[0]")
            .Define("e1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_ele)[0]")
            .Define("e2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_ele)[1]")
            .Define("e2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_ele)[1]")
            .Define("e2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_ele)[1]")
            .Define("e2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_ele)[1]")

            ########################################### MUONS ########################################### 

            # all isolated
            .Define("mu",  "FCCAnalyses::ReconstructedParticle::get(Muon_objIdx.index, ReconstructedParticles)")
            .Define("selpt_mu", "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(mu)")
            .Define("sel_mu_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_mu)")
            .Define("sel_mu", "AnalysisFCChh::SortParticleCollection(sel_mu_unsort)") 
            .Define("nmu",  "FCCAnalyses::ReconstructedParticle::get_n(sel_mu)")
            .Define("m1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_mu)[0]")
            .Define("m1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_mu)[0]")
            .Define("m1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_mu)[0]")
            .Define("m1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_mu)[0]")
            .Define("m2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_mu)[1]")
            .Define("m2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_mu)[1]")
            .Define("m2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_mu)[1]")
            .Define("m2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_mu)[1]")



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

            ########################################### EVENT WIDE KINEMATIC VARIABLES########################################### 

            #H(bb) system - using the loose WP b-jets -> if the events has < 2 bjets these variables do not get filled!
            .Define("bb_pairs_unmerged", "AnalysisFCChh::getPairs(sel_bjets)") #currently gets only leading pT pair, as a RecoParticlePair
            #then merge the bb pair into one object and get its kinematic properties
            .Define("bb_pairs", "AnalysisFCChh::merge_pairs(bb_pairs_unmerged)") #merge into one object to access inv masses etc
            .Define("m_bb", "FCCAnalyses::ReconstructedParticle::get_mass(bb_pairs)")


            #H(yy) if it exists, if there are no 2 selected photons, doesnt get filled 
            .Define("yy_pairs_unmerged", "AnalysisFCChh::getPairs(sel_gamma)")
            .Define("yy_pairs", "AnalysisFCChh::merge_pairs(yy_pairs_unmerged)")
            .Define("m_yy", "FCCAnalyses::ReconstructedParticle::get_mass(yy_pairs)")

            # Filter at least one candidate
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
                        "weight",
                        # Jets:             
                        "njets", "j1_e", "j1_pt", "j1_eta", "j1_phi",
                        "j2_e", "j2_pt", "j2_eta", "j2_phi",
                        # B-jets:
                        "nbjets", "b1_e", "b1_pt", "b1_eta","b1_phi",
                        "b2_e", "b2_pt", "b2_eta","b2_phi",
                        # Electrons:
                        "nele", "e1_e", "e1_pt", "e1_eta", "e1_phi",
                        "e2_e", "e2_pt", "e2_eta", "e2_phi",
                        # Muons:
                        "nmu", "m1_e", "m1_pt", "m1_eta", "m1_phi",
                        "m2_e", "m2_pt", "m2_eta", "m2_phi",             
                        # Photons:
                        "ngamma", "g1_e", "g1_pt", "g1_eta", "g1_phi",
                        "g2_e", "g2_pt", "g2_eta", "g2_phi",
                        # Hbb decay:
                        "m_bb", 
                        #Hyy decay:
                        "m_yy"     
        ]
        return branch_list