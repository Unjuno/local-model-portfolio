"""Pure unit guards for archive read-only codec and model dependency audit."""
import copy,json,unittest
from pathlib import Path
from scripts import research_dependency_closure_v26 as m
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class RestorationDependencyTests(unittest.TestCase):
    def test_original_codec_and_v2_have_different_role(self):
        self.assertEqual(len(m.CODECS),2)
        self.assertEqual(m.CODECS[0],'OpenMOSS-Team/MOSS-Audio-Tokenizer')
        self.assertEqual(m.CODECS[1],'OpenMOSS-Team/MOSS-Audio-Tokenizer-v2')
        self.assertNotEqual(m.CODECS[0],m.CODECS[1])
    def test_current_model_sources_and_selected_six_components(self):
        r=m.check_parent_models(load(m.MOSS_PARENT),load(m.LTX_PARENT),load(m.VIBE_PARENT))
        self.assertEqual(r['ltx_2_5']['preselected_original_BF16_bytes'],71_118_789_776)
        self.assertEqual(len(r['ltx_2_5']['selected_weight_files']),6)
        self.assertEqual(r['vibevoice']['qwen_tokenizer_nine_source_files_bytes'],11_505_079)
        self.assertFalse(r['vibevoice']['official_microsoft_model_HF_repo_confirmed'])
        self.assertFalse(r['ltx_2_5']['prompt_enhancer']['required_for_minimal_native_distilled_video'])
        self.assertIsNone(r['ltx_2_5']['prompt_enhancer']['bytes'])
        self.assertTrue(all(not x['sha256_visible'] for x in r['ltx_2_5']['selected_weight_files']))
    def test_incomplete_or_stale_parent_pin_fails_closed(self):
        miss=load(m.MOSS_PARENT);ltx=load(m.LTX_PARENT);vibe=load(m.VIBE_PARENT)
        miss['pinned_revision']='f'*40
        with self.assertRaises(AssertionError):m.check_parent_models(miss,ltx,vibe)
        src=load(m.LTX_PARENT);src['files']=[f for f in src['files'] if 'duration-head' not in f['path']]
        with self.assertRaises((AssertionError,ValueError)):m.check_parent_models(load(m.MOSS_PARENT),src,vibe)
    def test_read_only_guard(self):
        self.assertEqual(len(m.CODE_SHA),4)
        self.assertTrue(all(m.sha_ok(x) for x in m.CODE_SHA.values()))
        self.assertFalse(m.sha_ok('main'))
if __name__=='__main__':unittest.main()
