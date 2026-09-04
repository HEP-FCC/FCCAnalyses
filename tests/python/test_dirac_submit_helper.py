'''Tests for translating a submission plan into ILCDIRAC objects.'''

import shlex
import sys
import tempfile
import types
import unittest
from pathlib import Path


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
    _write_input_file_list,
)
from submission import (
    ResolvedSample,
    SubmissionRequest,
    UserBuildPayload,
    plan_jobs,
)


class DiracSubmitHelperTest(unittest.TestCase):
    '''Exercise the only translation boundary that depends on ILCDIRAC.'''

    def test_translates_lfn_plan_into_dirac_job(self) -> None:
        request = SubmissionRequest(
            analysis_script='/work/analysis.py',
            input_mode='dirac-lfn',
            input_lfns=('/fcc/data/input.root',),
            samples=(),
            files_per_job=1,
            lfn_sample_name=None,
            run_arguments=(),
            output_file='result.root',
            output_path='analysis/results',
            output_se='CERN-DST-EOS',
            key4hep_setup='/cvmfs/key4hep/setup.sh',
            job_name='FCCAnalysis',
            job_group='FCCAnalysis_Run',
            submit_mode='local',
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
                    'OutputPath': 'analysis/results',
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
            input_lfns=(),
            samples=(
                ResolvedSample(
                    name='signal',
                    output_stem='signal',
                    input_urls=('root://eospublic.cern.ch//eos/experiment/fcc/a.root',),
                    chunks=1,
                    stride=4,
                ),
            ),
            files_per_job=None,
            lfn_sample_name=None,
            run_arguments=('--analysis-option', 'value'),
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

        self.assertFalse(hasattr(job, 'input_data'))
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
                '--analysis-option',
                'value',
            ],
        )

    def test_removes_existing_output_before_replacement(self) -> None:
        request = SubmissionRequest(
            analysis_script='/work/analysis.py',
            input_mode='dirac-lfn',
            input_lfns=('/fcc/data/input.root',),
            samples=(),
            files_per_job=1,
            lfn_sample_name=None,
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
        output_lfn = _output_lfn(planned_job)
        FakeCatalog.existing_lfns = {output_lfn}
        removed = []

        class FakeDirac:
            def removeFile(self, lfn):
                removed.append(lfn)
                return {'OK': True}

        _remove_existing_output(FakeDirac(), planned_job)

        self.assertEqual(removed, [output_lfn])

    def test_uses_proxy_group_when_config_does_not_define_a_vo(self) -> None:
        proxy_info_module = sys.modules['DIRAC.Core.Security.ProxyInfo']
        original_get_proxy_info = proxy_info_module.getProxyInfo
        original_config_value = FakeConfig.value
        FakeConfig.value = None
        proxy_info_module.getProxyInfo = lambda: {
            'OK': True,
            'Value': {'username': 'alice', 'group': 'fcc_user'},
        }
        try:
            planned_job = types.SimpleNamespace(
                output_path='analysis/results', output_file='result.root'
            )
            self.assertEqual(
                _output_lfn(planned_job),
                '/fcc/user/a/alice/analysis/results/result.root',
            )
        finally:
            proxy_info_module.getProxyInfo = original_get_proxy_info
            FakeConfig.value = original_config_value


if __name__ == '__main__':
    unittest.main()
