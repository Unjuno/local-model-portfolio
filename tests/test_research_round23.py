"""Read-only R23 evidence checks. No network, model import or payload access."""
import json
import unittest
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

class MotionAvatarResearchTests(unittest.TestCase):
    def setUp(self):
        self.ledger = json.loads((ROOT / 'catalog/research/2026-11-05-round23-motion-avatar-decisions.json').read_text())
        self.plan = json.loads((ROOT / 'manifests/drafts/round23-motion-avatar.candidate.json').read_text())
        self.rows = {r['key']: r for r in self.ledger['candidates']}

    def test_six_unique_research_only_decisions(self):
        self.assertEqual(6, len(self.rows))
        self.assertEqual({'CONDITIONAL': 2, 'HOLD': 4}, dict(Counter(r['decision'] for r in self.rows.values())))
        for field in ('formal_catalog_changed', 'approved_queue_changed', 'user_disk_changed', 'model_executed'):
            self.assertIs(self.ledger[field], False)
        self.assertIs(self.plan['executable'], False)
        self.assertIs(self.plan['download_authorized'], False)

    def test_negative_evidence_and_reversal_are_required(self):
        for row in self.rows.values():
            for field in ('positive_evidence', 'negative_evidence', 'uniqueness_vs_portfolio', 'reversal_condition', 'next_check', 'license_assessment'):
                self.assertTrue(row[field])
            self.assertTrue(row['source_url'].startswith('https://'))
            self.assertIs(row['independent_reproduction_verified'], False)
            self.assertIsNone(row['regulatory_probability'])
            self.assertIsNone(row['local_peak_ram_bytes'])

    def test_wan_base_is_not_realtime_lite(self):
        row = self.rows['wan-animate2']
        self.assertEqual('BASE_DIFFUSERS', row['selected_variant'])
        self.assertEqual(22833447731, row['serialized_float_scalars'])
        self.assertEqual(16394878784, row['main_transformer_scalars'])
        self.assertEqual('Lite', row['speed_claim']['variant'])
        self.assertEqual(4, row['speed_claim']['gpu_count'])
        self.assertEqual('H100', row['speed_claim']['gpu'])
        self.assertIs(row['lite_checkpoint_verified'], False)
        self.assertIsNone(row['selected_variant_fps_measured'])

    def test_longcat_incomplete_total_never_becomes_pass(self):
        row = self.rows['longcat-avatar15']
        self.assertEqual(23834929027, row['partial_float_scalars'])
        self.assertIsNone(row['total_learned_parameters'])
        self.assertIn('vocal_separator/Kim_Vocal_2.onnx', row['uncounted_components'])
        self.assertEqual('SOURCE_BF16_CENSUS_NOT_PACKED_INT8_COUNT', row['parameter_count_scope'])
        self.assertEqual('INT8_PLUS_DMD', row['selected_variant'])

    def test_author_study_not_independent_quantized_parity(self):
        row = self.rows['longcat-avatar15']
        self.assertEqual(508, row['evaluation']['image_audio_pairs'])
        self.assertEqual(770, row['evaluation']['raters'])
        self.assertEqual(13240, row['evaluation']['judgments'])
        self.assertIs(row['evaluation']['independent'], False)
        self.assertIs(row['int8_quality_parity_verified'], False)
        self.assertIn('lip synchronization', row['negative_evidence'])

    def test_weight_sizes_hashes_and_revisions(self):
        identities = set()
        for package in self.plan['packages']:
            for f in package['weight_files']:
                identity = (f['repo_id'], f['revision'], f['path'])
                self.assertNotIn(identity, identities)
                identities.add(identity)
                self.assertRegex(f['revision'], r'^[0-9a-f]{40}$')
                self.assertRegex(f['source_sha256'], r'^[0-9a-f]{64}$')
                self.assertIs(type(f['bytes']), int)
                self.assertGreater(f['bytes'], 0)
                self.assertIs(f['local_full_hash_verified'], False)
            self.assertEqual(sum(f['bytes'] for f in package['weight_files']), package['selected_weight_bytes'])
            self.assertIsNone(package['complete_offline_pipeline_bytes'])
            self.assertIsNone(package['actual_incremental_disk_bytes'])
        self.assertEqual(22, len(identities))

    def test_longcat_includes_dependencies_without_duplicate_base(self):
        package = next(p for p in self.plan['packages'] if p['key'] == 'longcat-avatar15')
        paths = {f['path'] for f in package['weight_files']}
        self.assertIn('lora/dmd_lora.safetensors', paths)
        self.assertIn('whisper-large-v3/model.safetensors', paths)
        self.assertIn('vocal_separator/Kim_Vocal_2.onnx', paths)
        self.assertFalse(any(p.startswith(('dit/', 'base_model/')) for p in paths))
        self.assertFalse(any(p.endswith(('.bin', '.msgpack')) or 'fp32-' in p or 'turbo' in p.lower() for p in paths))

    def test_shared_vae_savings_are_conditional(self):
        a, b = self.plan['packages']
        ah = {f['source_sha256']: f['bytes'] for f in a['weight_files']}
        bh = {f['source_sha256']: f['bytes'] for f in b['weight_files']}
        common = set(ah) & set(bh)
        self.assertEqual({'d6e524b3fffede1787a74e81b30976dce5400c4439ba64222168e607ed19e793'}, common)
        self.assertEqual(sum(ah[h] for h in common), self.plan['potential_shared_weight_bytes'])
        self.assertEqual(507591892, self.plan['potential_shared_weight_bytes'])
        self.assertIsNone(self.plan['verified_user_disk_savings_bytes'])

    def test_tensor_count_is_not_model_runtime_or_weight_validation(self):
        audit = self.plan['header_audit']
        self.assertEqual(23, audit['files_inspected'])
        self.assertEqual(833936, audit['metadata_bytes_read'])
        self.assertEqual(0, audit['tensor_value_bytes_read'])
        self.assertEqual(22833447731, sum(audit['wan_components'].values()))
        self.assertEqual(23834929027, sum(audit['longcat_known_components'].values()))
        self.assertIs(audit['full_weight_sha256_verified'], False)
        self.assertIs(audit['local_runtime_tested'], False)

    def test_recency_and_access_are_not_fabricated(self):
        self.assertEqual('2026-08-07', self.rows['wan-animate2']['public_release_date'])
        self.assertFalse(self.rows['longcat-avatar15']['within_90_day_weight_window'])
        self.assertTrue(self.rows['longcat-avatar15']['older_unique_exception_reason'])
        self.assertEqual('auto_gated', self.rows['avtr1']['observed_access'])
        self.assertIs(self.rows['avtr1']['personal_access_accepted'], False)
        self.assertEqual('KlingTeam/LivePortrait', self.ledger['retain_existing'][0])
        self.assertIn('Nanbeige/Nanbeige4.3-33B', self.ledger['retain_existing'])

if __name__ == '__main__':
    unittest.main()
