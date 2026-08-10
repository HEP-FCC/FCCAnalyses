"""Tests for validating and packaging a user-built FCCAnalyses runtime."""

import stat
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "python"))

from software_payload import (
    PAYLOAD_ROOT,
    SoftwarePayloadError,
    create_user_build_archive,
    validate_user_build,
)


class SoftwarePayloadTest(unittest.TestCase):
    """Exercise the local-build compatibility and archive boundaries."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        temporary_path = Path(self.temporary_directory.name).resolve()

        self.source_dir = temporary_path / "FCCAnalyses"
        self.install_dir = self.source_dir / "install"
        self.setup_script = self.source_dir / "setup.sh"
        self.stack_record = self.source_dir / ".fccana" / "stack_build"
        self.fccanalysis_executable = self.install_dir / "bin" / "fccanalysis"
        self.key4hep_setup = temporary_path / "key4hep" / "setup.sh"

        self.fccanalysis_executable.parent.mkdir(parents=True)
        self.stack_record.parent.mkdir(parents=True)
        self.key4hep_setup.parent.mkdir(parents=True)
        (self.install_dir / "lib").mkdir()

        self.setup_script.write_text("# setup\n", encoding="utf-8")
        self.key4hep_setup.write_text("# key4hep\n", encoding="utf-8")
        self.fccanalysis_executable.write_text(
            "#!/usr/bin/env python3\n",
            encoding="utf-8",
        )
        self.fccanalysis_executable.chmod(
            self.fccanalysis_executable.stat().st_mode | stat.S_IXUSR
        )
        self.stack_record.write_text(
            f"{self.key4hep_setup}\n",
            encoding="utf-8",
        )
        (self.install_dir / "lib" / "libFCCAnalyses.so").write_text(
            "library\n",
            encoding="utf-8",
        )
        (self.source_dir / "not-in-payload.txt").write_text(
            "source file\n",
            encoding="utf-8",
        )
        self.environment = {
            "FCCANA_LOCAL_DIR": str(self.source_dir),
            "KEY4HEP_STACK": str(self.key4hep_setup),
        }

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_validates_build_and_creates_expected_archive(self) -> None:
        build = validate_user_build(self.environment)
        archive_path = Path(self.temporary_directory.name) / "payload.tar.gz"

        payload = create_user_build_archive(build, archive_path)

        self.assertEqual(build.key4hep_setup, self.key4hep_setup)
        self.assertEqual(payload.path, archive_path.resolve())
        self.assertGreater(payload.size_bytes, 0)
        with tarfile.open(payload.path, "r:gz") as archive:
            names = archive.getnames()
            self.assertIn(f"{PAYLOAD_ROOT}/setup.sh", names)
            self.assertIn(f"{PAYLOAD_ROOT}/.fccana/stack_build", names)
            self.assertIn(f"{PAYLOAD_ROOT}/install/bin/fccanalysis", names)
            self.assertIn(
                f"{PAYLOAD_ROOT}/install/lib/libFCCAnalyses.so",
                names,
            )
            self.assertNotIn(f"{PAYLOAD_ROOT}/not-in-payload.txt", names)
            executable = archive.getmember(
                f"{PAYLOAD_ROOT}/install/bin/fccanalysis"
            )
            self.assertTrue(executable.mode & stat.S_IXUSR)

    def test_requires_submission_environment(self) -> None:
        incomplete_environments = (
            ({"KEY4HEP_STACK": str(self.key4hep_setup)}, "FCCANA_LOCAL_DIR"),
            ({"FCCANA_LOCAL_DIR": str(self.source_dir)}, "KEY4HEP_STACK"),
        )

        for environment, message in incomplete_environments:
            with self.subTest(message=message):
                with self.assertRaisesRegex(SoftwarePayloadError, message):
                    validate_user_build(environment)

    def test_rejects_stack_mismatch(self) -> None:
        other_stack = Path(self.temporary_directory.name) / "other" / "setup.sh"
        other_stack.parent.mkdir()
        other_stack.write_text("# other key4hep\n", encoding="utf-8")
        self.environment["KEY4HEP_STACK"] = str(other_stack)

        with self.assertRaisesRegex(SoftwarePayloadError, "does not match"):
            validate_user_build(self.environment)

    def test_creates_byte_identical_archives(self) -> None:
        build = validate_user_build(self.environment)
        first_path = Path(self.temporary_directory.name) / "first.tar.gz"
        second_path = Path(self.temporary_directory.name) / "second.tar.gz"

        create_user_build_archive(build, first_path)
        create_user_build_archive(build, second_path)

        self.assertEqual(first_path.read_bytes(), second_path.read_bytes())

    def test_strips_shared_objects_without_modifying_build(self) -> None:
        library = self.install_dir / "lib" / "libFCCAnalyses.so"
        original_contents = b"\x7fELF\x02\x01" + b"\0" * 10 + b"\x03\0debug"
        library.write_bytes(original_contents)
        archive_path = Path(self.temporary_directory.name) / "payload.tar.gz"

        def strip_debug(command, check):
            self.assertTrue(check)
            self.assertEqual(command[1:3], ["--strip-debug", "-o"])
            Path(command[3]).write_bytes(b"stripped library")

        with patch("software_payload.shutil.which", return_value="/usr/bin/strip"):
            with patch(
                "software_payload.subprocess.run",
                side_effect=strip_debug,
            ):
                create_user_build_archive(
                    validate_user_build(self.environment),
                    archive_path,
                )

        self.assertEqual(library.read_bytes(), original_contents)
        with tarfile.open(archive_path, "r:gz") as archive:
            member = archive.extractfile(
                f"{PAYLOAD_ROOT}/install/lib/libFCCAnalyses.so"
            )
            self.assertIsNotNone(member)
            self.assertEqual(member.read(), b"stripped library")

    def test_rejects_archive_inside_source_directory(self) -> None:
        with self.assertRaisesRegex(SoftwarePayloadError, "outside"):
            create_user_build_archive(
                validate_user_build(self.environment),
                self.source_dir / "payload.tar.gz",
            )


if __name__ == "__main__":
    unittest.main()
