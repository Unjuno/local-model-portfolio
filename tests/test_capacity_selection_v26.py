"""v26 immutable file selection and dependency closure regression tests."""
import copy,json,unittest
from pathlib import Path
from scripts import capacity_selection_v26 as m
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class V26Capacity(unittest.TestCase):
    def args(self):
        return [load(m.HIST/'selected-file-capacity.json'),
          load('catalog/effective-portfolio-2026-11-06-v26.json'),
          load('catalog/revisions/v26-2026-11-06.json'),
          {k:load(v[0]) for k,v in m.SUBS.items()},
          load(m.VOICE[0]),load(m.QWEN[0])]
    def test_all_125_exact_and_no_unknown_count_as_zero(self):
        s=m.build(*self.args())
        self.assertEqual(s['exact_primary_file_scope_count'],125)
        self.assertEqual(s['unresolved_primary_scope_count'],0)
        self.assertEqual(s['new_scopes_exact'],3)
        self.assertGreater(s['new_selected_primary_bytes_sum'],32_000_000_000)
        self.assertLess(s['known_scope_content_union_bytes'],4_000_000_000_000)
        self.assertIsNone(s['complete_offline_archive_bytes'])
        self.assertIsNone(s['physical_disk_free_bytes'])
        self.assertFalse(s['download_authorized'])
    def test_voice_latents_and_tokenizer_minimum(self):
        s=m.build(*self.args())
        self.assertEqual(s['new_shared_voices_source_selected_bytes'],26_183_423)
        self.assertEqual(s['new_vibevoice_qwen_tokenizer_only_bytes'],11_505_079)
        self.assertEqual(s['nvidia_Cosmos_common_vae_bytes'],1_409_400_600)
        self.assertEqual(len(s['dependencies']),len(self.args()[0]['dependencies'])+2)
        new={x['repo_id']:x for x in s['items'][-3:]}
        self.assertEqual(new['gradium/phonon-31m-en']['primary_file_bytes'],103_745_734)
        self.assertEqual(new['gradium/phonon-40m-multilingual']['primary_file_bytes'],122_629_650)
        for x in (new['gradium/phonon-31m-en'],new['gradium/phonon-40m-multilingual']):
            self.assertFalse(x['download_authorized'])
            self.assertFalse(any(f['path'].endswith('.gguf') for f in x['files']))
        self.assertEqual(new['gradium/phonon-40m-multilingual']['gated'],'auto')
        self.assertGreater(new['gradium/phonon-40m-multilingual']['masked_or_unknown_payload_identity_files'],0)
    def test_no_fake_identity_or_missing_voices(self):
        args=self.args()
        args[3]=copy.deepcopy(args[3])
        args[3]['nvidia/Cosmos3-Nano-Sim-Auto']['pinned_revision']='a'*40
        with self.assertRaises(AssertionError):m.build(*args)
        args=self.args()
        args[4]=copy.deepcopy(args[4]);args[4]['files']=[x for x in args[4]['files'] if not x['path'].startswith('voices/')]
        with self.assertRaises(AssertionError):m.build(*args)
        args=self.args()
        args[5]=copy.deepcopy(args[5]);args[5]['pinned_revision']='b'*40
        with self.assertRaises(AssertionError):m.build(*args)
if __name__=='__main__':unittest.main()
