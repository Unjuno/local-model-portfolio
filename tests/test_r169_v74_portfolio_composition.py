"""V74 authorized selection delta, not a weight transfer or deletion."""
import collections, itertools, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def key(x):return x['asset_kind'],x['repo_id']
class V74Composition(unittest.TestCase):
 def setUp(self):
  self.c=read('catalog/snapshots/2026-11-28-v74-current-before-v75.json')
  self.old=read('catalog/effective-portfolio-2026-11-25-v73.json')
  self.new=read('catalog/effective-portfolio-2026-11-27-v74.json')
  self.ov=read('catalog/revisions/v74-2026-11-27.json')
  self.report=read('catalog/audits/2026-11-27-r169-v74-portfolio-composition-audit.json')
 def test_exact_preconditioned_delta_and_historical_integrity(self):
  old={key(i):i for i in self.old['items']};new={key(i):i for i in self.new['items']}
  self.assertEqual(set(old),set(new));self.assertEqual(len(new),265)
  k=('model','meta-llama/Llama-4-Scout-17B-16E')
  self.assertEqual([i for i in old if old[i]!=new[i]],[k])
  op,=self.ov['replacement_operations']
  self.assertEqual(key(op),k)
  self.assertEqual((old[k]['portfolio_decision'],old[k]['risk_tier']),(op['from_decision'],op['from_tier']))
  self.assertEqual((new[k]['portfolio_decision'],new[k]['risk_tier']),(op['to_decision'],op['to_tier']))
  self.assertEqual((op['to_decision'],op['to_tier']),('hold','HOLD'))
  self.assertFalse(op['physical_file_deletion']);self.assertFalse(op['download_approved'])
  self.assertEqual(self.ov['removed_assets'],[]);self.assertEqual(self.ov['additions'],[])
  self.assertIsNone(new[k]['r169_composition_review']['actual_incremental_or_freed_bytes'])
  self.assertEqual(self.ov['physical_files_deleted'],0)
 def test_live_v74_joins(self):
  c=self.c;self.assertEqual(c['revision_id'],'v74-20261127')
  self.assertEqual(c['materialized_catalog_path'],'catalog/effective-portfolio-2026-11-27-v74.json')
  active={key(i) for i in self.new['items'] if i['portfolio_decision'] in ('select','conditional')}
  conditional={key(i) for i in self.new['items'] if i['portfolio_decision']=='conditional'}
  self.assertEqual(len(active),210);self.assertEqual(len(conditional),154)
  self.assertEqual(collections.Counter(i['portfolio_decision'] for i in self.new['items']),{'select':56,'conditional':154,'hold':36,'deferred':13,'excluded':6})
  r=read(c['latest_active_readiness_audit']['summary_path']);q=read(c['priority_worklist_path']);p=read(c['insurance_preparation_worklist_path']);a=read(c['latest_conditional_access_audit']['path'])
  self.assertEqual(active,{key(i) for i in r['records']});self.assertEqual(active,{key(i) for i in q['candidates']});self.assertEqual(active,{key(i) for i in p['items']});self.assertEqual(conditional,{key(i) for i in a['entries']})
  self.assertTrue(all(not i['download_approved'] and not i['ready_to_acquire'] and i['final_selected_file_bytes'] is None for i in r['records']))
  self.assertEqual(read('queues/approved.json')['entries'],[])
 def test_receipt_counts_hashes_and_capacity_not_physical(self):
  l=read('catalog/execution/2026-11-19-acquisition-ledger.json');v=[i for i in l['models'] if i['status']=='VERIFIED'];ids={i['repo_id']:i['asset_kind'] for i in self.old['items']}
  m=self.report['metrics'];self.assertEqual(len(v),m['receipt_verified_count'])
  self.assertEqual(sum(ids.get(i['repo_id'])=='model' for i in v),127)
  self.assertEqual(sum(ids.get(i['repo_id'])=='dataset' for i in v),2)
  self.assertEqual(sum(i['repo_id'] not in ids for i in v),4)
  h=[frozenset(f['sha256'] for f in i.get('weight_files_sha256',[]) if f.get('sha256')) for i in v]
  self.assertEqual(sum(bool(s) for s in h),130)
  self.assertEqual(sum(n>1 for n in collections.Counter(s for s in h if s).values()),0)
  self.assertEqual(sum(bool(s&t) and s!=t for s,t in itertools.combinations(h,2)),33)
  self.assertEqual(self.c['latest_reported_ledger_summary']['reported_VERIFIED_models'],133)
  self.assertEqual(self.c['historical_reported_ledger_summary_116']['reported_VERIFIED_models'],116)
  self.assertFalse(m['physical_capacity_or_savings_verified']);self.assertFalse(self.report['owner_disk_sha_rechecked'])
if __name__=='__main__':unittest.main()
