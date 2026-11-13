"""v25 regression: one restricted-geo image derivative, no acquisition permissions."""
import copy,json,unittest
from pathlib import Path
from scripts.apply_selection_v25 import prepare
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def fixture():
    items=[{'asset_kind':'model','repo_id':f'test/m{i}',
       'portfolio_decision':'conditional' if i<121 else 'hold',
       'risk_tier':'R1' if i<121 else 'HOLD',
       'parameter_gate':{'status':'PASS_TOTAL_PARAMS_LT_150B','total_parameters':1000000},
       'download_approved':False,'selected_file_bytes':None,
       'forecast_priority':{'wave':['S1','S2','S3'][i%3],'rank':i+1}}
       for i in range(168)]
    c={'revision_id':'v24-20261106','expected':{'tracked':168,'active':121,'budget_scenario':{}},
      'ordered_overlays':[],'notes':'','application_rule':'','capacity_audit':{'source_revision':'v24-20261106'}}
    v={'revision_id':'v24-20261106','items':items,'budget':{},'counts':{}}
    q={'source_revision':'v24-20261106','approved':False,'download_enabled':False,
       'candidates':[{'asset_kind':x['asset_kind'],'repo_id':x['repo_id'],'not_authorized':True,'download_approved':False} for x in items[:121]]}
    return c,v,q,load('catalog/revisions/v25-2026-11-06.json')
class V25SelectionTests(unittest.TestCase):
    def test_exact_one_identity_and_license_overhang(self):
        o=load('catalog/revisions/v25-2026-11-06.json')
        self.assertEqual(len(o['additions']),1)
        x=o['additions'][0]
        self.assertEqual(x['repo_id'],'PrunaAI/P-H3-Image')
        self.assertEqual(x['selection_budget_cap_bytes'],105_000_000_000)
        self.assertEqual(x['preliminary_named_selected_primary_bytes'],99_840_428_064)
        self.assertEqual(x['parameter_gate']['status'],'UNVERIFIED_BLOCK_FINAL_LOCK')
        self.assertIsNone(x['parameter_gate']['total_parameters'])
        self.assertTrue(x['research_only_unknown_total_allow_conditional'])
        self.assertEqual(set(x['license_detail']['excluded_territories']),{'EU','UK','South Korea','USA'})
        self.assertFalse(x['download_approved'])
        self.assertFalse(x['license_text_reviewed'])
    def test_transition_maintains_168_old_and_adds_research_only(self):
        args=fixture(); before=copy.deepcopy(args)
        o=prepare(*args)
        self.assertEqual(args,before)
        self.assertEqual(o['view']['items'][:168],args[1]['items'])
        self.assertEqual(len(o['view']['items']),169)
        self.assertEqual(o['current']['expected']['active'],122)
        self.assertEqual(len(o['queue']['candidates']),122)
        self.assertEqual(len(o['plan']['items']),122)
        x=next(x for x in o['queue']['candidates'] if x['repo_id']=='PrunaAI/P-H3-Image')
        self.assertTrue(x['research_only'])
        self.assertFalse(x['can_enter_approved_queue'])
        self.assertTrue(x['requires_total_parameter_confirmation'])
        self.assertIsNone(o['view']['budget']['final_selected_total_bytes'])
        self.assertEqual(o['view']['budget']['archive_limit_bytes'],4_000_000_000_000)
        self.assertFalse(o['queue']['approved'])
        self.assertFalse(o['queue']['download_enabled'])
    def test_unauthorized_shortcuts_and_duplicate_refused(self):
        for f,v in (('download_approved',True),('fully_pinned_revision_sha','a'*40),('selected_file_bytes',99840428064)):
            args=list(fixture());args[3]['additions'][0][f]=v
            with self.subTest(f=f),self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['additions'][0]['repo_id']='test/m0'
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['additions'][0]['parameter_gate']['status']='PASS_TOTAL_PARAMS_LT_150B'
        with self.assertRaises(ValueError):prepare(*args)
        args=list(fixture());args[3]['max_new_selection_budget_bytes']=10
        with self.assertRaises(ValueError):prepare(*args)
if __name__=='__main__':unittest.main()
