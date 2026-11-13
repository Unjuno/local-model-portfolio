"""v27 Kanana one-original conditional selection with contract license gate."""
import copy,json,unittest
from pathlib import Path
from scripts.apply_selection_v27 import prepare
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def fixture():
    items=[{'asset_kind':'model','repo_id':f'fixture/m{i}',
        'portfolio_decision':'conditional' if i<125 else 'hold',
        'risk_tier':'R1' if i<125 else 'HOLD','download_approved':False,'selected_file_bytes':None,
        'parameter_gate':{'status':'PASS_TOTAL_PARAMS_LT_150B','total_parameters':1000000},
        'forecast_priority':{'wave':['S1','S2','S3'][i%3],'rank':i+1}}
        for i in range(172)]
    c={'revision_id':'v26-20261106','expected':{'tracked':172,'active':125,'budget_scenario':{}},
       'ordered_overlays':[],'notes':'','application_rule':'','capacity_audit':{'source_revision':'v26-20261106'}}
    v={'revision_id':'v26-20261106','items':items,'budget':{},'counts':{}}
    q={'source_revision':'v26-20261106','approved':False,'download_enabled':False,
       'candidates':[{'asset_kind':x['asset_kind'],'repo_id':x['repo_id'],'not_authorized':True,'download_approved':False}
       for x in items[:125]]}
    return c,v,q,load('catalog/revisions/v27-2026-11-07.json')
class V27SelectionTests(unittest.TestCase):
    def test_one_distinct_learned_outcome_and_license(self):
        o=load('catalog/revisions/v27-2026-11-07.json')
        self.assertEqual(o['previous_revision_id'],'v26-20261106')
        self.assertEqual(len(o['additions']),1)
        x=o['additions'][0]
        self.assertEqual(x['repo_id'],'kakaocorp/kanana-2-v-decide-3b-2611')
        self.assertEqual(x['selection_budget_cap_bytes'],8_000_000_000)
        self.assertEqual(x['preliminary_named_selected_primary_bytes'],7_341_102_234)
        self.assertEqual(x['parameter_gate']['total_parameters'],3_665_430_640)
        self.assertFalse(x['download_approved'])
        self.assertFalse(x['license_text_reviewed'])
        self.assertIsNone(x['selected_file_bytes'])
        self.assertIsNone(x['fully_pinned_revision_sha'])
        self.assertEqual(x['license_detail']['immutable_license_sha256'],'3c13f0cf41c4d49f6d3885bffb27c39431826f9886cacac75349b4ffb58361c4')
        self.assertEqual({y['repo_id'] for y in o['research_not_selected']},{'ricursiveAI/Ripple-65B-Base-Preview','ricursiveAI/Ripple-65B-Preview'})
    def test_old_172_unchanged_and_contract_blocked(self):
        args=fixture();pre=copy.deepcopy(args)
        o=prepare(*args)
        self.assertEqual(args,pre)
        self.assertEqual(o['view']['items'][:172],args[1]['items'])
        self.assertEqual(len(o['view']['items']),173)
        self.assertEqual(o['current']['expected']['active'],126)
        self.assertEqual(len(o['queue']['candidates']),126)
        self.assertEqual(len(o['plan']['items']),126)
        self.assertEqual(o['view']['budget']['new_active_reservation_cap_bytes'],8_000_000_000)
        self.assertIsNone(o['view']['budget']['final_selected_total_bytes'])
        n=next(x for x in o['queue']['candidates'] if x['repo_id']=='kakaocorp/kanana-2-v-decide-3b-2611')
        self.assertTrue(n['research_only'])
        self.assertFalse(n['can_enter_approved_queue'])
        self.assertTrue(n['personal_license_review_required'])
        self.assertFalse(o['queue']['approved'])
        self.assertFalse(o['queue']['download_enabled'])
        p=next(x for x in o['plan']['items'] if x['repo_id']==n['repo_id'])
        self.assertEqual(p['next_action'],'KANANA_CONTRACT_LICENSE_AND_OFFLINE_RUNTIME_REVIEW_ONLY')
    def test_mutations_fail_closed(self):
        for field,value in (('download_approved',True),('fully_pinned_revision_sha','a'*40),('selected_file_bytes',12345)):
            args=list(fixture());args[3]['additions'][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['additions'][0]['parameter_gate']['total_parameters']=286_000_000_000
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['additions'][0]['repo_id']='fixture/m1'
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['max_new_selection_budget_bytes']=1
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[0]['revision_id']='v25-20261106'
        with self.assertRaises(ValueError):prepare(*args)
if __name__=='__main__':unittest.main()
