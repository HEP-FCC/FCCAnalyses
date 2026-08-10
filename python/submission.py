"""Data-only submission contract and deterministic job planning.

This module is shared by the Key4hep-side frontend and the isolated DIRAC
helper. It deliberately contains no ROOT, XRootD, or DIRAC imports. The
frontend resolves samples to concrete inputs; this module validates, serialises,
and deterministically expands those inputs into worker jobs.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path, PurePosixPath
import re
from typing import Literal, Optional


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
    """One analysis sample resolved to ordered XRootD URLs by the frontend."""

    name: str
    output_stem: str
    input_urls: tuple[str, ...]
    chunks: int
    stride: Optional[int]

    def __post_init__(self) -> None:
        _require_simple_name(self.name, "sample.name")
        _require_simple_name(self.output_stem, "sample.output_stem")
        _require_positive_integer(self.chunks, "sample.chunks")
        if not self.input_urls:
            raise SubmissionValidationError(
                f"sample {self.name} has no resolved input URLs"
            )
        urls = tuple(_validate_xrootd_url(url) for url in self.input_urls)
        duplicates = _duplicates(urls)
        if duplicates:
            raise SubmissionValidationError(
                f"sample {self.name} contains a duplicate input URL: "
                f"{duplicates[0]}"
            )
        _require_optional_positive_integer(self.stride, "sample.stride")

    def to_dict(self) -> dict[str, object]:
        """Return the JSON-compatible representation of this resolved sample."""
        return {
            "name": self.name,
            "output_stem": self.output_stem,
            "input_urls": list(self.input_urls),
            "chunks": self.chunks,
            "stride": self.stride,
        }

    @classmethod
    def from_dict(cls, payload: object) -> "ResolvedSample":
        """Load and validate one resolved sample from JSON data."""
        if not isinstance(payload, dict):
            raise SubmissionValidationError("sample must be a JSON object")
        expected_keys = {
            "name",
            "output_stem",
            "input_urls",
            "chunks",
            "stride",
        }
        _require_exact_keys(payload, expected_keys, "sample")
        if not isinstance(payload["input_urls"], list):
            raise SubmissionValidationError("sample.input_urls must be a JSON array")
        return cls(
            name=payload["name"],
            output_stem=payload["output_stem"],
            input_urls=tuple(payload["input_urls"]),
            chunks=payload["chunks"],
            stride=payload["stride"],
        )


@dataclass(frozen=True)
class PlannedJob:
    """One concrete worker job derived from a submission request."""

    index: int
    job_name: str
    input_mode: InputMode
    sample_name: Optional[str]
    source_inputs: tuple[str, ...]
    worker_file_list_entries: tuple[str, ...]
    input_list_filename: str
    output_file: str
    output_path: str
    run_arguments: tuple[str, ...]


@dataclass(frozen=True)
class UserBuildPayload:
    """One local archive that supplies a user-built FCCAnalyses runtime."""

    archive_path: str
    size_bytes: int

    def __post_init__(self) -> None:
        _require_absolute_path(self.archive_path, "user_build_payload.archive_path")
        _require_positive_integer(self.size_bytes, "user_build_payload.size_bytes")

    def to_dict(self) -> dict[str, object]:
        return {"archive_path": self.archive_path, "size_bytes": self.size_bytes}

    @classmethod
    def from_dict(cls, payload: object) -> "UserBuildPayload":
        if not isinstance(payload, dict):
            raise SubmissionValidationError("user_build_payload must be a JSON object")
        _require_exact_keys(
            payload,
            {"archive_path", "size_bytes"},
            "user_build_payload",
        )
        return cls(
            archive_path=payload["archive_path"],
            size_bytes=payload["size_bytes"],
        )


@dataclass(frozen=True)
class SubmissionRequest:
    """Versioned data contract between FCCAnalyses and a grid helper process."""

    analysis_script: str
    input_mode: InputMode
    input_lfns: tuple[str, ...]
    samples: tuple[ResolvedSample, ...]
    files_per_job: Optional[int]
    lfn_sample_name: Optional[str]
    run_arguments: tuple[str, ...]
    output_file: str
    output_path: str
    output_se: Optional[str]
    key4hep_setup: str
    job_name: str
    job_group: str
    submit_mode: str
    destination_site: Optional[str]
    submission_id: str
    user_build_payload: Optional[UserBuildPayload]
    analysis_include_archive: Optional[str] = None
    n_chunks: Optional[int] = None

    VERSION = 12

    def __post_init__(self) -> None:
        _require_absolute_path(self.analysis_script, "analysis_script")
        _require_absolute_path(self.key4hep_setup, "key4hep_setup")
        if self.input_mode not in {"xrootd", "dirac-lfn"}:
            raise SubmissionValidationError(
                'input_mode must be "xrootd" or "dirac-lfn"'
            )
        _require_optional_positive_integer(self.files_per_job, "files_per_job")
        _require_optional_positive_integer(self.n_chunks, "n_chunks")
        if self.files_per_job is not None and self.n_chunks is not None:
            raise SubmissionValidationError(
                "files_per_job and n_chunks are mutually exclusive"
            )
        _require_run_arguments(self.run_arguments)

        if self.input_mode == "xrootd":
            if self.input_lfns:
                raise SubmissionValidationError(
                    "xrootd requests must not contain input LFNs"
                )
            if self.lfn_sample_name is not None:
                raise SubmissionValidationError(
                    "xrootd requests must not contain lfn_sample_name"
                )
            if not self.samples:
                raise SubmissionValidationError(
                    "xrootd requests require at least one resolved sample"
                )
            sample_names = tuple(sample.name for sample in self.samples)
            duplicates = _duplicates(sample_names)
            if duplicates:
                raise SubmissionValidationError(
                    f"sample is listed more than once: {duplicates[0]}"
                )
        else:
            if self.samples:
                raise SubmissionValidationError(
                    "dirac-lfn requests must not contain resolved samples"
                )
            group_input_lfns(
                self.input_lfns,
                files_per_job=self.files_per_job,
                n_chunks=self.n_chunks,
            )
            if self.lfn_sample_name is not None:
                _require_simple_name(self.lfn_sample_name, "lfn_sample_name")

        _require_output_filename(self.output_file)
        _require_relative_catalogue_path(self.output_path)
        if self.output_se is not None:
            _require_nonempty_string(self.output_se, "output_se")
        _require_nonempty_string(self.job_name, "job_name")
        _require_nonempty_string(self.job_group, "job_group")
        if self.submit_mode not in {"local", "wms"}:
            raise SubmissionValidationError('submit_mode must be "local" or "wms"')
        if self.destination_site is not None:
            _require_nonempty_string(self.destination_site, "destination_site")
        _require_submission_id(self.submission_id)
        if self.user_build_payload is not None and not isinstance(
            self.user_build_payload,
            UserBuildPayload,
        ):
            raise SubmissionValidationError(
                "user_build_payload must be a UserBuildPayload or null"
            )
        if self.analysis_include_archive is not None:
            _require_absolute_path(
                self.analysis_include_archive,
                "analysis_include_archive",
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "version": self.VERSION,
            "analysis_script": self.analysis_script,
            "input_mode": self.input_mode,
            "input_lfns": list(self.input_lfns),
            "samples": [sample.to_dict() for sample in self.samples],
            "files_per_job": self.files_per_job,
            "n_chunks": self.n_chunks,
            "lfn_sample_name": self.lfn_sample_name,
            "run_arguments": list(self.run_arguments),
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

        if not isinstance(payload, dict):
            raise SubmissionValidationError("submission request must be a JSON object")
        expected_keys = {
            "version",
            "analysis_script",
            "input_mode",
            "input_lfns",
            "samples",
            "files_per_job",
            "n_chunks",
            "lfn_sample_name",
            "run_arguments",
            "output_file",
            "output_path",
            "output_se",
            "key4hep_setup",
            "job_name",
            "job_group",
            "submit_mode",
            "destination_site",
            "submission_id",
            "user_build_payload",
            "analysis_include_archive",
        }
        _require_exact_keys(payload, expected_keys, "submission request")
        if payload["version"] != cls.VERSION:
            raise SubmissionValidationError(
                f"unsupported submission request version: {payload['version']}"
            )
        if not isinstance(payload["input_lfns"], list):
            raise SubmissionValidationError("input_lfns must be a JSON array")
        if not isinstance(payload["samples"], list):
            raise SubmissionValidationError("samples must be a JSON array")
        if not isinstance(payload["run_arguments"], list):
            raise SubmissionValidationError("run_arguments must be a JSON array")
        user_build_payload = payload["user_build_payload"]
        if user_build_payload is not None:
            user_build_payload = UserBuildPayload.from_dict(user_build_payload)
        return cls(
            analysis_script=payload["analysis_script"],
            input_mode=payload["input_mode"],
            input_lfns=tuple(payload["input_lfns"]),
            samples=tuple(ResolvedSample.from_dict(sample) for sample in payload["samples"]),
            files_per_job=payload["files_per_job"],
            n_chunks=payload["n_chunks"],
            lfn_sample_name=payload["lfn_sample_name"],
            run_arguments=tuple(payload["run_arguments"]),
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
    """Expand a validated request into deterministic worker jobs."""
    job_specs = _plan_input_groups(request)
    index_width = max(4, len(str(len(job_specs) - 1)))
    output_path = str(PurePosixPath(request.output_path))
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
        run_arguments.extend(request.run_arguments)

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
                output_path=output_path,
                run_arguments=tuple(run_arguments),
            )
        )
    return tuple(planned_jobs)


def _plan_input_groups(request: SubmissionRequest) -> list[dict[str, object]]:
    if request.input_mode == "dirac-lfn":
        groups = group_input_lfns(
            request.input_lfns,
            files_per_job=request.files_per_job,
            n_chunks=request.n_chunks,
        )
        return [
            {
                "sample_name": request.lfn_sample_name,
                "output_stem": None,
                "source_inputs": group.lfns,
                "worker_inputs": group.staged_filenames,
                "stride": None,
            }
            for group in groups
        ]

    job_specs = []
    for sample in request.samples:
        groups = _group_inputs(
            sample.input_urls,
            n_chunks=request.n_chunks,
            files_per_job=request.files_per_job,
            default_chunks=sample.chunks,
        )
        for group in groups:
            job_specs.append(
                {
                    "sample_name": sample.name,
                    "output_stem": sample.output_stem,
                    "source_inputs": group,
                    "worker_inputs": group,
                    "stride": sample.stride,
                }
            )
    return job_specs


def group_input_lfns(
    input_lfns: Sequence[str],
    files_per_job: Optional[int] = None,
    n_chunks: Optional[int] = None,
) -> tuple[InputGroup, ...]:
    """Validate and group concrete LFNs, including staging-name collisions."""
    _require_optional_positive_integer(files_per_job, "files_per_job")
    _require_optional_positive_integer(n_chunks, "n_chunks")
    if files_per_job is not None and n_chunks is not None:
        raise SubmissionValidationError(
            "files_per_job and n_chunks are mutually exclusive"
        )
    if not input_lfns:
        raise SubmissionValidationError("at least one input LFN is required")
    validated_lfns = tuple(_validate_lfn(lfn) for lfn in input_lfns)
    duplicates = _duplicates(validated_lfns)
    if duplicates:
        raise SubmissionValidationError(
            f"input LFN is listed more than once: {duplicates[0]}"
        )
    grouped_lfns = _group_inputs(
        validated_lfns,
        n_chunks=n_chunks,
        files_per_job=files_per_job,
        default_chunks=len(validated_lfns),
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
    n_chunks: Optional[int],
    files_per_job: Optional[int],
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


def _validate_lfn(lfn: object) -> str:
    if not isinstance(lfn, str):
        raise SubmissionValidationError("input LFNs must be strings")
    if not lfn:
        raise SubmissionValidationError("input LFN must not be empty")
    if not lfn.startswith("/"):
        raise SubmissionValidationError(f"input LFN must be absolute: {lfn}")
    path = PurePosixPath(lfn)
    if path.name in {"", ".", ".."}:
        raise SubmissionValidationError(f"input LFN must name a file: {lfn}")
    if ".." in path.parts:
        raise SubmissionValidationError(f"input LFN must not contain '..': {lfn}")
    return lfn


def _validate_xrootd_url(url: object) -> str:
    if not isinstance(url, str) or not url:
        raise SubmissionValidationError("input URLs must be non-empty strings")
    if not url.startswith("root://"):
        raise SubmissionValidationError(f"input URL must use root://: {url}")
    if ".." in PurePosixPath(url.split("//", 1)[-1]).parts:
        raise SubmissionValidationError(f"input URL must not contain '..': {url}")
    return url


def _duplicates(values: Sequence[str]) -> tuple[str, ...]:
    seen = set()
    duplicates = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return tuple(duplicates)


def _require_exact_keys(
    payload: dict[str, object], expected_keys: set[str], description: str
) -> None:
    missing_keys = expected_keys - set(payload)
    unknown_keys = set(payload) - expected_keys
    if not missing_keys and not unknown_keys:
        return
    details = []
    if missing_keys:
        details.append("missing " + ", ".join(sorted(missing_keys)))
    if unknown_keys:
        details.append("unknown " + ", ".join(sorted(unknown_keys)))
    raise SubmissionValidationError(
        f"invalid {description} keys: " + "; ".join(details)
    )


def _require_absolute_path(value: object, name: str) -> None:
    if not isinstance(value, str) or not value:
        raise SubmissionValidationError(f"{name} must be a non-empty path")
    if not Path(value).is_absolute():
        raise SubmissionValidationError(f"{name} must be an absolute path")


def _require_nonempty_string(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SubmissionValidationError(f"{name} must be a non-empty string")


def _require_simple_name(value: object, name: str) -> None:
    _require_nonempty_string(value, name)
    path = PurePosixPath(value)
    if path.name != value or value in {".", ".."}:
        raise SubmissionValidationError(f"{name} must be a simple name")


def _require_positive_integer(value: object, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise SubmissionValidationError(f"{name} must be greater than zero")


def _require_optional_positive_integer(value: object, name: str) -> None:
    if value is not None:
        _require_positive_integer(value, name)


def _require_run_arguments(value: object) -> None:
    if not isinstance(value, tuple) or not all(isinstance(item, str) for item in value):
        raise SubmissionValidationError("run_arguments must be a tuple of strings")


def _require_output_filename(value: object) -> None:
    _require_simple_name(value, "output_file")


def _require_relative_catalogue_path(value: object) -> None:
    _require_nonempty_string(value, "output_path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise SubmissionValidationError(
            "output_path must be a relative catalogue path without '..'"
        )


def _require_submission_id(value: object) -> None:
    _require_nonempty_string(value, "submission_id")
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value) is None:
        raise SubmissionValidationError(
            "submission_id may contain only letters, digits, '.', '_' and '-'"
        )


def _planned_output_filename(
    filename: str,
    output_stem: Optional[str],
    index: int,
    width: int,
) -> str:
    path = PurePosixPath(filename)
    suffix = path.suffix
    stem = path.name[:-len(suffix)] if suffix else path.name
    sample_part = f"_{output_stem}" if output_stem is not None else ""
    return f"{stem}{sample_part}_{index:0{width}d}{suffix}"
