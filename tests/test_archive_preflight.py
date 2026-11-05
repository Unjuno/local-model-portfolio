"""R25: local archive preflight must never authorize download or infer reuse from size alone."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from scripts.archive_preflight import audit_source_manifest, inspect_archive

ROOT = Path(__file__).resolve().parents[1]

def fixture(root):
    base=root/'models'/'qwen';base.mkdir(parents=True)
    (base/'w.bin').write_bytes(b'correct-base')
    adapter=root/'models'/'adapter';adapter.mkdir(parents=True)
    (adapter/'adapter.bin').write_bytes(b'lora weights')
    def entry(name,value):
        return dict(path=name,bytes=len(value),source_sha256=hashlib.sha256(value).hexdigest(),
                    git_blob_sha1=hashlib.sha1(b'version https://git-lfs.github.com/spec/v1\n').hexdigest(),
                    role='weight',local_hash_verified=False,body_downloaded=False)
    p=dict(status='EVIDENCE_ONLY_NOT_A_LOCK',executable=False,approved_manifest=False,
           download_authorized=False,auto_execute=False,auto_seed=False,
           repositories=[
               dict(key='qwen-image-base',repo_id='Qwen/Qwen-Image-2.1',revision='a'*40,
                    selected_bytes=len(b'correct-base'),file_count=1,files=[entry('w.bin',b'correct-base')]),
               dict(key='chatr-adapter',repo_id='chatr/model',revision='b'*40,
                    selected_bytes=len(b'lora weights'),file_count=1,files=[entry('adapter.bin',b'lora weights')])
           ],
           packages=[dict(key='chatr-image',repository_keys=['qwen-image-base','chatr-adapter'],
                          selected_model_and_support_bytes=len(b'correct-base')+len(b'lora weights'))])
    return p,base,adapter

class ArchivePreflightTests(unittest.TestCase):
    def test_actual_r21_plan_exact_and_nonexecutable(self):
        d=json.loads((ROOT/'manifests/drafts/round21-pinned-preservation.candidate.json').read_text())
        self.assertEqual([],audit_source_manifest(d))
        self.assertEqual(sum(len(x['files']) for x in d['repositories']),47)
        self.assertEqual(sum(x['selected_bytes'] for x in d['repositories']),51_541_147_139)
    def test_unknown_evidence_must_not_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p,_,_=fixture(root)
            x=inspect_archive(p,root,{},hash_existing=False,staging_reserve_bytes=None,
                              existing_archive_bytes=None,archive_target_bytes=3_800_000_000_000,free_floor_bytes=200_000_000_000)
            self.assertEqual(x['capacity']['physical_gate'],'UNCERTAIN')
            self.assertEqual(x['capacity']['archive_budget_gate'],'UNCERTAIN')
            self.assertEqual(x['capacity']['confirmed_reused_bytes'],0)
            self.assertFalse(x['download_authorized'])
            self.assertEqual(x['source_roots']['qwen-image-base']['status'],'UNMAPPED')
    def test_verified_existing_base_reuses_only_verified_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p,base,_=fixture(root)
            x=inspect_archive(p,root,{'qwen-image-base':base},hash_existing=True,
                              staging_reserve_bytes=0,existing_archive_bytes=0,free_floor_bytes=0)
            self.assertEqual(x['source_roots']['qwen-image-base']['status'],'FULLY_MATCHED')
            self.assertTrue(x['source_roots']['qwen-image-base']['inside_archive'])
            self.assertEqual(x['capacity']['confirmed_reused_bytes'],len(b'correct-base'))
            self.assertEqual(x['capacity']['new_payload_bytes_after_verified_reuse'],len(b'lora weights'))
            self.assertEqual(x['capacity']['physical_gate'],'PASS')
            self.assertFalse(x['download_authorized'])
    def test_size_only_is_not_reuse(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p,base,_=fixture(root)
            x=inspect_archive(p,root,{'qwen-image-base':base},hash_existing=False,
                              staging_reserve_bytes=0,existing_archive_bytes=0,free_floor_bytes=0)
            self.assertEqual(x['source_roots']['qwen-image-base']['status'],'SIZE_ONLY_UNVERIFIED')
            self.assertEqual(x['capacity']['confirmed_reused_bytes'],0)
    def test_hash_mismatch_is_not_reuse(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p,base,_=fixture(root)
            (base/'w.bin').write_bytes(b'incorrect!!!')
            x=inspect_archive(p,root,{'qwen-image-base':base},hash_existing=True,
                              staging_reserve_bytes=0,existing_archive_bytes=0,free_floor_bytes=0)
            self.assertEqual(x['source_roots']['qwen-image-base']['status'],'MISMATCH')
            self.assertEqual(x['capacity']['confirmed_reused_bytes'],0)
    def test_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp,tempfile.TemporaryDirectory() as other:
            root=Path(tmp);p,base,_=fixture(root)
            (Path(other)/'secret').write_bytes(b'correct-base')
            (base/'w.bin').unlink()
            try:os.symlink(str(Path(other)/'secret'),str(base/'w.bin'))
            except (OSError,NotImplementedError):self.skipTest('symlinks unavailable')
            x=inspect_archive(p,root,{'qwen-image-base':base},hash_existing=True,
                              staging_reserve_bytes=0,existing_archive_bytes=0,free_floor_bytes=0)
            self.assertEqual(x['source_roots']['qwen-image-base']['status'],'UNSAFE_PATH')
            self.assertEqual(x['capacity']['confirmed_reused_bytes'],0)
    def test_excess_staging_reserve_must_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p,_,_=fixture(root)
            x=inspect_archive(p,root,{},hash_existing=True,staging_reserve_bytes=10**18,
                              existing_archive_bytes=0,free_floor_bytes=0)
            self.assertEqual(x['capacity']['physical_gate'],'FAIL')
    def test_invalid_manifest_never_scanned(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p,_,_=fixture(root)
            p['download_authorized']=True
            self.assertTrue(audit_source_manifest(p))
            p['download_authorized']=False
            p['repositories'][0]['files'][0]['path']='../escape'
            self.assertTrue(audit_source_manifest(p))
    def test_another_directory_not_archive_reuse(self):
        with tempfile.TemporaryDirectory() as tmp,tempfile.TemporaryDirectory() as other:
            root=Path(tmp);p,_,_=fixture(root)
            elsewhere=Path(other);(elsewhere/'w.bin').write_bytes(b'correct-base')
            x=inspect_archive(p,root,{'qwen-image-base':elsewhere},hash_existing=True,
                              staging_reserve_bytes=0,existing_archive_bytes=0,free_floor_bytes=0)
            self.assertEqual(x['source_roots']['qwen-image-base']['status'],'FULLY_MATCHED')
            self.assertFalse(x['source_roots']['qwen-image-base']['inside_archive'])
            self.assertEqual(x['capacity']['confirmed_reused_bytes'],0)
    def test_unknown_archive_budget_blocks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p,_,_=fixture(root)
            x=inspect_archive(p,root,{},hash_existing=False,
                              staging_reserve_bytes=0,existing_archive_bytes=None,free_floor_bytes=0)
            self.assertEqual(x['capacity']['archive_budget_gate'],'UNCERTAIN')
if __name__=='__main__':unittest.main()
