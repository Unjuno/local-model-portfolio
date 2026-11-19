"""Safety tests for creating an UNAPPROVED owner-side batch review template."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts import prepare_owner_scope_approval as template
from scripts import download_r115_windows as engine


class OwnerTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = template.DEFAULT_MANIFEST

    def test_four_source_fingerprints_and_never_approved(self):
        with tempfile.TemporaryDirectory() as td:
            plan = template.prepare(self.manifest, Path(td))
            self.assertEqual(plan["schema_version"], 1)
            self.assertEqual(len(plan["entries"]), 4)
            self.assertEqual(plan["owner_disk_observation"]
                             ["publisher_source_bytes_if_all_new"], 6_127_042_272)
            self.assertFalse(any(row["approved"] for row in plan["entries"]))
            self.assertFalse(any(row["user_explicit_manifest_consent"] for row in plan["entries"]))
            self.assertFalse(any(row["license_and_parent_rights_reviewed"] for row in plan["entries"]))
            self.assertFalse(any(row["owner_archive_volume_verified"] for row in plan["entries"]))
            raw = json.loads(self.manifest.read_text(encoding="utf-8"))
            expected = engine.validate_manifest(raw)
            for i, row in enumerate(plan["entries"]):
                self.assertEqual(row["source_scope_sha256"], engine.source_fingerprint(expected[i]))

    def test_data_namespaces_not_ambiguous(self):
        with tempfile.TemporaryDirectory() as td:
            plan = template.prepare(self.manifest, Path(td))
            self.assertEqual([e["repository_type"] for e in plan["entries"]],
                             ["dataset", "dataset", "model", "model"])
            elyza = plan["entries"][0]
            self.assertNotEqual(elyza["source_scope_sha256"], engine.source_fingerprint({
                **engine.validate_manifest(json.loads(
                    self.manifest.read_text(encoding="utf-8")))[0],
                "repository_type": "model"
            }))

    def test_no_automatic_approval_from_generated_template(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "owner_approval.json"
            plan = template.prepare(self.manifest, Path(td))
            template.write_template(plan, Path(td), path)
            with self.assertRaises(ValueError):
                engine.assert_explicit_approved_sources(
                    engine.validate_manifest(json.loads(self.manifest.read_text(encoding="utf-8"))),
                    path
                )

    def test_write_inside_archive_only_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "archive"
            root.mkdir()
            plan = template.prepare(self.manifest, root)
            output = root / "approvals" / "review.json"
            template.write_template(plan, root, output)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["entries"][0]
                             ["approved"], False)
            with self.assertRaises(FileExistsError):
                template.write_template(plan, root, output)

    def test_no_approval_write_outside_archive(self):
        with tempfile.TemporaryDirectory() as td:
            top = Path(td)
            root = top / "archive"
            root.mkdir()
            plan = template.prepare(self.manifest, root)
            with self.assertRaises(ValueError):
                template.write_template(plan, root, top / "outside.json")
            with self.assertRaises(ValueError):
                template.write_template(plan, root, Path("relative.json"))

    def test_symlink_archive_and_missing_root_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            missing = root / "missing"
            with self.assertRaises(ValueError):
                template.prepare(self.manifest, missing)
            link = root / "link"
            link.symlink_to(root, target_is_directory=True)
            with self.assertRaises(ValueError):
                template.prepare(self.manifest, link)

    def test_disk_floor_not_weakened(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            plan = template.prepare(self.manifest, root)
            observed = plan["owner_disk_observation"]
            self.assertGreaterEqual(observed["minimum_free_floor_bytes"], 200_000_000_000)
            self.assertEqual(observed["conservative_required_free_bytes"],
                             observed["minimum_free_floor_bytes"]
                             + observed["publisher_source_bytes_if_all_new"]
                             + 2 * observed["maximum_single_source_file_bytes"])
            self.assertTrue(observed["not_a_full_offline_dependency_closure"])


if __name__ == "__main__":
    unittest.main()
