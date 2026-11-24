"""Reject partial HF source trees and unexpected cursor hosts; no HTTP calls."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("audit_hf_tree_pagination", ROOT / "scripts/audit_hf_tree_pagination.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)
REPO = "publisher/example"
REV = "a" * 40


class CursorSafety(unittest.TestCase):
    def test_follows_both_pages_and_keeps_full_count(self):
        page1 = [{"type": "file", "path": f"model-{i:02}.safetensors", "size": 42,
                  "oid": "b" * 40, "lfs": {"oid": "c" * 64}} for i in range(50)]
        page2 = [{"type": "file", "path": f"model-{i:02}.safetensors", "size": 41,
                  "oid": "b" * 40} for i in range(50, 62)]
        requests = []
        def opener(url):
            requests.append(url)
            if len(requests) == 1:
                nexturl = f"https://huggingface.co/api/models/{REPO}/tree/{REV}?recursive=true&expand=true&cursor=CURSOR123"
                return page1, f'<{nexturl}>; rel="next"'
            return page2, None
        result = mod.list_all_immutable_files(REPO, REV, opener=opener)
        self.assertEqual(len(requests), 2)
        self.assertEqual(result["file_count"], 62)
        self.assertEqual(result["pages_fetched"], 2)
        self.assertEqual(result["source_bytes"], 50*42+12*41)
        self.assertEqual(result["lfs_sha256_available"], 50)

    def test_blocks_unexpected_host(self):
        with self.assertRaises(ValueError):
            mod.next_page(f'<https://evil.example/api/models/{REPO}/tree/{REV}?cursor=x>; rel="next"', REPO, REV)

    def test_blocks_duplicate_path_across_pages(self):
        ff = {"type": "file", "path": "model.safetensors", "size": 1, "oid": "b"*40}
        cnt = [0]
        def opener(url):
            cnt[0] += 1
            if cnt[0] == 1:
                return [ff], f'<https://huggingface.co/api/models/{REPO}/tree/{REV}?cursor=NEXT>; rel="next"'
            return [ff], None
        with self.assertRaises(ValueError):
            mod.list_all_immutable_files(REPO, REV, opener=opener)

    def test_masks_unavailable_digest_instead_of_forging(self):
        obj = {"type": "file", "path": "gated.safetensors", "size": 31,
               "oid": "a" * 40, "lfs": {"oid": "*"*64}}
        result = mod.list_all_immutable_files(REPO, REV, opener=lambda url: ([obj], None))
        self.assertEqual(result["lfs_masked"], 1)
        self.assertIsNone(result["files"][0]["publisher_lfs_sha256"])

if __name__ == "__main__":
    unittest.main()
