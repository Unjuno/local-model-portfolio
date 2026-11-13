"""Read-only November 6 primary sources, explicit evidence-grain tests."""
import unittest
from scripts import research_nov6_candidates as r

class NovemberReleaseResearchTests(unittest.TestCase):
    def test_bounded_four_not_auto_download(self):
        self.assertEqual(len(r.SCOPE),4)
        self.assertEqual(len(set(r.SCOPE)),4)
        self.assertTrue(all(not r.DECISION[k].startswith('APPROVED') for k in r.SCOPE))
    def test_oversize_gated_stays_research(self):
        q='orcarouter/GLM-5.3-Flash-Uncensored-GGUF'
        self.assertIn('RESEARCH_ONLY',r.DECISION[q])
        self.assertIn('MTP',r.NEGATIVE[q])
        self.assertIn('matched',r.NEGATIVE[q])
    def test_world_model_variants_are_distinct_not_all_selected(self):
        self.assertIn('HOLD',r.DECISION['nvidia/Cosmos3-Nano-Sim-Auto'])
        self.assertIn('action',r.POSITIVE['nvidia/Cosmos3-Nano-Sim-Bimanual'])
    def test_release_sourced_and_license_nontrivial(self):
        self.assertIn('www.preferred.jp',r.SOURCE_URLS['pfnet/plamo-3-translate-31b'][0])
        self.assertIn('community license',r.NEGATIVE['pfnet/plamo-3-translate-31b'])
if __name__=='__main__':unittest.main()
