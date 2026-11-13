"""Regression for v24 primary-file accounting; no payload transfers."""
import copy
import json
import unittest
from pathlib import Path
from scripts import capacity_selection_v24 as m

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class V24CapacityTests(unittest.TestCase):
    def inputs(self):
        old=load(m.BASE/'selected-file-capacity.json')
        view=load('catalog/effective-portfolio-2026-11-06-v24.json')
        overlay=load('catalog/revisions/v24-2026-11-06.json')
        sources={k:load(r['path']) for k,r in m.RULES.items()}
        return old,view,overlay,sources
    def test_publisher_file_scopes_121_and_no_payload(self):
        old,view,overlay,sources=self.inputs()
        x=m.build(old,view,overlay,sources)
        self.assertEqual(len(x['items']),121)
        self.assertEqual(x['exact_primary_file_scope_count'],121)
        self.assertEqual(x['unresolved_primary_scope_count'],0)
        self.assertEqual(x['new_file_scopes_exact'],3)
        self.assertEqual(x['new_source_repos_all_bytes_sum'],97_135_887_841)
        self.assertLess(x['known_scope_content_union_bytes'],4_000_000_000_000)
        self.assertIsNone(x['complete_offline_archive_bytes'])
        self.assertIsNone(x['physical_disk_free_bytes'])
        self.assertFalse(x['download_authorized'])
    def test_teacher_student_and_robot_shards_not_bundled_formats(self):
        x=m.build(*self.inputs()); byid={r['repo_id']:r for r in x['items']}
        a=byid['pfnet/plamo-3-translate-31b']
        self.assertEqual(sum(f['path'].endswith('.safetensors') for f in a['files']),14)
        self.assertEqual(a['primary_file_bytes'],63_518_748_101)
        b=byid['pfnet/plamo-3-translate-0.8b']
        self.assertEqual(sum(f['path'].endswith('.safetensors') for f in b['files']),1)
        c=byid['nvidia/Cosmos3-Nano-Sim-Bimanual']
        self.assertEqual(len(c['files']),91)
        self.assertIn('cosmos3_nano_sim_bimanual_action_sources/action_schema.json',{f['path'] for f in c['files']})
        self.assertEqual(c['primary_file_bytes'],31_830_399_442)
        for row in (a,b,c):
            self.assertFalse(row['download_authorized'])
            self.assertFalse(row['offline_restore_tested'])
            self.assertTrue(row['open_dependencies'])
    def test_revision_license_and_shard_safety_fail_closed(self):
        old,view,overlay,sources=self.inputs()
        sources['pfnet/plamo-3-translate-31b']['pinned_revision']='f'*40
        with self.assertRaises(AssertionError):m.build(old,view,overlay,sources)
        old,view,overlay,sources=self.inputs()
        sources['nvidia/Cosmos3-Nano-Sim-Bimanual']['files']=[f for f in sources['nvidia/Cosmos3-Nano-Sim-Bimanual']['files'] if f['path']!='vae/diffusion_pytorch_model.safetensors']
        with self.assertRaises(AssertionError):m.build(old,view,overlay,sources)
if __name__=='__main__':unittest.main()
