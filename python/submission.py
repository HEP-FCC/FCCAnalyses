"""Data-only submission contract and deterministic job planning.

This module is shared by the Key4hep-side frontend and the isolated DIRAC
helper. It deliberately contains no ROOT, XRootD, or DIRAC imports. The
frontend resolves and validates samples; this module serialises requests and
deterministically expands them into worker jobs.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path, PurePosixPath
from typing import Any, Literal


class SubmissionValidationError(ValueError):
    """Raised when a submission request cannot be planned safely."""


InputMode = Literal["xrootd", "dirac-lfn"]


@dataclass(frozen=True)
class InputGroup:
    """One ordered group of concrete DIRAC LFNs for a future worker job."""

    index: int
    lfns: tuple[str, ...]
    staged_filenames: tuple[str, ...]


@dataclass(frozen=True)
class ResolvedSample:
    """One analysis sample resolved to concrete frontend-validated inputs."""

    name: str | None
    output_stem: str | None
    inputs: tuple[str, ...]
    chunks: int
    stride: int | None

    def to_dict(self) -> dict[str, object]:
        """Return the JSON-compatible representation of this resolved sample."""
        return {
            "name": self.name,
            "output_stem": self.output_stem,
            "inputs": list(self.inputs),
            "chunks": self.chunks,
            "stride": self.stride,
        }

    @classmethod
    def from_dict(cls, payload: Any) -> "ResolvedSample":
        """Rebuild a sample previously serialized by the frontend."""
        return cls(
            name=payload["name"],
            output_stem=payload["output_stem"],
            inputs=tuple(payload["inputs"]),
            chunks=payload["chunks"],
            stride=payload["stride"],
        )


@dataclass(frozen=True)
class PlannedJob:
    """One concrete worker job derived from a submission request."""

    index: int
    job_name: str
    input_mode: InputMode
    sample_name: str | None
    source_inputs: tuple[str, ...]
    worker_file_list_entries: tuple[str, ...]
    input_list_filename: str
    output_file: str
    output_path: str | None
    run_arguments: tuple[str, ...]


@dataclass(frozen=True)
class UserBuildPayload:
    """One local archive that supplies a user-built FCCAnalyses runtime."""

    archive_path: str
    size_bytes: int

    def to_dict(self) -> dict[str, object]:
        return {"archive_path": self.archive_path, "size_bytes": self.size_bytes}

    @classmethod
    def from_dict(cls, payload: Any) -> "UserBuildPayload":
        return cls(
            archive_path=payload["archive_path"],
            size_bytes=payload["size_bytes"],
        )


@dataclass(frozen=True)
class SubmissionRequest:
    """Versioned data contract between FCCAnalyses and a grid helper process."""

    analysis_script: str
    input_mode: InputMode
    samples: tuple[ResolvedSample, ...]
    files_per_job: int | None
    run_arguments: tuple[str, ...]
    output_file: str
    output_path: str | None
    output_se: str | None
    key4hep_setup: str
    job_name: str
    job_group: str
    submit_mode: str
    destination_site: str | None
    submission_id: str
    user_build_payload: UserBuildPayload | None
    analysis_include_archive: str | None = None
    n_chunks: int | None = None
    worker_stride: int | None = None
    worker_output_format: str | None = None
    worker_ncpus: int | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "analysis_script": self.analysis_script,
            "input_mode": self.input_mode,
            "samples": [sample.to_dict() for sample in self.samples],
            "files_per_job": self.files_per_job,
            "n_chunks": self.n_chunks,
            "run_arguments": list(self.run_arguments),
            "worker_stride": self.worker_stride,
            "worker_output_format": self.worker_output_format,
            "worker_ncpus": self.worker_ncpus,
            "output_file": self.output_file,
            "output_path": self.output_path,
            "output_se": self.output_se,
            "key4hep_setup": self.key4hep_setup,
            "job_name": self.job_name,
            "job_group": self.job_group,
            "submit_mode": self.submit_mode,
            "destination_site": self.destination_site,
            "submission_id": self.submission_id,
            "user_build_payload": (
                self.user_build_payload.to_dict()
                if self.user_build_payload is not None
                else None
            ),
            "analysis_include_archive": self.analysis_include_archive,
        }

    def write_json(self, path: Path) -> None:
        path.write_text(
            json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    @classmethod
    def read_json(cls, path: Path) -> "SubmissionRequest":
        """Read the temporary request written by the frontend."""
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except OSError as error:
            raise SubmissionValidationError(
                f"cannot read submission request: {path}"
            ) from error
        except json.JSONDecodeError as error:
            raise SubmissionValidationError(
                f"submission request is not valid JSON: {path}"
            ) from error

        user_build_payload = payload["user_build_payload"]
        if user_build_payload is not None:
            user_build_payload = UserBuildPayload.from_dict(user_build_payload)
        return cls(
            analysis_script=payload["analysis_script"],
            input_mode=payload["input_mode"],
            samples=tuple(
                ResolvedSample.from_dict(sample) for sample in payload["samples"]
            ),
            files_per_job=payload["files_per_job"],
            n_chunks=payload["n_chunks"],
            run_arguments=tuple(payload["run_arguments"]),
            worker_stride=payload["worker_stride"],
            worker_output_format=payload["worker_output_format"],
            worker_ncpus=payload["worker_ncpus"],
            output_file=payload["output_file"],
            output_path=payload["output_path"],
            output_se=payload["output_se"],
            key4hep_setup=payload["key4hep_setup"],
            job_name=payload["job_name"],
            job_group=payload["job_group"],
            submit_mode=payload["submit_mode"],
            destination_site=payload["destination_site"],
            submission_id=payload["submission_id"],
            user_build_payload=user_build_payload,
            analysis_include_archive=payload["analysis_include_archive"],
        )


def generate_submission_id() -> str:
    """Return the UTC timestamp identifier for one submission."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def plan_jobs(request: SubmissionRequest) -> tuple[PlannedJob, ...]:
    """Expand a frontend-created request into deterministic worker jobs."""
    job_specs = _plan_input_groups(request)
    index_width = max(4, len(str(len(job_specs) - 1)))
    planned_jobs = []

    for index, spec in enumerate(job_specs):
        output_file = _planned_output_filename(
            request.output_file,
            spec["output_stem"],
            index,
            index_width,
        )
        input_list_filename = f"input-files-{index:0{index_width}d}.txt"
        run_arguments = [
            Path(request.analysis_script).name,
            "--input-file-list",
            input_list_filename,
        ]
        if spec["sample_name"] is not None:
            run_arguments.extend(["--sample-name", spec["sample_name"]])
        run_arguments.extend(["--output", output_file])
        if spec["stride"] is not None:
            run_arguments.extend(["--stride", str(spec["stride"])])
        if request.worker_stride is not None:
            run_arguments.extend(["--stride", str(request.worker_stride)])
        if request.worker_output_format is not None:
            run_arguments.extend(["--output-format", request.worker_output_format])
        if request.worker_ncpus is not None:
            run_arguments.extend(["--ncpus", str(request.worker_ncpus)])
        if request.run_arguments:
            run_arguments.extend(["--", *request.run_arguments])

        job_label = spec["sample_name"] or "lfn"
        planned_jobs.append(
            PlannedJob(
                index=index,
                job_name=(
                    f"{request.job_name}-{job_label}-{index:0{index_width}d}"
                ),
                input_mode=request.input_mode,
                sample_name=spec["sample_name"],
                source_inputs=spec["source_inputs"],
                worker_file_list_entries=spec["worker_inputs"],
                input_list_filename=input_list_filename,
                output_file=output_file,
                output_path=request.output_path,
                run_arguments=tuple(run_arguments),
            )
        )
    return tuple(planned_jobs)


def _plan_input_groups(request: SubmissionRequest) -> list[dict[str, object]]:
    job_specs = []
    for sample in request.samples:
        if request.input_mode == "dirac-lfn":
            groups = _group_input_lfns(
                sample.inputs,
                files_per_job=request.files_per_job,
                n_chunks=request.n_chunks,
                default_chunks=sample.chunks,
            )
        else:
            groups = _group_inputs(
                sample.inputs,
                n_chunks=request.n_chunks,
                files_per_job=request.files_per_job,
                default_chunks=sample.chunks,
            )
        for group in groups:
            source_inputs = (
                group.lfns if request.input_mode == "dirac-lfn" else group
            )
            worker_inputs = (
                group.staged_filenames if request.input_mode == "dirac-lfn"
                else group
            )
            job_specs.append(
                {
                    "sample_name": sample.name,
                    "output_stem": sample.output_stem,
                    "source_inputs": source_inputs,
                    "worker_inputs": worker_inputs,
                    "stride": sample.stride,
                }
            )
    return job_specs


def _group_input_lfns(
    input_lfns: Sequence[str],
    files_per_job: int | None = None,
    n_chunks: int | None = None,
    default_chunks: int = 1,
) -> tuple[InputGroup, ...]:
    """Group frontend-validated LFNs and detect staged filename collisions."""
    grouped_lfns = _group_inputs(
        input_lfns,
        n_chunks=n_chunks,
        files_per_job=files_per_job,
        default_chunks=default_chunks,
    )

    groups = []
    for index, group in enumerate(grouped_lfns):
        staged_filenames = tuple(PurePosixPath(lfn).name for lfn in group)
        duplicate_basenames = _duplicates(staged_filenames)
        if duplicate_basenames:
            colliding_lfns = [
                lfn
                for lfn, basename in zip(group, staged_filenames)
                if basename == duplicate_basenames[0]
            ]
            raise SubmissionValidationError(
                "input LFNs would collide after basename staging: "
                + ", ".join(colliding_lfns)
            )
        groups.append(InputGroup(index, tuple(group), staged_filenames))
    return tuple(groups)


def _group_inputs(
    values: Sequence[str],
    n_chunks: int | None,
    files_per_job: int | None,
    default_chunks: int,
) -> tuple[tuple[str, ...], ...]:
    """Split inputs evenly using an explicit or derived chunk count."""
    chunk_count = n_chunks
    if files_per_job is not None:
        chunk_count = (len(values) + files_per_job - 1) // files_per_job
    if chunk_count is None:
        chunk_count = default_chunks
    return _split_into_chunks(values, chunk_count)


def _split_into_chunks(
    values: Sequence[str], chunks: int
) -> tuple[tuple[str, ...], ...]:
    chunk_count = min(chunks, len(values))
    return tuple(
        tuple(values[index * len(values) // chunk_count:(index + 1) * len(values) // chunk_count])
        for index in range(chunk_count)
    )


def _duplicates(values: Sequence[str]) -> tuple[str, ...]:
    seen = set()
    duplicates = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return tuple(duplicates)


def _planned_output_filename(
    filename: str,
    output_stem: str | None,
    index: int,
    width: int,
) -> str:
    path = PurePosixPath(filename)
    suffix = path.suffix
    stem = path.name[:-len(suffix)] if suffix else path.name
    sample_part = f"_{output_stem}" if output_stem is not None else ""
    return f"{stem}{sample_part}_{index:0{width}d}{suffix}"
