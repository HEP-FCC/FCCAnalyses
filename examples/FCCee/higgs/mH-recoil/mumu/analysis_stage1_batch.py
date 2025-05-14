'''
Analysis example, measure Higgs mass in the Z(mumu)H recoil measurement.
This analysis stage runs on HTCondor.
'''
from argparse import ArgumentParser


# Mandatory: Analysis class where the user defines the operations on the
# dataframe.
class Analysis():
    '''
    Higgs mass recoil analysis in Z(mumu)H.
    '''
    def __init__(self, cmdline_args):
        # Parse additional arguments not known to the FCCAnalyses parsers.
        # All command line arguments are provided in the `cmdline_arg`
        # dictionary and arguments after "--" are stored under "remaining" key.
        parser = ArgumentParser(
            description='Additional analysis arguments',
            usage='Provided after "--"')
        parser.add_argument('--muon-pt', default='10.', type=float,
                            help='Minimal pT of the mouns.')
        self.ana_args, _ = parser.parse_known_args(cmdline_args['remaining'])

        # Mandatory: List of datasets used in the analysis
        self.process_list = {
            # Run over the full statistics in 20 jobs per dataset and save the
            # output into <outputDir>/p8_ee_??_ecm240/chunk<N>.root
            'p8_ee_ZZ_ecm240': {'chunks': 20},
            'p8_ee_WW_ecm240': {'chunks': 20},
            'p8_ee_ZH_ecm240': {'chunks': 20}
        }

        # Mandatory: Production tag when running over the centrally produced
        # datasets (this points to a yaml file from which the sample )
        self.prod_tag = 'FCCee/spring2021/IDEA/'

        # Optional: output directory, default is local running directory
        self.output_dir = f'ZH_mumu_recoil_batch/stage1_{self.ana_args.muon_pt}'

        # Optional: analysis name, default is ''
        # self.analysis_name = 'My Analysis'

        # Optional: number of threads to run on, default is 'all available'
        self.n_threads = 4

        # Optional: batch queue name when running on HTCondor, default is
        # 'longlunch'
        self.batch_queue = 'espresso'

        # Optional: computing account when running on CERN's HTCondor, default
        # is 'group_u_FCC.local_gen'
        self.comp_group = 'group_u_FCC.local_gen'

        # Optional: output directory on eos, if specified files will be copied
        # there once the batch job is done, default is empty
        # self.output_dir_eos = '/eos/experiment/fcc/ee/analyses/case-studies/' \
        #                       f'higgs/mH-recoil/stage1_{self.ana_args.muon_pt}'
        self.output_dir_eos = '/eos/user/j/jsmiesko/FCCAnalyses/test-output'

        # Optional: type for eos, needed when <outputDirEos> is specified. The
        # default is FCC EOS, which is eospublic
        # self.eos_type = 'eospublic'

        # Optional: test file
        self.test_file = 'root://eospublic.cern.ch//eos/experiment/fcc/ee/' \
                         'generation/DelphesEvents/spring2021/IDEA/' \
                         'p8_ee_ZH_ecm240/events_101027117.root'

    # Mandatory: analyzers function to define the analysis graph, please make
    # sure you return the dataframe, in this example it is dframe2
    def analyzers(self, dframe):
        '''
        Analysis graph.
        '''

        muon_pt = self.ana_args.muon_pt

        dframe2 = (
            dframe
            # define an alias for muon index collection
            .Alias('Muon0', 'Muon#0.index')
            # define the muon collection
            .Define(
                'muons',
                'ReconstructedParticle::get(Muon0, ReconstructedParticles)')
            # select muons on pT
            .Define('selected_muons',
                    f'ReconstructedParticle::sel_pt({muon_pt})(muons)')
            # create column with muon transverse momentum
            .Define('selected_muons_pt',
                    'ReconstructedParticle::get_pt(selected_muons)')
            # create column with muon rapidity
            .Define('selected_muons_y',
                    'ReconstructedParticle::get_y(selected_muons)')
            # create column with muon total momentum
            .Define('selected_muons_p',
                    'ReconstructedParticle::get_p(selected_muons)')
            # create column with muon energy
            .Define('selected_muons_e',
                    'ReconstructedParticle::get_e(selected_muons)')
            # find zed candidates from  di-muon resonances
            .Define(
                'zed_leptonic',
                'ReconstructedParticle::resonanceBuilder(91)(selected_muons)')
            # create column with zed mass
            .Define('zed_leptonic_m',
                    'ReconstructedParticle::get_mass(zed_leptonic)')
            # create column with zed transverse momenta
            .Define('zed_leptonic_pt',
                    'ReconstructedParticle::get_pt(zed_leptonic)')
            # calculate recoil of zed_leptonic
            .Define('zed_leptonic_recoil',
                    'ReconstructedParticle::recoilBuilder(240)(zed_leptonic)')
            # create column with recoil mass
            .Define('zed_leptonic_recoil_m',
                    'ReconstructedParticle::get_mass(zed_leptonic_recoil)')
            # create column with leptonic charge
            .Define('zed_leptonic_charge',
                    'ReconstructedParticle::get_charge(zed_leptonic)')
            # Keep events with at least one candidate
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
