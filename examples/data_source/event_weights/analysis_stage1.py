'''
Analysis example, measure Higgs mass in the Z(mumu)H recoil measurement.
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

        #podio
        #line below tells FCCAnalyses to read the ROOT file using podio::DataSource instead of reading the raw ROOT branches directly
        #so that event header isn't split like: EventHeader
        #                                       EventHeader.weights_begin
        #                                       EventHeader.weights_end
        #                                       EventHeader_weights
        # With it enabled, podio reconstructs those pieces into a EDM4hep collection
        #use_data_source=False → raw split ROOT data; use_data_source=True →podio reconstructs them into edm4hep::EventHeaderCollection.
        self.use_data_source = True












        # Optional: analysis name, default is ''
        # self.analysis_name = 'My Analysis'

        # Optional: number of threads to run on, default is 1
        # self.n_threads = 4

        # Optional: providing additional analyzers
        # self.include_paths = ['additional_analyzers.h']
        self.include_paths = ["Definitions.h"]

        # Optional: test file
        self.test_file = '/afs/cern.ch/user/z/zcabukog/event_weights_project/pp_hhh_84TeV_weights_5evt.edm4hep.root'

    # Mandatory: analyzers function to define the analysis graph, please make
    # sure you return the dataframe, in this example it is dframe2
    def analyzers(self, dframe):
        #define creates a new column in the dataframe, and the first argument is the name of the new column, and the second argument is the function that will be used to create the new column. 
        dframe2 = dframe.Define(
            "event_weights",
            "GetAllWeights{}(EventHeader)"
        )

        return dframe2
        # Pass EventHeader into the GetAllWeights functor and store its returned weights in a new column called event_weights.



    # Mandatory: output function, please make sure you return the branch list
    # as a python list
    def output(self):
        return ["event_weights"]
