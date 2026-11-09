'''Submit planned FCCAnalyses jobs through ILCDIRAC.

This program is executed only by ``run_dirac_submission.sh`` after that script
has created the supported DIRAC client environment. Keep ILCDIRAC imports in
this file so the public FCCAnalyses process remains independent of DIRAC.
'''

import logging
import os
import shlex
import sys
import tempfile
from io import StringIO
from pathlib import Path, PurePosixPath

from submission import SubmissionRequest, SubmissionValidationError, plan_jobs

LOGGER = logging.getLogger('FCCAnalyses.grid_helper')


class MultiLineFormatter(logging.Formatter):
    '''
    Multi-line formatter.
    '''
    def get_header_length(self, record):
        '''
        Get the header length of a given record.
        '''
        return len(super().format(logging.LogRecord(
            name=record.name,
            level=record.levelno,
            pathname=record.pathname,
            lineno=record.lineno,
            msg='', args=(), exc_info=None
        )))

    def format(self, record):
        '''
        Format a record with added indentation.
        '''
        indent = ' ' * self.get_header_length(record)
        head, *trailing = super().format(record).splitlines(True)
        return head + ''.join(indent + line for line in trailing)

# DIRAC configuration, including DIRACSYSCONFIG and ~/.dirac.cfg, is loaded by
# parseCommandLine(). It must run before importing and using ILCDIRAC APIs.
from DIRAC.Core.Base.Script import Script

Script.parseCommandLine()

from DIRAC import gConfig
from DIRAC.ConfigurationSystem.Client.Helpers import Registry
from DIRAC.ConfigurationSystem.Client.Helpers.Operations import Operations
from DIRAC.Core.Security.ProxyInfo import getProxyInfo
from DIRAC.Resources.Catalog.FileCatalog import FileCatalog
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.Applications import GenericApplication
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob


def _require_file(path: Path, description: str) -> Path:
    '''Resolve a required local file.'''
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise RuntimeError(f'{description} not found: {resolved}')
    return resolved


def _load_request() -> SubmissionRequest:
    '''Load the data-only request supplied by the Key4hep-side frontend.'''
    request_path = os.environ.get('FCCANALYSES_SUBMISSION_REQUEST')
    if not request_path:
        raise RuntimeError('FCCANALYSES_SUBMISSION_REQUEST is unset.')
    try:
        return SubmissionRequest.read_json(Path(request_path))
    except SubmissionValidationError as error:
        raise RuntimeError(f'Invalid grid submission request: {error}') from error


def _require_user_build_archive(request: SubmissionRequest) -> Path | None:
    '''Return the optional archive that DIRAC stages through the input sandbox.'''
    if request.user_build_payload is None:
        return None
    return _require_file(
        Path(request.user_build_payload.archive_path),
        'User-build payload archive',
    )


def _require_analysis_include_archive(request: SubmissionRequest) -> Path | None:
    '''Return the optional archive containing Analysis.include_paths files.'''
    if request.analysis_include_archive is None:
        return None
    return _require_file(
        Path(request.analysis_include_archive),
        'Analysis include archive',
    )


def _require_local_storage_element() -> str:
    '''Return the LocalSE required by DIRAC's local execution mode.'''
    local_se = gConfig.getValue('/LocalSite/LocalSE')
    if not local_se:
        raise RuntimeError(
            'DIRAC local mode requires /LocalSite/LocalSE. Define it in '
            '~/.dirac.cfg or a configuration file named by DIRACSYSCONFIG.'
        )
    return local_se


def _create_job(
    request: SubmissionRequest,
    planned_job,
    analysis_script: Path,
    worker_wrapper: Path,
    user_build_archive: Path | None,
    analysis_include_archive: Path | None,
    input_file_list: Path,
) -> UserJob:
    '''Translate one backend-neutral plan into an ILCDIRAC UserJob.'''
    job = UserJob()
    job.setName(planned_job.job_name)
    job.setJobGroup(request.job_group)
    job.setNumberOfProcessors(numberOfProcessors=1)
    job.setLogLevel('DEBUG')
    job.setOutputSandbox(['*.log', '*.sh', '*.py', 'localEnv.log', 'std.out', 'std.err'])

    input_sandbox = [str(analysis_script), str(input_file_list)]
    if user_build_archive is not None:
        input_sandbox.append(str(user_build_archive))
    if analysis_include_archive is not None:
        input_sandbox.append(str(analysis_include_archive))
    job.setInputSandbox(input_sandbox)

    if planned_job.input_mode == 'dirac-lfn':
        job.setInputData(list(planned_job.source_inputs))
    output_options = {'OutputPath': _dirac_output_path(planned_job)}
    if request.output_se is not None:
        output_options['OutputSE'] = request.output_se
    result = job.setOutputData(planned_job.output_file, **output_options)
    if not result['OK']:
        raise RuntimeError(f"Unable to set job output data: {result['Message']}")
    if request.destination_site:
        job.setDestination(request.destination_site)

    application = GenericApplication()
    application.setScript(str(worker_wrapper))
    environment_mode = 'clean' if request.submit_mode == 'local' else 'inherit'
    arguments = [
        '--env',
        environment_mode,
        '--key4hep-setup',
        request.key4hep_setup,
    ]
    if request.key4hep_release is not None:
        arguments.extend(['--key4hep-release', request.key4hep_release])
    if user_build_archive is not None:
        arguments.extend(['--payload-archive', user_build_archive.name])
    if analysis_include_archive is not None:
        arguments.extend(['--include-archive', analysis_include_archive.name])
    arguments.extend(['--', *planned_job.run_arguments])
    application.setArguments(shlex.join(arguments))
    job.append(application)
    return job


def _write_input_file_list(planned_job, directory: Path) -> Path:
    '''Write the worker-side list, which DIRAC transfers through the sandbox.'''
    input_file_list = directory / planned_job.input_list_filename
    input_file_list.write_text(
        '\n'.join(planned_job.worker_file_list_entries) + '\n',
        encoding='utf-8',
    )
    return input_file_list


def _user_lfn_root() -> str:
    '''Return the absolute DIRAC user LFN root for the active proxy.'''
    result = getProxyInfo()
    if not result or not result.get('OK'):
        message = result.get('Message', result) if result else 'no result returned'
        raise RuntimeError(f'Unable to read DIRAC proxy information: {message}')
    proxy_info = result.get('Value', {})
    username = proxy_info.get('username')
    virtual_organization = gConfig.getValue('/DIRAC/VirtualOrganization')
    if not virtual_organization and proxy_info.get('group'):
        virtual_organization = Registry.getVOForGroup(proxy_info['group'])
    if not username or not virtual_organization:
        raise RuntimeError(
            'Cannot determine the DIRAC user LFN root needed to check for an '
            'existing output LFN; refusing to submit without overwrite '
            'protection.'
        )
    prefix = Operations(vo=virtual_organization).getValue('LFNUserPrefix', 'user')
    return f'/{virtual_organization}/{prefix}/{username[0]}/{username}'


def _dirac_output_path(planned_job) -> str:
    '''Return the relative directory to pass to ILCDIRAC.'''
    # An empty OutputPath selects ILCDIRAC's date/job-ID directory. The
    # explicit "." instead selects the root after DIRAC normalizes the LFN.
    return str(PurePosixPath(planned_job.output_path or '.'))


def _output_lfn(planned_job, user_lfn_root: str) -> str:
    '''Return the absolute user LFN corresponding to a planned output.'''
    return str(PurePosixPath(
        user_lfn_root, _dirac_output_path(planned_job), planned_job.output_file
    ))


def _catalog_file_exists(catalog, lfn: str) -> bool:
    '''Return whether an LFN is registered, accepting DIRAC bulk-result forms.'''
    result = catalog.exists(lfn)
    if not isinstance(result, dict) or not result.get('OK', True):
        raise RuntimeError(f'Unable to check whether output LFN exists: {result}')

    payload = result.get('Value', result)
    if not isinstance(payload, dict) or not any(
        key in payload for key in ('Successful', 'successful', 'Failed', 'failed')
    ):
        raise RuntimeError(f'Unexpected output LFN check response: {result}')
    successful = payload.get('Successful', payload.get('successful', {}))
    failed = payload.get('Failed', payload.get('failed', {}))
    if not isinstance(successful, dict) or not isinstance(failed, dict):
        raise RuntimeError(f'Unexpected output LFN check response: {result}')
    if failed:
        raise RuntimeError(f'Unable to check whether output LFN exists: {failed}')
    return bool(successful.get(lfn, False))


def _remove_existing_output(dirac, catalog, output_lfn: str) -> None:
    '''Remove a planned output LFN before submitting its replacement job.'''
    if not _catalog_file_exists(catalog, output_lfn):
        return

    LOGGER.info('Removing existing output LFN: %s', output_lfn)
    result = dirac.removeFile(output_lfn)
    if not result or not result.get('OK'):
        message = result.get('Message', result) if result else 'no result returned'
        raise RuntimeError(
            f'Unable to remove existing output LFN {output_lfn}: {message}'
        )


def _confirm_submission(existing_outputs: list[str], force: bool) -> bool:
    '''Confirm submission and any planned deletions before making changes.'''
    if existing_outputs:
        LOGGER.warning('Found existing output files that will be deleted before submission:\n%s',
                       '\n'.join(existing_outputs))
        LOGGER.warning(
            'Deleted files are not restored if submission or execution fails.'
        )
    if force:
        LOGGER.info('Automatically confirming submission and listed deletions (--force).')
        return True
    try:
        question = ('Proceed with submission and deletion of these files?'
                    if existing_outputs else 'Proceed with submission?')
        answer = input(f'{question} y/[n]: ')
    except EOFError:
        LOGGER.warning('Submission cancelled: confirmation was not provided.')
        return False
    if answer.strip().lower() not in ('y', 'yes'):
        LOGGER.info('Submission cancelled; no files were deleted and no jobs submitted.')
        return False
    return True


def _print_plan(
    request: SubmissionRequest,
    planned_jobs,
    analysis_script: Path,
    local_se: str | None,
    output_lfns: list[str],
) -> None:
    '''Print the concrete jobs before they are submitted.'''
    output = StringIO()

    def emit(*args):
        print(*args, file=output)

    emit('FCCAnalyses grid submission plan:')
    emit(f'  submission ID:   {request.submission_id}')
    emit(f'  analysis script: {analysis_script}')
    emit(f'  input mode:      {request.input_mode}')
    emit(
        '  input files:     '
        f'{sum(len(job.source_inputs) for job in planned_jobs)}'
    )
    if request.n_chunks is not None:
        job_grouping = f'{request.n_chunks} requested chunks'
    elif request.files_per_job is not None:
        job_grouping = f'{request.files_per_job} files per job'
    elif request.input_mode == 'dirac-lfn':
        job_grouping = 'one file per job'
    else:
        job_grouping = 'sample chunks'
    emit(f'  job grouping:    {job_grouping}')
    emit(f'  planned jobs:    {len(planned_jobs)}')
    emit(f'  output SE:       {request.output_se or "selected by DIRAC"}')
    emit(f'  destination:     {request.destination_site or "selected by DIRAC"}')
    emit(f'  submission mode: {request.submit_mode}')
    if local_se:
        emit(f'  local SE:        {local_se}')
    if request.user_build_payload is not None:
        payload = request.user_build_payload
        emit(
            f'  user build:      {Path(payload.archive_path).name} '
            f'({payload.size_bytes / 1024**2:.1f} MiB)'
        )
    if request.analysis_include_archive is not None:
        emit('  include files:   staged from Analysis.include_paths')
    for planned_job, output_lfn in zip(planned_jobs, output_lfns):
        emit(f'  job {planned_job.index:04d}:')
        emit('    inputs:')
        for source_input in planned_job.source_inputs:
            emit(f'      {source_input}')
        emit(f'    output:        {output_lfn}')
    LOGGER.info('%s', output.getvalue().rstrip())


def main() -> None:
    '''Load one request, create all jobs, and submit them to the WMS.'''
    request = _load_request()
    planned_jobs = plan_jobs(request)
    if not planned_jobs:
        raise SystemExit('No jobs to submit.')

    install_root = Path(__file__).resolve().parents[1]
    worker_wrapper = _require_file(
        install_root / 'scripts' / 'dirac' / 'run_fccanalysis.sh',
        'FCCAnalyses worker wrapper',
    )
    analysis_script = _require_file(Path(request.analysis_script), 'Analysis script')
    _require_file(Path(request.key4hep_setup), 'Key4hep setup script')
    user_build_archive = _require_user_build_archive(request)
    analysis_include_archive = _require_analysis_include_archive(request)
    local_se = None
    if request.submit_mode == 'local':
        local_se = _require_local_storage_element()

    user_lfn_root = _user_lfn_root()
    output_lfns = [_output_lfn(job, user_lfn_root) for job in planned_jobs]
    _print_plan(request, planned_jobs, analysis_script, local_se, output_lfns)

    dirac = DiracILC()
    catalog = FileCatalog()
    existing_outputs = [
        lfn for lfn in output_lfns if _catalog_file_exists(catalog, lfn)
    ]
    if not _confirm_submission(existing_outputs, request.force):
        raise SystemExit(1)
    confirmed_outputs = set(existing_outputs)
    submitted_job_ids = []
    failures = []
    with tempfile.TemporaryDirectory(prefix='fccanalyses-input-lists-') as directory:
        input_list_directory = Path(directory)
        for planned_job, output_lfn in zip(planned_jobs, output_lfns):
            LOGGER.info(
                f'Submitting planned job {planned_job.index + 1}/{len(planned_jobs)} '
                f'({planned_job.job_name})'
            )
            try:
                input_file_list = _write_input_file_list(
                    planned_job,
                    input_list_directory,
                )
                job = _create_job(
                    request,
                    planned_job,
                    analysis_script,
                    worker_wrapper,
                    user_build_archive,
                    analysis_include_archive,
                    input_file_list,
                )
                job.dontPromptMe()
                if output_lfn in confirmed_outputs:
                    _remove_existing_output(dirac, catalog, output_lfn)
                result = job.submit(dirac, mode=request.submit_mode)
                if not result or not result.get('OK'):
                    message = result.get('Message', result) if result else 'no result returned'
                    raise RuntimeError(str(message))
            except Exception as error:
                failures.append(f'{planned_job.job_name}: {error}')
                break
            submitted_job_ids.append(result.get('JobID', result.get('Value')))

    if submitted_job_ids:
        LOGGER.info('Submitted DIRAC job IDs: %s', ', '.join(map(str, submitted_job_ids)))
    if request.submit_mode == 'local':
        LOGGER.info('Local DIRAC output is in the created Local_<hash>_JobDir directory.')
    if failures:
        not_attempted = len(planned_jobs) - len(submitted_job_ids) - 1
        raise RuntimeError(
            f'Submission stopped after {len(submitted_job_ids)} of '
            f'{len(planned_jobs)} jobs were submitted. '
            f'{not_attempted} remaining job(s) were not attempted.\n'
            'Failed job:\n  ' + '\n  '.join(failures)
        )


if __name__ == '__main__':
    logger = logging.getLogger('FCCAnalyses')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(MultiLineFormatter('----> %(levelname)s: %(message)s'))
    logger.addHandler(handler)
    main()
