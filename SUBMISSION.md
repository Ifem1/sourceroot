# SourceRoot — Intelligent Contract Submission Notes

## Category

Standalone GenLayer Intelligent Contract / reusable primitive.

**No frontend.** `examples/authoritative_notice_gate.py` is a tiny composition proof, not an application.

## One-line purpose

SourceRoot creates a consensus-backed, scope-attenuating graph of public source authority so other Intelligent Contracts can reject unofficial, over-scoped, revoked, superseded or stale evidence sources before relying on their content.

## Why this is not a thin LLM wrapper

The LLM cannot create authority by itself.

Deterministic protocol mechanics control:

- the immutable entity definition;
- scope vocabulary and bit assignments;
- scope attenuation from parent to child;
- maximum lineage depth;
- immutable parent pointers;
- source lifecycle;
- lineage commitments;
- consumer certificate pins;
- descendant invalidation through ancestor state;
- which verdicts are legal in initial vs revalidation mode.

Consensus is used only for the genuinely semantic question: whether public anchor evidence establishes the exact claimed authority relationship for the exact frozen scopes.

## Consensus design

SourceRoot uses `gl.vm.run_nondet`.

Leader and validators independently:

1. fetch/render the authority anchor;
2. fetch/render the candidate source;
3. interpret a bounded relation (`ROOT`, `OFFICIAL_FOR`, `DELEGATED_FOR`, `MIRROR_OF`);
4. derive a bounded verdict;
5. require verbatim grounded anchor evidence for a material verdict.

A validator rejects a malicious leader if the independent verdict differs or the leader's evidence is not present in the validator's independently fetched anchor/source.

This is decision re-derivation, not schema-only validation.

## Persistent state design

SourceRoot maintains three durable layers:

1. **Entity definition** — immutable canonical anchor and scope vocabulary.
2. **Authority graph** — immutable parent pointers, relation type, scope mask and lineage hash.
3. **Review history** — every resolution/revalidation receipt with verdict, evidence and certificate commitment.

The graph becomes more useful as more authorised sources and narrower delegations are added.

## Important epistemic boundaries

- `AUTHORITATIVE` does not mean `TRUE`.
- The canonical entity URL is an explicit trust anchor, not magically discovered identity.
- Missing delegation text is not automatically revocation.
- Stale content is not automatically supersession.
- Revocation/supersession require affirmative evidence.
- Ambiguous/unavailable reviews fail closed but remain recoverable.

## Reusability proof

The repository contains `examples/authoritative_notice_gate.py`, a second Intelligent Contract that performs a typed IC-to-IC view call to SourceRoot.

The final submission should include a **live finalized cross-contract StudioNet proof**:

1. deploy SourceRoot;
2. create/seal an entity;
3. resolve a root authority;
4. resolve a narrower child authority;
5. deploy `AuthoritativeNoticeGate(SourceRootAddress)`;
6. accept a notice using the active child authority;
7. revalidate/revoke the parent using explicit public evidence;
8. show the same consumer action now fails because the descendant is no longer effective.

Do not submit until the consumer proof is executed on the canonical deployment and recorded in `docs/DEPLOYMENT.md`.

## Test evidence

Expected final gates:

- `python scripts/preflight.py`
- `pytest tests/static -q`
- `gltest tests/direct -v -s`
- `genvm-lint check contracts/sourceroot.py`
- `genvm-lint check examples/authoritative_notice_gate.py`

Current source pack contains 34 direct-mode scenarios plus static invariants. The live deployment and composability evidence is recorded in `docs/DEPLOYMENT.md`.

## Reviewer-focused differentiators

### Novelty

Most oracle/evidence contracts start by assuming the supplied URL is relevant and authoritative. SourceRoot moves one layer earlier: it makes source authority itself shared, scope-specific, version-pinned contract state.

### Complexity

The contract combines nondeterministic web/LLM verification with deterministic authority attenuation, immutable lineage, revalidation, terminal revocation/supersession states, recoverable fail-closed states, and descendant invalidation.

### Impact

Any web-enabled GenLayer contract can consume SourceRoot before trusting evidence: governance, insurance, SLA settlement, compliance, prediction resolution, agent systems, source quorum, policy engines and public-notice contracts.

## Canonical source

`contracts/sourceroot.py`

## Canonical deployment

Deployed on StudioNet with live cross-contract proof completed.

Canonical deployment evidence:

- Source commit: `ca8a511bf946ca4c226a891660a06d77b36ecd14`
- Source code SHA-256 external release checksum: `6133FCB34B43FCCD2032E9C7CCA964C4A5055A0B676059EF581E23C32FDCF8A7`
- StudioNet address: `0x6eBE7042EbD129EAB6E4972e6716F3C973F9b286`
- Deployment transaction: recorded in the CLI deployment receipt; hash was not retained by the command output capture
- Root-resolution transaction: `0x135a7d6daa3f591286efafac1a05adaa7b74a35059f896201c81cb3e3b6571c8`
- Child-resolution transaction: `0x09676233e759e0b8e2b1dfd0c696d0c5c587372f04d27b78560e1b1d7619bbce`
- Consumer deployment: `0xc472ab3670702948eb96446fa21cd3b9c9d819b43c6174f21d7bfa70a732498f`
- Successful consumer transaction: `0xac71d5171af45e5e1e23c2a46e2bde93b18d0e07de4813ee86e2246aabb307aa`
- Parent revocation/revalidation transaction: `0x515411954730eab20bf3b73b6789d40effa3e17f96e6166403b7adb544c7b810`
- Expected consumer rejection proof: `0x40ed8a3d575cbe0d36468ccf3ab300d57b39aefea835aa87376d978556c73422`
