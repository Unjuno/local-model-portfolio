"""v26: guard three distinct original learned outcomes and gated nonacquisition."""
import copy,json,unittest
from pathlib import Path
from scripts.apply_selection_v26 import prepare
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def fixture():
    items=[{'asset_kind':'model','repo_id':f'fixture/m{i}',
        'portfolio_decision':'conditional' if i<122 else 'hold',
        'risk_tier':'R1' if i<122 else 'HOLD','download_approved':False,'selected_file_bytes':None,
        'parameter_gate':{'status':'PASS_TOTAL_PARAMS_LT_150B','total_parameters':1000000},
        'forecast_priority':{'wave':['S1','S2','S3'][i%3],'rank':i+1}}
        for i in range(169)]
    c={'revision_id':'v25-20261106','expected':{'tracked':169,'active':122,'budget_scenario':{}},
       'ordered_overlays':[],'notes':'','application_rule':'',
       'capacity_audit':{'source_revision':'v25-20261106','status':'ALL_122_SOURCE_SCOPES_EXACT'}}
    v={'revision_id':'v25-20261106','items':items,'budget':{},'counts':{}}
    q={'source_revision':'v25-20261106','approved':False,'download_enabled':False,
       'candidates':[{'asset_kind':x['asset_kind'],'repo_id':x['repo_id'],
          'not_authorized':True,'download_approved':False} for x in items[:122]]}
    return c,v,q,load('catalog/revisions/v26-2026-11-06.json')
class V26Tests(unittest.TestCase):
    def test_overlay_three_unique_and_ernie_oversized_hold(self):
        o=load('catalog/revisions/v26-2026-11-06.json')
        self.assertEqual(o['previous_revision_id'],'v25-20261106')
        self.assertEqual(len(o['additions']),3)
        self.assertEqual(len({x['repo_id'].lower() for x in o['additions']}),3)
        self.assertEqual(sum(x['selection_budget_cap_bytes'] for x in o['additions']),35_600_000_000)
        self.assertEqual(o['previous_verified_capacity']['known_logical_dedup_bytes'],3_372_065_984_104)
        self.assertEqual(o['research_not_selected'][0]['repo_id'],'baidu/ERNIE-5.5-Flash-Base')
        self.assertIn('HOLD',o['research_not_selected'][0]['decision'])
        self.assertEqual(o['research_not_selected'][0]['publisher_tensor_elements'],286_245_697_882)
        for x in o['additions']:
            self.assertFalse(x['download_approved'])
            self.assertFalse(x['license_text_reviewed'])
            self.assertIsNone(x['fully_pinned_revision_sha'])
            self.assertIsNone(x['selected_file_bytes'])
            self.assertTrue(x['reason_selected'] and x['quality_negative'] and x['falsification_condition'])
            self.assertIsNone(x['restriction_assessment']['probability'])
    def test_old_169_unchanged_and_phonon_gate_is_noncompensatory(self):
        args=fixture();before=copy.deepcopy(args)
        x=prepare(*args)
        self.assertEqual(args,before)
        self.assertEqual(x['view']['items'][:169],args[1]['items'])
        self.assertEqual(len(x['view']['items']),172)
        self.assertEqual(x['current']['expected']['active'],125)
        self.assertEqual(len(x['queue']['candidates']),125)
        self.assertEqual(len(x['plan']['items']),125)
        self.assertEqual(x['view']['budget']['new_active_reservation_cap_bytes'],35_600_000_000)
        self.assertFalse(x['queue']['approved'])
        self.assertFalse(x['queue']['download_enabled'])
        self.assertIsNone(x['view']['budget']['final_selected_total_bytes'])
        r=next(q for q in x['queue']['candidates'] if q['repo_id']=='gradium/phonon-40m-multilingual')
        self.assertTrue(r['research_only'])
        self.assertTrue(r['gated_approval_required'])
        self.assertFalse(r['can_enter_approved_queue'])
        self.assertTrue(r['personal_gated_access_verification_required'])
        p=next(q for q in x['plan']['items'] if q['repo_id']=='gradium/phonon-40m-multilingual')
        self.assertEqual(p['next_action'],'PERSONAL_GATED_PERMISSION_AND_LICENSE_REVIEW_ONLY')
    def test_wrong_status_or_gate_fails_closed(self):
        args=list(fixture());args[3]['additions'][2]['observed_access']='public'
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['max_new_selection_budget_bytes']=1
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['additions'][2]['download_approved']=True
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['additions'][0]['parameter_gate']['total_parameters']=280_000_000_000
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[0]['revision_id']='v22-20261106'
        with self.assertRaises(ValueError):prepare(*args)
if __name__=='__main__':unittest.main()
