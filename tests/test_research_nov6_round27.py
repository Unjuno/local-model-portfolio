"""R27 pure consistency tests. No network, weights or owner disk."""
import unittest
from scripts import research_nov6_round27 as m

class R27Tests(unittest.TestCase):
    def test_bounded_six_disciplined_evidence_scopes(self):
        self.assertEqual(len(m.CANDIDATES),5)
        self.assertEqual(len(set(m.CANDIDATES)),5)
        self.assertIn('baidu/ERNIE-5.5-Flash-Base',m.CANDIDATES)
        self.assertIn('gradium/phonon-voices',m.CANDIDATES)
        self.assertEqual(len(m.TOK_FIXED),40)
    def test_source_has_explicit_rights_and_unapproved_flags(self):
        r=m.report('gradium/phonon-40m-multilingual',{'tree_complete':False,'gated':'auto',
                            'source_scope_bytes':None,'files':[],'parameter_metadata':{},'license_metadata':'cc-by-nc-4.0'})
        self.assertIn('GATED',r['decision'])
        self.assertFalse(r['download_authorized'])
        self.assertFalse(r['personal_access_verified'])
        self.assertIsNone(r['measured_peak_runtime_memory'])
    def test_oversized_does_not_sneak_in_due_active_expert_count(self):
        r=m.report('baidu/ERNIE-5.5-Flash-Base',{'tree_complete':False,'gated':False,'files':[],
            'parameter_metadata':{'total':286_245_700_000}})
        self.assertIn('OVERSIZED',r['decision'])
        self.assertIn('>=150B',r['size_rule'])
        self.assertFalse(r['legal_clearance'])
    def test_sha_pinned_tokenizer_and_no_qwen_full_weights(self):
        r=m.report('Qwen/Qwen2.5-1.5B',{'tree_complete':False,'files':[],'source_scope_bytes':None})
        self.assertEqual(r['required_commit'],m.TOK_FIXED)
        self.assertIn('NOT',r['independent_learned_outcome'])
        self.assertNotIn('pytorch_model.bin',r['subset_paths'])
if __name__=='__main__':unittest.main()
