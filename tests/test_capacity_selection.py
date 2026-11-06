import importlib.util
from pathlib import Path
import unittest
P=Path(__file__).resolve().parents[1]/'scripts/capacity_selection.py'
class CapacitySelectionTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(P.exists(), 'capacity selector missing')
        spec=importlib.util.spec_from_file_location('capacity_selection',P)
        self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
    def f(self,path,size=10):
        return {'path':path,'bytes':size,'sha256':None,'git_blob_sha1':None,'identity_kind':'unverified'}
    def test_single_variant_and_required_metadata(self):
        rows=[self.f(x) for x in ['chosen.gguf','other.gguf','README.md','chat_template.jinja','demo.png']]
        selected,_=self.m.choose_files(rows,{'weights':['chosen.gguf']})
        self.assertEqual({x['path'] for x in selected},{'chosen.gguf','README.md','chat_template.jinja'})
    def test_missing_requested_weight_fails(self):
        with self.assertRaises(ValueError):self.m.choose_files([self.f('other.gguf')],{'weights':['missing.gguf']})
    def test_standard_keeps_audio_codec_and_no_other_format(self):
        rows=[self.f(x) for x in ['model.safetensors','codec.pth','audio_tokenizer/model.safetensors','config.json','pytorch_model.bin','onnx/model.onnx','original/model.pth']]
        selected,_=self.m.choose_files(rows,{})
        self.assertEqual({x['path'] for x in selected},{'model.safetensors','codec.pth','audio_tokenizer/model.safetensors','config.json'})
    def test_granary_all_label_manifests_and_split_license(self):
        profile=self.m.PROFILES['nvidia/Granary-v2']
        rows=[self.f(x) for x in profile['support_paths']+profile['mandatory_labels']+
              ['ja/fleurs/ja_asr.jsonl.gz','en/librilight/en_asr.part00.jsonl.gz',
               'figures/granary-v2-icon.png','example_audio.wav']]
        selected,excluded=self.m.choose_files(rows,profile)
        self.assertEqual(len(selected),8)
        self.assertEqual(len(excluded),2)
        self.assertEqual(profile['license_scope']['en/people_speech/en_asr.jsonl.gz'],'CC-BY-SA-4.0')
        self.assertTrue(profile['labels_only_no_audio'])
        self.assertFalse(any(f['path'].endswith('.wav') for f in selected))
    def test_granary_missing_notice_or_exception_fails_closed(self):
        profile=self.m.PROFILES['nvidia/Granary-v2']
        rows=[self.f(x) for x in profile['support_paths']+profile['mandatory_labels']+
              ['ja/fleurs/ja_asr.jsonl.gz']]
        for index in (0,3,5):
            with self.subTest(index=index),self.assertRaises(ValueError):
                self.m.choose_files([row for j,row in enumerate(rows) if j!=index],profile)
    def test_granary_unrecognized_label_path_fails_closed(self):
        profile=self.m.PROFILES['nvidia/Granary-v2']
        rows=[self.f(x) for x in profile['support_paths']+profile['mandatory_labels']+
              ['en/unknown/sneak_asr.jsonl.gz','../problem.jsonl.gz']]
        with self.assertRaises(ValueError):self.m.choose_files(rows,profile)
    def test_dataset_subset_not_entire_repo(self):
        rows=[self.f(x) for x in ['math/math_proof.jsonl','swe/swe_agentic.jsonl','chat/all.jsonl','README.md']]
        selected,_=self.m.choose_files(rows,{'dataset_paths':['math/math_proof.jsonl','swe/swe_agentic.jsonl']})
        self.assertEqual(len(selected),3)
    def test_missing_shard_fails(self):
        with self.assertRaises(ValueError):self.m.check_shards([self.f('model-00001-of-00002.safetensors')])
    def test_all_shards_succeed(self):
        self.m.check_shards([self.f('model-00001-of-00002.safetensors'),self.f('model-00002-of-00002.safetensors')])
    def test_equal_size_is_not_content_identity(self):
        self.assertEqual(self.m.union_bytes([('a',self.f('x',100)),('b',self.f('y',100))]),200)
    def test_unknown_sum_remains_unknown(self):
        self.assertIsNone(self.m.sum_bytes([self.f('x',None)]))
    def test_sha256_dedup_and_conflict(self):
        f=self.f('x',100);f['sha256']='a'*64
        self.assertEqual(self.m.union_bytes([('a',f),('b',f)]),100)
        with self.assertRaises(ValueError):self.m.union_bytes([('a',f),('b',dict(f,bytes=101))])
    def test_masked_pointer_cannot_dedup(self):
        f=self.f('x',100);f['git_blob_sha1']='b'*40;f['identity_kind']='unverifiable_payload_hash'
        self.assertEqual(self.m.union_bytes([('a',f),('b',f)]),200)
    def test_diffusers_omits_native_pack_not_components(self):
        files=[self.f(x) for x in ['model.safetensors','ae.safetensors','text_encoder/model.safetensors','transformer/diffusion_pytorch_model.safetensors','vae/diffusion_pytorch_model.safetensors','model_index.json']]
        selected,_=self.m.choose_files(files,{'diffusers':True})
        self.assertEqual(len(selected),4)
    def test_unknown_additional_dependencies_prevent_final_total(self):
        self.assertIsNone(self.m.complete_total([{'package_bytes':100,'open_dependencies':['codec']},{'package_bytes':200,'open_dependencies':[]}]))
        self.assertEqual(self.m.complete_total([{'package_bytes':100,'open_dependencies':[]}]),100)
if __name__=='__main__':unittest.main()
