"""Masked public metadata preserves capacity but never establishes content reuse."""
import importlib.util
from pathlib import Path
import unittest

class MaskedCapacityTests(unittest.TestCase):
    def setUp(self):
        p=Path(__file__).resolve().parents[1]/'scripts/capacity_inventory.py'
        spec=importlib.util.spec_from_file_location('capacity_inventory',p)
        self.m=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)

    def test_masked_lfs_keeps_size_without_false_deduplication(self):
        r=self.m.normalize_file({'type':'file','path':'model.safetensors','size':100,
            'oid':'1'*40,'lfs':{'oid':'*'*64,'size':100},'xetHash':'*'*64})
        self.assertEqual(r['bytes'],100)
        self.assertIsNone(r['sha256'])
        self.assertEqual(r['identity_kind'],'unverifiable_payload_hash')
        self.assertEqual(self.m.deduplicated_bytes([('a',r),('b',r)]),200)

    def test_xet_without_digest_is_not_git_blob_dedup(self):
        r=self.m.normalize_file({'type':'file','path':'m','size':100,'oid':'1'*40,'xetHash':'*'*64})
        self.assertEqual(r['identity_kind'],'unverifiable_payload_hash')
        self.assertEqual(self.m.deduplicated_bytes([('a',r),('b',r)]),200)

if __name__=='__main__':unittest.main()
