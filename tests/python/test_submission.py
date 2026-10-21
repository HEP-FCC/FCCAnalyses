"""Tests for the data-only submission contract and job planning."""

import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "python"))

from submission import (
    ResolvedSample,
    SubmissionRequest,
    SubmissionValidationError,
    UserBuildPayload,
    group_input_lfns,
    plan_jobs,
)


def make_request(**overrides: object) -> SubmissionRequest:
    values: dict[str, object] = {
        "analysis_script": "/work/analysis.py",
        "input_mode": "dirac-lfn",
        "input_lfns": ("/fcc/data/input.root",),
        "samples": (),
        "files_per_job": 1,
        "lfn_sample_name": None,
        "run_arguments": (),
        "output_file": "result.root",
        "output_path": "analysis/results",
        "output_se": "CERN-DST-EOS",
        "key4hep_setup": "/cvmfs/key4hep/setup.sh",
        "job_name": "FCCAnalysis",
        "job_group": "FCCAnalysis_Run",
        "submit_mode": "wms",
        "destination_site": "LCG.CERN.ch",
        "submission_id": "20260729T150000Z",
        "user_build_payload": None,
    }
    values.update(overrides)
    return SubmissionRequest(**values)  # type: ignore[arg-type]


def make_xrootd_request(**overrides: object) -> SubmissionRequest:
    values: dict[str, object] = {
        "input_mode": "xrootd",
        "input_lfns": (),
        "samples": (
            ResolvedSample(
                name="signal",
                output_stem="signal",
                input_urls=(
                    "root://eospublic.cern.ch//eos/experiment/fcc/signal/a.root",
                ),
                chunks=1,
                stride=None,
            ),
        ),
        "files_per_job": None,
        "lfn_sample_name": None,
    }
    values.update(overrides)
    return make_request(**values)


class SubmissionTest(unittest.TestCase):
    """Exercise the shared request and planning invariants."""

    def test_round_trips_complete_request(self) -> None:
        request = make_xrootd_request(
            n_chunks=2,
            run_arguments=("--analysis-option", "value"),
            output_path=None,
            output_se=None,
            user_build_payload=UserBuildPayload(
                archive_path="/tmp/fccanalyses-payload.tar.gz",
                size_bytes=12345,
            ),
            analysis_include_archive="/tmp/analysis-includes.tar.gz",
        )

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "request.json"
            request.write_json(path)
            self.assertEqual(SubmissionRequest.read_json(path), request)

    def test_rejects_lfn_staging_name_collisions(self) -> None:
        lfns = ("/fcc/data-a/input.root", "/fcc/data-b/input.root")
        with self.assertRaisesRegex(
            SubmissionValidationError,
            "collide after basename staging",
        ):
            group_input_lfns(lfns, files_per_job=2)

    def test_plans_grouped_lfn_worker_jobs(self) -> None:
        request = make_request(
            input_lfns=tuple(
                f"/fcc/data/input-{index}.root" for index in range(5)
            ),
            files_per_job=2,
            lfn_sample_name="custom-lfn-sample",
            run_arguments=("--analysis-option", "value"),
            worker_stride=7,
        )

        jobs = plan_jobs(request)

        self.assertEqual(len(jobs), 3)
        self.assertEqual(
            [job.source_inputs for job in jobs],
            [
                ("/fcc/data/input-0.root",),
                ("/fcc/data/input-1.root", "/fcc/data/input-2.root"),
                ("/fcc/data/input-3.root", "/fcc/data/input-4.root"),
            ],
        )
        self.assertEqual(
            jobs[0].worker_file_list_entries,
            ("input-0.root",),
        )
        self.assertEqual(
            [job.output_file for job in jobs],
            ["result_0000.root", "result_0001.root", "result_0002.root"],
        )
        self.assertEqual(
            jobs[0].run_arguments,
            (
                "analysis.py",
                "--input-file-list",
                "input-files-0000.txt",
                "--sample-name",
                "custom-lfn-sample",
                "--output",
                "result_0000.root",
                "--stride",
                "7",
                "--",
                "--analysis-option",
                "value",
            ),
        )
        self.assertEqual(jobs[2].job_name, "FCCAnalysis-custom-lfn-sample-0002")

    def test_plans_balanced_lfn_chunks(self) -> None:
        request = make_request(
            input_lfns=tuple(
                f"/fcc/data/input-{index}.root" for index in range(5)
            ),
            files_per_job=None,
            n_chunks=3,
        )

        jobs = plan_jobs(request)

        self.assertEqual([len(job.source_inputs) for job in jobs], [1, 2, 2])
        self.assertEqual(
            [job.output_file for job in jobs],
            ["result_0000.root", "result_0001.root", "result_0002.root"],
        )

    def test_plans_xrootd_samples_without_mixing_them(self) -> None:
        request = make_xrootd_request(
            run_arguments=("--analysis-option", "value"),
            worker_stride=7,
            samples=(
                ResolvedSample(
                    name="signal",
                    output_stem="sig",
                    input_urls=(
                        "root://eospublic.cern.ch//eos/experiment/fcc/signal/a.root",
                        "root://eospublic.cern.ch//eos/experiment/fcc/signal/b.root",
                        "root://eospublic.cern.ch//eos/experiment/fcc/signal/c.root",
                    ),
                    chunks=2,
                    stride=5,
                ),
                ResolvedSample(
                    name="background",
                    output_stem="background",
                    input_urls=(
                        "root://eospublic.cern.ch//eos/experiment/fcc/background/a.root",
                    ),
                    chunks=1,
                    stride=None,
                ),
            ),
        )

        jobs = plan_jobs(request)

        self.assertEqual([job.sample_name for job in jobs], ["signal", "signal", "background"])
        self.assertEqual(
            [job.output_file for job in jobs],
            [
                "result_sig_0000.root",
                "result_sig_0001.root",
                "result_background_0002.root",
            ],
        )
        self.assertEqual(jobs[0].worker_file_list_entries, jobs[0].source_inputs)
        self.assertIn("--stride", jobs[0].run_arguments)
        self.assertEqual(
            jobs[0].run_arguments[-3:],
            ("--", "--analysis-option", "value"),
        )

    def test_files_per_job_derives_balanced_chunk_count(self) -> None:
        request = make_xrootd_request(
            files_per_job=2,
            samples=(
                ResolvedSample(
                    name="signal",
                    output_stem="signal",
                    input_urls=tuple(
                        f"root://eospublic.cern.ch//eos/experiment/fcc/signal/{index}.root"
                        for index in range(5)
                    ),
                    chunks=4,
                    stride=None,
                ),
            ),
        )

        jobs = plan_jobs(request)

        self.assertEqual([len(job.source_inputs) for job in jobs], [1, 2, 2])

    def test_n_chunks_overrides_each_xrootd_sample(self) -> None:
        request = make_xrootd_request(
            n_chunks=3,
            samples=(
                ResolvedSample(
                    name="signal",
                    output_stem="signal",
                    input_urls=tuple(
                        f"root://eospublic.cern.ch//eos/experiment/fcc/signal/{index}.root"
                        for index in range(5)
                    ),
                    chunks=1,
                    stride=None,
                ),
                ResolvedSample(
                    name="background",
                    output_stem="background",
                    input_urls=tuple(
                        f"root://eospublic.cern.ch//eos/experiment/fcc/background/{index}.root"
                        for index in range(4)
                    ),
                    chunks=2,
                    stride=None,
                ),
            ),
        )

        jobs = plan_jobs(request)

        self.assertEqual(
            [len(job.source_inputs) for job in jobs],
            [1, 2, 2, 1, 1, 2],
        )


if __name__ == "__main__":
    unittest.main()
