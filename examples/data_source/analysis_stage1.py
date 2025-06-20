'''
Analysis example, measure Higgs mass in the Z(mumu)H recoil measurement.
'''
from argparse import ArgumentParser
from string import Template


# Mandatory: Analysis class where the user defines the operations on the
# dataframe.
class Analysis():
    '''
    Higgs mass recoil analysis in Z(mumu)H.
    '''
    def __init__(self, cmdline_args):
        parser = ArgumentParser(
            description='Additional analysis arguments',
            usage='Provide additional arguments after analysis script path')
        parser.add_argument('--muon-pt', default='10.', type=float,
                            help='Minimal pT of the mouns.')
        # Parse additional arguments not known to the FCCAnalyses parsers
        # All command line arguments know to fccanalysis are provided in the
        # `cmdline_arg` dictionary.
        self.ana_args, _ = parser.parse_known_args(cmdline_args['remaining'])

        # Mandatory: List of samples (processes) used in the analysis
        self.process_list = {
            # Run over the full statistics and save it to one output file named
            # <outputDir>/<process_name>.root
            'p8_ee_ZZ_ecm240': {'fraction': 1.},
            # Run over 50% of the statistics and save output into two files
            # named <outputDir>/p8_ee_WW_ecm240/chunk<N>.root
            # Number of input files needs to be larger that number of chunks
            'p8_ee_WW_ecm240': {'fraction': 0.5, 'chunks': 2},
            # Run over 20% of the statistics and save output into one file
            # named <outputDir>/p8_ee_ZH_ecm240_out_f02.root
            'p8_ee_ZH_ecm240': {'fraction': 0.2,
                                'output': 'p8_ee_ZH_ecm240_out_f02'}
        }

        # Mandatory: Production tag when running over the centrally produced
        # samples (this points to the yaml file for getting sample statistics)
        # self.prod_tag = 'FCCee/spring2021/IDEA/'
        # or Input directory when not running over the centrally produced
        # samples.
        self.input_dir = '/eos/experiment/fcc/hh/tutorials/' \
                         'edm4hep_tutorial_data/'

        # Optional: output directory, default is local running directory
        self.output_dir = 'outputs/FCCee/higgs/mH-recoil/mumu/' \
                          f'stage1_{self.ana_args.muon_pt}'

        # Optional: analysis name, default is ''
        # self.analysis_name = 'My Analysis'

        # Optional: number of threads to run on, default is 'all available'
        # self.n_threads = 4

        # Optional: running on HTCondor, default is False
        # self.run_batch = False

        # Optional: test file
        self.test_file = Template(
            'https://fccsw.web.cern.ch/fccsw/analysis/test-samples/edm4hep099/'
            '$key4hep_os/$key4hep_stack/p8_ee_WW_ecm240_edm4hep.root'
        )

        # Optional: read the input files with podio::DataSource
        self.use_data_source = True

    # Mandatory: analyzers function to define the analysis graph, please make
    # sure you return the dataframe, in this example it is dframe2
    def analyzers(self, dframe):
        '''
        Analysis graph.
        '''

        muon_pt = self.ana_args.muon_pt

        dframe2 = (
            dframe
            # select muons on pT
            .Define('selected_muons',
                    f'ReconstructedParticle::selPt({muon_pt})(Muon)')
            # create column with muon transverse momentum
            .Define('selected_muons_pt',
                    'ReconstructedParticle::getPt(selected_muons)')
            # create column with muon rapidity
            .Define('selected_muons_y',
                    'ReconstructedParticle::getY(selected_muons)')
            # create column with muon total momentum
            .Define('selected_muons_p',
                    'ReconstructedParticle::getP(selected_muons)')
            # create column with muon energy
            .Define('selected_muons_e',
                    'ReconstructedParticle::getE(selected_muons)')
            # find zed candidates from  di-muon resonances
            .Define(
                'zed_leptonic',
                'ReconstructedParticle::resonanceBuilder(91)(selected_muons)')
            # create column with zed mass
            .Define('zed_leptonic_m',
                    'ReconstructedParticle::getMass(zed_leptonic)')
            # create column with zed transverse momenta
            .Define('zed_leptonic_pt',
                    'ReconstructedParticle::getPt(zed_leptonic)')
            # calculate recoil of zed_leptonic
            .Define('zed_leptonic_recoil',
                    'ReconstructedParticle::recoilBuilder(240)(zed_leptonic)')
            # create column with recoil mass
            .Define('zed_leptonic_recoil_m',
                    'ReconstructedParticle::getMass(zed_leptonic_recoil)')
            # create column with leptonic charge
            .Define('zed_leptonic_charge',
                    'ReconstructedParticle::getCharge(zed_leptonic)')
            # Filter on at least one candidate
            .Filter('zed_leptonic_recoil_m.size() > 0')
        )

        return dframe2

    # Mandatory: output function, please make sure you return the branch list
    # as a python list
    def output(self):
        '''
        Output variables which will be saved to output root file.
        '''
        branch_list = [
            'selected_muons_pt',
            'selected_muons_y',
            'selected_muons_p',
            'selected_muons_e',
            'zed_leptonic_pt',
            'zed_leptonic_m',
            'zed_leptonic_charge',
            'zed_leptonic_recoil_m'
        ]
        return branch_list
