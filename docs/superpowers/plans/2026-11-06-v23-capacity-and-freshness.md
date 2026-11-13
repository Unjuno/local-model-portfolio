# v23 Capacity and Latest Access Verification Implementation Plan

Goal: Finish the pending two-asset capacity calculation and verify recent upstream access/license/commit changes without approving acquisition or changing selections.
Architecture: Keep v22 fixed evidence immutable. Complete a v23 accounting view from its two already-pinned source inventories. Recheck current metadata for all 118 active IDs, with a bounded review of PFN translation releases and the Saluki license change.
Tech stack: Python >=3.10 standard library and existing repository utilities; metadata-only GitHub Actions on the dedicated risk branch.
Spec: user request dated 2026-11-06; policies/archival-insurance.json and policies/limits.json.

Constraints: preserve main; 165 tracked / 118 active; 4,000,000,000,000-byte budget and 200,000,000,000-byte free-space floor; all approvals remain false. No weights, dataset payload, model execution or paid cloud jobs. Owner-disk evidence remains unknown when no device is connected.

1. Reproduce the unfinished v23 script's initialization and integer/file aggregation faults using its regression tests. Fix only those causes; preserve unknown dependencies and historical sources.
2. Verify all 118 active primary scopes and the no-double-count target dependency rule. Publish a separate v23 capacity view and update CURRENT pointers only.
3. Write and run negative tests for unknown metadata, license-list normalization, immutable text URLs, payload/redirect blocking. Implement a bounded anonymous metadata refresh. Compare source commits and gate/license fields, not an invented regulation score.
4. Recheck PFN's November 5 release and Saluki's November 5 license history with pinned creator material. Scan previous catalog/research decisions before recommending any new inclusion. Preserve negative evidence and do not silently replace selected checkpoints.
5. Run the complete repository suite and both audits. Hash protected files before and after; reject concurrent branch changes; commit results to strategy/2026-11-03-01-risk only.

Local test evidence: eight new metadata/URL tests failed before implementation (missing functions), then all eight passed with the implementation on Python 3.13. Full repository integration runs in GitHub Actions, not on the owner's machine. Do not equate code test success, metadata file sizes or a LICENSE keyword with physical storage, model quality or legal clearance.
