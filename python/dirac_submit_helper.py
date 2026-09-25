'''Submit planned FCCAnalyses jobs through ILCDIRAC.

This program is executed only by ``run_dirac_submission.sh`` after that script
has created the supported DIRAC client environment. Keep ILCDIRAC imports in
this file so the public FCCAnalyses process remains independent of DIRAC.
'''

from __future__ import annotations

import os
from pathlib import Path
import shlex
import tempfile

from submission import SubmissionRequest, SubmissionValidationError, plan_jobs

# DIRAC configuration, including DIRACSYSCONFIG and ~/.dirac.cfg, is loaded by
# parseCommandLine(). It must run before importing and using ILCDIRAC APIs.
from DIRAC.Core.Base.Script import Script

Script.parseCommandLine()

from DIRAC import gConfig
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
    output_options = {'OutputPath': planned_job.output_path}
    if request.output_se is not None:
        output_options['OutputSE'] = request.output_se
    job.setOutputData(planned_job.output_file, **output_options)
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


def _output_lfn(planned_job) -> str:
    '''Return the absolute user LFN corresponding to a planned output.'''
    from DIRAC.Core.Security.ProxyInfo import getProxyInfo

    result = getProxyInfo()
    if not result or not result.get('OK'):
        message = result.get('Message', result) if result else 'no result returned'
        raise RuntimeError(f'Unable to read DIRAC proxy information: {message}')
    proxy_info = result.get('Value', {})
    username = proxy_info.get('username')
    virtual_organization = gConfig.getValue('/DIRAC/VirtualOrganization')
    if not virtual_organization and proxy_info.get('group'):
        from DIRAC.ConfigurationSystem.Client.Helpers import Registry

        virtual_organization = Registry.getVOForGroup(proxy_info['group'])
    if not username or not virtual_organization:
        raise RuntimeError(
            'Cannot determine the DIRAC user LFN root needed to check for an '
            'existing output LFN; refusing to submit without overwrite '
            'protection.'
        )

    relative_output = f'{planned_job.output_path}/{planned_job.output_file}'
    return f'/{virtual_organization}/user/{username[0]}/{username}/{relative_output}'


def _catalog_file_exists(catalog, lfn: str) -> bool:
    '''Return whether an LFN is registered, accepting DIRAC bulk-result forms.'''
    result = catalog.exists(lfn)
    if result.get('OK') is False:
        raise RuntimeError(f'Unable to check whether output LFN exists: {result}')

    payload = result.get('Value', result)
    successful = payload.get('Successful', payload.get('successful', {}))
    failed = payload.get('Failed', payload.get('failed', {}))
    if lfn in failed:
        raise RuntimeError(
            f'Unable to check whether output LFN exists: {failed[lfn]}'
        )
    return lfn in successful


def _remove_existing_output(dirac, planned_job) -> None:
    '''Remove a planned output LFN before submitting its replacement job.'''
    from DIRAC.Resources.Catalog.FileCatalog import FileCatalog

    output_lfn = _output_lfn(planned_job)
    if not _catalog_file_exists(FileCatalog(), output_lfn):
        return

    print(f'WARNING: Removing existing output LFN: {output_lfn}')
    result = dirac.removeFile(output_lfn)
    if not result or not result.get('OK'):
        message = result.get('Message', result) if result else 'no result returned'
        raise RuntimeError(
            f'Unable to remove existing output LFN {output_lfn}: {message}'
        )


def _print_plan(
    request: SubmissionRequest,
    planned_jobs,
    analysis_script: Path,
    local_se: str | None,
) -> None:
    '''Print the concrete jobs before they are submitted.'''
    print('FCCAnalyses grid submission plan:')
    print(f'  submission ID:   {request.submission_id}')
    print(f'  analysis script: {analysis_script}')
    print(f'  input mode:      {request.input_mode}')
    print(
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
    print(f'  job grouping:    {job_grouping}')
    print(f'  planned jobs:    {len(planned_jobs)}')
    print(f'  output SE:       {request.output_se or "selected by DIRAC"}')
    print(f'  destination:     {request.destination_site or "selected by DIRAC"}')
    print(f'  submission mode: {request.submit_mode}')
    if local_se:
        print(f'  local SE:        {local_se}')
    if request.user_build_payload is not None:
        payload = request.user_build_payload
        print(
            f'  user build:      {Path(payload.archive_path).name} '
            f'({payload.size_bytes / 1024**2:.1f} MiB)'
        )
    if request.analysis_include_archive is not None:
        print('  include files:   staged from Analysis.include_paths')
    for planned_job in planned_jobs:
        print(f'  job {planned_job.index:04d}:')
        print('    inputs:')
        for source_input in planned_job.source_inputs:
            print(f'      {source_input}')
        print(
            f'    output:        '
            f'{planned_job.output_path}/{planned_job.output_file}'
        )


def main() -> None:
    '''Load one request, create all jobs, and submit them to the WMS.'''
    request = _load_request()
    planned_jobs = plan_jobs(request)

    source_root = Path(__file__).resolve().parents[1]
    worker_wrapper = _require_file(
        source_root / 'scripts' / 'dirac' / 'run_fccanalysis.sh',
        'FCCAnalyses worker wrapper',
    )
    analysis_script = _require_file(Path(request.analysis_script), 'Analysis script')
    _require_file(Path(request.key4hep_setup), 'Key4hep setup script')
    user_build_archive = _require_user_build_archive(request)
    analysis_include_archive = _require_analysis_include_archive(request)
    local_se = None
    if request.submit_mode == 'local':
        local_se = _require_local_storage_element()

    _print_plan(request, planned_jobs, analysis_script, local_se)

    dirac = DiracILC()
    submitted_job_ids = []
    failures = []
    with tempfile.TemporaryDirectory(prefix='fccanalyses-input-lists-') as directory:
        input_list_directory = Path(directory)
        for planned_job in planned_jobs:
            print(
                f'Submitting planned job {planned_job.index + 1}/{len(planned_jobs)} '
                f'({planned_job.job_name})'
            )
            input_file_list = _write_input_file_list(
                planned_job,
                input_list_directory,
            )
            _remove_existing_output(dirac, planned_job)
            result = _create_job(
                request,
                planned_job,
                analysis_script,
                worker_wrapper,
                user_build_archive,
                analysis_include_archive,
                input_file_list,
            ).submit(dirac, mode=request.submit_mode)
            if not result or not result.get('OK'):
                message = result.get('Message', result) if result else 'no result returned'
                failures.append(f'{planned_job.job_name}: {message}')
                continue
            submitted_job_ids.append(result.get('JobID', result.get('Value')))

    if submitted_job_ids:
        print('Submitted DIRAC job IDs: ' + ', '.join(map(str, submitted_job_ids)))
    if request.submit_mode == 'local':
        print('Local DIRAC output is in the created Local_<hash>_JobDir directory.')
    if failures:
        raise RuntimeError(
            'Some DIRAC jobs were not submitted:\n  ' + '\n  '.join(failures)
        )


if __name__ == '__main__':
    main()
