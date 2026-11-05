"""Offline checks for R20 research evidence; no network or model execution."""
import json
from collections import Counter
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / 'catalog/research/2026-11-05-round20-decisions.json'
DRAFT = ROOT / 'manifests/drafts/round20-llm-gui-evidence.candidate.json'

class ResearchRound20Tests(unittest.TestCase):
    def read_ledger(self):
        self.assertTrue(LEDGER.is_file(), 'R20 research ledger is missing')
        return json.loads(LEDGER.read_text(encoding='utf-8'))

    def test_ledger_exists(self):
        self.read_ledger()

    def test_scoped_decisions_unique_and_non_executable(self):
        data = self.read_ledger()
        rows = data['decisions']
        self.assertEqual(len(rows), 6)
        self.assertEqual(len({r['repo_id'].casefold() for r in rows}), 6)
        self.assertEqual(Counter(r['decision'] for r in rows), {'CONDITIONAL':3,'HOLD':2,'REJECT':1})
        self.assertEqual(data['scope'], ['llm_posttraining','gui_grounding_and_agents'])
        self.assertFalse(data['effective_catalog_changed'])
        for row in rows:
            self.assertFalse(row['download_authorized'])
            self.assertFalse(row['local_runtime_verified'])
            self.assertIsNone(row['regulation_probability'])
            self.assertIsNone(row['complete_selected_pipeline_bytes'])

    def test_positive_negative_and_reversal_conditions(self):
        for row in self.read_ledger()['decisions']:
            for key in ('positive_evidence','negative_evidence','incumbent_comparison','next_validation','reversal_condition'):
                self.assertTrue(row[key], (row['repo_id'], key))
            self.assertTrue(row['source_urls'])
            self.assertTrue(all(u.startswith('https://') for u in row['source_urls']))
            self.assertIn('hardware', row['measurement_conditions'])
            self.assertIn('clock', row['measurement_conditions'])
            self.assertIn('batch', row['measurement_conditions'])

    def test_selective_refusal_axes_and_precision_are_separate(self):
        row = self.read_ledger()['decisions'][0]
        self.assertEqual(row['repo_id'], 'InterpreticAI/Qwen3.8-27B-Uncensored-v2')
        m = row['measurements']
        self.assertEqual(m['political_censored_bf16'], {'base':98,'candidate':4,'n':113})
        self.assertEqual(m['harmful_refusals_bf16'], {'base':100,'candidate':95,'n':100})
        self.assertFalse(m['harmful_refusals_measured_on_q4'])
        self.assertEqual(m['mmlu_matched_n'], 200)
        self.assertEqual(row['mechanism_confirmation'], 'targeted_behavior_confirmed_method_undisclosed')

    def test_no_false_venus_parameter_pass(self):
        row = next(r for r in self.read_ledger()['decisions'] if r['repo_id']=='inclusionAI/UI-Venus-2-9B')
        e = row['parameter_evidence']
        self.assertIsNone(e['verified_total'])
        self.assertEqual(e['rejected_index_total_parameters'], 1469680)
        self.assertEqual(e['embedding_lower_bound'], 248320 * 4096)
        self.assertGreater(e['embedding_lower_bound'], e['rejected_index_total_parameters'])
        self.assertEqual(e['index_tensor_payload_bytes'], 18819627488)
        self.assertEqual(row['measurements']['osworld2_binary_percent'], 0.0)
        self.assertEqual(row['measurements']['osworld2_tasks'], 108)
        self.assertEqual(row['measurements']['osworld2_max_steps'], 150)

    def test_grounding_not_end_to_end_and_missing_release_not_available(self):
        rows = self.read_ledger()['decisions']
        g = next(r for r in rows if r['repo_id']=='PrentisAI/GroundGUI-8B')
        self.assertEqual(g['task_scope'], 'single_screen_point_localization_not_complete_agent')
        self.assertEqual(g['measurements']['screenspot_pro'], {'success':1011,'n':1581,'percent':63.9})
        p = next(r for r in rows if r['repo_id']=='inclusionAI/UI-Venus-2-27B')
        self.assertFalse(p['public_weight_repository_verified'])
        self.assertIsNone(p['published_update_date'])
        self.assertIsNone(p['complete_selected_pipeline_bytes'])

    def test_davidau_matched_subset_and_counterexample(self):
        rows = self.read_ledger()['decisions']
        d = next(r for r in rows if r['repo_id'].startswith('DavidAU/'))
        self.assertEqual(d['measurements']['mmlu_common_format_n'], 430)
        self.assertEqual(d['measurements']['mmlu_common_format_delta_pp'], 8.8)
        self.assertFalse(d['measurements']['contamination_tested'])
        self.assertFalse(d['measurements']['multiplicity_adjusted'])
        self.assertEqual(d['measurement_conditions']['quantization'], 'Q6_K for tasks; BF16 for distribution distance')
        o = next(r for r in rows if r['repo_id'].startswith('OBLITERATUS/'))
        self.assertEqual(o['decision'], 'REJECT')
        self.assertEqual(o['measurements']['mmlu_pro_delta_pp'], -4.6)

    def test_file_evidence_is_metadata_not_download_verification(self):
        self.assertTrue(DRAFT.is_file())
        data = json.loads(DRAFT.read_text(encoding='utf-8'))
        self.assertFalse(data['executable'])
        self.assertFalse(data['download_authorized'])
        self.assertEqual(sum(r['source_reported_bytes'] for r in data['artifacts'][:2]), 17738321536)
        for row in data['artifacts']:
            self.assertEqual(len(row['source_reported_sha256']), 64)
            int(row['source_reported_sha256'], 16)
            self.assertFalse(row['local_hash_verified'])
            self.assertIsNone(row['pinned_full_revision'])

    def test_current_repository_all_asset_states_and_protected_choices(self):
        current_path = ROOT / 'catalog/CURRENT.json'
        if not current_path.is_file():
            self.skipTest('full connected repository not mounted locally; this check must run in GitHub CI')
        current = json.loads(current_path.read_text(encoding='utf-8'))
        portfolio = json.loads((ROOT/current['materialized_catalog_path']).read_text(encoding='utf-8'))
        items = portfolio['items']
        keyed = {(r['asset_kind'],r['repo_id']):r for r in items}
        self.assertEqual(len(items), len(keyed))
        self.assertEqual(len(items), current['expected']['tracked'])
        counts = Counter(r['portfolio_decision'] for r in items)
        self.assertEqual(dict(counts), current['expected']['by_decision'])
        self.assertEqual(keyed[('model','Nanbeige/Nanbeige4.3-33B')]['portfolio_decision'], 'select')
        excluded = {r['repo_id'] for r in items if r['portfolio_decision']=='excluded'}
        self.assertEqual(excluded, {
            'state-spaces/mamba-2.8b','Wigtn/Qwen3-VL-2B-WigtnOCR','Wigtn/KoGovDoc-Bench',
            'qvac/TranscribePsy-250M-EU','nvidia/nemotron-labs-unified-asr-0.6b',
            'PerceptronAI/Isaac-0.2-2B-Preview'})
        proposed = json.loads((ROOT/current['priority_worklist_path']).read_text(encoding='utf-8'))
        active = {k for k,r in keyed.items() if r['portfolio_decision'] in ('select','conditional')}
        self.assertEqual(active, {(r['asset_kind'],r['repo_id']) for r in proposed['candidates']})
        self.assertFalse(proposed['download_enabled'])
        for r in self.read_ledger()['decisions']:
            self.assertNotIn(('model',r['repo_id']), keyed, 'R20 decisions are not materialized catalog entries')
        print('R20 full inventory:', len(items), dict(counts), 'active=',len(active))

if __name__ == '__main__':
    unittest.main()
