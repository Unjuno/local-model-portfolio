"""R126: original Microsoft Aion Windows SLM source, offline invariant tests."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/download_r115_windows.py"
SOURCE = ROOT / "queues/proposed-v53-r126-aion-bf16-first-public-source.json"
PREV = ROOT / "catalog/effective-portfolio-2026-11-19-v52.json"
CURRENT = ROOT / "catalog/effective-portfolio-2026-11-20-v53.json"
LOG = ROOT / "catalog/execution/2026-11-19-acquisition-ledger.json"
spec = importlib.util.spec_from_file_location("archive_aion", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def jsonfile(p):
    return json.loads(p.read_text(encoding="utf-8"))


class AionArchiveTests(unittest.TestCase):
    def test_immutable_manifest(self):
        d = jsonfile(SOURCE)
        sources = mod.validate_manifest(d)
        self.assertEqual(len(sources), 1)
        m = sources[0]
        self.assertEqual(m["source_repo_id"], "microsoft/Aion-1.0-Instruct-2.3B")
        self.assertEqual(m["source_revision"], "28902cbfd9f4e0347d6c853aa1301f5d559b2fc0")
        self.assertEqual(m["license_metadata"], "mit")
        self.assertFalse(m["gated"])
        self.assertEqual(len(m["files"]), 11)
        self.assertEqual(m["source_bytes"], 4593276272)
        self.assertEqual(sum(x["bytes"] for x in m["files"]), 4593276272)
        weights = [x for x in m["files"] if x["path"] == "model.safetensors"]
        self.assertEqual(len(weights), 1)
        self.assertEqual(weights[0]["bytes"], 4577698688)
        self.assertEqual(weights[0]["sha256"],
                         "6c779881b539d9074f356964ad3089459e9e837da7649d6f271859135256984e")

    def test_original_code_and_license_present_no_quantizations(self):
        m = mod.validate_manifest(jsonfile(SOURCE))[0]
        paths = {x["path"] for x in m["files"]}
        self.assertTrue({"LICENSE", "README.md", "tokenizer.json",
                         "configuration_aion_instruct.py", "modeling_aion_instruct.py",
                         "config.json", "chat_template.jinja"}.issubset(paths))
        self.assertFalse(any("/" in x or x.endswith((".gguf", ".onnx", ".pt", ".pth"))
                             for x in paths))
        self.assertTrue(all(x["sha256"] or x["git_blob_sha1"] for x in m["files"]))

    def test_existing_205_are_exactly_preserved(self):
        a = jsonfile(PREV)
        b = jsonfile(CURRENT)
        self.assertEqual(len(a["items"]), 205)
        self.assertEqual(len(b["items"]), 206)
        self.assertEqual(a["items"], b["items"][:205])
        self.assertEqual(b["items"][205]["repo_id"], "microsoft/Aion-1.0-Instruct-2.3B")
        self.assertEqual(b["counts"]["active"], 159)
        self.assertEqual(b["counts"]["by_decision"]["conditional"], 106)

    def test_no_claim_of_prior_owner_acquisition(self):
        entries = jsonfile(LOG)["models"]
        acq=[x for x in entries if x["repo_id"] == "microsoft/Aion-1.0-Instruct-2.3B"]
        self.assertEqual(len(acq),1)
        self.assertEqual(acq[0]["status"],"VERIFIED")
        self.assertFalse(jsonfile(CURRENT)["items"][-1]["download_approved"])

    def test_execution_requires_exact_owner_approval(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "approved.json"
            path.write_text('{"schema_version":1,"entries":[]}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "No explicitly approved"):
                mod.assert_explicit_approved_sources(mod.validate_manifest(jsonfile(SOURCE)), path)


if __name__ == "__main__":
    unittest.main()
