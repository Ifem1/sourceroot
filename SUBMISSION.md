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

Current source pack contains 30 direct-mode scenarios plus static invariants. The final live deployment/transaction fields are deliberately blank until executed; no deployment evidence is fabricated.

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

Not yet deployed.

Populate only after final source commit is frozen:

- Source commit: `TBD`
- Source code Keccak/SHA-256 external release checksum: `TBD`
- StudioNet address: `TBD`
- Deployment transaction: `TBD`
- Root-resolution transaction: `TBD`
- Child-resolution transaction: `TBD`
- Consumer deployment: `TBD`
- Successful consumer transaction: `TBD`
- Parent revocation/revalidation transaction: `TBD`
- Expected consumer rejection proof: `TBD`
