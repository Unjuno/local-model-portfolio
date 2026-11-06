"""Non-executable v23 chosen-file profile checks."""
import importlib
import json
import unittest
from pathlib import Path
from scripts import capacity_selection_v23 as mod

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))

class V23CapacityTests(unittest.TestCase):
    def src(self):
        return {repo:load(rule['source_path']) for repo,rule in mod.NEW.items()}
    def test_exact_two_sources_and_original_shards(self):
        old=load(mod.HIST/'selected-file-capacity.json')
        view=load('catalog/effective-portfolio-2026-11-06-v23.json')
        overlay=load('catalog/revisions/v23-2026-11-06.json')
        rows=mod.verify_sources(old,view,overlay,self.src())
        self.assertEqual(len(rows),118)
        self.assertTrue(all(r['primary_file_bytes'] is not None for r in rows))
        h=next(r for r in rows if r['repo_id']=='Hcompany/Holotron4-30B-A3B')
        self.assertEqual(sum(x['path'].endswith('.safetensors') for x in h['files']),17)
        self.assertEqual(h['source_revision'],'52184310f6c916e5e7d4b8f055af49fc41642574')
        self.assertLessEqual(h['primary_file_bytes'],66_051_239_820)
        d=next(r for r in rows if r['repo_id']=='LiquidAI/LFM2.5-24B-A2B-DSpark')
        self.assertEqual(sum(x['path'].endswith('.safetensors') for x in d['files']),1)
        self.assertEqual(d['shared_dependencies'],['LiquidAI/LFM2.5-24B-A2B'])
        self.assertLessEqual(d['primary_file_bytes'],656_291_264)
        self.assertTrue(h['open_dependencies'] and d['open_dependencies'])
        self.assertFalse(h['download_authorized'] or d['download_authorized'])
    def test_dedup_is_reproducible_and_not_physical_disk(self):
        old=load(mod.HIST/'selected-file-capacity.json')
        view=load('catalog/effective-portfolio-2026-11-06-v23.json')
        overlay=load('catalog/revisions/v23-2026-11-06.json')
        rows=mod.verify_sources(old,view,overlay,self.src())
        s=mod.compute_summary(old,rows)
        self.assertEqual(s['exact_primary_file_scope_count'],118)
        self.assertEqual(s['unresolved_primary_scope_count'],0)
        self.assertGreater(s['known_scope_content_union_bytes'],old['known_scope_content_union_bytes'])
        self.assertLess(s['known_scope_content_union_bytes'],4_000_000_000_000)
        self.assertIsNone(s['complete_offline_archive_bytes'])
        self.assertIsNone(s['physical_disk_free_bytes'])
        self.assertFalse(s['download_authorized'])
        self.assertEqual(s['new_assets_publisher_all_repo_bytes_sum'],66_707_531_084)
    def test_snapshot_substitution_and_missing_index_fail_closed(self):
        old=load(mod.HIST/'selected-file-capacity.json')
        view=load('catalog/effective-portfolio-2026-11-06-v23.json')
        overlay=load('catalog/revisions/v23-2026-11-06.json')
        sources=self.src()
        sources['Hcompany/Holotron4-30B-A3B']['pinned_revision']='f'*40
        with self.assertRaises(AssertionError):
            mod.verify_sources(old,view,overlay,sources)
        sources=self.src()
        sources['Hcompany/Holotron4-30B-A3B']['files']=[
          f for f in sources['Hcompany/Holotron4-30B-A3B']['files']
          if f['path']!='model.safetensors.index.json']
        with self.assertRaises(AssertionError):
            mod.verify_sources(old,view,overlay,sources)

if __name__=='__main__':unittest.main()
