'''Frontend-only validation for DIRAC grid submissions.

This module deliberately has no DIRAC or ILCDIRAC imports. It turns the
parsed grid command into the data-only request consumed by the isolated DIRAC
submission process.
'''

import argparse
import importlib.util
import logging
import math
import os
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile
from typing import Any, Optional

from anascript import validate_sample_list

from software_payload import (
    SoftwarePayloadError,
    create_user_build_archive,
    validate_user_build,
)
from submission import (
    ResolvedSample,
    SubmissionRequest,
    SubmissionValidationError,
    UserBuildPayload,
    generate_submission_id,
)


LOGGER = logging.getLogger('FCCAnalyses.grid_submission')

_GRID_OWNED_RUN_OPTIONS = {
    '-i',
    '--input',
    '-f',
    '--input-file-list',
    '--files-list',
    '-o',
    '--output',
    '-s',
    '--sample-name',
    '--n-chunks',
}


class GridSubmissionError(ValueError):
    '''Raised when frontend grid-submission validation fails.'''


def create_grid_submission_request(
    args: argparse.Namespace,
    key4hep_setup: Optional[str] = None,
    user_build_payload: Optional[UserBuildPayload] = None,
    analysis_include_archive_path: Optional[Path] = None,
) -> SubmissionRequest:
    '''Create a backend-neutral grid request from validated CLI arguments.'''
    analysis_script = _require_file(args.anascript_path, 'Analysis script')
    selected_key4hep_setup = _require_key4hep_setup(key4hep_setup)

    if user_build_payload is not None and not args.ship_local_build:
        raise GridSubmissionError(
            'A user-build payload requires --ship-local-build.'
        )

    try:
        run_arguments = _validated_run_arguments(getattr(args, 'remaining', []))
        n_chunks = getattr(args, 'n_chunks', None)
        analysis_class = _load_analysis_class(analysis_script, args)
        _warn_ignored_sample_event_limits(analysis_class)
        if args.lfn_input is not None:
            input_mode = 'dirac-lfn'
            input_lfns = _read_lfn_input(args.lfn_input)
            samples = ()
            lfn_sample_name = args.sample_name
        else:
            input_mode = 'xrootd'
            input_lfns = ()
            samples = _resolve_analysis_samples(args, analysis_script, analysis_class)
            lfn_sample_name = None

        analysis_include_archive = _create_analysis_include_archive(
            analysis_script,
            analysis_class,
            analysis_include_archive_path,
        )

        return SubmissionRequest(
            analysis_script=str(analysis_script),
            input_mode=input_mode,
            input_lfns=input_lfns,
            samples=samples,
            files_per_job=args.files_per_job,
            n_chunks=n_chunks,
            lfn_sample_name=lfn_sample_name,
            run_arguments=run_arguments,
            output_file=args.output,
            output_path=args.output_dir,
            output_se=args.output_se,
            key4hep_setup=str(selected_key4hep_setup),
            job_name='FCCAnalyses',
            job_group='FCCAnalyses_Grid',
            submit_mode=args.mode,
            destination_site=args.site,
            submission_id=generate_submission_id(),
            user_build_payload=user_build_payload,
            analysis_include_archive=(
                str(analysis_include_archive)
                if analysis_include_archive is not None
                else None
            ),
        )
    except SubmissionValidationError as error:
        raise GridSubmissionError(str(error)) from error


def _validated_run_arguments(arguments: list[str]) -> tuple[str, ...]:
    '''Validate explicit fccanalysis-run arguments passed after ``--``.'''
    for argument in arguments:
        option = argument.split('=', 1)[0]
        if option in _GRID_OWNED_RUN_OPTIONS:
            raise GridSubmissionError(
                f'Pass-through argument {option} is controlled by grid submission.'
            )
    return tuple(arguments)


def _read_lfn_input(path_value: str) -> tuple[str, ...]:
    '''Read one concrete, whitespace-normalised DIRAC LFN per text-file line.'''
    path = _require_file(path_value, 'LFN input file')
    if path.suffix != '.txt':
        raise GridSubmissionError('--lfn-input must name a .txt file.')
    try:
        return tuple(
            line.strip()
            for line in path.read_text(encoding='utf-8').splitlines()
            if line.strip()
        )
    except OSError as error:
        raise GridSubmissionError(f'Cannot read LFN input file: {path}') from error


def _resolve_analysis_samples(
    args: argparse.Namespace,
    analysis_script: Path,
    analysis_class: Any,
) -> tuple[ResolvedSample, ...]:
    '''Resolve the modern Analysis input model to concrete XRootD URLs.'''
    samples = _validated_analysis_samples(analysis_class)
    input_dir = getattr(analysis_class, 'input_dir', None)
    if input_dir is not None and not isinstance(input_dir, str):
        raise GridSubmissionError('Analysis.input_dir must be a string.')

    resolved_samples = []
    for sample_name, sample in samples.items():
        sample_input_dir = sample['input-dir']
        if sample_input_dir is None:
            if input_dir is None:
                raise GridSubmissionError(
                    f'Sample {sample_name!r} has no input-dir and '
                    'Analysis.input_dir is unset.'
                )
            sample_input_dir = _join_input_directory(input_dir, sample_name)
        input_urls = _discover_xrootd_root_files(sample_input_dir)
        if not input_urls:
            raise GridSubmissionError(
                f'No immediate .root files found for sample {sample_name!r} '
                f'in {sample_input_dir}.'
            )
        fraction = sample['fraction']
        if fraction < 1.0:
            input_urls = _apply_fraction(input_urls, fraction, sample_name)

        chunks = sample['chunks']
        if args.files_per_job is not None and chunks != 1:
            LOGGER.warning(
                '--files-per-job overrides chunks=%s for sample %s.',
                chunks,
                sample_name,
            )
        n_chunks = getattr(args, 'n_chunks', None)
        if n_chunks is not None and chunks not in (1, n_chunks):
            LOGGER.warning(
                '--n-chunks=%s overrides chunks=%s for sample %s.',
                n_chunks,
                chunks,
                sample_name,
            )
        LOGGER.info(
            'Resolved %d input file(s) for sample %s.',
            len(input_urls),
            sample_name,
        )
        resolved_samples.append(
            ResolvedSample(
                name=sample_name,
                output_stem=sample['output-stem'],
                input_urls=tuple(input_urls),
                chunks=chunks,
                stride=sample['stride'],
            )
        )
    return tuple(resolved_samples)


def _create_analysis_include_archive(
    analysis_script: Path,
    analysis_class: Any,
    archive_path: Optional[Path],
) -> Optional[Path]:
    '''Archive Analysis.include_paths while preserving analysis-relative paths.'''
    include_paths = getattr(analysis_class, 'include_paths', None)
    if include_paths is None:
        return None
    if not isinstance(include_paths, (list, tuple)):
        raise GridSubmissionError('Analysis.include_paths must be a list of paths.')
    if not include_paths:
        return None
    if archive_path is None:
        raise GridSubmissionError(
            'Analysis.include_paths cannot be staged without an archive destination.'
        )

    analysis_directory = analysis_script.parent.resolve()
    resolved_includes = []
    seen_paths = set()
    for value in include_paths:
        if not isinstance(value, str) or not value:
            raise GridSubmissionError(
                'Analysis.include_paths entries must be non-empty strings.'
            )
        relative_path = Path(value)
        if relative_path.is_absolute() or '..' in relative_path.parts:
            raise GridSubmissionError(
                f'Analysis include path must stay below the analysis directory: {value}'
            )
        normalized_path = relative_path.as_posix()
        if normalized_path in seen_paths:
            raise GridSubmissionError(
                f'Analysis.include_paths contains a duplicate path: {value}'
            )
        seen_paths.add(normalized_path)
        try:
            source_path = (analysis_directory / relative_path).resolve(strict=True)
            source_path.relative_to(analysis_directory)
        except (FileNotFoundError, ValueError) as error:
            raise GridSubmissionError(
                f'Analysis include file is missing or outside the analysis directory: '
                f'{value}'
            ) from error
        if not source_path.is_file():
            raise GridSubmissionError(f'Analysis include is not a file: {value}')
        resolved_includes.append((normalized_path, source_path))

    try:
        with tarfile.open(archive_path, 'w:gz') as archive:
            for relative_path, source_path in resolved_includes:
                archive.add(source_path, arcname=relative_path, recursive=False)
    except (OSError, tarfile.TarError) as error:
        raise GridSubmissionError(
            f'Cannot create analysis include archive {archive_path}: {error}'
        ) from error

    return archive_path.resolve()


def _load_analysis_class(analysis_script: Path, args: argparse.Namespace) -> Any:
    '''Import one Analysis-style script and construct its Analysis instance.'''
    try:
        specification = importlib.util.spec_from_file_location(
            'fccanalysis_grid', analysis_script
        )
        if specification is None or specification.loader is None:
            raise GridSubmissionError(f'Cannot load analysis script: {analysis_script}')
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except (OSError, SyntaxError) as error:
        raise GridSubmissionError(
            f'Cannot load analysis script {analysis_script}: {error}'
        ) from error
    if not hasattr(module, 'Analysis'):
        raise GridSubmissionError(
            'Grid submission requires a modern Analysis-style analysis script.'
        )

    constructor_arguments = vars(args).copy()
    constructor_arguments['unknown'] = list(getattr(args, 'remaining', []))
    try:
        return module.Analysis(constructor_arguments)
    except Exception as error:
        raise GridSubmissionError(
            f'Could not construct Analysis from {analysis_script}: {error}'
        ) from error


def _validated_analysis_samples(analysis_class: Any) -> dict[str, dict[str, Any]]:
    '''Select and validate samples, retaining the modern process-list alias.'''
    if hasattr(analysis_class, 'samples'):
        provided_samples = analysis_class.samples
    elif hasattr(analysis_class, 'process_list'):
        provided_samples = analysis_class.process_list
    else:
        raise GridSubmissionError(
            'Analysis must define samples (or the deprecated process_list).'
        )
    if not isinstance(provided_samples, dict):
        raise GridSubmissionError('Analysis samples must be a dictionary.')
    try:
        samples = validate_sample_list(provided_samples)
    except SystemExit as error:
        raise GridSubmissionError('Analysis samples are invalid.') from error
    if not samples:
        raise GridSubmissionError('Analysis samples must not be empty.')
    return samples


def _warn_ignored_sample_event_limits(analysis_class: Any) -> None:
    '''Warn about sample event limits that grid planning never applies.'''
    provided_samples = getattr(
        analysis_class,
        'samples',
        getattr(analysis_class, 'process_list', None),
    )
    if not isinstance(provided_samples, dict):
        return
    for sample_name, sample in provided_samples.items():
        if isinstance(sample, dict) and sample.get('n-events-max') is not None:
            LOGGER.warning(
                'Ignoring sample-level n-events-max during grid submission '
                'for sample %s. To apply an event limit independently to '
                'every planned job, pass --nevents after --.',
                sample_name,
            )


def _join_input_directory(input_dir: str, sample_name: str) -> str:
    if input_dir.startswith('root://'):
        return input_dir.rstrip('/') + '/' + sample_name
    return os.path.join(input_dir, sample_name)


def _discover_xrootd_root_files(directory: str) -> list[str]:
    '''List immediate ROOT files in an EOS/XRootD directory through xrdfs.'''
    host, remote_directory = _xrootd_location(directory)
    try:
        result = subprocess.run(
            ['xrdfs', host, 'ls', '-l', remote_directory],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        raise GridSubmissionError(
            'xrdfs is unavailable; source a Key4hep environment with XRootD.'
        ) from error
    except subprocess.CalledProcessError as error:
        message = error.stderr.strip() or error.stdout.strip() or str(error)
        raise GridSubmissionError(
            f'Cannot list XRootD directory {directory} through {host}: {message}'
        ) from error

    files = []
    for line in result.stdout.splitlines():
        entry = _parse_xrdfs_listing(line)
        if entry is None:
            continue
        entry_type, path = entry
        if entry_type == 'd' or not path.endswith('.root'):
            continue
        files.append(f'root://{host}//{path.lstrip("/")}')
    return sorted(set(files))


def _xrootd_location(directory: str) -> tuple[str, str]:
    '''Turn an EOS path or root URL into an xrdfs host/path pair.'''
    if directory.startswith('root://'):
        match = re.fullmatch(r'root://([^/]+)(/.*)', directory)
        if match is None:
            raise GridSubmissionError(f'Invalid XRootD directory URL: {directory}')
        return match.group(1), '/' + match.group(2).lstrip('/')
    if not directory.startswith('/eos/'):
        raise GridSubmissionError(
            f'Input directory must be an /eos/... path or root:// URL: {directory}'
        )
    if directory.startswith('/eos/experiment/'):
        return 'eospublic.cern.ch', directory
    if directory.startswith('/eos/user/'):
        return 'eosuser.cern.ch', directory
    raise GridSubmissionError(
        f'Cannot infer an EOS redirector for input directory: {directory}'
    )


def _parse_xrdfs_listing(line: str) -> Optional[tuple[str, str]]:
    '''Extract the entry type and path from one ``xrdfs ls -l`` line.'''
    parts = line.split()
    if not parts:
        return None
    if len(parts) >= 2 and parts[0][0:1] in {'-', 'd'}:
        return parts[0][0], parts[-1]
    return '-', parts[-1]


def _apply_fraction(
    input_urls: list[str],
    fraction: float,
    sample_name: str,
) -> list[str]:
    '''Select whole files according to the existing per-sample fraction rule.'''
    event_counts = [_event_count(url) for url in input_urls]
    target = math.floor(sum(event_counts) * fraction)
    if target <= 0:
        raise GridSubmissionError(
            f'Fraction {fraction} leaves no events for sample {sample_name!r}.'
        )
    selected = []
    selected_events = 0
    for url, count in zip(input_urls, event_counts):
        if selected_events >= target:
            break
        selected.append(url)
        selected_events += count
    LOGGER.info(
        'Applied fraction %s to sample %s: %d/%d files selected for '
        '%d requested events.',
        fraction,
        sample_name,
        len(selected),
        len(input_urls),
        target,
    )
    return selected


def _event_count(url: str) -> int:
    '''Read the ``events`` entry count through ROOT for fraction planning.'''
    try:
        import ROOT  # type: ignore
    except ImportError as error:
        raise GridSubmissionError(
            'ROOT is unavailable for fraction-based XRootD planning.'
        ) from error
    input_file = ROOT.TFile.Open(url, 'READ')
    if not input_file or input_file.IsZombie():
        raise GridSubmissionError(f'Cannot open XRootD input file: {url}')
    try:
        events = input_file.Get('events')
        if events is None:
            raise GridSubmissionError(f'Input file has no events tree: {url}')
        return int(events.GetEntries())
    finally:
        input_file.Close()


def submit_grid_submission(args: argparse.Namespace) -> None:
    '''Start the isolated DIRAC helper for one parsed grid submission.'''
    source_root = _fccanalyses_root()
    runner = _require_file(
        str(source_root / 'scripts' / 'dirac' / 'run_dirac_submission.sh'),
        'DIRAC submission launcher',
    )
    helper = _require_file(
        str(source_root / 'python' / 'dirac_submit_helper.py'),
        'DIRAC submission helper',
    )

    with tempfile.TemporaryDirectory(prefix='fccanalyses-dirac-') as directory:
        user_build_payload = None
        key4hep_setup = None
        if args.ship_local_build:
            try:
                build = validate_user_build()
                archive = create_user_build_archive(
                    build,
                    Path(directory) / 'fccanalyses-payload.tar.gz',
                )
            except SoftwarePayloadError as error:
                raise GridSubmissionError(str(error)) from error
            key4hep_setup = str(build.key4hep_setup)
            user_build_payload = UserBuildPayload(
                archive_path=str(archive.path),
                size_bytes=archive.size_bytes,
            )

        request = create_grid_submission_request(
            args,
            key4hep_setup=key4hep_setup,
            user_build_payload=user_build_payload,
            analysis_include_archive_path=(
                Path(directory) / 'analysis-includes.tar.gz'
            ),
        )
        request_path = Path(directory) / 'submission-request.json'
        request.write_json(request_path)

        print('Preparing DIRAC grid submission.', flush=True)
        print(f'Worker Key4hep setup: {request.key4hep_setup}', flush=True)
        if user_build_payload is None:
            print('Worker runtime: FCCAnalyses from the Key4hep stack', flush=True)
        else:
            print(
                'Worker runtime: shipped local FCCAnalyses build '
                f'({user_build_payload.size_bytes / 1024**2:.1f} MiB)',
                flush=True,
            )
        print('Starting isolated DIRAC submission client.', flush=True)

        try:
            subprocess.run(
                [str(runner), str(helper)],
                check=True,
                env=_dirac_environment(request_path),
            )
        except subprocess.CalledProcessError as error:
            raise GridSubmissionError(
                f'DIRAC submission helper failed with exit code {error.returncode}.'
            ) from error


def _fccanalyses_root() -> Path:
    '''Return the checkout or release root selected by the FCCAnalyses setup.'''
    local_dir = os.environ.get('FCCANA_LOCAL_DIR')
    if local_dir:
        return Path(local_dir).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def _dirac_environment(request_path: Path) -> dict[str, str]:
    '''Return the minimum environment required by the clean DIRAC child.'''
    inherited_names = (
        'HOME',
        'USER',
        'LOGNAME',
        'TMPDIR',
        'LANG',
        'LC_ALL',
        'TERM',
        'X509_USER_CERT',
        'X509_USER_KEY',
        'X509_USER_PROXY',
        'DIRACSYSCONFIG',
        'DIRAC_SETUP',
        'DIRAC_GROUP',
        'FCC_GRID_SETUP',
    )
    environment = {
        name: os.environ[name]
        for name in inherited_names
        if os.environ.get(name)
    }
    environment['PATH'] = '/usr/bin:/bin'
    environment['FCCANALYSES_SUBMISSION_REQUEST'] = str(request_path)
    return environment


def _require_file(path_value: str, description: str) -> Path:
    path = Path(path_value).expanduser().resolve()
    if not path.is_file():
        raise GridSubmissionError(f'{description} not found: {path}')
    return path


def _require_key4hep_setup(override: Optional[str]) -> Path:
    path_value = override or os.environ.get('KEY4HEP_STACK')
    if not path_value:
        raise GridSubmissionError(
            'KEY4HEP_STACK is unset. Source the intended Key4hep stack before '
            'submitting to the grid.'
        )
    return _require_file(path_value, 'Key4hep setup script')
