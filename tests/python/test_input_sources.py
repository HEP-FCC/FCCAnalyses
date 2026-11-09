'''Regression tests for input-source configuration.'''

import argparse
import importlib.util
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'python'))

from anascript import get_sample_input_source, validate_sample_list
from parsers import setup_run_parser
from input_resolver import InputResolutionError


class InputSourceTest(unittest.TestCase):
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
                ('input-files', [], 'input-files'),
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


if __name__ == '__main__':
    unittest.main()
