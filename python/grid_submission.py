'''Frontend-only validation for DIRAC grid submissions.

This module deliberately has no DIRAC or ILCDIRAC imports. It turns the
parsed grid command into the data-only request consumed by the isolated DIRAC
submission process.
'''

import argparse
import logging
import math
import os
from pathlib import Path, PurePosixPath
import subprocess
import tarfile
import tempfile
from types import ModuleType
from typing import Any

from anascript import get_sample_input_source, validate_sample_list
from input_resolver import (
    InputResolutionError,
    normalize_input_path,
    read_input_file_list,
    resolve_directory,
    resolve_inputs,
)

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

class GridSubmissionError(ValueError):
    '''Raised when frontend grid-submission validation fails.'''


def create_grid_submission_request(
    args: argparse.Namespace,
    analysis_module: ModuleType,
    key4hep_setup: str | None = None,
    user_build_payload: UserBuildPayload | None = None,
    analysis_include_archive_path: Path | None = None,
) -> SubmissionRequest:
    '''Create a backend-neutral grid request from validated CLI arguments.'''
    analysis_script = _require_file(args.anascript_path, 'Analysis script')
    selected_key4hep_setup = _require_key4hep_setup(key4hep_setup)
    output_file = _require_single_name(args.output, '--output')
    output_path = _require_catalogue_path(args.output_dir)
    output_se = _require_optional_nonempty_string(args.output_se, '--output-se')
    destination_site = _require_optional_nonempty_string(args.site, '--site')

    try:
        run_arguments = tuple(getattr(args, 'remaining', []))
        n_chunks = getattr(args, 'n_chunks', None)
        analysis_class = _create_analysis_instance(
            analysis_module, analysis_script, args
        )
        _reject_sample_event_limits(analysis_class)
        has_cli_input = (
            args.input is not None or args.input_file_list is not None
        )
        sample_name = (
            _require_single_name(args.sample_name, '--sample-name')
            if args.sample_name is not None
            and (args.input_lfn_list is not None or has_cli_input)
            else None
        )
        if args.input_lfn_list is not None:
            input_mode = 'dirac-lfn'
            samples = (_resolve_grid_cli_lfn_sample(args, sample_name),)
        elif has_cli_input:
            input_mode = 'xrootd'
            samples = (_resolve_grid_cli_input_sample(args, sample_name),)
        else:
            input_mode, samples = _resolve_analysis_samples(args, analysis_class)

        analysis_include_archive = _create_analysis_include_archive(
            analysis_script,
            analysis_class,
            analysis_include_archive_path,
        )

        return SubmissionRequest(
            analysis_script=str(analysis_script),
            input_mode=input_mode,
            samples=samples,
            files_per_job=args.files_per_job,
            n_chunks=n_chunks,
            run_arguments=run_arguments,
            worker_stride=args.stride,
            worker_output_format=args.output_format,
            worker_ncpus=args.ncpus,
            output_file=output_file,
            output_path=output_path,
            output_se=output_se,
            key4hep_setup=str(selected_key4hep_setup),
            job_name='FCCAnalyses',
            job_group='FCCAnalyses_Grid',
            submit_mode=args.mode,
            destination_site=destination_site,
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


def _read_lfn_input(path_value: str) -> tuple[str, ...]:
    '''Read one concrete, whitespace-normalised DIRAC LFN per text-file line.'''
    path = _require_file(path_value, 'LFN input file')
    if path.suffix != '.txt':
        raise GridSubmissionError('--input-lfn-list must name a .txt file.')
    try:
        input_lfns = tuple(
            line.strip()
            for line in path.read_text(encoding='utf-8').splitlines()
            if line.strip()
        )
    except OSError as error:
        raise GridSubmissionError(f'Cannot read LFN input file: {path}') from error
    if not input_lfns:
        raise GridSubmissionError('--input-lfn-list contains no LFNs.')
    for lfn in input_lfns:
        _validate_lfn(lfn)
    _require_unique_inputs(input_lfns, 'input LFN')
    return input_lfns


def _resolve_grid_cli_lfn_sample(
    args: argparse.Namespace,
    sample_name: str | None,
) -> ResolvedSample:
    '''Resolve the command-line LFN list as one independent grid sample.'''
    return ResolvedSample(
        name=sample_name,
        output_stem=sample_name,
        inputs=_read_lfn_input(args.input_lfn_list),
        chunks=1,
        stride=None,
    )


def _resolve_grid_cli_input_sample(
    args: argparse.Namespace,
    sample_name: str | None,
) -> ResolvedSample:
    '''Resolve one independent XRootD sample supplied on the command line.'''
    try:
        if args.input is not None:
            input_urls = resolve_inputs(args.input)
        else:
            input_urls = read_input_file_list(args.input_file_list)
    except InputResolutionError as error:
        raise GridSubmissionError(str(error)) from error
    _require_grid_urls(input_urls)
    return ResolvedSample(
        name=sample_name or 'output',
        output_stem=sample_name,
        inputs=tuple(input_urls),
        chunks=1,
        stride=None,
    )


def _resolve_analysis_samples(
    args: argparse.Namespace,
    analysis_class: Any,
) -> tuple[str, tuple[ResolvedSample, ...]]:
    '''Resolve one uniform Analysis input mode to concrete worker inputs.'''
    global_lfn_list = getattr(analysis_class, 'input_lfn_list', None)
    if global_lfn_list is not None:
        if not isinstance(global_lfn_list, str):
            raise GridSubmissionError('Analysis.input_lfn_list must be a string.')
        provided_samples = getattr(
            analysis_class,
            'samples',
            getattr(analysis_class, 'process_list', None),
        )
        if (
            provided_samples
            or getattr(analysis_class, 'input_dir', None) is not None
        ):
            raise GridSubmissionError(
                'Analysis.input_lfn_list cannot be combined with XRootD inputs.'
            )
        return 'dirac-lfn', (
            ResolvedSample(
                name=None,
                output_stem=None,
                inputs=_read_lfn_input(global_lfn_list),
                chunks=1,
                stride=None,
            ),
        )

    samples = _validated_analysis_samples(analysis_class)
    input_dir = getattr(analysis_class, 'input_dir', None)
    if input_dir is not None and not isinstance(input_dir, str):
        raise GridSubmissionError('Analysis.input_dir must be a string.')

    configured_sources = tuple(
        (
            sample_name,
            sample,
            *get_sample_input_source(sample, input_dir, None),
        )
        for sample_name, sample in samples.items()
    )
    input_modes = {
        'dirac-lfn' if source == 'input-lfn-list' else 'xrootd'
        for _, _, source, _ in configured_sources
    }
    if len(input_modes) != 1:
        raise GridSubmissionError(
            'Grid submission cannot mix XRootD and DIRAC LFN sample inputs.'
        )

    resolved_samples = []
    for sample_name, sample, input_source, input_value in configured_sources:
        if input_source == 'input-lfn-list':
            input_mode = 'dirac-lfn'
            inputs = _read_lfn_input(input_value)
        else:
            input_mode = 'xrootd'
            try:
                inputs = _resolve_grid_sample_inputs(
                    input_source, input_value, sample_name
                )
            except InputResolutionError as error:
                raise GridSubmissionError(str(error)) from error
            fraction = sample['fraction']
            if fraction < 1.0:
                inputs = _apply_fraction(inputs, fraction, sample_name)
        LOGGER.info(
            'Resolved %d input file(s) for sample %s.',
            len(inputs),
            sample_name,
        )

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
        resolved_samples.append(
            ResolvedSample(
                name=sample_name,
                output_stem=sample['output-stem'],
                inputs=tuple(inputs),
                chunks=chunks,
                stride=sample['stride'],
            )
        )
    return input_modes.pop(), tuple(resolved_samples)


def _resolve_grid_sample_inputs(
    input_source: str | None,
    input_value: Any,
    sample_name: str,
) -> list[str]:
    '''Resolve one configured sample input source to grid-readable URLs.'''
    if input_source == 'input-files':
        input_urls = [normalize_input_path(path) for path in input_value]
        _require_grid_urls(input_urls)
        return resolve_inputs(input_urls)
    if input_source == 'input-file-list':
        input_urls = read_input_file_list(input_value)
        _require_grid_urls(input_urls)
        return input_urls
    if input_source in {'sample-input-dir', 'global-input-dir'}:
        directory = normalize_input_path(input_value)
        if input_source == 'global-input-dir':
            directory = directory.rstrip('/') + '/' + sample_name
        _require_grid_urls([directory])
        return resolve_directory(directory)
    raise GridSubmissionError(
        f'Sample {sample_name!r} has no XRootD input source. Set a per-sample '
        'source or Analysis.input_dir, or use --input-lfn-list <list.txt> for '
        'DIRAC-registered input files.'
    )


def _require_grid_urls(input_urls: list[str]) -> None:
    for input_url in input_urls:
        if not input_url.startswith('root://'):
            raise GridSubmissionError(
                'In XRootD input mode, grid input files and directories must use '
                'mounted EOS paths or root:// URLs; local input paths cannot be '
                'staged in this mode. For DIRAC-registered input files, use '
                '--input-lfn-list <list.txt> containing their LFNs.'
            )


def _create_analysis_include_archive(
    analysis_script: Path,
    analysis_class: Any,
    archive_path: Path | None,
) -> Path | None:
    '''Archive Analysis.include_paths while preserving analysis-relative paths.'''
    include_paths = getattr(analysis_class, 'include_paths', None)
    if not include_paths:
        return None
    if not isinstance(include_paths, (list, tuple)):
        raise GridSubmissionError('Analysis.include_paths must be a list of paths.')

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


def _create_analysis_instance(
    analysis_module: ModuleType,
    analysis_script: Path,
    args: argparse.Namespace,
) -> Any:
    '''Construct an Analysis instance from an already loaded module.'''
    if not hasattr(analysis_module, 'Analysis'):
        raise GridSubmissionError(
            'Grid submission requires an Analysis class to be defined '
            'in the analysis script.'
        )

    constructor_arguments = vars(args).copy()
    constructor_arguments['unknown'] = list(getattr(args, 'remaining', []))
    try:
        return analysis_module.Analysis(constructor_arguments)
    except Exception as error:
        raise GridSubmissionError(
            f'Could not construct Analysis from {analysis_script}: {error}'
        ) from error


def _validated_analysis_samples(analysis_class: Any) -> dict[str, dict[str, Any]]:
    '''Select and validate samples.'''
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


def _reject_sample_event_limits(analysis_class: Any) -> None:
    '''Reject sample event limits with ambiguous multi-job semantics.'''
    provided_samples = getattr(
        analysis_class,
        'samples',
        getattr(analysis_class, 'process_list', None),
    )
    if not isinstance(provided_samples, dict):
        return
    for sample_name, sample in provided_samples.items():
        if isinstance(sample, dict) and sample.get('n-events-max') is not None:
            raise GridSubmissionError(
                'Sample-level n-events-max is not supported for grid '
                f'submission (sample {sample_name!r}) because one sample '
                'may be split across multiple jobs.'
            )


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


def submit_grid_submission(
    args: argparse.Namespace,
    analysis_module: ModuleType,
) -> None:
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
            analysis_module,
            key4hep_setup=key4hep_setup,
            user_build_payload=user_build_payload,
            analysis_include_archive_path=(
                Path(directory) / 'analysis-includes.tar.gz'
            ),
        )
        request_path = Path(directory) / 'submission-request.json'
        request.write_json(request_path)

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


def _validate_lfn(lfn: str) -> None:
    path = PurePosixPath(lfn)
    if not lfn.startswith('/'):
        raise GridSubmissionError(f'input LFN must be absolute: {lfn}')
    if path.name in {'', '.', '..'}:
        raise GridSubmissionError(f'input LFN must name a file: {lfn}')
    if '..' in path.parts:
        raise GridSubmissionError(f"input LFN must not contain '..': {lfn}")


def _require_unique_inputs(
    inputs: tuple[str, ...] | list[str], description: str
) -> None:
    seen = set()
    for value in inputs:
        if value in seen:
            raise GridSubmissionError(f'duplicate {description}: {value}')
        seen.add(value)


def _require_single_name(value: object, option: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or value in {'.', '..'}
        or PurePosixPath(value).name != value
    ):
        raise GridSubmissionError(f'{option} must be a single name, not a path.')
    return value


def _require_catalogue_path(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise GridSubmissionError('--output-dir must be a non-empty relative path.')
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts:
        raise GridSubmissionError(
            '--output-dir must be a relative catalogue path without "..".'
        )
    return value


def _require_optional_nonempty_string(value: object, option: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise GridSubmissionError(f'{option} must be a non-empty string.')
    return value


def _require_key4hep_setup(override: str | None) -> Path:
    path_value = override or os.environ.get('KEY4HEP_STACK')
    if not path_value:
        raise GridSubmissionError(
            'KEY4HEP_STACK is unset. Source the intended Key4hep stack before '
            'submitting to the grid.'
        )
    return _require_file(path_value, 'Key4hep setup script')
