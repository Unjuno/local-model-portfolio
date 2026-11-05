"""Offline checks for R22. No network, weights, inference, or disk mutations."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
from scripts.audit_component_census import audit, verify_support_bytes
ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'catalog/preparation/2026-11-05-component-census.json'
PLAN=ROOT/'manifests/drafts/round21-pinned-preservation.candidate.json'

class ComponentCensusTests(unittest.TestCase):
    def setUp(self):
        self.e=json.loads(EVIDENCE.read_text())
        self.p=json.loads(PLAN.read_text())
    def test_complete_evidence(self):
        self.assertEqual([],audit(self.e,self.p))
    def test_exact_totals_and_separate_vision(self):
        self.assertEqual(16_555_533_156,self.e['packages']['chatr-image']['serialized_scalar_total'])
        self.assertEqual(27_781_427_952,self.e['packages']['interpretic-q4']['serialized_scalar_total'])
        self.assertEqual(460_730_096,self.e['component_scalars']['interpretic-vision'])
    def test_missing_file_cannot_pass(self):
        self.e['weight_headers'].pop()
        self.assertTrue(audit(self.e,self.p))
    def test_byte_size_not_tensor_count(self):
        self.e['weight_headers'][0]['scalars_by_dtype']['BF16']+=1
        self.assertTrue(audit(self.e,self.p))
    def test_wrong_total_rejected(self):
        self.e['packages']['chatr-image']['serialized_scalar_total']=7_115_124_736
        self.assertTrue(audit(self.e,self.p))
    def test_no_transfer_or_runtime_approval(self):
        self.e['download_authorized']=True
        self.assertTrue(audit(self.e,self.p))
    def test_header_digest_is_not_full_weight_digest(self):
        self.e['weight_headers'][0]['full_weight_hash_verified']=True
        self.assertTrue(audit(self.e,self.p))
    def test_mixed_gguf_not_all_four_bit(self):
        row=next(x for x in self.e['weight_headers'] if x['component']=='interpretic-language')
        self.assertEqual({'0','12','14'},set(row['scalars_by_dtype']))
    def test_all_adapter_targets_required(self):
        self.e['adapter_compatibility']['matched_pairs']=223
        self.assertTrue(audit(self.e,self.p))
    def test_stale_publisher_checksums_not_silently_rewritten(self):
        c=self.e['publisher_checksum_discrepancies']
        self.assertEqual({'README.md','inference.py'},{x['path'] for x in c})
        self.assertTrue(all(x['publisher_sha256']!=x['observed_sha256'] for x in c))
        self.e['publisher_checksum_discrepancies']=[]
        self.assertTrue(audit(self.e,self.p))
    def test_lfs_resolved_bytes_use_sha256_not_pointer_blob(self):
        b=b'example payload'; f={'bytes':len(b),'source_sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha1':'0'*40}
        self.assertEqual('source_sha256',verify_support_bytes(b,f))
        with self.assertRaises(ValueError): verify_support_bytes(b+b'!',f)
    def test_ordinary_git_blob_compares_header_plus_content(self):
        b=b'example'; sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        self.assertEqual('git_blob_sha1',verify_support_bytes(b,{'bytes':len(b),'source_sha256':None,'git_blob_sha1':sha}))
    def test_corruption_and_boolean_sizes_rejected(self):
        with self.assertRaises(ValueError): verify_support_bytes(b'x',{'bytes':True,'source_sha256':'0'*64})
        with self.assertRaises(ValueError): verify_support_bytes(b'x',{'bytes':1,'source_sha256':'0'*64})
    def test_original_file_plan_unchanged(self):
        b=PLAN.read_bytes(); git=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        self.assertEqual('c3574bfe8df5c0c1edd81f6d3e16c11291a6dda0',git)

if __name__=='__main__': unittest.main()
