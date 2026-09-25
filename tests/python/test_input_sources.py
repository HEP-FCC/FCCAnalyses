'''Regression tests for input-source configuration.'''

import argparse
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'python'))

from anascript import get_sample_input_source, validate_sample_list
from parsers import setup_run_parser


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

    def test_analysis_source_hierarchy(self):
        self.assertEqual(
            get_sample_input_source({'input-dir': None}, None, 'campaign'),
            ('campaign', 'campaign'),
        )
        self.assertEqual(
            get_sample_input_source({'input-dir': None}, '/inputs', 'campaign'),
            ('global-input-dir', '/inputs'),
        )
        sample = validate_sample_list({
            'events': {'input-files': ['one.root']},
        })['events']
        self.assertEqual(
            get_sample_input_source(sample, '/inputs', 'campaign'),
            ('input-files', ['one.root']),
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


if __name__ == '__main__':
    unittest.main()
