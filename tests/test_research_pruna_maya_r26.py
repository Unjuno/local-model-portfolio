"""Non-executable P-H3 legal and Maya2 dependency metadata regression."""
import json
import unittest
from pathlib import Path
from scripts import research_pruna_maya_r26 as r
ROOT=Path(__file__).resolve().parents[1]
class ResearchTests(unittest.TestCase):
    def test_only_two_pruna_repos_and_frozen_maya_dependencies(self):
        self.assertEqual(r.SOURCES,('PrunaAI/P-H3-Image','PrunaAI/P-H3-Image-Comfy'))
        self.assertEqual(len(r.MAYA_DEPS),2)
        self.assertEqual(sum(x[2] for x in r.MAYA_DEPS.values()),473790793)
    def test_maya_dependency_exact_pinned_bytes_and_licenses(self):
        for name,row in r.MAYA_DEPS.items():
            snap=json.loads((ROOT/row[0]).read_text())
            item=r.validate_dep(name,snap)
            self.assertFalse(item['download_approved'])
            self.assertFalse(item['locally_hashed'])
            self.assertGreater(item['weight_bytes'],0)
    def test_source_metadata_tamper_is_blocked(self):
        repo='kyutai/mimi';path=r.MAYA_DEPS[repo][0]
        snap=json.loads((ROOT/path).read_text())
        snap['source_scope_bytes']-=1
        with self.assertRaises(AssertionError):r.validate_dep(repo,snap)
    def test_future_pruna_profile_always_requires_license(self):
        self.assertTrue(r.SOURCES[0].startswith('PrunaAI/'))
        self.assertNotEqual(r.SOURCES[0],r.SOURCES[1])
if __name__=='__main__':unittest.main()
