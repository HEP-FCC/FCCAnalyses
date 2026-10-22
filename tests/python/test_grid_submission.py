'''Tests for the Key4hep-side grid submission frontend.'''

import argparse
import importlib.util
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
    _create_analysis_instance,
    _resolve_grid_sample_inputs,
    create_grid_submission_request,
    submit_grid_submission,
)
from parsers import setup_submit_parser
from submission import SubmissionRequest, UserBuildPayload, plan_jobs


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
            '    def __init__(self, arguments):\n'
            f'{body}',
            encoding='utf-8',
        )

    @staticmethod
    def grid_arguments(lfn_input: Path) -> list[str]:
        return [
            '--input-lfn-list',
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

    def test_constructs_analysis_from_supplied_module(self) -> None:
        class Analysis:
            def __init__(self, arguments):
                self.arguments = arguments

        module = SimpleNamespace(Analysis=Analysis)
        args = argparse.Namespace(remaining=['--custom', 'value'])
        analysis = _create_analysis_instance(module, Path('not-imported.py'), args)
        self.assertIsInstance(analysis, Analysis)
        self.assertEqual(analysis.arguments['unknown'], ['--custom', 'value'])
        self.assertFalse(hasattr(args, 'unknown'))

    def test_parses_lfn_contract_and_creates_request(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_script = root / 'analysis.py'
            key4hep_setup = root / 'setup.sh'
            self.write_modern_analysis(analysis_script)
            key4hep_setup.touch()
            args = self.parse_grid_arguments(
                str(analysis_script),
                [
                    '--input-lfn-list', str(self.write_lfn_input(root)),
                    '--output-se', 'CERN-DST-EOS',
                    '--site', 'LCG.CERN.ch',
                ],
            )

            request = create_grid_submission_request(
                args,
                self.load_analysis_module(analysis_script),
                key4hep_setup=str(key4hep_setup),
            )

        self.assertEqual(request.analysis_script, str(analysis_script.resolve()))
        self.assertEqual(request.input_mode, 'dirac-lfn')
        self.assertEqual(
            request.samples[0].inputs,
            ('/fcc/user/a/alice/input-1.root', '/fcc/user/a/alice/input-2.root'),
        )
        self.assertIsNone(request.files_per_job)
        self.assertEqual(len(plan_jobs(request)), 1)
        self.assertIsNone(request.n_chunks)
        self.assertEqual(request.output_file, 'output.root')
        self.assertIsNone(request.output_path)
        self.assertEqual(request.output_se, 'CERN-DST-EOS')
        self.assertEqual(request.destination_site, 'LCG.CERN.ch')
        self.assertEqual(request.submit_mode, 'wms')
        self.assertIsNone(request.user_build_payload)
        self.assertIsNone(request.analysis_include_archive)
        self.assertRegex(request.submission_id, r'^\d{8}T\d{6}Z$')

    def test_parses_lfn_chunk_override(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_script = root / 'analysis.py'
            key4hep_setup = root / 'setup.sh'
            self.write_modern_analysis(analysis_script)
            key4hep_setup.touch()
            args = self.parse_grid_arguments(
                str(analysis_script),
                [
                    '--input-lfn-list', str(self.write_lfn_input(root)),
                    '--output', 'analysis.root',
                    '--output-dir', 'analysis/results',
                    '--n-chunks', '2',
                ],
            )

            request = create_grid_submission_request(
                args,
                self.load_analysis_module(analysis_script),
                key4hep_setup=str(key4hep_setup),
            )

        self.assertIsNone(request.files_per_job)
        self.assertEqual(request.n_chunks, 2)

    def test_resolves_analysis_lfn_inputs_and_rejects_mixed_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            key4hep_setup = root / 'setup.sh'
            lfn_list = self.write_lfn_input(root)
            global_script = root / 'global-lfns.py'
            sample_script = root / 'sample-lfns.py'
            mixed_script = root / 'mixed.py'
            key4hep_setup.touch()
            self.write_modern_analysis(
                global_script,
                f'        self.input_lfn_list = {str(lfn_list)!r}\n',
            )
            self.write_modern_analysis(
                sample_script,
                '        self.samples = {\n'
                f'            "signal": {{"input-lfn-list": {str(lfn_list)!r}}}\n'
                '        }\n',
            )
            self.write_modern_analysis(
                mixed_script,
                '        self.samples = {\n'
                f'            "signal": {{"input-lfn-list": {str(lfn_list)!r}}},\n'
                '            "background": {"input-files": [\n'
                '                "root://storage.example.org//data/a.root"\n'
                '            ]},\n'
                '        }\n',
            )

            global_request = create_grid_submission_request(
                self.parse_grid_arguments(str(global_script), []),
                self.load_analysis_module(global_script),
                key4hep_setup=str(key4hep_setup),
            )
            sample_request = create_grid_submission_request(
                self.parse_grid_arguments(str(sample_script), []),
                self.load_analysis_module(sample_script),
                key4hep_setup=str(key4hep_setup),
            )
            with self.assertRaisesRegex(GridSubmissionError, 'cannot mix'):
                create_grid_submission_request(
                    self.parse_grid_arguments(str(mixed_script), []),
                    self.load_analysis_module(mixed_script),
                    key4hep_setup=str(key4hep_setup),
                )

        self.assertEqual(global_request.input_mode, 'dirac-lfn')
        self.assertIsNone(global_request.samples[0].name)
        self.assertEqual(sample_request.samples[0].name, 'signal')
        self.assertEqual(plan_jobs(sample_request)[0].sample_name, 'signal')

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

            with patch('grid_submission.resolve_directory', side_effect=discover):
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
        self.assertEqual(request.n_chunks, 2)
        self.assertEqual([sample.name for sample in request.samples], ['signal', 'background'])
        self.assertEqual(request.samples[0].chunks, 2)
        self.assertEqual(request.samples[0].stride, 3)
        self.assertTrue(request.analysis_include_archive.endswith('includes.tar.gz'))

    def test_resolves_sample_input_files_for_grid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_script = root / 'analysis.py'
            key4hep_setup = root / 'setup.sh'
            self.write_modern_analysis(
                analysis_script,
                '        self.samples = {\n'
                '            "signal": {"input-files": [\n'
                '                "root://storage.example.org//data/a.root"\n'
                '            ]}\n'
                '        }\n',
            )
            key4hep_setup.touch()
            args = self.parse_grid_arguments(str(analysis_script), [])

            with patch(
                'grid_submission.resolve_inputs',
                return_value=['root://storage.example.org//data/a.root'],
            ) as resolve:
                request = create_grid_submission_request(
                    args,
                    self.load_analysis_module(analysis_script),
                    key4hep_setup=str(key4hep_setup),
                )

        resolve.assert_called_once_with(['root://storage.example.org//data/a.root'])
        self.assertEqual(
            request.samples[0].inputs,
            ('root://storage.example.org//data/a.root',),
        )

    def test_resolves_direct_grid_cli_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_script = root / 'analysis.py'
            key4hep_setup = root / 'setup.sh'
            self.write_modern_analysis(analysis_script)
            key4hep_setup.touch()
            args = self.parse_grid_arguments(
                str(analysis_script),
                ['--input', 'root://storage.example.org//data/a.root'],
            )

            with patch(
                'grid_submission.resolve_inputs',
                return_value=['root://storage.example.org//data/a.root'],
            ) as resolve:
                request = create_grid_submission_request(
                    args,
                    self.load_analysis_module(analysis_script),
                    key4hep_setup=str(key4hep_setup),
                )
            named_args = self.parse_grid_arguments(
                str(analysis_script),
                [
                    '--input', 'root://storage.example.org//data/a.root',
                    '--sample-name', 'signal',
                ],
            )
            with patch(
                'grid_submission.resolve_inputs',
                return_value=['root://storage.example.org//data/a.root'],
            ):
                named_request = create_grid_submission_request(
                    named_args,
                    self.load_analysis_module(analysis_script),
                    key4hep_setup=str(key4hep_setup),
                )

        resolve.assert_called_once_with(['root://storage.example.org//data/a.root'])
        self.assertEqual(request.samples[0].name, 'output')
        self.assertIsNone(request.samples[0].output_stem)
        self.assertEqual(plan_jobs(request)[0].output_file, 'output_0000.root')
        self.assertEqual(plan_jobs(request)[0].sample_name, 'output')
        self.assertEqual(named_request.samples[0].name, 'signal')
        self.assertEqual(named_request.samples[0].output_stem, 'signal')
        self.assertEqual(
            plan_jobs(named_request)[0].output_file, 'output_signal_0000.root'
        )

    def test_resolves_direct_grid_cli_input_file_list(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_script = root / 'analysis.py'
            key4hep_setup = root / 'setup.sh'
            input_list = root / 'inputs.txt'
            self.write_modern_analysis(analysis_script)
            key4hep_setup.touch()
            input_list.write_text(
                'root://storage.example.org//data/a.root\n', encoding='utf-8'
            )
            args = self.parse_grid_arguments(
                str(analysis_script), ['--input-file-list', str(input_list)]
            )

            request = create_grid_submission_request(
                args,
                self.load_analysis_module(analysis_script),
                key4hep_setup=str(key4hep_setup),
            )

        self.assertEqual(
            request.samples[0].inputs,
            ('root://storage.example.org//data/a.root',),
        )

    def test_rejects_local_grid_input_files(self) -> None:
        with patch('grid_submission.resolve_inputs') as resolve:
            with self.assertRaisesRegex(
                GridSubmissionError,
                'In XRootD input mode, grid input files and directories',
            ) as error:
                _resolve_grid_sample_inputs(
                    'input-files', ['/local/input.root'], 'signal'
                )

        self.assertIn('--input-lfn-list', str(error.exception))
        resolve.assert_not_called()

    def test_stages_optional_analysis_includes_in_lfn_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_script = root / 'analysis.py'
            key4hep_setup = root / 'setup.sh'
            include_file = root / 'helpers' / 'functions.h'
            include_file.parent.mkdir()
            include_file.write_text('int answer() { return 42; }\n', encoding='utf-8')
            self.write_modern_analysis(
                analysis_script,
                '        self.include_paths = ["helpers/functions.h"]\n'
                '        self.samples = {"signal": {}}\n',
            )
            key4hep_setup.touch()
            args = self.parse_grid_arguments(
                str(analysis_script),
                self.grid_arguments(self.write_lfn_input(root)),
            )

            request = create_grid_submission_request(
                args,
                self.load_analysis_module(analysis_script),
                key4hep_setup=str(key4hep_setup),
                analysis_include_archive_path=root / 'includes.tar.gz',
            )

            with tarfile.open(request.analysis_include_archive) as archive:
                self.assertEqual(archive.getnames(), ['helpers/functions.h'])
            self.assertIsNotNone(request.analysis_include_archive)

    def test_requires_modern_analysis_style_in_lfn_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_script = root / 'analysis.py'
            key4hep_setup = root / 'setup.sh'
            analysis_script.write_text('value = 1\n', encoding='utf-8')
            key4hep_setup.touch()
            args = self.parse_grid_arguments(
                str(analysis_script),
                self.grid_arguments(self.write_lfn_input(root)),
            )

            with self.assertRaisesRegex(GridSubmissionError, 'requires an Analysis class'):
                create_grid_submission_request(
                    args,
                    self.load_analysis_module(analysis_script),
                    key4hep_setup=str(key4hep_setup),
                )

    def test_keeps_custom_arguments_separate_from_worker_options(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            analysis_script = root / 'analysis.py'
            key4hep_setup = root / 'setup.sh'
            self.write_modern_analysis(analysis_script)
            key4hep_setup.touch()
            args = self.parse_grid_arguments(
                str(analysis_script),
                [
                    *self.grid_arguments(self.write_lfn_input(root)),
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
            )

            self.assertEqual(request.run_arguments, tuple(args.remaining))
            self.assertEqual(request.worker_stride, 5)
            self.assertEqual(request.worker_ncpus, 2)
            self.assertEqual(request.worker_output_format, 'rntuple')

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
                        str(
                            REPOSITORY_ROOT
                            / 'scripts'
                            / 'dirac'
                            / 'run_dirac_submission.sh'
                        ),
                        str(REPOSITORY_ROOT / 'python' / 'dirac_submit_helper.py'),
                    ],
                )
                self.assertEqual(env['PATH'], '/usr/bin:/bin')
                self.assertNotIn('KEY4HEP_STACK', env)
                request_path = Path(env['FCCANALYSES_SUBMISSION_REQUEST'])
                request = SubmissionRequest.read_json(request_path)
                self.assertEqual(request.key4hep_setup, str(key4hep_setup.resolve()))
                self.assertIsNotNone(request.user_build_payload)
                payload_path = Path(request.user_build_payload.archive_path)
                self.assertTrue(payload_path.is_file())
                temporary_paths.extend([request_path, payload_path])

            with patch.dict(
                'os.environ',
                {
                    'KEY4HEP_STACK': str(key4hep_setup),
                    'FCCANA_LOCAL_DIR': str(REPOSITORY_ROOT),
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
