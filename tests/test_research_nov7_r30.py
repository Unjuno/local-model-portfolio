"""Ensure no fake capacity/RAM or permission shortcuts for R30 research."""
import copy
import json
import unittest
from pathlib import Path
from scripts import research_nov7_r30 as r
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class R30Tests(unittest.TestCase):
    def test_repo_identity(self):
        self.assertEqual(r.REPOS[0],'kakaocorp/kanana-2-v-decide-3b-2611')
        self.assertEqual(set(r.REPOS[1:]),{'ricursiveAI/Ripple-65B-Base-Preview','ricursiveAI/Ripple-65B-Preview'})
        self.assertEqual(len(set(x.casefold() for x in r.REPOS)),3)
    def test_codec_identities_and_derived_increment(self):
        old=load(r.V26);a=load(r.MOSS_AUDIT);s=load(r.MOSS_SOURCE)
        before=copy.deepcopy((old,s,a))
        x=r.codec_accounting(old,s,a)
        self.assertEqual((old,s,a),before)
        self.assertEqual(x['required_moss_audio_codec_new_selected_primary_bytes'],7_098_711_111)
        self.assertGreaterEqual(x['required_moss_audio_codec_hash_aware_logical_new_bytes'],0)
        self.assertLessEqual(x['required_moss_audio_codec_hash_aware_logical_new_bytes'],7_098_711_111)
        self.assertEqual(x['source_only_expanded_known_hash_aware_bytes'],
                         x['baseline_known_hash_aware_logical_bytes']+x['required_moss_audio_codec_hash_aware_logical_new_bytes'])
        self.assertIsNone(x['complete_offline_archive_bytes'])
        self.assertIsNone(x['disk_real_free_bytes'])
        self.assertFalse(x['model_payload_sha256_measured_locally'])
    def test_wrong_codec_or_empty_file_set_fails_closed(self):
        old=load(r.V26);a=load(r.MOSS_AUDIT);s=load(r.MOSS_SOURCE)
        s['pinned_revision']='f'*40
        with self.assertRaises(ValueError):r.codec_accounting(old,s,a)
        s=load(r.MOSS_SOURCE);a=load(r.MOSS_AUDIT)
        a['codec_source_snapshots'][0]['candidate_files'].pop()
        with self.assertRaises(ValueError):r.codec_accounting(old,s,a)
    def test_sha_helper(self):
        self.assertTrue(r.sha('f'*40))
        self.assertFalse(r.sha('head'))
        self.assertFalse(r.sha('a'*64))
if __name__=='__main__':unittest.main()
