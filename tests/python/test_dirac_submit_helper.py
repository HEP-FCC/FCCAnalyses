'''Tests for translating a submission plan into ILCDIRAC objects.'''

import shlex
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / 'python'))


class FakeScript:
    '''Minimal replacement for DIRAC command-line initialisation.'''

    @staticmethod
    def parseCommandLine() -> None:
        pass


class FakeApplication:
    '''Capture the worker wrapper and its arguments.'''

    def setScript(self, script: str) -> None:
        self.script = script

    def setArguments(self, arguments: str) -> None:
        self.arguments = arguments


class FakeUserJob:
    '''Capture the ILCDIRAC job settings used by the adapter.'''

    def setName(self, value):
        self.name = value

    def setJobGroup(self, value):
        self.job_group = value

    def setNumberOfProcessors(self, **options):
        self.processors = options

    def setLogLevel(self, value):
        self.log_level = value

    def setOutputSandbox(self, value):
        self.output_sandbox = value

    def setInputSandbox(self, value):
        self.input_sandbox = value

    def setInputData(self, value):
        self.input_data = value

    def setOutputData(self, output_file, **options):
        self.output_data = (output_file, options)
        return {'OK': True}

    def setDestination(self, value):
        self.destination = value

    def append(self, application):
        self.application = application


class FakeCatalog:
    '''Minimal File Catalog used to exercise overwrite handling.'''

    existing_lfns = set()

    def exists(self, lfn):
        if lfn in self.existing_lfns:
            return {'Successful': {lfn: ['CERN-DST-EOS']}, 'Failed': {}}
        return {'Successful': {}, 'Failed': {}}


class FakeConfig:
    '''Return the VO used to construct user output LFNs.'''

    value = 'fcc'

    @staticmethod
    def getValue(path):
        assert path == '/DIRAC/VirtualOrganization'
        return FakeConfig.value


def install_dirac_stubs() -> None:
    '''Provide only the external modules imported by dirac_submit_helper.'''
    modules = {
        'DIRAC': types.ModuleType('DIRAC'),
        'DIRAC.Core': types.ModuleType('DIRAC.Core'),
        'DIRAC.Core.Base': types.ModuleType('DIRAC.Core.Base'),
        'DIRAC.Core.Base.Script': types.ModuleType('DIRAC.Core.Base.Script'),
        'DIRAC.Core.Security': types.ModuleType('DIRAC.Core.Security'),
        'DIRAC.Core.Security.ProxyInfo': types.ModuleType(
            'DIRAC.Core.Security.ProxyInfo'
        ),
        'DIRAC.ConfigurationSystem': types.ModuleType('DIRAC.ConfigurationSystem'),
        'DIRAC.ConfigurationSystem.Client': types.ModuleType(
            'DIRAC.ConfigurationSystem.Client'
        ),
        'DIRAC.ConfigurationSystem.Client.Helpers': types.ModuleType(
            'DIRAC.ConfigurationSystem.Client.Helpers'
        ),
        'DIRAC.ConfigurationSystem.Client.Helpers.Registry': types.ModuleType(
            'DIRAC.ConfigurationSystem.Client.Helpers.Registry'
        ),
        'DIRAC.ConfigurationSystem.Client.Helpers.Operations': types.ModuleType(
            'DIRAC.ConfigurationSystem.Client.Helpers.Operations'
        ),
        'DIRAC.Resources': types.ModuleType('DIRAC.Resources'),
        'DIRAC.Resources.Catalog': types.ModuleType('DIRAC.Resources.Catalog'),
        'DIRAC.Resources.Catalog.FileCatalog': types.ModuleType(
            'DIRAC.Resources.Catalog.FileCatalog'
        ),
        'ILCDIRAC': types.ModuleType('ILCDIRAC'),
        'ILCDIRAC.Interfaces': types.ModuleType('ILCDIRAC.Interfaces'),
        'ILCDIRAC.Interfaces.API': types.ModuleType('ILCDIRAC.Interfaces.API'),
        'ILCDIRAC.Interfaces.API.DiracILC': types.ModuleType(
            'ILCDIRAC.Interfaces.API.DiracILC'
        ),
        'ILCDIRAC.Interfaces.API.NewInterface': types.ModuleType(
            'ILCDIRAC.Interfaces.API.NewInterface'
        ),
        'ILCDIRAC.Interfaces.API.NewInterface.Applications': types.ModuleType(
            'ILCDIRAC.Interfaces.API.NewInterface.Applications'
        ),
        'ILCDIRAC.Interfaces.API.NewInterface.UserJob': types.ModuleType(
            'ILCDIRAC.Interfaces.API.NewInterface.UserJob'
        ),
    }
    modules['DIRAC'].gConfig = FakeConfig()
    modules['DIRAC.Core.Base.Script'].Script = FakeScript
    modules['DIRAC.Core.Security.ProxyInfo'].getProxyInfo = lambda: {
        'OK': True,
        'Value': {'username': 'alice'},
    }
    modules['DIRAC.ConfigurationSystem.Client.Helpers'].Registry = modules[
        'DIRAC.ConfigurationSystem.Client.Helpers.Registry'
    ]
    modules['DIRAC.ConfigurationSystem.Client.Helpers.Registry'].getVOForGroup = (
        lambda group: 'fcc'
    )
    modules['DIRAC.ConfigurationSystem.Client.Helpers.Operations'].Operations = (
        lambda **kwargs: types.SimpleNamespace(getValue=lambda key, default: default)
    )
    modules['DIRAC.Resources.Catalog.FileCatalog'].FileCatalog = FakeCatalog
    modules['ILCDIRAC.Interfaces.API.DiracILC'].DiracILC = object
    modules[
        'ILCDIRAC.Interfaces.API.NewInterface.Applications'
    ].GenericApplication = FakeApplication
    modules['ILCDIRAC.Interfaces.API.NewInterface.UserJob'].UserJob = FakeUserJob
    sys.modules.update(modules)


install_dirac_stubs()

from dirac_submit_helper import (
    _create_job,
    _output_lfn,
    _remove_existing_output,
    _user_lfn_root,
    _write_input_file_list,
    main,
)
from submission import (
    ResolvedSample,
    SubmissionRequest,
    UserBuildPayload,
    plan_jobs,
)


class DiracSubmitHelperTest(unittest.TestCase):
    '''Exercise the only translation boundary that depends on ILCDIRAC.'''

    def test_confirmation_precedes_deletion_and_submission(self) -> None:
        request = SubmissionRequest(
            analysis_script='/work/analysis.py', input_mode='dirac-lfn',
            input_lfns=('/fcc/data/input.root',), samples=(), files_per_job=1,
            lfn_sample_name=None, run_arguments=(), output_file='result.root',
            output_path=None, output_se=None, key4hep_setup='/work/setup.sh',
            job_name='FCCAnalysis', job_group='test', submit_mode='wms',
            destination_site=None, submission_id='test', user_build_payload=None,
        )
        output_lfn = '/fcc/users/a/alice/result_0000.root'
        for answer, force, should_submit in (
            ('n', False, False), ('', False, False),
            (EOFError(), False, False), ('y', False, True),
            (None, True, True),
        ):
            with self.subTest(answer=answer, force=force):
                from dataclasses import replace
                current = replace(request, force=force)
                events = []
                dirac = MagicMock()
                dirac.removeFile.side_effect = lambda lfn: (
                    events.append(('delete', lfn)) or {'OK': True}
                )
                job = MagicMock()
                job.submit.side_effect = lambda *args, **kwargs: (
                    events.append(('submit',)) or {'OK': True, 'JobID': 42}
                )
                catalog = FakeCatalog()
                catalog.existing_lfns = {output_lfn}
                with patch('dirac_submit_helper._load_request', return_value=current), \
                     patch('dirac_submit_helper._require_file', side_effect=lambda path, _: path), \
                     patch('dirac_submit_helper.DiracILC', return_value=dirac), \
                     patch('dirac_submit_helper.Operations') as operations, \
                     patch('dirac_submit_helper.FileCatalog', return_value=catalog), \
                     patch('dirac_submit_helper._create_job', return_value=job), \
                     patch('builtins.input', side_effect=(answer if isinstance(answer, Exception) else None),
                           return_value=answer) as prompt, self.assertLogs('FCCAnalyses.grid_helper', level='INFO') as logs:
                    operations.return_value.getValue.return_value = 'users'
                    if should_submit:
                        main()
                    else:
                        with self.assertRaises(SystemExit) as cancelled:
                            main()
                        self.assertNotEqual(cancelled.exception.code, 0)
                operations.assert_called_once_with(vo='fcc')
                operations.return_value.getValue.assert_called_once_with('LFNUserPrefix', 'user')
                self.assertIn(f'output:        {output_lfn}', '\n'.join(logs.output))
                self.assertIn('Found existing output files that will be '
                              'deleted before submission:', '\n'.join(logs.output))
                self.assertIn('Deleted files are not restored if submission or execution fails.',
                              '\n'.join(logs.output))
                if should_submit:
                    self.assertEqual(events, [('delete', output_lfn), ('submit',)])
                    job.dontPromptMe.assert_called_once()
                    self.assertIn(f'Removing existing output LFN: {output_lfn}',
                                  '\n'.join(logs.output))
                else:
                    self.assertEqual(events, [])
                    job.submit.assert_not_called()
                self.assertEqual(prompt.call_count, 0 if force else 1)
                if not force:
                    prompt.assert_called_once_with(
                        'Proceed with submission and deletion of these files? y/[n]: '
                    )

    def test_empty_plan_exits_unsuccessfully(self) -> None:
        with patch('dirac_submit_helper._load_request'), \
             patch('dirac_submit_helper.plan_jobs', return_value=()):
            with self.assertRaisesRegex(SystemExit, 'No jobs to submit'):
                main()

    def test_partial_submission_reports_ids_and_unattempted_jobs(self) -> None:
        request = SubmissionRequest(
            analysis_script='/work/analysis.py', input_mode='dirac-lfn',
            input_lfns=('/fcc/data/a.root', '/fcc/data/b.root', '/fcc/data/c.root'),
            samples=(), files_per_job=1, lfn_sample_name=None, run_arguments=(),
            output_file='result.root', output_path=None, output_se=None,
            key4hep_setup='/work/setup.sh', job_name='FCCAnalysis', job_group='test',
            submit_mode='wms', destination_site=None, submission_id='test',
            user_build_payload=None, force=True,
        )
        job = MagicMock()
        job.submit.side_effect = [
            {'OK': True, 'JobID': 42}, {'OK': False, 'Message': 'rejected'},
        ]
        with patch('dirac_submit_helper._load_request', return_value=request), \
             patch('dirac_submit_helper._require_file', side_effect=lambda path, _: path), \
             patch('dirac_submit_helper.DiracILC'), \
             patch('dirac_submit_helper.FileCatalog', return_value=FakeCatalog()), \
             patch('dirac_submit_helper._create_job', return_value=job), \
             self.assertLogs('FCCAnalyses.grid_helper', level='INFO') as logs:
            with self.assertRaisesRegex(RuntimeError, '1 remaining job\\(s\\) were not attempted') as error:
                main()
        self.assertIn('Submitted DIRAC job IDs: 42', '\n'.join(logs.output))
        self.assertIn('rejected', str(error.exception))
        self.assertEqual(job.submit.call_count, 2)

    def test_failed_submission_does_not_restore_deleted_output(self) -> None:
        request = SubmissionRequest(
            analysis_script='/work/analysis.py', input_mode='dirac-lfn',
            input_lfns=('/fcc/data/a.root', '/fcc/data/b.root'),
            samples=(), files_per_job=1, lfn_sample_name=None, run_arguments=(),
            output_file='result.root', output_path=None, output_se=None,
            key4hep_setup='/work/setup.sh', job_name='FCCAnalysis', job_group='test',
            submit_mode='wms', destination_site=None, submission_id='test',
            user_build_payload=None, force=True,
        )
        output_lfn = '/fcc/user/a/alice/result_0000.root'
        for result in ({'OK': False, 'Message': 'rejected'}, None, {},
                       RuntimeError('connection failed')):
            with self.subTest(result=result):
                dirac = MagicMock()
                dirac.removeFile.return_value = {'OK': True}
                job = MagicMock()
                if isinstance(result, Exception):
                    job.submit.side_effect = result
                else:
                    job.submit.return_value = result
                catalog = FakeCatalog()
                catalog.existing_lfns = {output_lfn}
                with patch('dirac_submit_helper._load_request', return_value=request), \
                     patch('dirac_submit_helper._require_file', side_effect=lambda path, _: path), \
                     patch('dirac_submit_helper._user_lfn_root', return_value='/fcc/user/a/alice'), \
                     patch('dirac_submit_helper.DiracILC', return_value=dirac), \
                     patch('dirac_submit_helper.FileCatalog', return_value=catalog), \
                     patch('dirac_submit_helper._create_job', return_value=job) as create_job, \
                     self.assertLogs('FCCAnalyses.grid_helper', level='INFO'):
                    with self.assertRaises(RuntimeError) as error:
                        main()
                self.assertIn('0 of 2 jobs were submitted', str(error.exception))
                self.assertIn('1 remaining job(s) were not attempted', str(error.exception))
                dirac.removeFile.assert_called_once_with(output_lfn)
                create_job.assert_called_once()
                job.submit.assert_called_once()

    def test_translates_lfn_plan_into_dirac_job(self) -> None:
        request = SubmissionRequest(
            analysis_script='/work/analysis.py',
            input_mode='dirac-lfn',
            samples=(
                ResolvedSample(
                    name=None,
                    output_stem=None,
                    inputs=('/fcc/data/input.root',),
                    chunks=1,
                    stride=None,
                ),
            ),
            files_per_job=1,
            run_arguments=(),
            output_file='result.root',
            output_path=None,
            output_se='CERN-DST-EOS',
            key4hep_setup='/cvmfs/key4hep/setup.sh',
            job_name='FCCAnalysis',
            job_group='FCCAnalysis_Run',
            submit_mode='local',
            worker_ncpus=4,
            destination_site='LCG.CERN.ch',
            submission_id='20260729T150000Z',
            user_build_payload=UserBuildPayload(
                archive_path='/tmp/fccanalyses-payload.tar.gz',
                size_bytes=12345,
            ),
            analysis_include_archive='/tmp/analysis-includes.tar.gz',
        )
        planned_job = plan_jobs(request)[0]

        with tempfile.TemporaryDirectory() as directory:
            input_file_list = _write_input_file_list(planned_job, Path(directory))
            self.assertEqual(input_file_list.read_text(), 'input.root\n')
            job = _create_job(
                request,
                planned_job,
                Path(request.analysis_script),
                Path('/work/run_fccanalysis.sh'),
                Path(request.user_build_payload.archive_path),
                Path(request.analysis_include_archive),
                input_file_list,
            )

        self.assertEqual(job.processors, {'numberOfProcessors': 1})
        self.assertEqual(job.name, 'FCCAnalysis-lfn-0000')
        self.assertEqual(job.job_group, 'FCCAnalysis_Run')
        self.assertEqual(
            job.input_sandbox,
            [
                '/work/analysis.py',
                str(input_file_list),
                '/tmp/fccanalyses-payload.tar.gz',
                '/tmp/analysis-includes.tar.gz',
            ],
        )
        self.assertEqual(job.input_data, ['/fcc/data/input.root'])
        self.assertEqual(
            job.output_data,
            (
                'result_0000.root',
                {
                    'OutputPath': '.',
                    'OutputSE': 'CERN-DST-EOS',
                },
            ),
        )
        self.assertEqual(job.destination, 'LCG.CERN.ch')
        self.assertEqual(job.application.script, '/work/run_fccanalysis.sh')
        self.assertEqual(
            shlex.split(job.application.arguments),
            [
                '--env',
                'clean',
                '--key4hep-setup',
                '/cvmfs/key4hep/setup.sh',
                '--payload-archive',
                'fccanalyses-payload.tar.gz',
                '--include-archive',
                'analysis-includes.tar.gz',
                '--',
                'analysis.py',
                '--input-file-list',
                'input-files-0000.txt',
                '--output',
                'result_0000.root',
            ],
        )

    def test_translates_xrootd_plan_without_dirac_input_data(self) -> None:
        request = SubmissionRequest(
            analysis_script='/work/analysis.py',
            input_mode='xrootd',
            samples=(
                ResolvedSample(
                    name='signal',
                    output_stem='signal',
                    inputs=('root://eospublic.cern.ch//eos/experiment/fcc/a.root',),
                    chunks=1,
                    stride=4,
                ),
            ),
            files_per_job=None,
            run_arguments=('--analysis-option', 'value'),
            output_file='result.root',
            output_path='analysis/results',
            output_se=None,
            key4hep_setup='/cvmfs/key4hep/setup.sh',
            key4hep_release='2026-04-08',
            job_name='FCCAnalysis',
            job_group='FCCAnalysis_Run',
            submit_mode='wms',
            worker_ncpus=-1,
            destination_site=None,
            submission_id='20260729T150000Z',
            user_build_payload=None,
            analysis_include_archive='/tmp/analysis-includes.tar.gz',
        )
        planned_job = plan_jobs(request)[0]

        with tempfile.TemporaryDirectory() as directory:
            input_file_list = _write_input_file_list(planned_job, Path(directory))
            self.assertEqual(
                input_file_list.read_text(),
                'root://eospublic.cern.ch//eos/experiment/fcc/a.root\n',
            )
            job = _create_job(
                request,
                planned_job,
                Path(request.analysis_script),
                Path('/work/run_fccanalysis.sh'),
                None,
                Path(request.analysis_include_archive),
                input_file_list,
            )

        self.assertEqual(job.processors, {'numberOfProcessors': 1})
        self.assertFalse(hasattr(job, 'input_data'))
        self.assertEqual(
            job.output_data, ('result_signal_0000.root', {'OutputPath': 'analysis/results'})
        )
        self.assertEqual(
            job.input_sandbox,
            [
                '/work/analysis.py',
                str(input_file_list),
                '/tmp/analysis-includes.tar.gz',
            ],
        )
        self.assertEqual(
            shlex.split(job.application.arguments),
            [
                '--env',
                'inherit',
                '--key4hep-setup',
                '/cvmfs/key4hep/setup.sh',
                '--key4hep-release', '2026-04-08',
                '--include-archive',
                'analysis-includes.tar.gz',
                '--',
                'analysis.py',
                '--input-file-list',
                'input-files-0000.txt',
                '--sample-name',
                'signal',
                '--output',
                'result_signal_0000.root',
                '--stride',
                '4',
                '--',
                '--analysis-option',
                'value',
            ],
        )

    def test_removes_existing_output_before_replacement(self) -> None:
        request = SubmissionRequest(
            analysis_script='/work/analysis.py',
            input_mode='dirac-lfn',
            samples=(
                ResolvedSample(
                    name=None,
                    output_stem=None,
                    inputs=('/fcc/data/input.root',),
                    chunks=1,
                    stride=None,
                ),
            ),
            files_per_job=1,
            run_arguments=(),
            output_file='result.root',
            output_path='analysis/results',
            output_se=None,
            key4hep_setup='/cvmfs/key4hep/setup.sh',
            job_name='FCCAnalysis',
            job_group='FCCAnalysis_Run',
            submit_mode='wms',
            destination_site=None,
            submission_id='20260729T150000Z',
            user_build_payload=None,
        )
        planned_job = plan_jobs(request)[0]
        user_lfn_root = _user_lfn_root()
        output_lfn = _output_lfn(planned_job, user_lfn_root)
        FakeCatalog.existing_lfns = {output_lfn}
        removed = []

        class FakeDirac:
            def removeFile(self, lfn):
                removed.append(lfn)
                return {'OK': True}

        with self.assertLogs('FCCAnalyses.grid_helper', level='INFO') as logs:
            _remove_existing_output(
                FakeDirac(),
                FakeCatalog(),
                output_lfn,
            )

        self.assertEqual(removed, [output_lfn])
        self.assertIn(
            f'Removing existing output LFN: {output_lfn}',
            '\n'.join(logs.output),
        )

    def test_uses_proxy_group_when_config_does_not_define_a_vo(self) -> None:
        original_config_value = FakeConfig.value
        FakeConfig.value = None
        try:
            planned_job = types.SimpleNamespace(
                output_path='analysis/results', output_file='result.root'
            )
            with patch(
                'dirac_submit_helper.getProxyInfo',
                return_value={
                    'OK': True,
                    'Value': {'username': 'alice', 'group': 'fcc_user'},
                },
            ):
                self.assertEqual(
                    _output_lfn(planned_job, _user_lfn_root()),
                    '/fcc/user/a/alice/analysis/results/result.root',
                )
        finally:
            FakeConfig.value = original_config_value


if __name__ == '__main__':
    unittest.main()
