'''
Analysis example using PODIO ROOT DataSource for reading input files.
'''

from string import Template


class Analysis():
    '''
    Mandatory class, with three mandatory methods:
      * __init__
      * analyzers
      * output
    '''
    def __init__(self, _):
        # list of processes (mandatory)
        self.process_list = {
            'p8_ee_WW_ecm240': {'output': 'p8_ee_WW_ecm240_out'}
        }

        # Production tag when running over EDM4Hep centrally produced events,
        # this points to the yaml files for getting sample statistics
        # (mandatory)
        self.prod_tag = 'FCCee/winter2023/IDEA/'

        # Optional: output directory, default is local running directory
        self.output_dir = "stages-source-output"

        # Ncpus, default is 4, -1 uses all cores available
        # self.n_threads = -1

        # How to read input files
        self.use_data_source = True

        # Optional test file
        self.test_file = Template(
            'https://fccsw.web.cern.ch/fccsw/analysis/test-samples/edm4hep099/'
            '$key4hep_os/$key4hep_stack/p8_ee_WW_ecm240_edm4hep.root'
        )

    def analyzers(self, dframe):
        '''
        Analysis function to define the analyzers to process, please make sure
        you return the last dataframe, in this example it is dframe2
        '''
        dframe2 = (
            dframe
            .Define(
              "electron_truth",
              "ReconstructedParticle::selPDG(11)(RecoMCLink)")

            .Define(
              "electron_truth_pt",
              "ReconstructedParticle::getPt(electron_truth)")
        )

        return dframe2

    def output(self) -> list[str]:
        '''
        List of columns to cave into output file.
        '''
        return [
                # "electron_truth",
                "electron_truth_pt"
        ]
