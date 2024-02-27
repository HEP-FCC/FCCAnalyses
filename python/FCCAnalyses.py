'''@package FCCAnalyses
Provides FCCAnalysis facilities as a Python import.
'''

import os
import sys
import ROOT

class Analysis:
    '''
    The main class holding analysis settings
    '''
    def __init__(self, name, datasource='local_files'):
        self.name = name
        self.description = ''
        self.datasource = datasource
        if isinstance(datasource, int):
            self.n_events = datasource
            self.datasource = 'n_events'
        if datasource == 'local_files':
            self.local_files = []

        self.additional_analyzers = []

    def set_description(self, description):
        '''
        Set Analysis description.
        '''
        self.description = description

    def get_dataframe(self):
        '''
        Create and return ROOT RDataFrame
        '''
        print('----> INFO: Loading standard FCCAnalyses analyzers...')
        ROOT.gSystem.Load("libFCCAnalyses")
        ROOT.gInterpreter.Declare("using namespace FCCAnalyses;")
        ROOT.dummyLoader()

        print('----> INFO: Loading additional analyzers from:')
        for path in self.additional_analyzers:
            print('       -', path)

        for path in self.additional_analyzers:
            ROOT.gInterpreter.Declare(f'#include "{path}"')

        if self.datasource == 'local_files':
            if not self.local_files:
                print('----> ERROR: No input files provided. Aborting...')
                sys.exit(3)
            print('----> INFO: Analysis will run over the following input '
                  'files:')
            for path in self.local_files:
                print('       -', path)

            dframe = ROOT.RDataFrame('events', self.local_files)

        elif self.datasource == 'n_events':
            print('----> INFO: Creating clear ROOT RDataFrame from '
                  f'{self.n_events} events')
            dframe = ROOT.RDataFrame(self.n_events)

        return dframe

    def add_files(self, infile_paths):
        '''
        Adds file paths of local input files
        '''
        if isinstance(infile_paths, str):
            infile_paths = [infile_paths]
        if isinstance(infile_paths, list):
            for path in infile_paths:
                if os.path.exists(path):
                    self.local_files.append(os.path.abspath(path))
                else:
                    print('----> ERROR: Input file not found!')
                    print('             ' + os.path.abspath(path))
                    sys.exit(3)
        else:
            print('----> ERROR: Input files object is not a string nor a list')
            sys.exit(3)

    def add_analyzers(self, add_analyzers_paths):
        '''
        Loads additional analyzers to the ROOT gInterpreter.
        The analyzers are JITed every time the analysis is run.

        Accepts either string or list of string.
        '''
        if isinstance(add_analyzers_paths, str):
            add_analyzers_paths = [add_analyzers_paths]
        if isinstance(add_analyzers_paths, list):
            for path in add_analyzers_paths:
                if os.path.exists(path):
                    self.additional_analyzers.append(os.path.abspath(path))
                else:
                    print('----> ERROR: File with additional analyzers not '
                          'found!')
                    print('             ' + os.path.abspath(path))
                    sys.exit(3)
        else:
            print('----> ERROR: Additional analyzer object is not a string nor '
                  'a list')
            sys.exit(3)
