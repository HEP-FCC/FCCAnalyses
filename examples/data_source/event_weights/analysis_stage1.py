'''Example: retrieve event weights from EDM4hep EventHeader.'''


import ROOT
# Mandatory: Analysis class where the user defines the operations on the
# dataframe.
class Analysis():
    ''' Retrieve per-event weights from the EDM4hep EventHeader:  the full weights vector, and one weight selected by name.  '''   
    def __init__(self, cmdline_args):
        # Mandatory: List of datasets used in the analysis
        # Note: currently using the first pp-hhh file since couldn't find metadata in 10000 event file
        self.process_list = {
            "/afs/cern.ch/user/z/zcabukog/event_weights_project/"
            "pp_hhh_84TeV_weights_5evt.edm4hep.root": {}
        }
   #'pp_hhh_84TeV_weights_5evt'


        # Mandatory: Production tag when running over the centrally produced
        # samples (this points to the yaml file for getting sample statistics)
        # self.prod_tag = 'FCCee/spring2021/IDEA/'
        # or Input directory when not running over the centrally produced
        # samples.
        self.input_dir = '/eos/experiment/fcc/hh/tutorials/' \
                         'edm4hep_tutorial_data/'

    

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
        self.test_file = (
            "/afs/cern.ch/user/z/zcabukog/event_weights_project/"
            "pp_hhh_84TeV_weights_5evt.edm4hep.root"
        )
    # Mandatory: analyzers function to define the analysis graph, please make
    # sure you return the dataframe
    def analyzers(self, dframe):
        #define creates a new column in the dataframe, and the first argument is the name of the new column, and the second argument is the function that will be used to create the new column. 
      
        dframe2 = dframe.Define(
            "event_weights",
            "GetAllWeights{}(EventHeader)"
        )

        # Create one GetWeightByName object and store the requested label.
        # The functor no longer receives or opens the input file.
        selected_weight_functor = ROOT.GetWeightByName("rwgt_4")

        # Create a new column containing the numerical value of rwgt_4
        # for each event.
        #
        # RDataFrame passes two columns into the functor:
        # EventHeader supplies the numerical event weights.
        # _EventWeightNames supplies the corresponding weight labels.
        dframe3 = dframe2.Define(
            "selected_weight",
            selected_weight_functor,
            ["EventHeader", "_EventWeightNames"]
        )

       # Return the dataframe containing both event_weights and selected_weight.
        return dframe3
        # Pass EventHeader into the GetAllWeights functor and store its returned weights in a new column called event_weights.



    # Mandatory: output function, please make sure you return the branch list
    # as a python list
    def output(self):
         return ["event_weights", "selected_weight"]
        
