"""Offline regression: v23 selects two distinct learned outcomes without payload approval."""
import copy
import json
import unittest
from pathlib import Path
from scripts.apply_selection_v23 import prepare
ROOT=Path(__file__).resolve().parents[1]
def overlay():
    return json.loads((ROOT/'catalog/revisions/v23-2026-11-06.json').read_text(encoding='utf-8'))
def fixture():
    items=[]
    for i in range(163):
        items.append({'asset_kind':'model','repo_id':f'fixture/m{i}',
            'portfolio_decision':'conditional' if i<116 else 'hold',
            'risk_tier':'R1' if i<116 else 'HOLD','download_approved':False,
            'parameter_gate':{'status':'PASS_TOTAL_PARAMS_LT_150B','total_parameters':1_000_000},
            'forecast_priority':{'wave':['S1','S2','S3'][i%3],'rank':i+1},
            'selected_file_bytes':None})
    c={'revision_id':'v22-20261106','expected':{'tracked':163,'active':116,'budget_scenario':{}},
       'ordered_overlays':[],'notes':'','application_rule':'',
       'capacity_audit':{'source_revision':'v22-20261106','status':'SOURCE_116_EXACT'}}
    v={'revision_id':'v22-20261106','items':items,'budget':{},'counts':{}}
    q={'source_revision':'v22-20261106','approved':False,'download_enabled':False,
        'candidates':[{'asset_kind':x['asset_kind'],'repo_id':x['repo_id'],
                       'not_authorized':True,'download_approved':False} for x in items[:116]]}
    return c,v,q,overlay()

class V23BoundedSelection(unittest.TestCase):
    def test_two_additions_and_reproducibility_provenance(self):
        o=overlay()
        self.assertEqual(len(o['additions']),2)
        self.assertEqual({x['repo_id'] for x in o['additions']},
           {'Hcompany/Holotron4-30B-A3B','LiquidAI/LFM2.5-24B-A2B-DSpark'})
        self.assertEqual(sum(x['selection_budget_cap_bytes'] for x in o['additions']),71_000_000_000)
        self.assertEqual(o['previous_verified_capacity']['known_logical_dedup_bytes'],3_108_440_834_201)
        for x in o['additions']:
            self.assertTrue(x['reason_selected'])
            self.assertTrue(x['quality_negative'])
            self.assertTrue(x['falsification_condition'])
            self.assertEqual(len(x['upstream_revision_sha_observed']),40)
            self.assertTrue(x['publisher_immutable_snapshot_path'])
            self.assertIsNone(x['selected_file_bytes'])
            self.assertFalse(x['download_approved'])
            self.assertFalse(x['license_text_reviewed'])
            self.assertTrue(x['preservation_bundle']['scope_reference_only_no_download_manifest'])
        self.assertEqual(o['additions'][0]['parameter_gate']['total_parameters'],33_015_598_915)
        self.assertEqual(o['additions'][1]['source_model_standalone_parameters'],327_707_521)
        self.assertEqual(o['additions'][1]['parameter_gate']['total_parameters'],24_299_307_521)
    def test_preserves_all_v22_identities_and_approvals(self):
        args=fixture();before=copy.deepcopy(args);r=prepare(*args)
        self.assertEqual(args,before)
        self.assertEqual(r['view']['items'][:163],args[1]['items'])
        self.assertEqual(len(r['view']['items']),165)
        self.assertEqual(r['current']['expected']['active'],118)
        self.assertEqual(len(r['queue']['candidates']),118)
        self.assertEqual(len(r['plan']['items']),118)
        self.assertFalse(r['queue']['approved']);self.assertFalse(r['plan']['download_enabled'])
        self.assertTrue(all(not x['download_approved'] for x in r['view']['items']))
        self.assertEqual(r['current']['capacity_audit']['latest_revision_scope_coverage'],116)
        self.assertEqual(r['current']['capacity_audit']['v23_new_assets_unmeasured_count'],2)
        self.assertIsNone(r['view']['budget']['final_selected_total_bytes'])
        self.assertIsNone(r['view']['budget']['final_headroom_bytes'])
    def test_forged_rights_or_duplicate_or_bogus_risk_rejected(self):
        for field,value in (('download_approved',True),('fully_pinned_revision_sha','a'*40),
                            ('selected_file_bytes',0)):
            args=list(fixture());args[3]['additions'][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['additions'][1]['repo_id']='FIXTURE/m0'
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['additions'][0]['restriction_assessment']['probability']=0.9
        with self.assertRaises(ValueError):prepare(*args)
    def test_original_parameter_count_and_budget_gates_not_waived(self):
        args=list(fixture());args[3]['max_new_selection_budget_bytes']=10
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['additions'][0]['parameter_gate']['total_parameters']=180_000_000_000
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[0]['revision_id']='v19-20261106'
        with self.assertRaises(ValueError):prepare(*args)

if __name__=='__main__':unittest.main()
