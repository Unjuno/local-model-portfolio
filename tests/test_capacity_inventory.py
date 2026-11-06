"""Offline metadata capacity accounting; no model payload or user disk access."""
import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / 'scripts/capacity_inventory.py'

class CapacityInventoryTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(PATH.is_file(), 'capacity inventory implementation is missing')
        spec = importlib.util.spec_from_file_location('capacity_inventory', PATH)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)

    def test_unknown_is_not_zero(self):
        self.assertIsNone(self.m.exact_sum([10, None]))
        self.assertEqual(self.m.exact_sum([10, 0, 20]), 30)

    def test_invalid_bytes_rejected(self):
        for value in (True, -1, 1.2, '12'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.m.exact_sum([value])

    def test_lfs_digest_is_not_git_pointer(self):
        r = self.m.normalize_file({'type':'file','path':'model.safetensors','size':1000,
            'oid':'1'*40, 'lfs':{'oid':'2'*64,'size':1000}})
        self.assertEqual(r['bytes'], 1000)
        self.assertEqual(r['sha256'], '2'*64)
        self.assertEqual(r['git_blob_sha1'], '1'*40)

    def test_lfs_size_disagreement_fails(self):
        with self.assertRaises(ValueError):
            self.m.normalize_file({'type':'file','path':'x','size':10,'lfs':{'oid':'2'*64,'size':1000}})

    def test_pagination_host_and_path_are_restricted(self):
        self.m.validate_url('https://huggingface.co/api/models/a/b/tree/'+'1'*40+'?cursor=ab')
        for u in ('https://evil.example/api/models/a/b', 'https://huggingface.co/a/b/resolve/main/model.bin',
                  'https://huggingface.co/api/../../a/b', 'https://user:pass@huggingface.co/api/models/a/b'):
            with self.subTest(url=u), self.assertRaises(ValueError): self.m.validate_url(u)

    def test_no_payload_raw_fetch(self):
        self.m.validate_url('https://huggingface.co/a/b/raw/'+'1'*40+'/config.json')
        with self.assertRaises(ValueError):
            self.m.validate_url('https://huggingface.co/a/b/raw/'+'1'*40+'/model.safetensors')

    def test_hash_dedup_and_weak_identity(self):
        f = {'bytes':100,'sha256':'a'*64,'git_blob_sha1':'b'*40,'path':'m'}
        g = {'bytes':20,'sha256':None,'git_blob_sha1':None,'path':'n'}
        result = self.m.deduplicated_bytes([('a',f),('b',f),('a',g),('b',g)])
        self.assertEqual(result, 140)

    def test_digest_size_conflict_rejected(self):
        f = {'bytes':100,'sha256':'a'*64,'git_blob_sha1':None,'path':'m'}
        with self.assertRaises(ValueError):
            self.m.deduplicated_bytes([('a',f),('b',dict(f,bytes=101))])

    def test_path_traversal_rejected(self):
        for p in ('../x','/x','a/../x','a\\x'):
            with self.subTest(path=p), self.assertRaises(ValueError):
                self.m.normalize_file({'type':'file','path':p,'size':1})

if __name__ == '__main__': unittest.main()
