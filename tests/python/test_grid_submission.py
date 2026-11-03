'''Tests for the Key4hep-side grid submission frontend.'''

import argparse
import importlib.util
import platform
import sys
import tarfile
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / 'python'))

from grid_submission import (
    GridSubmissionError,
    _create_analysis_include_archive,
    create_grid_submission_request,
    submit_grid_submission,
)
from parsers import setup_submit_parser
from submission import SubmissionRequest, UserBuildPayload


class GridSubmissionFrontendTest(unittest.TestCase):
    '''Exercise parsing, request creation, and the isolated child hand-off.'''

    @staticmethod
    def make_submit_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        setup_submit_parser(parser)
        return parser

    def parse_grid_arguments(
        self,
        analysis_script: str,
        arguments: list[str],
    ) -> argparse.Namespace:
        return self.make_submit_parser().parse_args(
            ['grid', analysis_script, *arguments]
        )

    @staticmethod
    def load_analysis_module(path):
        specification = importlib.util.spec_from_file_location('test_analysis', path)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        return module

    @staticmethod
    def write_lfn_input(directory: Path) -> Path:
        path = directory / 'input-lfns.txt'
        path.write_text(
            '\n/fcc/user/a/alice/input-1.root\n'
            ' /fcc/user/a/alice/input-2.root \n',
            encoding='utf-8',
        )
        return path

    @staticmethod
    def write_modern_analysis(path: Path, body: str = '        pass\n') -> None:
        path.write_text(
            'class Analysis:\n'
            '    analyzers = None\n'
            '    output = []\n'
            '    def __init__(self, arguments):\n'
            f'{body}',
            encoding='utf-8',
        )

    @staticmethod
    def grid_arguments(lfn_input: Path) -> list[str]:
        return [
            '--lfn-input',
            str(lfn_input),
            '--output',
            'analysis.root',
            '--files-per-job',
            '2',
            '--output-dir',
            'analysis/results',
            '--output-se',
            'CERN-DST-EOS',
            '--site',
            'LCG.CERN.ch',
        ]

    def test_parses_lfn_contract_and_creates_request(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_script = root / 'analysis.py'
            key4hep_setup = root / 'setup.sh'
            include_file = root / 'helpers' / 'functions.h'
            include_file.parent.mkdir()
            include_file.write_text('int answer() { return 42; }\n', encoding='utf-8')
            self.write_modern_analysis(
                analysis_script,
                '        self.include_paths = ["helpers/functions.h"]\n',
            )
            key4hep_setup.touch()
            args = self.parse_grid_arguments(
                str(analysis_script),
                [
                    '--lfn-input', str(self.write_lfn_input(root)),
                    '--files-per-job', '2',
                    '--output-se', 'CERN-DST-EOS',
                    '--site', 'LCG.CERN.ch',
                    '--stride', '5',
                    '--ncpus', '2',
                    '--output-format', 'rntuple',
                ],
            )

            args.remaining = ['--output', 'custom.root', '--nevents', '100']
            request = create_grid_submission_request(
                args,
                self.load_analysis_module(analysis_script),
                key4hep_setup=str(key4hep_setup),
                analysis_include_archive_path=root / 'includes.tar.gz',
            )

            with tarfile.open(request.analysis_include_archive) as archive:
                self.assertEqual(archive.getnames(), ['helpers/functions.h'])

            module = self.load_analysis_module(analysis_script)
            for cli, script, expected in (
                (None, 3, 3), (-2, 3, -2), (None, 0, None),
            ):
                with self.subTest(cli=cli, script=script):
                    if script is not None:
                        module.Analysis.n_threads = script
                    options = ['--lfn-input', str(self.write_lfn_input(root))]
                    if cli is not None:
                        options.extend(['-j', str(cli)])
                    cpu_args = self.parse_grid_arguments(str(analysis_script), options)
                    if expected is None:
                        with self.assertRaisesRegex(GridSubmissionError, 'nonzero integer'):
                            create_grid_submission_request(cpu_args, module, str(key4hep_setup))
                    else:
                        cpu_request = create_grid_submission_request(
                            cpu_args, module, str(key4hep_setup),
                            analysis_include_archive_path=root / 'cpu-includes.tar.gz',
                        )
                        self.assertEqual(cpu_request.worker_ncpus, expected)

        self.assertEqual(request.analysis_script, str(analysis_script.resolve()))
        self.assertEqual(request.input_mode, 'dirac-lfn')
        self.assertEqual(
            request.input_lfns,
            (
                '/fcc/user/a/alice/input-1.root',
                '/fcc/user/a/alice/input-2.root',
            ),
        )
        self.assertEqual(request.files_per_job, 2)
        self.assertIsNone(request.n_chunks)
        self.assertEqual(request.output_file, 'output.root')
        self.assertIsNone(request.output_path)
        self.assertEqual(request.output_se, 'CERN-DST-EOS')
        self.assertEqual(request.destination_site, 'LCG.CERN.ch')
        self.assertEqual(request.submit_mode, 'wms')
        self.assertIsNone(request.user_build_payload)
        self.assertIsNotNone(request.analysis_include_archive)
        self.assertEqual(request.run_arguments, tuple(args.remaining))
        self.assertEqual(request.worker_stride, 5)
        self.assertEqual(request.worker_ncpus, 2)
        self.assertEqual(request.worker_output_format, 'rntuple')
        self.assertRegex(request.submission_id, r'^\d{8}T\d{6}Z$')

    def test_resolves_analysis_samples_for_xrootd_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_script = root / 'analysis.py'
            key4hep_setup = root / 'setup.sh'
            include_file = root / 'include' / 'functions.h'
            include_file.parent.mkdir()
            include_file.write_text('int answer() { return 42; }\n', encoding='utf-8')
            analysis_script.write_text(
                'class Analysis:\n'
                '    analyzers = None\n'
                '    output = []\n'
                '    def __init__(self, arguments):\n'
                '        self.input_dir = "/eos/experiment/fcc/test"\n'
                '        self.include_paths = ["include/functions.h"]\n'
                '        self.samples = {\n'
                '            "signal": {"chunks": 2, "stride": 3},\n'
                '            "background": {},\n'
                '        }\n',
                encoding='utf-8',
            )
            key4hep_setup.touch()
            args = self.parse_grid_arguments(
                str(analysis_script),
                [
                    '--output', 'analysis.root',
                    '--output-dir', 'analysis/results',
                    '--n-chunks', '2',
                ],
            )

            def discover(directory_name: str) -> list[str]:
                if directory_name.endswith('/signal'):
                    return [
                        'root://eospublic.cern.ch//eos/experiment/fcc/test/signal/a.root',
                        'root://eospublic.cern.ch//eos/experiment/fcc/test/signal/b.root',
                    ]
                return [
                    'root://eospublic.cern.ch//eos/experiment/fcc/test/background/a.root',
                ]

            with patch('grid_submission._discover_xrootd_root_files', side_effect=discover):
                request = create_grid_submission_request(
                    args,
                    self.load_analysis_module(analysis_script),
                    key4hep_setup=str(key4hep_setup),
                    analysis_include_archive_path=root / 'includes.tar.gz',
                )
            with tarfile.open(request.analysis_include_archive) as archive:
                self.assertEqual(archive.getnames(), ['include/functions.h'])
                archived_file = archive.extractfile('include/functions.h')
                self.assertIsNotNone(archived_file)
                self.assertEqual(
                    archived_file.read(),
                    b'int answer() { return 42; }\n',
                )

        self.assertEqual(request.input_mode, 'xrootd')
        self.assertEqual(request.input_lfns, ())
        self.assertEqual(request.n_chunks, 2)
        self.assertEqual([sample.name for sample in request.samples], ['signal', 'background'])
        self.assertEqual(request.samples[0].chunks, 2)
        self.assertEqual(request.samples[0].stride, 3)
        self.assertTrue(request.analysis_include_archive.endswith('includes.tar.gz'))

    def test_rejects_invalid_analysis_before_submission(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_script = root / 'analysis.py'
            key4hep_setup = root / 'setup.sh'
            self.write_modern_analysis(analysis_script)
            key4hep_setup.touch()
            args = self.parse_grid_arguments(
                str(analysis_script),
                self.grid_arguments(self.write_lfn_input(root)),
            )

            for attribute, message in (
                ('Analysis', 'requires an Analysis class'),
                ('analyzers', 'Analysis chain not provided'),
                ('output', 'Analysis output variables not provided'),
                ('run_batch', 'run_batch analysis attribute is no longer supported'),
            ):
                with self.subTest(attribute=attribute):
                    module = self.load_analysis_module(analysis_script)
                    if attribute == 'Analysis':
                        del module.Analysis
                    elif attribute == 'run_batch':
                        module.Analysis.run_batch = True
                    else:
                        delattr(module.Analysis, attribute)
                    with patch.dict('os.environ', {'KEY4HEP_STACK': str(key4hep_setup)}):
                        with patch('grid_submission.subprocess.run') as start_child:
                            with self.assertRaisesRegex(GridSubmissionError, message):
                                submit_grid_submission(args, module)
                            start_child.assert_not_called()

    def test_rejects_sample_event_limits(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_script = root / 'analysis.py'
            key4hep_setup = root / 'setup.sh'
            self.write_modern_analysis(
                analysis_script,
                '        self.samples = {"signal": {"n-events-max": 10}}\n',
            )
            key4hep_setup.touch()
            args = self.parse_grid_arguments(
                str(analysis_script), self.grid_arguments(self.write_lfn_input(root))
            )

            with self.assertRaisesRegex(GridSubmissionError, 'n-events-max'):
                create_grid_submission_request(
                    args,
                    self.load_analysis_module(analysis_script),
                    key4hep_setup=str(key4hep_setup),
                )

    def test_rejects_include_paths_outside_analysis_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_directory = root / 'analysis'
            analysis_directory.mkdir()
            analysis_script = analysis_directory / 'analysis.py'
            analysis_script.touch()
            (root / 'outside.h').touch()

            with self.assertRaisesRegex(GridSubmissionError, 'must stay below'):
                _create_analysis_include_archive(
                    analysis_script,
                    SimpleNamespace(include_paths=['../outside.h']),
                    root / 'includes.tar.gz',
                )

    def test_starts_clean_child_with_shipped_build_request(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_script = root / 'analysis.py'
            key4hep_setup = root / 'setup.sh'
            self.write_modern_analysis(analysis_script)
            key4hep_setup.touch()
            install_root = root.resolve() / 'install'
            runner = install_root / 'scripts' / 'dirac' / 'run_dirac_submission.sh'
            helper = install_root / 'python' / 'dirac_submit_helper.py'
            for path in (runner, helper):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
            args = self.parse_grid_arguments(
                str(analysis_script),
                [*self.grid_arguments(self.write_lfn_input(root)), '--ship-local-build'],
            )
            temporary_paths: list[Path] = []

            def create_archive(build, archive_path):
                self.assertEqual(build.key4hep_setup, key4hep_setup)
                archive_path.write_bytes(b'payload')
                return SimpleNamespace(path=archive_path, size_bytes=7)

            def check_child(command, check, env):
                self.assertTrue(check)
                self.assertEqual(
                    command,
                    [
                        str(runner),
                        str(helper),
                    ],
                )
                self.assertEqual(env['PATH'], '/usr/bin:/bin')
                self.assertNotIn('KEY4HEP_STACK', env)
                request_path = Path(env['FCCANALYSES_SUBMISSION_REQUEST'])
                request = SubmissionRequest.read_json(request_path)
                self.assertEqual(request.key4hep_setup, str(key4hep_setup.resolve()))
                self.assertIsNotNone(request.user_build_payload)
                self.assertEqual(request.user_build_payload.build_os, platform.system())
                self.assertEqual(request.user_build_payload.build_arch, platform.machine())
                payload_path = Path(request.user_build_payload.archive_path)
                self.assertTrue(payload_path.is_file())
                temporary_paths.extend([request_path, payload_path])

            with patch.dict(
                'os.environ',
                {
                    'KEY4HEP_STACK': str(key4hep_setup),
                    'FCCANA_LOCAL_DIR': str(root),
                },
                clear=True,
            ):
                with patch(
                    'grid_submission.validate_user_build',
                    return_value=SimpleNamespace(key4hep_setup=key4hep_setup),
                ):
                    with patch(
                        'grid_submission.create_user_build_archive',
                        side_effect=create_archive,
                    ):
                        with patch(
                            'grid_submission.subprocess.run',
                            side_effect=check_child,
                        ):
                            with redirect_stdout(StringIO()):
                                submit_grid_submission(
                                    args, self.load_analysis_module(analysis_script)
                                )

        self.assertTrue(temporary_paths)
        self.assertTrue(all(not path.exists() for path in temporary_paths))


if __name__ == '__main__':
    unittest.main()
