'''Small regression suite for local and remote input discovery.'''

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'python'))

from input_resolver import (
    InputResolutionError, eos_to_xrootd, normalize_input_path, read_input_file_list,
    resolve_directory, resolve_inputs,
)


class InputResolverTest(unittest.TestCase):
    def test_local_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / 'a file.root').touch()
            (base / 'notes.txt').touch()
            nested = base / 'nested'
            nested.mkdir()
            (nested / 'b.root').touch()
            self.assertEqual(resolve_directory(directory), [str(base / 'a file.root')])
            self.assertEqual(
                resolve_inputs([directory, str(nested), str(base / 'a file.root')]),
                [str(base / 'a file.root'), str(nested / 'b.root')],
            )

    def test_eos_mapping_and_remote_files(self):
        with patch('input_resolver.subprocess.run') as run:
            for path, host in [
                ('/eos/experiment/fcc/a.root', 'eospublic.cern.ch'),
                ('/eos/user/a/alice/a.root', 'eosuser.cern.ch'),
            ]:
                self.assertEqual(resolve_inputs([path]), [f'root://{host}/{path}'])
            self.assertEqual(resolve_inputs(['root://example.org/data/a.root']),
                             ['root://example.org//data/a.root'])
            run.assert_not_called()

    def test_eos_redirector_mappings(self):
        for path, expected in (
            ('/eos/experiment/other/a.root',
             'root://eospublic.cern.ch//eos/experiment/other/a.root'),
            ('/eos/user/b/bwach/a.root',
             'root://eosuser.cern.ch//eos/user/b/bwach/a.root'),
            ('/eos/home-b/bwach/a.root',
             'root://eosuser.cern.ch//eos/user/b/bwach/a.root'),
            ('/eos/home-b/bwach/home-b-notes/a.root',
             'root://eosuser.cern.ch//eos/user/b/bwach/home-b-notes/a.root'),
            ('/eos/project/f/fccanalyses/a.root',
             'root://eosproject.cern.ch//eos/project/f/fccanalyses/a.root'),
        ):
            with self.subTest(path=path):
                self.assertEqual(eos_to_xrootd(path), expected)

    def test_mounted_eos_directory_is_listed_locally(self):
        for path in ('/eos/experiment/other/data', '/eos/home-b/bwach/data',
                     '/eos/project/f/project/data', '/eos/unknown/data'):
            with self.subTest(path=path), \
                    patch('input_resolver.os.listdir', return_value=['a.root']), \
                    patch('input_resolver.os.path.isfile', return_value=True), \
                    patch('input_resolver.subprocess.run') as run:
                self.assertEqual(resolve_directory(path, use_xrootd=False),
                                 [path + '/a.root'])
                run.assert_not_called()

    def test_eos_directory_uses_remote_mapping_by_default(self):
        with patch('input_resolver.os.listdir') as listdir, \
                patch('input_resolver.subprocess.run') as run:
            run.return_value.stdout = '-rw-r--r-- 1 user group 1 /eos/project/f/test/a.root\n'
            self.assertEqual(resolve_directory('/eos/project/f/test'), [
                'root://eosproject.cern.ch//eos/project/f/test/a.root',
            ])
            run.assert_called_once_with(
                ['xrdfs', 'eosproject.cern.ch', 'ls', '-l', '/eos/project/f/test'],
                check=True, capture_output=True, text=True,
            )
            listdir.assert_not_called()

    def test_fuse_mode_does_not_fall_back_to_xrootd(self):
        with patch('input_resolver.os.listdir', side_effect=FileNotFoundError), \
                patch('input_resolver.subprocess.run') as run:
            with self.assertRaises(InputResolutionError):
                resolve_directory('/eos/home-b/bwach/missing', use_xrootd=False)
            run.assert_not_called()

    @patch('input_resolver.subprocess.run')
    def test_remote_directory(self, run):
        run.return_value.stdout = (
            '-rw------- ganis sf 117334351 2022-08-31 11:46:27 /data/b file.root\n'
            'drwxr-xr-x ganis sf 0 2025-01-26 22:46:35 /data/.sys.v#.a.root\n'
            '-rw------- ganis sf 117209126 2022-08-31 11:46:46 /data/a.root\n'
            '-rw------- ganis sf 117209126 2022-08-31 11:46:46 /data/a.root\n'
            '-rw------- ganis sf 100 2022-08-31 11:46:49 /data/notes.txt\n'
        )
        for host in ['storage.example.org:1094', 'eosproject.cern.ch']:
            self.assertEqual(resolve_inputs([f'root://{host}//data/']), [
                f'root://{host}//data/a.root', f'root://{host}//data/b file.root',
            ])
            run.assert_called_with(
                ['xrdfs', host, 'ls', '-l', '/data/'],
                check=True, capture_output=True, text=True,
            )

    def test_file_list(self):
        with tempfile.TemporaryDirectory() as directory:
            listing = Path(directory) / 'inputs.txt'
            listing.write_text('# comment\n\na file.root\na file.root\n',
                               encoding='utf-8')
            self.assertEqual(read_input_file_list(str(listing)),
                             [str(Path('a file.root').absolute())])

    def test_invalid_paths(self):
        for path in ['root://', 'root://host', '/eos/unknown/data']:
            with self.subTest(path=path):
                with self.assertRaises(InputResolutionError):
                    normalize_input_path(path)
        with tempfile.TemporaryDirectory() as directory:
            for path in [directory, str(Path(directory) / 'missing')]:
                with self.assertRaises(InputResolutionError):
                    resolve_directory(path)

    @patch('input_resolver.subprocess.run')
    def test_remote_errors(self, run):
        run.return_value.stdout = ''
        with self.assertRaisesRegex(InputResolutionError, 'no immediate'):
            resolve_directory('root://host//data')
        run.side_effect = subprocess.CalledProcessError(
            1, ['xrdfs'], stderr='Permission denied',
        )
        with self.assertRaisesRegex(InputResolutionError, 'Permission denied'):
            resolve_directory('root://host//data')


if __name__ == '__main__':
    unittest.main()
