"""Pure tests: metadata changes are not evidence of bans or acquisition rights."""
import unittest
try:
    from scripts.latest_access_v23 import changes, detect_license, validate_text_url
except ImportError:
    changes = detect_license = validate_text_url = None

class LatestAccessTests(unittest.TestCase):
    def test_unchanged(self):
        self.assertIsNotNone(changes, 'metadata comparison not implemented')
        r=changes({'pinned_revision':'a'*40,'gated':False,'license_metadata':'other'},
                  {'sha':'a'*40,'gated':False,'cardData':{'license':'other'}})
        self.assertEqual(r, {'revision_changed':False,'gated_changed':False,'license_metadata_changed':False})
    def test_license_change_is_separate_from_revision(self):
        self.assertIsNotNone(changes)
        r=changes({'pinned_revision':'a'*40,'gated':False,'license_metadata':'apache-2.0'},
                  {'sha':'b'*40,'gated':False,'cardData':{'license':'cc-by-nc-4.0'}})
        self.assertTrue(r['license_metadata_changed']); self.assertTrue(r['revision_changed'])
        self.assertFalse(r['gated_changed'])
        self.assertNotIn('regulation_probability',r)
    def test_unknown_prior_is_not_unchanged_or_change(self):
        self.assertIsNotNone(changes)
        r=changes({}, {'sha':'a'*40,'gated':False,'cardData':{'license':'apache-2.0'}})
        self.assertTrue(all(x is None for x in r.values()))
    def test_unknown_current_is_not_a_downgrade(self):
        self.assertIsNotNone(changes)
        r=changes({'pinned_revision':'a'*40,'gated':False,'license_metadata':'apache-2.0'}, {})
        self.assertTrue(all(x is None for x in r.values()))
    def test_license_order_and_false_gate_are_preserved(self):
        self.assertIsNotNone(changes)
        r=changes({'gated':False,'license_metadata':['a','b']},
                  {'gated':False,'cardData':{'license':['b','a']}})
        self.assertFalse(r['gated_changed']);self.assertFalse(r['license_metadata_changed'])
    def test_primary_license_marker(self):
        self.assertIsNotNone(detect_license)
        self.assertEqual(detect_license('Apache License\nVersion 2.0, January 2004'),'apache-2.0')
        self.assertEqual(detect_license('Attribution-NonCommercial 4.0 International'),'cc-by-nc-4.0')
        self.assertEqual(detect_license('PLaMo Community License'),'plamo-community')
        self.assertEqual(detect_license('A comment about no license'),'undetermined')
    def test_raw_license_requires_immutable_commit(self):
        self.assertIsNotNone(validate_text_url)
        self.assertIsNone(validate_text_url('https://huggingface.co/pfnet/name/raw/'+'a'*40+'/LICENSE'))
        with self.assertRaises(ValueError):validate_text_url('https://huggingface.co/pfnet/name/raw/main/LICENSE')
    def test_exact_nested_license_documents(self):
        self.assertIsNone(validate_text_url('https://huggingface.co/pfnet/name/raw/'+'a'*40+'/LICENSE/en'))
        self.assertIsNone(validate_text_url('https://huggingface.co/pfnet/name/raw/'+'a'*40+'/LICENSE/ja'))
        with self.assertRaises(ValueError):validate_text_url('https://huggingface.co/pfnet/name/raw/'+'a'*40+'/LICENSE/model.bin')
    def test_notice_parent_reference_is_not_assigned_as_child_license(self):
        text='Parent: Apache License Version 2.0. The derived model: CC BY-NC 4.0.'
        self.assertEqual(detect_license(text),'cc-by-nc-4.0')
    def test_weights_redirects_credentials_and_traversal_blocked(self):
        self.assertIsNotNone(validate_text_url)
        for u in ('https://huggingface.co/a/b/raw/'+'a'*40+'/model.safetensors',
                  'https://evil.example/a/b/raw/'+'a'*40+'/LICENSE',
                  'https://name:secret@huggingface.co/a/b/raw/'+'a'*40+'/LICENSE',
                  'https://huggingface.co/a/b/raw/'+'a'*40+'/%2e%2e/LICENSE'):
            with self.subTest(u=u),self.assertRaises(ValueError):validate_text_url(u)
if __name__=='__main__':unittest.main()
