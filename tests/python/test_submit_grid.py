'''Tests for the public submit router's grid path.'''

import argparse
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / 'python'))

from parsers import setup_submit_parser

# The existing submit module imports the HTCondor backend at module load time.
# This router test does not exercise that backend or require its PyYAML dependency.
batch_module = types.ModuleType('batch')
batch_module.send_to_batch = lambda *arguments: None
sys.modules['batch'] = batch_module

from submit import submit_analysis


class SubmitGridTest(unittest.TestCase):
    '''Ensure grid submission arguments reach the dedicated frontend.'''

    @staticmethod
    def make_submit_parser() -> argparse.ArgumentParser:
        '''Create the top-level parser and its nested submit backends.'''
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='command', required=True)
        setup_submit_parser(subparsers.add_parser('submit'))
        return parser

    def test_routes_lfn_grid_arguments_to_grid_frontend(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            analysis_script = Path(directory) / 'analysis.py'
            analysis_script.write_text('this is not valid Python\n', encoding='utf-8')
            parser = self.make_submit_parser()
            command = [
                'fccanalysis',
                'submit',
                'grid',
                str(analysis_script),
                '--lfn-input', '/tmp/input-lfns.txt',
                '--output', 'analysis.root',
                '--output-dir', 'analysis/results',
                '--', '--stride', '5', '--nevents', '100',
            ]

            with patch.object(sys, 'argv', command):
                with patch('submit.submit_grid_submission') as submit_grid:
                    submit_analysis(parser)

        submit_grid.assert_called_once()
        args = submit_grid.call_args.args[0]
        self.assertEqual(args.anascript_path, str(analysis_script))
        self.assertEqual(args.lfn_input, '/tmp/input-lfns.txt')
        self.assertEqual(args.output, 'analysis.root')
        self.assertIsNone(args.output_se)
        self.assertEqual(args.remaining, ['--stride', '5', '--nevents', '100'])

    def test_rejects_unknown_grid_argument_without_separator(self) -> None:
        parser = self.make_submit_parser()
        command = [
            'fccanalysis',
            'submit',
            'grid',
            'analysis.py',
            '--output', 'analysis.root',
            '--output-dir', 'analysis/results',
            '--analysis-option', 'value',
        ]

        with patch.object(sys, 'argv', command):
            with self.assertRaises(SystemExit) as error:
                submit_analysis(parser)

        self.assertEqual(error.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
