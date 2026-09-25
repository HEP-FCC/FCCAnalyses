"""Tests for the data-only submission contract and job planning."""

import json
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

    def test_round_trips_complete_versioned_request(self) -> None:
        request = make_xrootd_request(
            n_chunks=2,
            run_arguments=("--analysis-option", "value"),
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

            payload = request.to_dict()
            payload["version"] = SubmissionRequest.VERSION + 1
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(
                SubmissionValidationError,
                "unsupported submission request version",
            ):
                SubmissionRequest.read_json(path)

    def test_rejects_unsafe_request_values(self) -> None:
        invalid_requests = (
            ({"output_path": "../other-user"}, "relative catalogue"),
            ({"submission_id": "../other-run"}, "submission_id"),
            (
                {"input_mode": "xrootd", "input_lfns": ("/fcc/a.root",)},
                "must not contain input LFNs",
            ),
            (
                {"input_mode": "dirac-lfn", "samples": make_xrootd_request().samples},
                "must not contain resolved samples",
            ),
            (
                {"files_per_job": 1, "n_chunks": 2},
                "mutually exclusive",
            ),
        )

        for overrides, message in invalid_requests:
            with self.subTest(overrides=overrides):
                with self.assertRaisesRegex(SubmissionValidationError, message):
                    make_request(**overrides)

    def test_rejects_invalid_input_groups(self) -> None:
        invalid_groups = (
            (("/fcc/data/input.root",), 0, "greater than zero"),
            (
                ("/fcc/data/input.root", "/fcc/data/input.root"),
                2,
                "listed more than once",
            ),
            (
                ("/fcc/data-a/input.root", "/fcc/data-b/input.root"),
                2,
                "collide after basename staging",
            ),
            (("fcc/data/input.root",), 1, "must be absolute"),
            (("/fcc/data/../input.root",), 1, "must not contain"),
        )

        for lfns, files_per_job, message in invalid_groups:
            with self.subTest(lfns=lfns, files_per_job=files_per_job):
                with self.assertRaisesRegex(SubmissionValidationError, message):
                    group_input_lfns(lfns, files_per_job)

    def test_plans_grouped_lfn_worker_jobs(self) -> None:
        request = make_request(
            input_lfns=tuple(
                f"/fcc/data/input-{index}.root" for index in range(5)
            ),
            files_per_job=2,
            lfn_sample_name="custom-lfn-sample",
            run_arguments=("--stride", "7", "--nevents", "100"),
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
                "--nevents",
                "100",
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
            run_arguments=("--stride", "7"),
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
        self.assertEqual(jobs[0].run_arguments[-2:], ("--stride", "7"))
        self.assertNotIn("--nevents", jobs[0].run_arguments)
        self.assertNotIn("--nevents", jobs[2].run_arguments)

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
