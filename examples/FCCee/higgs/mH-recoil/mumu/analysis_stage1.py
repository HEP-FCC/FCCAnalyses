'''
Analysis example, measure Higgs mass in the Z(mumu)H recoil measurement.
'''
from argparse import ArgumentParser


# Mandatory: Analysis class where the user defines the dataframe operations
class Analysis():
    '''
    Higgs mass recoil analysis in Z(mumu)H.
    '''
    def __init__(self, cmdline_args):
        parser = ArgumentParser(
            description='Additional analysis arguments',
            usage='Provide additional arguments after analysis script path')
        parser.add_argument('--mva', default="", type=str,
                            help='Path to the trained MVA ROOT file.')
        self.args = parser.parse_args(cmdline_args)

        # Mandatory: List of processes to run over
        self.process_list = {
            # Run the full statistics in one output file named
            # <outputDir>/p8_ee_ZZ_ecm240.root
            'p8_ee_ZZ_ecm240': {'fraction': 0.005},
            # Run 50% of the statistics with output into two files named
            # <outputDir>/p8_ee_WW_ecm240/chunk<N>.root
            'p8_ee_WW_ecm240': {'fraction': 0.5, 'chunks': 2},
            # Run 20% of the statistics in one file named
            # <outputDir>/p8_ee_ZH_ecm240_out.root (example on how to change
            # the output name)
            'p8_ee_ZH_ecm240': {'fraction': 0.2,
                                'output': 'p8_ee_ZH_ecm240_out'}
        }

        # Mandatory: Production tag when running over centrally produced
        # samples, this points to the yaml files for getting sample statistics
        self.prod_tag = 'FCCee/spring2021/IDEA/'

        # Optional: output directory, default is local running directory
        self.output_dir = 'outputs/FCCee/higgs/mH-recoil/mumu/stage1'

        # Optional: analysisName, default is ""
        # self.analysis_name = "My Analysis"

        # Optional: ncpus, default is 4
        self.n_threads = 8

        # Optional running on HTCondor, default is False
        # runBatch    = False

        # Optional: batch queue name when running on HTCondor, default is
        # "workday"
        # batchQueue = "longlunch"

        # Optional: computing account when running on CERN's HTCondor, default
        # is "group_u_FCC.local_gen"
        # compGroup = 'group_u_FCC.local_gen'

        # Optional test file
        self.test_file = 'root://eospublic.cern.ch//eos/experiment/fcc/ee/' \
                         'generation/DelphesEvents/spring2021/IDEA/' \
                         'p8_ee_ZH_ecm240/events_101027117.root'

    # Mandatory: analyzers function to define the analysis graph, please make
    # sure you return the dataframe, in this example it is dframe2
    def analyzers(self, dframe):
        '''
        Analysis graph.
        '''
        dframe2 = (
            dframe
            # define an alias for muon index collection
            .Alias("Muon0", "Muon#0.index")
            # define the muon collection
            .Define(
                "muons",
                "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
            # select muons on pT
            .Define("selected_muons",
                    "ReconstructedParticle::sel_pt(10.)(muons)")
            # create branch with muon transverse momentum
            .Define("selected_muons_pt",
                    "ReconstructedParticle::get_pt(selected_muons)")
            # create branch with muon rapidity
            .Define("selected_muons_y",
                    "ReconstructedParticle::get_y(selected_muons)")
            # create branch with muon total momentum
            .Define("selected_muons_p",
                    "ReconstructedParticle::get_p(selected_muons)")
            # create branch with muon energy
            .Define("selected_muons_e",
                    "ReconstructedParticle::get_e(selected_muons)")
            # find zed candidates from  di-muon resonances
            .Define(
                "zed_leptonic",
                "ReconstructedParticle::resonanceBuilder(91)(selected_muons)")
            # create branch with zed mass
            .Define("zed_leptonic_m",
                    "ReconstructedParticle::get_mass(zed_leptonic)")
            # create branch with zed transverse momenta
            .Define("zed_leptonic_pt",
                    "ReconstructedParticle::get_pt(zed_leptonic)")
            # calculate recoil of zed_leptonic
            .Define("zed_leptonic_recoil",
                    "ReconstructedParticle::recoilBuilder(240)(zed_leptonic)")
            # create branch with recoil mass
            .Define("zed_leptonic_recoil_m",
                    "ReconstructedParticle::get_mass(zed_leptonic_recoil)")
            # create branch with leptonic charge
            .Define("zed_leptonic_charge",
                    "ReconstructedParticle::get_charge(zed_leptonic)")
            # Filter at least one candidate
            .Filter("zed_leptonic_recoil_m.size()>0")
        )
        return dframe2

    # Mandatory: output function, please make sure you return the branch_list
    # as a python list
    def output(self):
        '''
        Output variables which will be saved to output root file.
        '''
        branch_list = [
            "selected_muons_pt",
            "selected_muons_y",
            "selected_muons_p",
            "selected_muons_e",
            "zed_leptonic_pt",
            "zed_leptonic_m",
            "zed_leptonic_charge",
            "zed_leptonic_recoil_m"
        ]
        return branch_list
