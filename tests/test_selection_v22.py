"""Offline regression tests for insurance-first archival selection, no weights."""
import copy
import importlib
import unittest

try:
    module = importlib.import_module('scripts.apply_selection_v22')
except ModuleNotFoundError:
    module = None


def fixture():
    items=[]
    for i in range(159):
        items.append({'asset_kind':'model','repo_id':f'fixture/m{i}',
            'portfolio_decision':'conditional' if i<112 else 'hold',
            'risk_tier':'R1' if i<112 else 'HOLD',
            'parameter_gate':{'status':'PASS_TOTAL_PARAMS_LT_150B','total_parameters':1_000_000},
            'forecast_priority':{'wave':('S1','S2','S3')[i%3],'rank':i+1},
            'download_approved':False,'selected_file_bytes':None})
    current={'revision_id':'v21-20261106','expected':{'tracked':159,'active':112},
        'ordered_overlays':[],'notes':'','application_rule':''}
    view={'revision_id':'v21-20261106','items':items,'budget':{},'counts':{}}
    queue={'source_revision':'v21-20261106','approved':False,'download_enabled':False,
        'candidates':[{'asset_kind':x['asset_kind'],'repo_id':x['repo_id'],'not_authorized':True,
                       'download_approved':False} for x in items[:112]]}
    additions=[]
    for i in range(4):
        additions.append({'asset_kind':'model','repo_id':f'new/m{i}',
          'portfolio_decision':'conditional','risk_tier':'R1',
          'url':f'https://huggingface.co/new/m{i}', 'reason_selected':'unique learned outcome',
          'quality_negative':'not fastest; not independently repeated','evidence_date':'2026-11-06',
          'parameter_gate':{'status':'PASS_TOTAL_PARAMS_LT_150B','total_parameters':1_000_000},
          'forecast_priority':{'wave':'S1' if i<3 else 'S3','category':'special'},
          'download_approved':False,'selected_file_bytes':None,'fully_pinned_revision_sha':None,
          'selection_budget_cap_bytes':1_000_000_000,
          'restriction_assessment':{'observed':'public listing','scenario':'hypothesis','probability':None},
          'preservation_bundle':{'learned_outcome':'unique trained delta','must_preserve':['weights','config','license'],
              'shared_dependencies':[],'fixed_manifest_complete':False}})
    overlay={'revision_id':'v22-20261106','previous_revision_id':'v21-20261106',
        'archive_target_bytes':4_000_000_000_000,'minimum_free_bytes':200_000_000_000,
        'max_new_selection_budget_bytes':156_000_000_000,'additions':additions}
    return current,view,queue,overlay


class InsuranceSelectionTests(unittest.TestCase):
    def prepare(self,*args):
        self.assertIsNotNone(module, 'insurance transition not implemented')
        return module.prepare(*args)
    def test_preserves_every_prior_record_and_adds_four(self):
        args=fixture(); before=copy.deepcopy(args); result=self.prepare(*args)
        self.assertEqual(args,before)
        self.assertEqual(result['view']['items'][:159],args[1]['items'])
        self.assertEqual(len(result['view']['items']),163)
        self.assertEqual(result['current']['expected']['active'],116)
    def test_no_imminent_ban_or_fastest_runtime_required_for_selection(self):
        result=self.prepare(*fixture())
        self.assertEqual(sum(x['portfolio_decision']=='conditional' for x in result['view']['items'][-4:]),4)
        self.assertTrue(all(x['restriction_assessment']['probability'] is None for x in result['view']['items'][-4:]))
    def test_unknown_totals_are_selected_research_not_download_preparation(self):
        args=fixture(); row=args[3]['additions'][0]
        row['parameter_gate']={'status':'UNVERIFIED_BLOCK_FINAL_LOCK','total_parameters':None,
                              'research_screening_exception':'CONDITIONAL_RESEARCH_ONLY_NON_EXECUTABLE'}
        row['research_only_unknown_total_allow_conditional']=True
        result=self.prepare(*args)
        entry=next(x for x in result['queue']['candidates'] if x['repo_id']==row['repo_id'])
        self.assertTrue(entry['research_only']); self.assertFalse(entry['can_enter_approved_queue'])
        bundle=next(x for x in result['plan']['items'] if x['repo_id']==row['repo_id'])
        self.assertEqual(bundle['next_action'],'PUBLIC_METADATA_PARAMETER_CENSUS_ONLY')
    def test_unknown_without_marker_rejected(self):
        args=fixture(); args[3]['additions'][0]['parameter_gate']={'status':'UNVERIFIED_BLOCK_FINAL_LOCK','total_parameters':None}
        with self.assertRaises(ValueError): self.prepare(*args)
    def test_authorization_cannot_be_inferred(self):
        for field in ('download_approved','fully_pinned_revision_sha','selected_file_bytes'):
            args=fixture(); args[3]['additions'][0][field]=True
            with self.subTest(field=field), self.assertRaises(ValueError): self.prepare(*args)
    def test_probability_is_not_invented(self):
        args=fixture(); args[3]['additions'][0]['restriction_assessment']['probability']=0.9
        with self.assertRaises(ValueError): self.prepare(*args)
    def test_stale_baseline_and_duplicates_fail_closed(self):
        args=fixture(); args[0]['revision_id']='stale'
        with self.assertRaises(ValueError): self.prepare(*args)
        args=fixture(); args[3]['additions'][0]['repo_id']='FIXTURE/M0'
        with self.assertRaises(ValueError): self.prepare(*args)
    def test_oversized_variant_still_requires_existing_memory_gate(self):
        args=fixture(); row=args[3]['additions'][0]
        row['parameter_gate']={'status':'OVER_150B_QUANT_REVIEW_REQUIRED','total_parameters':180_000_000_000}
        with self.assertRaises(ValueError): self.prepare(*args)
    def test_cap_is_not_known_storage_and_unknown_is_not_zero(self):
        result=self.prepare(*fixture())
        self.assertIsNone(result['view']['budget']['final_selected_total_bytes'])
        self.assertIsNone(result['view']['budget']['final_headroom_bytes'])
        self.assertEqual(result['view']['budget']['archive_limit_bytes'],4_000_000_000_000)
        args=fixture(); args[3]['max_new_selection_budget_bytes']=1
        with self.assertRaises(ValueError): self.prepare(*args)
    def test_plan_has_all_active_assets_and_is_nonexecutable(self):
        result=self.prepare(*fixture()); q=result['queue']; p=result['plan']
        self.assertEqual(len(q['candidates']),116); self.assertEqual(len(p['items']),116)
        self.assertFalse(p['download_enabled']); self.assertFalse(q['approved'])
        stages=[x['stage'] for x in p['items']]
        self.assertEqual(stages,sorted(stages))
        self.assertTrue(all(x['download_approved'] is False and x['not_authorized'] is True for x in q['candidates']))
    def test_missing_preservation_bundle_cannot_be_selected(self):
        args=fixture(); args[3]['additions'][0]['preservation_bundle']={}
        with self.assertRaises(ValueError): self.prepare(*args)

if __name__=='__main__': unittest.main()
