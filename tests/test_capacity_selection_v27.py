"""v27: 126 original file scopes, source-only MOSS and hash-aware deduction."""
import copy,json,unittest
from pathlib import Path
from scripts import capacity_selection_v27 as m
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class V27CapacityTests(unittest.TestCase):
    def args(self):
        return (load(m.BASE/'selected-file-capacity.json'),load('catalog/effective-portfolio-2026-11-07-v27.json'),
            load('catalog/revisions/v27-2026-11-07.json'),load(m.RESEARCH/'research.json'),
            load(m.RESEARCH/'sources/kakaocorp--kanana-2-v-decide-3b-2611.json'),load(m.RESEARCH/'research.json'))
    def test_full_source_scope_and_codec_placement(self):
        a=self.args();data=m.build(*a)
        self.assertEqual(data['tracked'],173)
        self.assertEqual(data['active'],126)
        self.assertEqual(data['exact_primary_file_scope_count'],126)
        self.assertEqual(data['unresolved_primary_scope_count'],0)
        self.assertEqual(data['new_kanana_selected_primary_bytes'],7_341_102_234)
        self.assertEqual(data['new_moss_external_dependency_selected_bytes'],7_098_711_111)
        self.assertEqual(data['new_moss_external_dependency_hash_aware_logical_increment_bytes'],7_098_711_111)
        self.assertEqual(len(data['assets_with_open_dependency_issues']),35)
        self.assertLess(data['known_scope_content_union_bytes'],4_000_000_000_000)
        self.assertIsNone(data['complete_offline_archive_bytes'])
        self.assertIsNone(data['physical_disk_free_bytes'])
        self.assertIsNone(data['actual_acquisition_peak_bytes'])
        self.assertEqual(len(data['dependencies']),len(a[0]['dependencies'])+1)
        self.assertTrue(data['moss_external_codec_not_newly_selected_asset'])
        self.assertFalse(data['download_authorized'])
        self.assertEqual(data['model_payload_bytes_downloaded'],0)
    def test_missing_licensed_files_and_mutated_byte_count_rejected(self):
        a=list(self.args());a[4]=copy.deepcopy(a[4])
        a[4]['files']=[f for f in a[4]['files'] if f['path']!='LICENSE']
        with self.assertRaises((AssertionError,ValueError,KeyError)):m.build(*a)
        a=list(self.args());a[5]=copy.deepcopy(a[5])
        a[5]['mandatory_moss_codec_capacity_accounting']['codec_selected_files'][0]['bytes']=0
        with self.assertRaises((AssertionError,ValueError)):m.build(*a)
    def test_baseline_remains_readonly(self):
        a=self.args();old=copy.deepcopy(a)
        m.build(*a)
        self.assertEqual(a,old)
if __name__=='__main__':unittest.main()
