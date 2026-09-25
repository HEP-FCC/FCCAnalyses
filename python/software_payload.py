"""Create a reproducible payload for a locally built FCCAnalyses installation.

This Key4hep-side module validates that the active Key4hep stack matches the
one used to build FCCAnalyses. It packages only the installed runtime, setup
script, and recorded build-stack path for staging through a DIRAC input sandbox.
Archive metadata is normalised and ELF shared-library debug information is
removed to keep payloads reproducible and compact.
"""

from collections.abc import Mapping
from dataclasses import dataclass
import gzip
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
from typing import Optional


class SoftwarePayloadError(ValueError):
    """Raised when a local FCCAnalyses build cannot be shipped safely."""


@dataclass(frozen=True)
class ValidatedUserBuild:
    """Filesystem contract for one validated local FCCAnalyses installation."""

    source_dir: Path
    install_dir: Path
    setup_script: Path
    stack_record: Path
    key4hep_setup: Path
    fccanalysis_executable: Path


@dataclass(frozen=True)
class UserBuildArchive:
    """One reproducible archive containing a validated user build."""

    path: Path
    size_bytes: int


PAYLOAD_ROOT = "fccanalyses-payload"


def validate_user_build(
    environment: Optional[Mapping[str, str]] = None,
) -> ValidatedUserBuild:
    """Validate the active local build required for a future grid payload."""
    environment = os.environ if environment is None else environment

    source_dir_value = environment.get("FCCANA_LOCAL_DIR")
    if not source_dir_value:
        raise SoftwarePayloadError(
            "User-build grid submission requires FCCANA_LOCAL_DIR. "
            "Source the setup.sh of the FCCAnalyses checkout to submit."
        )

    active_stack_value = environment.get("KEY4HEP_STACK")
    if not active_stack_value:
        raise SoftwarePayloadError(
            "User-build grid submission requires KEY4HEP_STACK. "
            "Source the intended Key4hep stack and FCCAnalyses setup.sh."
        )

    source_dir = Path(source_dir_value).expanduser().resolve()
    _require_directory(source_dir, "FCCAnalyses source directory")

    install_dir = source_dir / "install"
    setup_script = source_dir / "setup.sh"
    stack_record = source_dir / ".fccana" / "stack_build"
    fccanalysis_executable = install_dir / "bin" / "fccanalysis"

    _require_directory(install_dir, "FCCAnalyses install directory")
    _require_readable_file(setup_script, "FCCAnalyses setup script")
    _require_readable_file(stack_record, "Key4hep build-stack record")
    _require_executable(fccanalysis_executable, "installed fccanalysis executable")

    recorded_stack = _read_stack_record(stack_record)
    active_stack = Path(active_stack_value).expanduser()
    if not active_stack.is_absolute():
        raise SoftwarePayloadError(
            f"KEY4HEP_STACK must be an absolute path: {active_stack_value}"
        )

    _require_readable_file(recorded_stack, "recorded Key4hep setup script")
    _require_readable_file(active_stack, "active Key4hep setup script")
    resolved_recorded_stack = recorded_stack.resolve()
    active_stack = active_stack.resolve()
    if resolved_recorded_stack != active_stack:
        raise SoftwarePayloadError(
            "The active Key4hep stack does not match the stack used to build "
            "FCCAnalyses:\n"
            f"  build stack:  {resolved_recorded_stack}\n"
            f"  active stack: {active_stack}\n"
            "From the local FCCAnalyses build directory, run "
            "`source ./setup.sh --from-build` before submitting."
        )

    return ValidatedUserBuild(
        source_dir=source_dir,
        install_dir=install_dir,
        setup_script=setup_script,
        stack_record=stack_record,
        key4hep_setup=recorded_stack,
        fccanalysis_executable=fccanalysis_executable,
    )


def create_user_build_archive(
    build: ValidatedUserBuild,
    archive_path: Path,
) -> UserBuildArchive:
    """Create a deterministic tar.gz archive for a validated user build."""
    archive_path = archive_path.expanduser().resolve()
    if archive_path.exists():
        raise SoftwarePayloadError(f"Payload archive already exists: {archive_path}")
    if not archive_path.parent.is_dir():
        raise SoftwarePayloadError(
            f"Payload archive directory does not exist: {archive_path.parent}"
        )
    if _is_within(archive_path, build.source_dir):
        raise SoftwarePayloadError(
            "Payload archive must be created outside the FCCAnalyses source "
            f"directory: {archive_path}"
        )

    try:
        with tempfile.TemporaryDirectory(prefix="fccanalyses-payload-") as directory:
            stripped_directory = Path(directory)
            with archive_path.open("xb") as archive_file:
                with gzip.GzipFile(
                    filename="",
                    mode="wb",
                    fileobj=archive_file,
                    mtime=0,
                ) as compressed_file:
                    with tarfile.open(
                        mode="w",
                        fileobj=compressed_file,
                        format=tarfile.PAX_FORMAT,
                        dereference=False,
                    ) as archive:
                        _add_root_directory(archive)
                        _add_directory_entry(
                            archive,
                            build.stack_record.parent,
                            f"{PAYLOAD_ROOT}/.fccana",
                        )
                        _add_path(
                            archive,
                            build.stack_record,
                            f"{PAYLOAD_ROOT}/.fccana/stack_build",
                            stripped_directory,
                        )
                        _add_path(
                            archive,
                            build.install_dir,
                            f"{PAYLOAD_ROOT}/install",
                            stripped_directory,
                        )
                        _add_path(
                            archive,
                            build.setup_script,
                            f"{PAYLOAD_ROOT}/setup.sh",
                            stripped_directory,
                        )
    except Exception:
        archive_path.unlink(missing_ok=True)
        raise

    return UserBuildArchive(
        path=archive_path,
        size_bytes=archive_path.stat().st_size,
    )


def _read_stack_record(path: Path) -> Path:
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) != 1 or not lines[0].strip():
        raise SoftwarePayloadError(
            f"Key4hep build-stack record must contain exactly one path: {path}"
        )

    stack_path = Path(lines[0].strip()).expanduser()
    if not stack_path.is_absolute():
        raise SoftwarePayloadError(
            f"Key4hep build-stack record must contain an absolute path: {path}"
        )
    return stack_path


def _add_root_directory(archive: tarfile.TarFile) -> None:
    info = tarfile.TarInfo(PAYLOAD_ROOT)
    info.type = tarfile.DIRTYPE
    info.mode = 0o755
    _normalise_metadata(info)
    archive.addfile(info)


def _add_directory_entry(
    archive: tarfile.TarFile,
    source_path: Path,
    archive_name: str,
) -> None:
    info = archive.gettarinfo(str(source_path), arcname=archive_name)
    if not info.isdir():
        raise SoftwarePayloadError(f"Expected a directory to archive: {source_path}")
    _normalise_metadata(info)
    archive.addfile(info)


def _add_path(
    archive: tarfile.TarFile,
    source_path: Path,
    archive_name: str,
    stripped_directory: Path,
) -> None:
    info = archive.gettarinfo(str(source_path), arcname=archive_name)
    _normalise_metadata(info)

    if info.isreg():
        archive_source = _stripped_shared_object(source_path, stripped_directory)
        if archive_source != source_path:
            info.size = archive_source.stat().st_size
        with archive_source.open("rb") as source_file:
            archive.addfile(info, source_file)
    else:
        archive.addfile(info)

    if info.isdir():
        for child in sorted(source_path.iterdir(), key=lambda path: path.name):
            _add_path(
                archive,
                child,
                f"{archive_name}/{child.name}",
                stripped_directory,
            )


def _stripped_shared_object(source_path: Path, directory: Path) -> Path:
    """Return a temporary debug-stripped copy of an ELF shared object."""
    if not _is_elf_shared_object(source_path):
        return source_path

    strip = shutil.which("strip")
    if strip is None:
        raise SoftwarePayloadError(
            "Cannot package ELF shared libraries: the `strip` command is unavailable"
        )

    with tempfile.NamedTemporaryFile(dir=directory, delete=False) as temporary_file:
        stripped_path = Path(temporary_file.name)
    stripped_path.unlink()
    try:
        subprocess.run(
            [strip, "--strip-debug", "-o", str(stripped_path), str(source_path)],
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        stripped_path.unlink(missing_ok=True)
        raise SoftwarePayloadError(
            f"Cannot strip debug information from shared library: {source_path}"
        ) from error
    return stripped_path


def _is_elf_shared_object(path: Path) -> bool:
    """Return whether path is an ELF ET_DYN object, including shared libraries."""
    with path.open("rb") as source_file:
        header = source_file.read(18)
    if len(header) != 18 or header[:4] != b"\x7fELF":
        return False
    if header[4] not in (1, 2) or header[5] not in (1, 2):
        return False

    byteorder = "little" if header[5] == 1 else "big"
    return int.from_bytes(header[16:18], byteorder) == 3


def _normalise_metadata(info: tarfile.TarInfo) -> None:
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0


def _is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def _require_directory(path: Path, description: str) -> None:
    if not path.is_dir():
        raise SoftwarePayloadError(f"{description} not found: {path}")


def _require_readable_file(path: Path, description: str) -> None:
    if not path.is_file() or not os.access(path, os.R_OK):
        raise SoftwarePayloadError(f"{description} is not readable: {path}")


def _require_executable(path: Path, description: str) -> None:
    if not path.is_file() or not os.access(path, os.X_OK):
        raise SoftwarePayloadError(f"{description} is not executable: {path}")
