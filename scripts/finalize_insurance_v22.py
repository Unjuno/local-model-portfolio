#!/usr/bin/env python3
"""Materialize v22 with explicit historical-test scope and verified source reads.
Standard library only; no model/vault/network use. Called only by branch CI.
"""
from __future__ import annotations
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'tests/test_quantized_memory_research.py'

def main():
    reviewed=REG.read_bytes()
    required=(b'test_research_is_unapproved_and_historical_catalog_unchanged',
              b'test_current_catalog_and_queue_are_consistent_without_freezing_revision')
    if not all(n in reviewed for n in required):
        raise RuntimeError('reviewed historical/current regression source missing')
    old=json.loads((ROOT/'catalog/effective-portfolio-2026-11-06-v21.json').read_text())
    subprocess.run([sys.executable,'-m','scripts.apply_selection_v22','--apply'],cwd=ROOT,check=True)
    REG.write_bytes(reviewed)
    # R20 describes its v17-time research, not a ban on subsequent adoption.
    p=ROOT/'tests/test_research_round20.py'
    source=p.read_text()
    anchor="        for r in self.read_ledger()['decisions']:\n            self.assertNotIn(('model',r['repo_id']), keyed, 'R20 decisions are not materialized catalog entries')"
    replacement="        historical = json.loads((ROOT/'catalog/effective-portfolio-2026-11-04-v17.json').read_text(encoding='utf-8'))\n        historical_keys = {(r['asset_kind'],r['repo_id']) for r in historical['items']}\n        for r in self.read_ledger()['decisions']:\n            self.assertNotIn(('model',r['repo_id']), historical_keys, 'R20 research must be checked against its historical v17 catalog')"
    if anchor in source:
        if source.count(anchor)!=1: raise RuntimeError('ambiguous historical scope patch')
        p.write_text(source.replace(anchor,replacement))
    elif replacement not in source:
        raise RuntimeError('R20 historical test anchor changed')
    current=json.loads((ROOT/'catalog/CURRENT.json').read_text())
    view=json.loads((ROOT/current['materialized_catalog_path']).read_text())
    queue=json.loads((ROOT/current['priority_worklist_path']).read_text())
    plan=json.loads((ROOT/'catalog/preparation/2026-11-06-insurance-bundles-v22.json').read_text())
    if current['revision_id']!='v22-20261106' or len(view['items'])!=163 or view['items'][:159]!=old['items']:
        raise RuntimeError('catalog transition or original record preservation failed')
    active={(x['asset_kind'],x['repo_id']) for x in view['items'] if x['portfolio_decision'] in ('select','conditional')}
    if len(active)!=116 or len(queue['candidates'])!=116 or len(plan['items'])!=116:
        raise RuntimeError('invalid cardinality')
    if active!={(x['asset_kind'],x['repo_id']) for x in queue['candidates']} or active!={(x['asset_kind'],x['repo_id']) for x in plan['items']}:
        raise RuntimeError('selection/queue/preparation identities differ')
    if queue['approved'] or queue['download_enabled'] or plan['download_enabled'] or json.loads((ROOT/'queues/approved.json').read_text())['entries']:
        raise RuntimeError('unexpected acquisition authorization')
    # Execute all test modules from explicit source bytes; reject mutation.
    snapshots={x.resolve():x.read_bytes() for x in (ROOT/'tests').glob('test_*.py')}
    def guard(event,args):
        if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
            path=Path(os.fsdecode(args[0])).resolve()
            mode=args[1]; flags=args[2]
            write=(isinstance(mode,str) and any(m in mode for m in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
            if path in snapshots and write:
                raise RuntimeError('test source write during verification: '+str(path))
    sys.addaudithook(guard)
    sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(ROOT/'tests'))
    suite=unittest.TestSuite()
    loaded=[]
    for path,data in sorted(snapshots.items()):
        name=path.stem
        spec=importlib.util.spec_from_file_location(name,path)
        module=importlib.util.module_from_spec(spec)
        sys.modules[name]=module
        exec(compile(data,str(path),'exec'),module.__dict__)
        tests=unittest.defaultTestLoader.loadTestsFromModule(module)
        suite.addTests(tests)
        loaded.append({'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(data).hexdigest(),'tests':tests.countTestCases()})
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    print(stream.getvalue())
    if not result.wasSuccessful(): raise RuntimeError('full source-loaded suite failed')
    if any(p.read_bytes()!=data for p,data in snapshots.items()): raise RuntimeError('test source changed')
    if REG.read_bytes()!=reviewed: raise RuntimeError('reviewed regression changed')
    from scripts.check_parameter_cutoff import audit as parameter_audit
    from scripts.audit_selection_decisions import audit as selection_audit
    for name,audit in [('parameter',parameter_audit),('selection',selection_audit)]:
        errors=audit(ROOT)
        if errors: raise RuntimeError(name+' audit failed: '+repr(errors))
        print('PASS '+name+' audit')
    report=ROOT/'catalog/preparation/2026-11-06-v22-integration-check.json'
    evidence=json.loads(report.read_text())
    evidence.update(full_suite_verified=True,full_repository_unittest_count=result.testsRun,
                    parameter_audit_passed=True,selection_audit_passed=True,
                    exact_catalog_plan_consistency_passed=True,test_source_fingerprints=loaded,
                    regression_source_sha256=hashlib.sha256(reviewed).hexdigest())
    report.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'revision':current['revision_id'],'tracked':163,'active':116,'tests_passed':result.testsRun,'download_approved':False}))

if __name__=='__main__': main()
