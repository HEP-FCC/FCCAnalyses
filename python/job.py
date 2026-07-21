'''
Run analysis of style "Analysis", which can be split into several stages.
'''

import sys
import time
import logging
import traceback
from threading import Thread
from queue import Queue
from typing import Optional, Union
from collections.abc import Callable

import ROOT  # type: ignore
import cppyy  # type: ignore
from sample import get_one_file_quantities
from utils import generate_graph


ROOT.gROOT.SetBatch(True)

LOGGER = logging.getLogger('FCCAnalyses.job')


# _____________________________________________________________________________
class Job:
    '''
    One unit of work, producing one ROOT file.
    '''
    def __init__(self,
                 input_file_list: list[str],
                 analysis_chain: Callable,
                 use_data_source: bool = False):
        '''
        Initialize all required parameters.
        '''
        # Event counts
        self._evtcount: dict[str, Union[int, float, None]] = {}
        self._evtcount['raw-orig'] = None
        self._evtcount['sow-orig'] = None
        self._evtcount['raw-ttree'] = None
        self._evtcount['raw-init'] = None
        self._evtcount['sow-init'] = None
        self._evtcount['raw-restricted'] = None
        self._evtcount['sow-restricted'] = None
        self._evtcount['raw-final'] = None
        self._evtcount['sow-final'] = None

        # Creates self._input_file_list: list[str]
        self._setup_input(input_file_list)

        # Creates: self._init_dframe: ROOT.RDataFrame
        #          self._restricted_dframe: ROOT.RDataFrame
        self._setup_dframe(use_data_source)

        # Setup analysis chain
        self._analysis_chain: Callable = analysis_chain

        # Output of the job
        self._output_file_path: Optional[str] = None
        self._output_variables: Optional[list[str]] = None

        # Benchmark
        self._elapsed_time: Optional[float] = None

    def _setup_input(self,
                     infile_list: list[str]) -> None:
        '''
        Define input files and check event counts.
        '''
        self._input_file_list: list[str] = []

        if len(infile_list) == 1:
            info_msg = 'RDataFrame will be created from one file:\n'
        else:
            info_msg = 'RDataFrame will be created from ' \
                       f'{len(infile_list)} files:\n'

        threads = []
        results: Queue = Queue()
        for filepath in infile_list:
            self._input_file_list.append(filepath)

            info_msg += f'  - {filepath}\n'

            thread = Thread(target=get_one_file_quantities,
                            args=(filepath, results))
            threads.append(thread)

        if not self._input_file_list:
            LOGGER.error('No suitable input files provided!')
            sys.exit(3)

        LOGGER.info(info_msg.rstrip())

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        evtcount_raw_orig = 0
        evtcount_sow_orig = 0
        evtcount_raw_ttree = 0
        for result in results.queue:
            if result['events-processed'] is not None:
                evtcount_raw_orig += result['events-processed']
            if result['sow-processed'] is not None:
                evtcount_sow_orig += result['sow-processed']
            if result['events-in-ttree'] is not None:
                evtcount_raw_ttree += result['events-in-ttree']
        if evtcount_raw_orig != 0:
            self._evtcount['raw-orig'] = evtcount_raw_orig
        if evtcount_sow_orig != 0:
            self._evtcount['sow-orig'] = evtcount_sow_orig
        if evtcount_raw_ttree != 0:
            self._evtcount['raw-ttree'] = evtcount_raw_ttree

    def _setup_dframe(self, use_data_source: bool = False) -> None:
        '''
        Create initial dataframe.
        '''
        if use_data_source:
            if ROOT.podio.DataSource:
                LOGGER.debug('Found podio::DataSource...')
            else:
                LOGGER.error('podio::DataSource library not '
                             'found!\nAborting...')
                sys.exit(3)
            LOGGER.info('Loading events through podio::DataSource...')

            try:
                self._init_dframe = \
                    ROOT.podio.CreateDataFrame(self._input_file_list)
            except TypeError as excp:
                LOGGER.error('Unable to build dataframe using '
                             'podio::DataSource!\n%s', excp)
                sys.exit(3)
        else:
            LOGGER.info('Letting RDataFrame to load events directly from the '
                        'ROOT file(s)...')
            self._init_dframe = ROOT.RDataFrame("events",
                                                self._input_file_list)

        # In case there will be no restriction on events this will be identical
        self._restricted_dframe = self._init_dframe

    def setup_output(self,
                     output_filepath: str,
                     output_variables: Callable[[], list[str]],
                     output_format: str = 'ttree') -> None:
        '''
        Setup output of this work unit, output variables and output file path.
        '''
        self._output_file_path = output_filepath

        self._output_format: str = output_format

        self._output_variables = output_variables()

        if not self._output_variables:
            LOGGER.error('No output variables provided!')
            sys.exit(3)

        info_msg = 'Expect output of the job in:\n'
        info_msg += f' - {self._output_file_path}\n'
        info_msg += 'with the following output variables:\n'
        for variable in self._output_variables:
            info_msg += f' - {variable}\n'
        LOGGER.info(info_msg.rstrip())

    def enable_progress_bar(self) -> None:
        """
        Enable ROOT's progress bar.
        """
        ROOT.RDF.Experimental.AddProgressBar(self._init_dframe)

    def restrict_events(self,
                        n_events_max: Optional[int] = None,
                        stride: Optional[int] = None) -> None:
        '''
        Set number of events to run on or how many events to stride.
        '''
        if stride is not None:
            if stride > 3:
                LOGGER.info('Will process only every %ith event...', stride)
            elif stride == 3:
                LOGGER.info('Will process only every 3rd event...')
            elif stride == 2:
                LOGGER.info('Will process only every 2nd event...')
            # pylint: disable=attribute-defined-outside-init
            self._restricted_dframe = self._restricted_dframe.Filter(
                f'FCCAnalyses::EventFilter::stride({stride})(rdfentry_)'
            )

        if n_events_max is not None:
            LOGGER.info('Will try to process up to %i events...',
                        n_events_max)
            # pylint: disable=attribute-defined-outside-init
            self._restricted_dframe = self._restricted_dframe.Filter(
                f'FCCAnalyses::EventFilter::nEvents({n_events_max})()'
            )

    def run(self) -> None:
        '''
        Run the data frame and snapshot it.
        '''

        evtcount_raw_init = self._init_dframe.Count()
        try:
            evtcount_sow_init = self._init_dframe.Sum("EventHeader.weight")
        except cppyy.gbl.std.runtime_error:
            LOGGER.warning('The provided input file does not contain event '
                           'weight information.')
            evtcount_sow_init = evtcount_raw_init
        evtcount_raw_restricted = self._restricted_dframe.Count()
        try:
            evtcount_sow_restricted = \
                self._restricted_dframe.Sum("EventHeader.weight")
        except cppyy.gbl.std.runtime_error:
            evtcount_sow_restricted = evtcount_raw_restricted

        try:
            LOGGER.debug('Defining the analysis chain...')
            final_dframe = self._analysis_chain(self._restricted_dframe)
            LOGGER.debug('Finished defining the analysis chain...')
        except (NameError, AttributeError, TypeError, KeyError) as err:
            tb_list = traceback.extract_tb(sys.exc_info()[2])
            line_number = tb_list[-1][1]
            LOGGER.error('A problem encountered in the definition of the '
                         'analysis chain:\n - error message: %s\n - line '
                         'number: %i',
                         err, line_number)
            sys.exit(3)
        except cppyy.gbl.std.runtime_error as err:
            tb_list = traceback.extract_tb(sys.exc_info()[2])
            line_number = tb_list[-2][1]
            LOGGER.error('A problem encountered in the definition of the '
                         'analysis chain:\n - error message:\n%s\n\n - line '
                         'number: %i',
                         err, line_number)
            sys.exit(3)

        evtcount_raw_final = final_dframe.Count()
        try:
            evtcount_sow_final = final_dframe.Sum("EventHeader.weight")
        except cppyy.gbl.std.runtime_error:
            evtcount_sow_final = evtcount_raw_final

        start_time = time.time()
        try:
            LOGGER.info('Snapshoting...')
            options = ROOT.RDF.RSnapshotOptions()
            if self._output_format == 'rntuple':
                options.fOutputFormat = ROOT.RDF.ESnapshotOutputFormat.kRNTuple

            final_dframe.Snapshot(
                "events",
                self._output_file_path,
                self._output_variables,
                options
            )
            LOGGER.info('Finished snapshoting...')
        except TypeError as err:
            LOGGER.error('A problem encountered during the execution of the '
                         'analysis chain:\n - error message:\n%s\n',
                         err)
            sys.exit(3)

        self._elapsed_time = time.time() - start_time

        self._evtcount['raw-init'] = evtcount_raw_init.GetValue()
        self._evtcount['sow-init'] = float(evtcount_sow_init.GetValue())
        self._evtcount['raw-restricted'] = evtcount_raw_restricted.GetValue()
        self._evtcount['sow-restricted'] = \
            float(evtcount_sow_restricted.GetValue())
        self._evtcount['raw-final'] = evtcount_raw_final.GetValue()
        self._evtcount['sow-final'] = float(evtcount_sow_final.GetValue())

        info_msg = self._get_run_info()
        LOGGER.info(info_msg)

    def _get_run_info(self) -> str:
        '''
        Print all run info.
        '''
        # Check if the running was successful
        if self._elapsed_time is None:
            LOGGER.error('No elapsed time recorded!\nAborting...')
            sys.exit(3)

        if not isinstance(self._evtcount['raw-restricted'], int):
            LOGGER.error('Event count of the restricted dataframe not '
                         'recorded!\nAborting...')
            sys.exit(3)

        if not isinstance(self._evtcount['sow-restricted'], float):
            LOGGER.error('Sum of weights of the restricted dataframe not '
                         'recorded!\nAborting...')
            sys.exit(3)

        if not isinstance(self._evtcount['raw-final'], int):
            LOGGER.error('Event count of the final dataframe not '
                         'recorded!\nAborting...')
            sys.exit(3)

        if not isinstance(self._evtcount['sow-final'], float):
            LOGGER.error('Sum of weights of the final dataframe not '
                         'recorded!\nAborting...')
            sys.exit(3)

        info_msg = f"{' SUMMARY ':=^80}\n"
        info_msg += 'Elapsed time (HH:MM:SS):                 '
        info_msg += time.strftime('%H:%M:%S', time.gmtime(self._elapsed_time))

        n_events_per_second = self._evtcount['raw-restricted'] / \
            self._elapsed_time

        info_msg += '\nNumber of events processed:              ' \
                    f'{self._evtcount["raw-restricted"]:,}'
        info_msg += '\nEvents processed per second:             ' \
                    f'{n_events_per_second:0,.4g}'
        if self._evtcount['raw-restricted'] != \
                int(self._evtcount['sow-restricted']):
            sow_per_second = self._evtcount['sow-restricted'] / \
                             self._elapsed_time
            info_msg += '\nSum of weights processed:                ' \
                        f'{self._evtcount["sow-restricted"]:0,.2g}'
            info_msg += '\nSum of weights processed per second:     ' \
                        f'{sow_per_second:0,.4g}'

        # If there is filtering happening
        if self._evtcount['raw-restricted'] != self._evtcount['raw-final']:
            local_n_events_factor = self._evtcount['raw-final'] / \
                                    self._evtcount['raw-restricted']
            info_msg += '\nNumber of result events:                 ' \
                        f'{self._evtcount["raw-final"]:,}'
            info_msg += '\nLocal number of events reduction factor: ' \
                        f'{local_n_events_factor:0,.4g}'
        if self._evtcount['raw-restricted'] != \
                int(self._evtcount['sow-restricted']) and \
                self._evtcount['sow-restricted'] != \
                self._evtcount['sow-final']:
            local_sow_factor = self._evtcount['sow-final'] / \
                               self._evtcount['sow-restricted']
            info_msg += '\nResulting sum of weights:                ' \
                        f'{self._evtcount["sow-final"]:0,.2g}'
            info_msg += '\nLocal sum of weights reduction factor:   ' \
                        f'{local_sow_factor:0,.4g}'

        # If there is a restriction on initial events
        if self._evtcount['raw-init'] != self._evtcount['raw-restricted']:
            info_msg += '\nNumber of events available locally:      ' \
                    f'{self._evtcount["raw-init"]:,}'
        if self._evtcount['raw-restricted'] != \
                int(self._evtcount['sow-restricted']) and \
                self._evtcount['sow-init'] != \
                self._evtcount['sow-restricted']:
            info_msg += '\nSum of weights available locally:        ' \
                    f'{self._evtcount["sow-init"]:0,.2g}'

        # It the current processing is part of a chain
        if self._evtcount['raw-orig'] is not None:
            total_n_events_factor = self._evtcount['raw-final'] / \
                                    self._evtcount['raw-orig']
            info_msg += '\nTotal number of events available:        ' \
                        f'{self._evtcount["raw-orig"]:,}'
            info_msg += '\nTotal reduction factor:                  ' \
                        f'{total_n_events_factor:0,.4g}'
        if self._evtcount['sow-orig'] is not None:
            total_sow_factor = self._evtcount['raw-final'] / \
                               self._evtcount['sow-orig']
            info_msg += '\nTotal sum of weights available:          ' \
                        f'{self._evtcount["sow-orig"]:0,.2g}'
            info_msg += '\nTotal reduction factor:                  ' \
                        f'{total_sow_factor:0,.4g}'

        info_msg += '\n'
        info_msg += 80 * '='
        info_msg += '\n'

        return info_msg

    def finalize(self) -> None:
        '''
        Finalize the running of the dataframe.
        '''

        # Update resulting root file
        with ROOT.TFile(self._output_file_path, 'UPDATE') as outfile:
            # Original number of events / sum of weights
            if self._evtcount['raw-orig'] is not None:
                param = ROOT.TParameter(int)('eventsProcessed',
                                             self._evtcount['raw-orig'])
            else:
                param = ROOT.TParameter(int)('eventsProcessed',
                                             self._evtcount['raw-restricted'])
            param.Write()
            if self._evtcount['sow-orig'] is not None:
                param = ROOT.TParameter(float)('SumOfWeights',
                                               self._evtcount['sow-orig'])
            else:
                param = ROOT.TParameter(float)(
                    'SumOfWeights',
                    self._evtcount['sow-restricted']
                )
            param.Write()

            # Resulting number of events
            param = ROOT.TParameter(int)('eventsSelected',
                                         self._evtcount['raw-final'])
            param.Write()
            param = ROOT.TParameter(float)('SumOfWeightsSelected',
                                           self._evtcount['sow-final'])
            param.Write()

            # FCCAnalyses metadata directory
            fccana_dir = outfile.mkdir('fccana')
            fccana_dir.cd()

            # Processed with
            string = ROOT.TNamed('processed-with', 'FCCAnalyses')
            string.Write()

            # Original number of events / sum of weights
            if self._evtcount['raw-orig'] is not None:
                param = ROOT.TParameter(int)('n-events-original',
                                             self._evtcount['raw-orig'])
                param.Write()
            if self._evtcount['sow-orig'] is not None:
                param = ROOT.TParameter(float)('sow-original',
                                               self._evtcount['sow-orig'])
                param.Write()

            # Initial number of events
            param = ROOT.TParameter(int)('n-events-initial',
                                         self._evtcount['raw-init'])
            param.Write()
            param = ROOT.TParameter(float)('sow-initial',
                                           self._evtcount['sow-init'])
            param.Write()

            # Restricted number of events
            param = ROOT.TParameter(int)('n-events-restricted',
                                         self._evtcount['raw-restricted'])
            param.Write()
            param = ROOT.TParameter(float)('sow-restricted',
                                           self._evtcount['sow-restricted'])
            param.Write()

            # Resulting number of events
            param = ROOT.TParameter(int)('n-events-final',
                                         self._evtcount['raw-final'])
            param.Write()
            param = ROOT.TParameter(float)('sow-final',
                                           self._evtcount['sow-final'])
            param.Write()

    def get_benchmark_info(self) -> tuple[int, float]:
        '''
        Retrieve benchmark information.
        '''
        if self._elapsed_time is None:
            LOGGER.error('No elapsed time recorded!\nAborting...')
            sys.exit(3)

        if not isinstance(self._evtcount['raw-restricted'], int):
            LOGGER.error('Event count of the restricted dataframe not '
                         'recorded!\nAborting...')
            sys.exit(3)

        return self._evtcount['raw-restricted'], self._elapsed_time

    def generate_analysis_graph(self, graph_path: str) -> None:
        '''
        Generate computational graph of the analysis.
        '''
        if self._elapsed_time is None:
            LOGGER.error('Elapsed time not recorded! RDataFrame job probably '
                         'have not run yet.\nAborting...')
            sys.exit(3)

        generate_graph(self._init_dframe, graph_path)
