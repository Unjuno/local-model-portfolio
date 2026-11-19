import importlib.util
import hashlib
import tempfile
from pathlib import Path
import unittest
spec = importlib.util.spec_from_file_location('audit', Path(__file__).resolve().parents[1] / 'scripts' / 'audit_r123_owner_readonly.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

class TestReadOnlyAudit(unittest.TestCase):
    def source(self, sha):
        x={'repo_id':'abc/model','source_revision':'a'*40,'repository_type':'model',
           'source_files':[{'path':'model.safetensors','bytes':4,'sha256':sha,'git_blob_sha1':None,'prior_61_reported_content_hash_match':True}]}
        return {'canonical_revision':'v52-20261119', 'source_repositories':[x]+[{'repo_id':f'x{i}/y{i}', 'source_revision':'b'*40, 'repository_type':'model','source_files':[]} for i in range(16)]}
    def test_match_and_corruption(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            f=root/'models/abc/model/model.safetensors'
            f.parent.mkdir(parents=True)
            f.write_bytes(b'data')
            manifest=self.source(hashlib.sha256(b'data').hexdigest())
            self.assertEqual(p.audit(manifest,root)['status_counts']['VERIFIED_ON_OWNER_VOLUME'],1)
            f.write_bytes(b'wrong')
            self.assertEqual(p.audit(manifest,root)['status_counts']['CONFLICT'],1)
    def test_no_file_not_verified(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(p.audit(self.source(hashlib.sha256(b'data').hexdigest()),Path(td))['status_counts']['UNLOCATED_IN_KNOWN_LAYOUTS'],1)
    def test_parent_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as out:
            root=Path(td); other=Path(out); (other/'model.safetensors').write_bytes(b'data')
            prefix=root/'models/abc';prefix.mkdir(parents=True)
            try:
                (prefix/'model').symlink_to(other, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest('Symlink creation unavailable on this platform')
            self.assertEqual(p.audit(self.source(hashlib.sha256(b'data').hexdigest()),root)['status_counts']['CONFLICT'],1)
    def test_path_rejections(self):
        for s in ['../x', 'C:/x', 'dir\\x', 'CON.txt', 'file:x','x/../b','a//b','x.']:
            with self.subTest(s=s):
                with self.assertRaises(ValueError):p.safe_rel(s)
    def test_git_blob(self):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'config.json';f.write_bytes(b'{}')
            sha=hashlib.sha1(b'blob 2\0{}').hexdigest()
            self.assertEqual(p.fingerprint(f,2,None,sha),(True,'VERIFIED'))
            self.assertFalse(p.fingerprint(f,2,None,'0'*40)[0])

if __name__=='__main__':unittest.main()
