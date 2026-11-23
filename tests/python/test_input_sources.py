'''Regression tests for input-source configuration.'''

import argparse
import importlib.util
import logging
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
import sys
import tempfile
from threading import Event
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

import numpy  # Load before temporarily patching sys.modules for ROOT.

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'python'))

from anascript import get_sample_input_source, validate_sample_list
from parsers import setup_run_parser
from input_resolver import InputResolutionError


class InputSourceTest(unittest.TestCase):
    def test_eos_mount_options(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        self.assertIsNone(parser.parse_args(['analysis.py']).use_xrootd)
        with redirect_stderr(StringIO()) as stderr:
            args = parser.parse_args(['analysis.py', '--use-eos-mount'])
        self.assertFalse(args.use_xrootd)
        self.assertEqual(stderr.getvalue(), '')
        args = parser.parse_args(['analysis.py', '--no-filepath-rewrites'])
        self.assertTrue(args.deprecated_no_filepath_rewrites)
        for options in (['--apply-filepath-rewrites'],
                        ['--use-eos-mount', '--no-filepath-rewrites']):
            with self.subTest(options=options), redirect_stderr(StringIO()):
                with self.assertRaises(SystemExit):
                    parser.parse_args(['analysis.py', *options])

    def test_unset_sources_allow_fallback(self):
        sources = ('input-dir', 'input-files', 'input-file-list')
        for provided in ({}, dict.fromkeys(sources)):
            with self.subTest(provided=provided):
                sample = validate_sample_list({'events': provided})['events']
                for source in sources:
                    self.assertIsNone(sample[source])
                self.assertEqual(
                    get_sample_input_source(sample, '/inputs', 'campaign'),
                    ('global-input-dir', '/inputs'),
                )
                self.assertEqual(
                    get_sample_input_source(sample, None, 'campaign'),
                    ('campaign', 'campaign'),
                )
                self.assertEqual(
                    get_sample_input_source(sample, None, None),
                    (None, None),
                )

    def test_explicit_source_prevents_fallback(self):
        for source, value, expected in (
                ('input-files', ['one.root'], 'input-files'),
                ('input-file-list', 'inputs.txt', 'input-file-list'),
                ('input-dir', '/sample', 'sample-input-dir')):
            with self.subTest(source=source):
                sample = validate_sample_list({
                    'events': {source: value},
                })['events']
                self.assertEqual(
                    get_sample_input_source(sample, '/inputs', 'campaign'),
                    (expected, value),
                )

    def test_malformed_input_files_are_rejected(self):
        for value in ('one.root', 42, ('one.root',), ['one.root', 42]):
            with self.subTest(value=value):
                with self.assertLogs('FCCAnalyses.run', level='ERROR') as logs:
                    with self.assertRaises(SystemExit) as error:
                        validate_sample_list({'signal': {'input-files': value}})
                self.assertEqual(error.exception.code, 3)
                self.assertIn('signal', logs.output[0])
                self.assertIn('input-files must be a non-empty list', logs.output[0])

    def test_invalid_sample_fields_are_rejected(self):
        invalid = {
            'input-dir': ['', '  ', 10],
            'input_dir': ['', '  ', 10],
            'input-file-list': ['', '  ', []],
            'input-lfn-list': ['', '  ', []],
            'input-files': [[], [''], ['  ']],
            'output-stem': ['', '  ', 10],
            'output': ['', '  ', 10],
            'fraction': ['0.5', True, 0, -0.1, 1.1, float('nan'), float('inf')],
            'chunks': ['4', True, 0, -1, 1.5],
            'stride': ['4', True, 0, -1, 1.5],
            'n-events-max': ['4', True, -1, 1.5],
        }
        for field, values in invalid.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    with self.assertLogs('FCCAnalyses.run', level='ERROR') as logs:
                        with self.assertRaises(SystemExit) as error:
                            validate_sample_list({'signal': {field: value}})
                    self.assertEqual(error.exception.code, 3)
                    self.assertIn('signal', logs.output[-1])
                    self.assertIn(field, logs.output[-1])
        with self.assertLogs('FCCAnalyses.run', level='ERROR'):
            with self.assertRaises(SystemExit):
                validate_sample_list({'signal': 'not a dictionary'})

    def test_sample_fields_accept_defaults_and_boundary_values(self):
        fields = ('input-dir', 'input_dir', 'input-file-list', 'input-lfn-list',
                  'input-files', 'output-stem', 'output', 'fraction', 'chunks',
                  'stride', 'n-events-max')
        for field in fields:
            with self.subTest(field=field):
                sample = validate_sample_list({'signal': {field: None}})['signal']
                self.assertEqual(sample['fraction'], 1.0)
                self.assertIsNone(sample['chunks'])
        sample = validate_sample_list({'signal': {
            'fraction': 1, 'chunks': 1, 'stride': 1, 'n-events-max': 0,
        }})['signal']
        self.assertEqual(sample['fraction'], 1.0)
        self.assertIsInstance(sample['fraction'], float)
        self.assertEqual((sample['chunks'], sample['stride'], sample['n-events-max']),
                         (1, 1, 0))

    def test_nchunks_and_legacy_chunks(self):
        self.assertEqual(validate_sample_list({'signal': {'nchunks': 3}})
                         ['signal']['chunks'], 3)
        with self.assertLogs('FCCAnalyses.run', level='WARNING') as logs:
            sample = validate_sample_list({'signal': {'chunks': 2}})['signal']
        self.assertEqual(sample['chunks'], 2)
        self.assertIn('nchunks', logs.output[0])
        for values in ({'nchunks': 0}, {'nchunks': 1, 'chunks': 1}):
            with self.subTest(values=values), self.assertRaises(SystemExit):
                validate_sample_list({'signal': values})
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        for option in ('--nchunks', '--n-chunks'):
            self.assertEqual(parser.parse_args(['analysis.py', option, '4']).n_chunks, 4)

    def test_input_sources_are_mutually_exclusive(self):
        sample = validate_sample_list({
            'events': {
                'input-dir': None,
                'input-files': ['one.root'],
            },
        })['events']
        self.assertEqual(sample['input-files'], ['one.root'])

        with self.assertRaises(SystemExit):
            validate_sample_list({
                'events': {
                    'input-dir': '/inputs',
                    'input-file-list': 'inputs.txt',
                },
            })

        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        with self.assertRaises(SystemExit):
            parser.parse_args([
                'analysis.py', '--input', 'one.root', '--input-file-list',
                'inputs.txt',
            ])
        args = parser.parse_args(['analysis.py', '--input', 'one.root',
                                  'two.root'])
        self.assertEqual(args.input, ['one.root', 'two.root'])
        error_output = StringIO()
        with redirect_stderr(error_output), self.assertRaises(SystemExit):
            parser.parse_args(['analysis.py', '--files-list', 'one.root'])
        self.assertIn('unrecognized arguments: --files-list', error_output.getvalue())


class LegacyInputTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Import the legacy runner without requiring a ROOT installation.
        path = Path(__file__).resolve().parents[2] / 'python' / 'run_analysis.py'
        spec = importlib.util.spec_from_file_location('test_legacy_runner', path)
        cls.runner = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {
            'ROOT': MagicMock(),
            'cppyy': MagicMock(),
            'run_fccanalysis': MagicMock(),
        }):
            spec.loader.exec_module(cls.runner)

    def test_deprecated_eos_mount_option_warns_and_disables_rewrites(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        args = parser.parse_args(['missing-analysis.py', '--no-filepath-rewrites'])
        args.command = 'run'
        with self.assertLogs('FCCAnalyses.run', level='WARNING') as logs:
            with self.assertRaises(SystemExit):
                self.runner.run(args)
        self.assertFalse(args.use_xrootd)
        self.assertTrue(any('--use-eos-mount' in msg for msg in logs.output))

    def test_explicit_inputs_override_process_list(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_file = root / 'events.root'
            input_file.touch()
            input_list = root / 'inputs.txt'
            input_list.write_text(f'{input_file}\n', encoding='utf-8')
            for option, value in (('--input', str(input_file)),
                                  ('--input-file-list', str(input_list))):
                with self.subTest(option=option):
                    parser = argparse.ArgumentParser()
                    setup_run_parser(parser)
                    args = parser.parse_args([
                        'analysis.py', option, value, '--output', 'out.root',
                    ])
                    module = SimpleNamespace(processList={'unused': {}})
                    with patch.object(self.runner, 'initialize'), \
                            patch.object(self.runner, 'run_local') as run_local, \
                            patch.object(self.runner, 'get_process_info') as process:
                        with self.assertRaises(SystemExit) as exit_error:
                            self.runner.run_stages(args, module, 'analysis.py')
                    self.assertEqual(exit_error.exception.code, 0)
                    run_local.assert_called_once_with(module, [str(input_file)], args)
                    process.assert_not_called()

    def test_resolution_error_does_not_fall_back(self):
        args = SimpleNamespace(test=False, input=['missing'],
                               input_file_list=None, output='out.root')
        module = SimpleNamespace(processList={'unused': {}})
        with patch.object(self.runner, 'initialize'), \
                patch.object(self.runner, 'resolve_inputs',
                             side_effect=InputResolutionError('bad input')), \
                patch.object(self.runner, 'run_local') as run_local, \
                patch.object(self.runner, 'get_process_info') as process:
            with self.assertLogs('FCCAnalyses.run', level='ERROR') as logs:
                with self.assertRaises(SystemExit) as exit_error:
                    self.runner.run_stages(args, module, 'analysis.py')
        self.assertEqual(exit_error.exception.code, 3)
        self.assertIn('bad input', logs.output[0])
        run_local.assert_not_called()
        process.assert_not_called()

    def test_test_mode_takes_precedence_over_explicit_input(self):
        args = SimpleNamespace(test=True, input=['ignored.root'],
                               input_file_list=None, output='out.root')
        module = SimpleNamespace(testFile='test.root')
        with patch.object(self.runner, 'initialize'), \
                patch.object(self.runner, 'resolve_inputs') as resolve, \
                patch.object(self.runner, 'run_local') as run_local:
            with self.assertRaises(SystemExit) as exit_error:
                self.runner.run_stages(args, module, 'analysis.py')
        self.assertEqual(exit_error.exception.code, 0)
        run_local.assert_called_once_with(module, ['test.root'], args)
        resolve.assert_not_called()


class EosRewriteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[2] / 'python' / 'run_fccanalysis.py'
        spec = importlib.util.spec_from_file_location('test_modern_runner', path)
        cls.runner = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {'ROOT': MagicMock(), 'cppyy': MagicMock()}):
            spec.loader.exec_module(cls.runner)

    def test_data_source_uses_configured_value_and_cli_override(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        cases = (
            (SimpleNamespace(), [], False),
            (SimpleNamespace(use_data_source=False), [], False),
            (SimpleNamespace(use_data_source=True), [], True),
            (SimpleNamespace(use_data_source=False), ['--use-data-source'], True),
        )
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            for analysis, options, expected in cases:
                with self.subTest(analysis=analysis, options=options):
                    args = parser.parse_args(['analysis.py', *options])
                    config = self.runner.merge_config(args, analysis)
                    self.assertIs(config['use-data-source'], expected)

    def test_sample_cli_overrides_and_event_limit_precedence(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        analysis = SimpleNamespace(nevents=90, samples={
            'signal': {'input-files': ['one.root', 'two.root'], 'nchunks': 1,
                       'stride': 2, 'nevents': 30},
            'background': {'input-files': ['three.root', 'four.root']},
        })
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            args = parser.parse_args(['analysis.py', '--output-dir', '/tmp/out',
                                      '--nchunks', '1', '--stride', '5',
                                      '--nevents', '10'])
            config = self.runner.merge_config(args, analysis)
            with self.assertLogs('FCCAnalyses.run_analysis', level='DEBUG') as logs:
                jobs = self.runner.generate_jobs(config)
        self.assertEqual(
            [record.getMessage() for record in logs.records
             if 'overrides sample nchunks' in record.getMessage()],
            ['--nchunks=1 overrides sample nchunks=1 for signal.'],
        )
        self.assertFalse(any(record.levelno >= logging.WARNING for record in logs.records))
        self.assertEqual(len(jobs), 2)
        self.assertEqual([job['stride'] for job in jobs], [5, 5])
        self.assertEqual([job['n-events-max'] for job in jobs], [10, 10])

        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            args = parser.parse_args(['analysis.py', '--output-dir', '/tmp/out',
                                      '--n-chunks', '1'])
            config = self.runner.merge_config(args, analysis)
            jobs = self.runner.generate_jobs(config)
        self.assertEqual([job['n-events-max'] for job in jobs], [30, 90])
        self.assertEqual([job['stride'] for job in jobs], [2, None])

    def test_nevents_aliases_conflicts_and_invalid_values(self):
        with self.assertLogs('FCCAnalyses.run', level='WARNING') as logs:
            sample = validate_sample_list({'signal': {'n-events-max': 5}})['signal']
        self.assertEqual(sample['n-events-max'], 5)
        self.assertIn('DEPRECATED', logs.output[0])
        self.assertEqual(validate_sample_list({'signal': {'nevents': 0}})
                         ['signal']['n-events-max'], 0)
        for sample in ({'nevents': 1, 'n-events-max': 1}, {'nevents': -1}):
            with self.subTest(sample=sample), self.assertRaises(SystemExit):
                validate_sample_list({'signal': sample})
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            with self.assertLogs('FCCAnalyses.run_analysis', level='WARNING'):
                config = self.runner.merge_config(
                    parser.parse_args(['analysis.py']), SimpleNamespace(n_events_max=7))
            self.assertEqual(config['n-events-max'], 7)
            for analysis in (SimpleNamespace(nevents=1, n_events_max=2),
                             SimpleNamespace(nevents=-1)):
                with self.subTest(analysis=analysis), self.assertRaises(SystemExit):
                    self.runner.merge_config(parser.parse_args(['analysis.py']), analysis)

    def test_direct_single_chunk_preserves_output_and_limit(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        args = parser.parse_args(['analysis.py', '--input', 'one.root',
                                  '--n-chunks', '1', '--output', 'out.root',
                                  '--nevents', '5'])
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            job = self.runner.generate_jobs(self.runner.merge_config(args, SimpleNamespace()))[0]
        self.assertEqual(job['output-file'], 'out.root')
        self.assertEqual(job['n-events-max'], 5)

    def test_multichunk_ignores_event_limit_with_warning(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        analysis = SimpleNamespace(nevents=5, samples={
            'signal': {'input-files': ['one.root', 'two.root'], 'chunks': 2},
        })
        args = parser.parse_args(['analysis.py', '--output-dir', '/tmp/out'])
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            config = self.runner.merge_config(args, analysis)
            with self.assertLogs('FCCAnalyses.run_analysis', level='WARNING') as logs:
                jobs = self.runner.generate_jobs(config)
        self.assertEqual([job['n-events-max'] for job in jobs], [None, None])
        self.assertIn('Ignoring the setting', '\n'.join(logs.output))

    def test_direct_input_requires_output_directory_only_when_needed(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            for options in (['--input', 'one.root'],
                            ['--input', 'one.root', 'two.root', '--n-chunks', '2']):
                with self.subTest(options=options):
                    config = self.runner.merge_config(
                        parser.parse_args(['analysis.py', *options]), SimpleNamespace())
                    with self.assertLogs('FCCAnalyses.run_analysis', level='ERROR') as logs:
                        with self.assertRaises(SystemExit):
                            self.runner.generate_jobs(config)
                    self.assertIn('--output-dir', logs.output[0])

    def test_chunk_and_stride_require_positive_integers(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        for option in ('--n-chunks', '--stride'):
            for value in ('0', '-1'):
                with self.subTest(option=option, value=value), redirect_stderr(StringIO()):
                    with self.assertRaises(SystemExit):
                        parser.parse_args(['analysis.py', option, value])

    def test_missing_output_dir_and_ignored_options(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        analysis = SimpleNamespace(samples={'signal': {'input-files': ['one.root']}})
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            args = parser.parse_args(['analysis.py', '--sample-name', 'ignored',
                                      '--output', 'ignored.root', '--test-file', 'unused.root'])
            with self.assertLogs('FCCAnalyses.run_analysis', level='WARNING') as logs:
                config = self.runner.merge_config(args, analysis)
                with self.assertRaises(SystemExit):
                    self.runner.generate_jobs(config)
            output = '\n'.join(logs.output)
            self.assertIn('--test-file', output)
            self.assertIn('--sample-name', output)
            self.assertIn('output file', output)
            self.assertIn('Analysis.output_dir', output)

    def test_test_mode_ignores_unused_sample_configuration_without_warning(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        args = parser.parse_args(['analysis.py', '--test', '--n-chunks', '3',
                                  '--sample-name', 'ignored'])
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            analysis = SimpleNamespace(test_file='test.root', samples={'signal': {'chunks': 'bad'}})
            config = self.runner.merge_config(args, analysis)
            with self.assertNoLogs('FCCAnalyses.run_analysis', level='WARNING'):
                self.runner.generate_jobs(config)

    def test_local_runner_rejects_lfn_without_override(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        for analysis in (SimpleNamespace(input_lfn_list='files.txt'),
                         SimpleNamespace(samples={'signal': {'input-lfn-list': 'files.txt'}}),
                         SimpleNamespace(process_list={'signal': {'input-lfn-list': 'files.txt'}})):
            with self.subTest(analysis=analysis):
                args = parser.parse_args(['analysis.py'])
                module = SimpleNamespace(Analysis=lambda _: analysis)
                with self.assertLogs('FCCAnalyses.run_analysis', level='ERROR') as logs:
                    with self.assertRaises(SystemExit):
                        self.runner.run_fccanalysis(args, module)
                self.assertIn('input-lfn-list' if not hasattr(analysis, 'input_lfn_list')
                              else 'input_lfn_list', logs.output[0])

    def test_test_mode_uses_physical_file_with_script_lfn_inputs(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        analyses = (
            SimpleNamespace(test_file='test.root', input_lfn_list='missing-lfns.txt'),
            SimpleNamespace(test_file='test.root', samples={
                'signal': {'input-lfn-list': 'missing-lfns.txt'}}),
            SimpleNamespace(test_file='test.root', process_list={
                'signal': {'input-lfn-list': 'missing-lfns.txt'}}),
        )
        for analysis in analyses:
            for options in ([], ['--input', 'ignored-directory'],
                            ['--input-file-list', 'missing-inputs.txt']):
                with self.subTest(analysis=analysis, options=options), \
                        patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}), \
                        patch.object(self.runner, 'validate_analysis_class', return_value={
                            'analysis-class': analysis, 'analysis-chain': None,
                            'output-variables': [],
                        }), \
                        patch.object(self.runner, 'global_setup'), \
                        patch.object(self.runner, 'resolve_inputs') as resolve, \
                        patch.object(self.runner, 'read_input_file_list') as read, \
                        patch.object(self.runner, 'Job') as job:
                    args = parser.parse_args(['analysis.py', '--test', *options])
                    job.return_value.get_benchmark_info.return_value = (1, 1.0)
                    self.runner.run_fccanalysis(args, SimpleNamespace(Analysis=lambda _: analysis))
                    self.assertEqual(job.call_args.args[0], [str(Path('test.root').resolve())])
                    resolve.assert_not_called()
                    read.assert_not_called()

    def test_worker_file_list_overrides_script_lfn_configuration(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        with tempfile.TemporaryDirectory() as directory:
            listing = Path(directory) / 'input-files-0000.txt'
            listing.write_text('staged.root\n', encoding='utf-8')
            args = parser.parse_args(['analysis.py', '--input-file-list', str(listing),
                                      '--output', 'output.root'])
            for analysis in (SimpleNamespace(input_lfn_list='files.txt'),
                             SimpleNamespace(samples={'signal': {'input-lfn-list': 'files.txt'}})):
                with self.subTest(analysis=analysis), \
                        patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}), \
                        patch.object(self.runner, 'validate_analysis_class', return_value={
                            'analysis-class': analysis, 'analysis-chain': None,
                            'output-variables': [],
                        }), \
                        patch.object(self.runner, 'global_setup'), \
                        patch.object(self.runner, 'Job') as job:
                    job.return_value.get_benchmark_info.return_value = (1, 1.0)
                    self.runner.run_fccanalysis(args, SimpleNamespace(Analysis=lambda _: analysis))
                    self.assertEqual(job.call_args.args[0], [str(Path('staged.root').resolve())])

    def test_campaign_rewrites_files_and_fraction_metadata(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        path = '/eos/home-b/bwach/events.root'
        analysis = SimpleNamespace(
            campaign='campaign', samples={'signal': {'fraction': 0.5}}
        )
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            for rewrite in (False, True):
                command = ['analysis.py', '--output-dir', '/tmp/results']
                if not rewrite:
                    command.append('--use-eos-mount')
                config = self.runner.merge_config(parser.parse_args(command), analysis)
                expected = (path if not rewrite else
                            'root://eosuser.cern.ch//eos/user/b/bwach/events.root')
                with self.subTest(rewrite=rewrite), \
                        patch.object(self.runner, 'get_files_in_yaml', return_value=(
                            [path], [{'path': path, 'events-in-ttree': 100}]
                        )), \
                        patch.object(self.runner, 'get_subfile_list',
                                     side_effect=lambda files, counts, fraction: files) as subset:
                    job = self.runner.generate_jobs(config)[0]
                subset.assert_called_once_with([expected], [100], 0.5)
                self.assertEqual(list(job['input-file-list']), [expected])

    def test_duplicate_campaign_input_is_rejected_before_fraction_selection(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        analysis = SimpleNamespace(
            campaign='campaign', samples={'signal': {'fraction': 0.5}}
        )
        path = '/eos/home-b/bwach/events.root'
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            config = self.runner.merge_config(
                parser.parse_args(['analysis.py', '--output-dir', '/tmp/results']),
                analysis,
            )
        with patch.object(self.runner, 'get_files_in_yaml', return_value=(
                [path, path], [{'path': path, 'events-in-ttree': 100}] * 2
        )), patch.object(self.runner, 'get_subfile_list') as select:
            with self.assertLogs('FCCAnalyses.run_analysis', level='ERROR') as logs:
                with self.assertRaises(SystemExit):
                    self.runner.generate_jobs(config)
        self.assertIn('signal', logs.output[0])
        self.assertIn('Duplicate input path', logs.output[0])
        select.assert_not_called()

    def test_same_input_may_be_used_by_different_samples(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        path = 'root://storage.example.org//events.root'
        analysis = SimpleNamespace(samples={
            'signal': {'input-files': [path]},
            'background': {'input-files': [path]},
        })
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            config = self.runner.merge_config(
                parser.parse_args(['analysis.py', '--output-dir', '/tmp/results']),
                analysis,
            )
        jobs = self.runner.generate_jobs(config)
        self.assertEqual([list(job['input-file-list']) for job in jobs], [[path], [path]])

    def test_fraction_selection_preserves_input_order_after_parallel_reads(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        paths = [f'root://storage.example.org//{name}.root' for name in ('b', 'a', 'c')]
        analysis = SimpleNamespace(samples={
            'signal': {'input-files': paths, 'fraction': 0.5},
        })
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            config = self.runner.merge_config(
                parser.parse_args(['analysis.py', '--output-dir', '/tmp/results']),
                analysis,
            )

        first_read_done, second_read_done = Event(), Event()
        completed = []

        def read_quantities(path, result_queue):
            if path == paths[0] and not first_read_done.wait(timeout=5):
                raise RuntimeError('First metadata read did not finish')
            if path == paths[2] and not second_read_done.wait(timeout=5):
                raise RuntimeError('Second metadata read did not finish')
            result_queue.put({'path': path, 'events-in-ttree': 100})
            completed.append(path)
            if path == paths[1]:
                first_read_done.set()
            elif path == paths[0]:
                second_read_done.set()

        with patch.dict(self.runner.get_file_quantities.__globals__,
                        {'get_one_file_quantities': read_quantities}):
            job = self.runner.generate_jobs(config)[0]
        self.assertEqual(completed, [paths[1], paths[0], paths[2]])
        self.assertEqual(list(job['input-file-list']), paths[:2])

    def test_normal_runner_rejects_invalid_source_before_fallback(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        analysis = SimpleNamespace(
            input_dir='/inputs', samples={'signal': {'input-file-list': ''}}
        )
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            with self.assertLogs('FCCAnalyses.run', level='ERROR'):
                with self.assertRaises(SystemExit):
                    self.runner.merge_config(parser.parse_args(['analysis.py']), analysis)

    def test_cli_input_modes_use_fuse_only_when_requested(self):
        eos_path = '/eos/home-b/bwach/data'
        local_file = eos_path + '/a.root'
        remote_file = 'root://eosuser.cern.ch//eos/user/b/bwach/data/a.root'
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            for use_fuse in (False, True):
                with self.subTest(use_fuse=use_fuse), \
                        patch('input_resolver.os.listdir', return_value=['a.root']) as listdir, \
                        patch('input_resolver.os.path.isfile', return_value=True), \
                        patch('input_resolver.subprocess.run') as xrdfs:
                    xrdfs.return_value.stdout = (
                        '-rw-r--r-- 1 user group 1 /eos/user/b/bwach/data/a.root\n'
                    )
                    command = ['analysis.py', '--input', eos_path, '--output', 'out.root']
                    if use_fuse:
                        command.append('--use-eos-mount')
                    args = parser.parse_args(command)
                    config = self.runner.merge_config(args, SimpleNamespace())
                    files = self.runner.generate_jobs(config)[0]['input-file-list']
                    self.assertEqual(files, [local_file if use_fuse else remote_file])
                    self.assertEqual(listdir.called, use_fuse)
                    self.assertEqual(xrdfs.called, not use_fuse)

    def test_cli_file_list_keeps_fuse_paths_when_requested(self):
        path = '/eos/project/f/fccanalyses/events.root'
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        with tempfile.TemporaryDirectory() as directory:
            listing = Path(directory) / 'inputs.txt'
            listing.write_text(path + '\n', encoding='utf-8')
            with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
                for use_fuse in (False, True):
                    command = ['analysis.py', '--input-file-list', str(listing),
                               '--output', 'out.root']
                    if use_fuse:
                        command.append('--use-eos-mount')
                    config = self.runner.merge_config(parser.parse_args(command), SimpleNamespace())
                    expected = path if use_fuse else 'root://eosproject.cern.ch/' + path
                    self.assertEqual(self.runner.generate_jobs(config)[0]['input-file-list'],
                                     [expected])

    def test_sample_directory_uses_requested_discovery_mode(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        analysis = SimpleNamespace(
            input_dir='/eos/project/f/project', samples={'signal': {}}
        )
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            for use_fuse in (False, True):
                with self.subTest(use_fuse=use_fuse), \
                        patch('input_resolver.os.listdir', return_value=['a.root']) as listdir, \
                        patch('input_resolver.os.path.isfile', return_value=True), \
                        patch('input_resolver.subprocess.run') as xrdfs:
                    xrdfs.return_value.stdout = (
                        '-rw-r--r-- 1 user group 1 /eos/project/f/project/signal/a.root\n'
                    )
                    command = ['analysis.py', '--output-dir', '/tmp/results']
                    if use_fuse:
                        command.append('--use-eos-mount')
                    config = self.runner.merge_config(parser.parse_args(command), analysis)
                    job = self.runner.generate_jobs(config)[0]
                    path = '/eos/project/f/project/signal/a.root'
                    expected = path if use_fuse else 'root://eosproject.cern.ch/' + path
                    self.assertEqual(list(job['input-file-list']), [expected])
                    self.assertEqual(listdir.called, use_fuse)
                    self.assertEqual(xrdfs.called, not use_fuse)

    def test_test_mode_does_not_resolve_direct_inputs(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        analysis = SimpleNamespace(test_file='test.root')
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            for options in (['--input', 'missing-directory'],
                            ['--input-file-list', 'missing-list.txt']):
                with self.subTest(options=options), \
                        patch.object(self.runner, 'resolve_inputs') as resolve, \
                        patch.object(self.runner, 'read_input_file_list') as read:
                    args = parser.parse_args(['analysis.py', '--test', *options])
                    config = self.runner.merge_config(args, analysis)
                    self.assertEqual(
                        self.runner.generate_jobs(config)[0]['input-file-list'],
                        [str(Path('test.root').resolve())],
                    )
                    resolve.assert_not_called()
                    read.assert_not_called()

    def test_test_file_uses_requested_eos_mode(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        path = '/eos/home-b/bwach/events.root'
        analysis = SimpleNamespace(test_file=path)
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            for use_fuse in (False, True):
                command = ['analysis.py', '--test']
                if use_fuse:
                    command.append('--use-eos-mount')
                config = self.runner.merge_config(parser.parse_args(command), analysis)
                expected = (path if use_fuse else
                            'root://eosuser.cern.ch//eos/user/b/bwach/events.root')
                self.assertEqual(self.runner.generate_jobs(config)[0]['input-file-list'],
                                 [expected])

    def test_https_test_file_is_preserved(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        url = 'https://example.org/events.root'
        with patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
            config = self.runner.merge_config(
                parser.parse_args(['analysis.py', '--test']),
                SimpleNamespace(test_file=url),
            )
        self.assertEqual(self.runner.generate_jobs(config)[0]['input-file-list'], [url])

    def test_https_cli_input_and_file_list(self):
        parser = argparse.ArgumentParser()
        setup_run_parser(parser)
        url = 'https://example.org/events.root'
        with tempfile.TemporaryDirectory() as directory:
            listing = Path(directory) / 'inputs.txt'
            listing.write_text(url + '\n', encoding='utf-8')
            for arguments in (['--input', url], ['--input-file-list', str(listing)]):
                with self.subTest(arguments=arguments), \
                        patch.dict('os.environ', {'KEY4HEP_STACK': '/cvmfs/sw.hsf.org/almalinux9'}):
                    config = self.runner.merge_config(
                        parser.parse_args(['analysis.py', *arguments]), SimpleNamespace()
                    )
                    self.assertEqual(config['input-file-list'], [url])


if __name__ == '__main__':
    unittest.main()
