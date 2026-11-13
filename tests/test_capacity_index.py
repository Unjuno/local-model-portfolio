"""Filename denominators are not authoritative when a pinned index names shards."""
import importlib.util
from pathlib import Path
import unittest

class CapacityIndexTests(unittest.TestCase):
    def setUp(self):
        p=Path(__file__).resolve().parents[1]/'scripts/capacity_selection.py'
        spec=importlib.util.spec_from_file_location('capacity_selection',p)
        self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
    def test_zero_based_last_index_requires_publisher_index(self):
        rows=[{'path':'model-%05d-of-00002.safetensors'%i,'bytes':100} for i in range(3)]
        with self.assertRaises(ValueError):self.m.check_shards(rows)
        self.m.check_shards(rows,[f['path'] for f in rows])
    def test_missing_index_declared_shard_still_fails(self):
        rows=[{'path':'model-00001-of-00001.safetensors','bytes':100}]
        with self.assertRaises(ValueError):
            self.m.check_shards(rows,[rows[0]['path'],'model-00002-of-00001.safetensors'])
if __name__=='__main__':unittest.main()
