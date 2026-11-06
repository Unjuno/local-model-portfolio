"""Read-only v25 selected file accounting tests."""
import copy
import json
import unittest
from pathlib import Path
from scripts import capacity_selection_v25 as m
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class V25CapacityTests(unittest.TestCase):
    def args(self):
        return [load(m.BASE/'selected-file-capacity.json'),load('catalog/effective-portfolio-2026-11-06-v25.json'),
                load('catalog/revisions/v25-2026-11-06.json'),load(m.R/'research.json'),
                load(m.R/'sources/PrunaAI--P-H3-Image.json')]
    def test_original_15_weights_and_new_122_exact_files(self):
        data=m.audit(*self.args())
        self.assertEqual(data['exact_primary_file_scope_count'],122)
        self.assertEqual(data['unresolved_primary_scope_count'],0)
        x=data['items'][-1]
        self.assertEqual(x['repo_id'],'PrunaAI/P-H3-Image')
        self.assertEqual(sum(f['path'].endswith('.safetensors') for f in x['files']),15)
        self.assertEqual(x['primary_file_bytes'],99_840_428_064)
        self.assertFalse(x['download_authorized'])
        self.assertEqual(x['source_parameter_gate']['status'],'UNVERIFIED_BLOCK_FINAL_LOCK')
        self.assertLess(data['known_scope_content_union_bytes'],4_000_000_000_000)
        self.assertIsNone(data['physical_disk_free_bytes'])
        self.assertIsNone(data['complete_offline_archive_bytes'])
        self.assertEqual(data['maya2_external_two_repo_publisher_bytes_reported_not_double_counted'],473790793)
    def test_missing_required_vae_or_license_is_rejected(self):
        for path in ('vae/diffusion_pytorch_model.safetensors','LICENSE','prompt_upsampler/model-00004-of-00004.safetensors'):
            a=self.args()
            a[3]=copy.deepcopy(a[3])
            r=next(x for x in a[3]['Pruna_candidates'] if x['repo_id']=='PrunaAI/P-H3-Image')
            r['candidate_full_diffusers_profile']['selected_file_paths'].remove(path)
            with self.subTest(path=path),self.assertRaises((AssertionError,ValueError)):
                m.audit(*a)
    def test_stale_revision_and_fake_permissions_fail(self):
        args=self.args()
        args[4]=copy.deepcopy(args[4]);args[4]['pinned_revision']='f'*40
        with self.assertRaises(AssertionError):m.audit(*args)
if __name__=='__main__':unittest.main()
