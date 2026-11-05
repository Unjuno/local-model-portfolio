"""Read-only R21 package checks; no network, loading, or acquisition."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'manifests/drafts/round21-pinned-preservation.candidate.json'
REGISTRY = ROOT / 'catalog/preparation/2026-11-05-priority-packages.json'

class PreparationRound21Tests(unittest.TestCase):
    def read(self):
        self.assertTrue(MANIFEST.is_file(), 'R21 pinned package manifest missing')
        return json.loads(MANIFEST.read_text(encoding='utf-8'))

    def test_no_payload_authorization(self):
        d = self.read()
        for key in ('executable', 'approved_manifest', 'download_authorized', 'auto_execute', 'auto_seed'):
            self.assertIs(d[key], False)
        self.assertEqual(len(d['packages']), 2)

    def test_all_repository_files_pinned_and_unique(self):
        d = self.read()
        keys = []
        for repo in d['repositories']:
            self.assertRegex(repo['revision'], r'^[0-9a-f]{40}$')
            for f in repo['files']:
                keys.append((repo['repo_id'], repo['revision'], f['path']))
                self.assertGreater(f['bytes'], 0)
                self.assertRegex(f['git_blob_sha1'], r'^[0-9a-f]{40}$')
                self.assertIn('/' + repo['revision'] + '/', repo['resolve_url_prefix'])
                self.assertFalse(f['path'].startswith('/'))
                self.assertNotIn('..', Path(f['path']).parts)
                self.assertNotIn('/main/', repo['resolve_url_prefix'])
                self.assertFalse(f['local_hash_verified'])
        self.assertEqual(len(keys), len(set(keys)))

    def test_weights_have_source_sha_not_blob_substitution(self):
        d = self.read()
        weights = [f for r in d['repositories'] for f in r['files'] if f['role'] == 'weight']
        self.assertEqual(len(weights), 10)
        for f in weights:
            self.assertRegex(f['source_sha256'], r'^[0-9a-f]{64}$')
            self.assertNotEqual(f['source_sha256'], f['git_blob_sha1'])
            self.assertFalse(f['body_downloaded'])

    def test_repository_and_package_arithmetic(self):
        d = self.read()
        by_id = {r['key']: r for r in d['repositories']}
        for r in by_id.values():
            self.assertEqual(r['selected_bytes'], sum(f['bytes'] for f in r['files']))
            self.assertEqual(r['file_count'], len(r['files']))
        for p in d['packages']:
            self.assertEqual(p['selected_model_and_support_bytes'], sum(by_id[k]['selected_bytes'] for k in p['repository_keys']))
            self.assertIsNone(p['complete_offline_environment_bytes'])
            self.assertIsNone(p['measured_user_peak_ram_bytes'])

    def test_image_base_components_are_not_adapter_size(self):
        d = self.read()
        by_id = {r['key']: r for r in d['repositories']}
        p = next(p for p in d['packages'] if p['key'] == 'chatr-image')
        b = by_id['qwen-image-base']
        paths = {f['path'] for f in b['files']}
        for path in ('model_index.json', 'scheduler/scheduler_config.json', 'processor/tokenizer.json', 'text_encoder/model.safetensors.index.json', 'transformer/diffusion_pytorch_model.safetensors.index.json', 'vae/diffusion_pytorch_model.safetensors'):
            self.assertIn(path, paths)
        self.assertGreater(p['selected_model_and_support_bytes'], 33_000_000_000)
        self.assertIsNone(p['actual_incremental_bytes'])
        self.assertEqual(p['incremental_if_exact_base_verified_bytes'], by_id['chatr-adapter']['selected_bytes'])
        self.assertIsNone(p['complete_logical_parameter_total'])

    def test_exact_weight_identities_match_observed_sources(self):
        d = self.read()
        files = {f['path']: f for r in d['repositories'] for f in r['files']}
        f = files['chatrlabs-omni-lora-v0.1-bf16.safetensors']
        self.assertEqual(f['bytes'], 671151136)
        self.assertEqual(f['source_sha256'], '5991a9845bc5251240febf944f653505a00966515b77073f2c639c4dfcba672a')
        f = files['Qwen3.8-27B-Uncensored-v2-Q4_K_M.gguf']
        self.assertEqual(f['bytes'], 16810714592)
        self.assertEqual(f['source_sha256'], '2a76f31d17e879589f2527bb4f657526ce0f4719aa352adc944e13f9f7365972')
        self.assertEqual(files['mmproj-Qwen3.8-27B-Uncensored-v2-F16.gguf']['bytes'], 927606944)

    def test_current_and_historical_recipe_not_conflated(self):
        d = self.read()
        p = next(p for p in d['packages'] if p['key'] == 'chatr-image')
        self.assertEqual(p['runtime_recipe']['current_steps'], 35)
        self.assertEqual(p['runtime_recipe']['current_true_cfg'], 5.0)
        self.assertEqual(p['runtime_recipe']['historical_timing_steps'], 25)
        self.assertFalse(p['runtime_recipe']['current_recipe_speed_measured_here'])
        self.assertEqual(p['runtime_recipe']['negative_prompt'], ' ')
        self.assertEqual(p['runtime_recipe']['diffusers_commit'], '80c7ed262aeffbeb43ef13ae04baeb9b84515a69')

    def test_refusal_axes_and_precision_are_separate(self):
        d = self.read()
        p = next(p for p in d['packages'] if p['key'] == 'interpretic-q4')
        self.assertEqual(p['parameters']['bf16_source_total'], 27781427952)
        self.assertEqual(p['parameters']['gguf_language_only_total'], 27320697856)
        self.assertFalse(p['parameters']['conversion_tensor_equivalence_verified'])
        self.assertEqual(p['quality_scope']['political_eval_precision'], 'Q4_K_M')
        self.assertEqual(p['quality_scope']['general_capability_precision'], 'BF16')
        self.assertFalse(p['quality_scope']['q4_general_capability_verified'])

    def test_preparation_is_not_materialization_or_disk_permission(self):
        self.assertTrue(REGISTRY.is_file(), 'R21 preparation registry missing')
        d = json.loads(REGISTRY.read_text(encoding='utf-8'))
        self.assertEqual(d['catalog_state']['revision_id'], 'v17-20261104')
        self.assertEqual(d['catalog_state']['tracked'], 142)
        self.assertEqual(d['catalog_state']['active'], 97)
        for k in ('current_catalog_changed', 'approved_queue_changed', 'user_disk_changed'):
            self.assertFalse(d[k])
        self.assertEqual(d['download_approvals_added'], 0)
        self.assertTrue(all(x['blocking_before_acquisition'] for x in d['priorities']))

    def test_noncommercial_rights_and_specific_remaining_checks(self):
        d = self.read()
        for p in d['packages']:
            self.assertTrue(p['license']['text_read'])
            self.assertTrue(p['license']['noncommercial_research_grant_identified'])
            self.assertFalse(p['license']['user_acceptance_inferred'])
            self.assertFalse(p['payload_access_tested'])
            self.assertFalse(p['runtime_executed'])
            self.assertTrue(p['blocking_before_acquisition'])
            self.assertTrue(p['source_urls'])

if __name__ == '__main__':
    unittest.main()
