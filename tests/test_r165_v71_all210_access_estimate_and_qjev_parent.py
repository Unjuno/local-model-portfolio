"""R165 v71 post-publication full-catalog reconciliation; offline and source-only."""
import json,unittest,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def J(p):return json.loads((R/p).read_text(encoding='utf-8'))
class R165PostPublication(unittest.TestCase):
 def test_v71_owner_stop_sidecars_match_exact_unmodified_selection(self):
  c=J('catalog/CURRENT.json')
  v=J(c['materialized_catalog_path'])
  a=J(c['latest_conditional_access_audit']['path'])
  q=J(c['priority_worklist_path'])
  d=J(c['latest_active_readiness_audit']['summary_path'])
  p=J(c['insurance_preparation_worklist_path'])
  self.assertIn((c['revision_id'],c['expected']['tracked'],c['expected']['active']),(('v71-20261125',260,210),('v72-20261125',264,210),('v73-20261125',265,211)))
  self.assertEqual(v['items'][:260],J('catalog/effective-portfolio-2026-11-25-v71.json')['items'])
  self.assertEqual(v['items'][:258],J('catalog/effective-portfolio-2026-11-25-v70.json')['items'])
  active={(x['asset_kind'],x['repo_id']) for x in v['items'] if x['portfolio_decision'] in ('select','conditional')}
  cond={(x['asset_kind'],x['repo_id']) for x in v['items'] if x['portfolio_decision']=='conditional'}
  self.assertEqual((len(active),len(cond)),(c['expected']['active'],c['expected']['by_decision']['conditional']))
  self.assertEqual({(x['asset_kind'],x['repo_id']) for x in q['candidates']},active)
  self.assertEqual({(x['asset_kind'],x['repo_id']) for x in p['items']},active)
  self.assertEqual({(x['asset_kind'],x['repo_id']) for x in d['records']},active)
  self.assertEqual({(x['asset_kind'],x['repo_id']) for x in a['entries']},cond)
  self.assertEqual(a['source_revision'],c['revision_id'])
  self.assertEqual((a['scope'],a['tracked_conditional'],a['gated_count']),(c['expected']['by_decision']['conditional'],c['expected']['by_decision']['conditional'],21))
  self.assertEqual(J('catalog/readiness/CURRENT.json')['catalog_revision'],c['revision_id'])
  self.assertEqual(J('catalog/estimates/CURRENT.json')['portfolio_revision'],c['revision_id'])
  self.assertEqual(c['expected']['budget_scenario'],v['budget'])
  self.assertEqual(d['summary']['blocked_any'],c['expected']['active'])
  self.assertEqual(d['summary']['downloads_approved'],0)
  self.assertEqual(d['summary']['ready_to_approve'],0)
  self.assertFalse(q['download_enabled'] or a['download_authorized'] or p['download_enabled'])
  self.assertEqual(J('queues/approved.json')['entries'],[])
  self.assertTrue(all(not x['download_approved'] and not x['ready_to_acquire'] for x in d['records']))
 def test_aligned_head_sha_equal_but_backbone_differs_and_uncertainty_is_not_inferred(self):
  x=J('catalog/research/2026-11-25-r165-qjev-parent-head-immutable-provenance.json')
  m=J('manifests/drafts/r163-2026-11-25-five-uncensored-source-complete-publisher-OID-SHA.candidate.json')
  q=next(s for s in m['publisher_sources'] if s['repo_id']=='AnkitNayak-dev/QJev-1.5B-Abliterated')
  f={z['path']:z for z in q['publisher_exact_files']}
  self.assertEqual(x['abliterated_head_sha256'],x['aligned_head_sha256'])
  self.assertEqual(x['abliterated_head_sha256'],f['decision_head.safetensors']['publisher_lfs_sha256'])
  self.assertEqual(x['abliterated_backbone_sha256'],f['model.safetensors']['publisher_lfs_sha256'])
  self.assertNotEqual(x['aligned_backbone_sha256'],x['abliterated_backbone_sha256'])
  self.assertTrue(x['probability_calibration_preserved_not_proven'])
  self.assertFalse(x['owner_device_local_SHA_checked'])
  self.assertFalse(x['owner_explicit_acquisition_authorization'])
  self.assertFalse(x['complete_offline_runtime_or_calibration_approved'])
  self.assertEqual({s['repo_id'] for s in m['publisher_sources']}.issuperset({'2Beyes/Aurum-2B-Uncensored','AnkitNayak-dev/QJev-1.5B-Abliterated'}),True)
if __name__=='__main__':unittest.main()
