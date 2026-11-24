"""R149 source-priority research integrity checks; never downloads or imports model code."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

class Post99PriorityIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = load('catalog/CURRENT.json')
        cls.prior = load('queues/proposed-v63-r149-after99-11-research-only.json')
        cls.new = load('queues/proposed-v63-r150-prioritized-sources-and-watchlist.json')
        cls.audit = load('catalog/research/2026-11-22-r149-post99-compact-and-rare-source-screen.json')

    def test_canonical_unmodified(self):
        self.assertIn(self.current['revision_id'], ('v63-20261122','v64-20261122','v65-20261122', 'v66-20261124','v67-20261124'))
        self.assertEqual(load('catalog/effective-portfolio-2026-11-22-v63.json')['counts']['tracked'], 235)
        self.assertEqual(load('catalog/effective-portfolio-2026-11-22-v63.json')['counts']['active'], 188)
        self.assertEqual(load('catalog/effective-portfolio-2026-11-22-v63.json')['counts']['by_decision']['select'], 55)
        self.assertEqual(load('catalog/effective-portfolio-2026-11-22-v63.json')['counts']['by_decision']['conditional'], 133)
        self.assertEqual(load('queues/approved.json')['entries'], [])

    def test_exact_publisher_identity_and_no_implicit_approval(self):
        old = {x['repo_id']: x for x in self.prior['candidate_research_only']}
        entries = self.new['priority_sources']
        self.assertEqual(len(entries), len(old))
        self.assertEqual(len(entries), 11)
        self.assertEqual(set(old), {x['repo_id'] for x in entries})
        for x in entries:
            before = old[x['repo_id']]
            self.assertTrue(re.fullmatch(r'[0-9a-f]{40}', x['publisher_revision_sha']))
            self.assertEqual(x['publisher_revision_sha'], before['publisher_revision_sha'])
            self.assertEqual(x['publisher_reference_bytes'], before['publisher_reference_bytes'])
            self.assertEqual(x['source_manifest'], before['source_manifest'])
            self.assertFalse(x['download_approved'])
            self.assertFalse(x['download_enabled'])
            self.assertFalse(x['owner_manifest_approval_present'])

    def test_phase_sources_budget_reconciles(self):
        phases = self.new['phase_decisions']
        expected = {'P0A': 3620182749, 'P0B': 349292901, 'P1': 9188749234, 'P2': 947927443, 'P3': 54438018606, 'P4': 129572889973}
        self.assertEqual({p['phase']: p['source_bytes'] for p in phases}, expected)
        self.assertEqual(sum(p['source_bytes'] for p in phases if p['phase'] != 'P4'), 68544170933)
        self.assertEqual(self.new['nonhold_10_publisher_source_bytes'], 68544170933)
        self.assertEqual(self.new['unduplicated_sum_not_claimed_referenced_bytes'], 86115544829)
        self.assertEqual(self.new['formal_catalog_new_entries'], 0)
        self.assertEqual(self.new['approved_download_entries_added'], 0)

    def test_new_releases_not_promoted(self):
        watch = self.new['new_release_unfrozen_watchlist']
        self.assertEqual(len(watch), 5)
        self.assertEqual(len({x['repo_id'] for x in watch}), 5)
        for x in watch:
            self.assertIsNone(x['publisher_revision_sha'])
            self.assertIsNone(x['selected_files'])
            self.assertIsNone(x['selected_file_bytes'])
            self.assertFalse(x['formal_catalog_adoption'])
            self.assertFalse(x['download_approved'])
        self.assertEqual(len(self.audit['model_source_evidence']), 11)

if __name__ == '__main__':
    unittest.main()
