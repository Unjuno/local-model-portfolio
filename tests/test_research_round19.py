"""Read-only validation of the bounded R19 research decision ledger.

No network, model loading, third-party imports or repository writes.
"""
import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / 'catalog/research/2026-11-04-round19-decisions.json'
DRAFT = ROOT / 'manifests/drafts/round19-media-evidence.candidate.json'


class ResearchRound19Tests(unittest.TestCase):
    def load_ledger(self):
        return json.loads(LEDGER.read_text(encoding='utf-8'))

    def test_ledger_exists(self):
        self.assertTrue(LEDGER.is_file(), 'R19 research ledger must exist')

    def test_decisions_unique_and_scoped(self):
        data = self.load_ledger()
        rows = data['candidates']
        self.assertEqual(len(rows), len({r['repo_id'].lower() for r in rows}))
        self.assertEqual(len(rows), 8)
        self.assertEqual({r['modality'] for r in rows}, {'image', 'audio'})
        for row in rows:
            self.assertIn(row['decision'], {'SELECT', 'CONDITIONAL', 'HOLD', 'REJECT'})
            self.assertEqual(row['decision_scope'], 'RESEARCH_ONLY_NOT_EFFECTIVE_CATALOG')
        counts = {s: sum(r['decision'] == s for r in rows) for s in ('SELECT','CONDITIONAL','HOLD','REJECT')}
        self.assertEqual(counts, data['decision_counts'])

    def test_evidence_and_counterarguments_present(self):
        for row in self.load_ledger()['candidates']:
            for field in ('why_add', 'why_not_add', 'next_verification', 'first_restriction_scenario'):
                self.assertTrue(row[field], (row['repo_id'], field))
            self.assertTrue(row['sources'])
            for url in row['sources'] + [row['primary_url']]:
                self.assertEqual(urlparse(url).scheme, 'https')
                self.assertTrue(urlparse(url).hostname)
            self.assertRegex(row['reviewed_on'], r'^\d{4}-\d{2}-\d{2}$')
            self.assertIsNone(row['regulation_probability'])
            self.assertIs(row['user_hardware_tested'], False)

    def test_quantized_parameter_count_is_not_packed_count(self):
        row = next(r for r in self.load_ledger()['candidates'] if r['repo_id'] == 'fishaudio/drama-3-int4')
        self.assertEqual(row['parameters']['logical_main_model_publisher'], 35899600000)
        self.assertEqual(row['parameters']['hub_packed_tensor_scalar_count'], 6857800000)
        self.assertIsNone(row['parameters']['complete_pipeline_verified'])
        self.assertFalse(row['new_capability_separate_from_parent'])
        self.assertEqual(row['runtime']['measured_peak_gpu_gb_author'], 57.9)
        self.assertFalse(row['runtime']['verified_on_24gb_gpu'])
        self.assertFalse(row['runtime']['verified_on_32gb_gpu'])
        self.assertFalse(row['runtime']['verified_on_48gb_gpu'])

    def test_author_measurements_not_independent(self):
        data = self.load_ledger()
        for row in data['candidates']:
            for measure in row.get('benchmarks', []):
                self.assertEqual(measure['origin'], 'publisher_report')
                self.assertIs(measure['independently_reproduced'], False)
                self.assertIn('measurement_scope', measure)
                self.assertIn('hardware', measure)
                self.assertIn('sample_size', measure)

    def test_draft_is_non_executable_and_sizes_are_not_pipeline_sizes(self):
        draft = json.loads(DRAFT.read_text(encoding='utf-8'))
        self.assertEqual(draft['status'], 'EVIDENCE_ONLY_NOT_A_DOWNLOAD_MANIFEST')
        self.assertIs(draft['approved'], False)
        self.assertIs(draft['download_enabled'], False)
        self.assertIsNone(draft['complete_pipeline_bytes'])
        for artifact in draft['artifacts']:
            self.assertGreater(artifact['source_reported_bytes'], 0)
            self.assertRegex(artifact['source_reported_sha256'], r'^[0-9a-f]{64}$')
            self.assertIs(artifact['local_hash_verified'], False)
            self.assertIs(artifact['download_authorized'], False)
            self.assertIsNone(artifact['complete_inference_bytes'])

    def test_source_hashes_and_component_bytes_preserved(self):
        draft = json.loads(DRAFT.read_text(encoding='utf-8'))
        artifacts = {r['repo_id']: r for r in draft['artifacts']}
        self.assertEqual(artifacts['chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1']['source_reported_bytes'], 671151136)
        self.assertEqual(artifacts['ausboss/Qwen-Image-2.1-Consistency-LoRA']['source_reported_bytes'], 159436496)
        self.assertEqual(artifacts['laion/Humaneness-Voice-Converter']['source_reported_bytes'], 1056773004)
        self.assertFalse(artifacts['chatrlabs/Qwen-Image-2.1-Uncensored-Omni-LoRA-v0.1']['release_immutable'])

    def test_research_is_not_formal_selection_or_approval(self):
        data = self.load_ledger()
        self.assertIs(data['effective_catalog_changed'], False)
        self.assertIs(data['acquisition_queue_changed'], False)
        self.assertEqual(data['baseline']['revision_id'], 'v17-20261104')
        self.assertEqual(data['baseline']['tracked'], 142)
        self.assertEqual(data['baseline']['active'], 97)
        self.assertEqual(data['payload_downloads'], 0)
        self.assertFalse(data['torrent_seeding'])
        for row in data['candidates']:
            self.assertFalse(row['download_authorized'])
            self.assertFalse(row['independent_quality_verified_for_exact_artifact'])

    def test_previous_recommendation_downgrade_is_explicit(self):
        row = next(r for r in self.load_ledger()['candidates'] if r['repo_id'] == 'laion/Humaneness-Voice-Converter')
        self.assertEqual(row['previous_recommendation'], 'ADD_CONDITIONAL_RESEARCH')
        self.assertEqual(row['decision'], 'HOLD')
        self.assertIn('speaker', row['why_not_add'].lower())


if __name__ == '__main__':
    unittest.main()
