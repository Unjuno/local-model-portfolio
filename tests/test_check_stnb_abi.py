"""Deterministic synthetic-header checks; no model weights or network are needed."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from scripts.check_stnb_abi import inspect_header, main


class NanoSTNBTests(unittest.TestCase):
    def test_v1_header_matches_pinned_c_loader_only(self):
        a = inspect_header(b"STNB" + (1).to_bytes(4, "little"))
        self.assertEqual(a["verdict"], "PASS_HEADER_VERSION_ONLY")
        self.assertEqual(a["actual_version"], 1)
        self.assertIn("UNTESTED", a["meaning"])

    def test_v2_header_rejected_by_v1_loader(self):
        a = inspect_header(b"STNB" + (2).to_bytes(4, "little"))
        self.assertEqual(a["verdict"], "FAIL_VERSION_MISMATCH")
        self.assertEqual(a["loader_version"], 1)
        self.assertEqual(a["actual_version"], 2)
        self.assertEqual(inspect_header(b"STNB" + (2).to_bytes(4, "little"), 2)["verdict"], "PASS_HEADER_VERSION_ONLY")

    def test_wrong_magic_and_truncated(self):
        self.assertEqual(inspect_header(b"NOPE" + (1).to_bytes(4, "little"))["verdict"], "FAIL_MAGIC")
        self.assertEqual(inspect_header(b"STNB\x02")["verdict"], "UNCERTAIN_TRUNCATED")

    def test_fail_closed_on_invalid_runtime_version(self):
        for val in (0, -1, True):
            with self.subTest(val=val), self.assertRaises(ValueError):
                inspect_header(b"STNB" + (1).to_bytes(4, "little"), val)

    def test_local_synthetic_files_and_missing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "fake-nano.bin"
            path.write_bytes(b"STNB" + (2).to_bytes(4, "little") + bytes(12))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = main([str(path)])
            self.assertEqual(code, 1)
            self.assertEqual(json.loads(out.getvalue())["verdict"], "FAIL_VERSION_MISMATCH")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = main([str(path), "--loader-version", "2"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out.getvalue())["verdict"], "PASS_HEADER_VERSION_ONLY")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = main([str(Path(folder) / "missing.bin")])
            self.assertEqual(code, 2)
            self.assertEqual(json.loads(out.getvalue())["verdict"], "UNCERTAIN_FILE_ACCESS")


if __name__ == "__main__":
    unittest.main()
