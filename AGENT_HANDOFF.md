# Mary / Agent Handoff

Repository target: `https://github.com/Ifem1/sourceroot`

## Objective

Finish SourceRoot as a **standalone GenLayer Intelligent Contract submission**. Do not add a frontend. Do not convert it into a product/app. The canonical submission is `contracts/sourceroot.py`; `examples/authoritative_notice_gate.py` exists only to prove real IC-to-IC composability.

## Non-negotiable architecture

Preserve these properties unless a real GenVM compatibility issue forces a narrowly documented change:

1. Custom `run_nondet_unsafe` leader/validator consensus.
2. Validators independently re-fetch anchor and candidate evidence.
3. Material verdicts require grounded anchor evidence.
4. Entity canonical URL + scope vocabulary freeze at seal time.
5. Child authority can only narrow parent scope; never expand it.
6. Parent pointers are immutable and lineage depth is bounded.
7. `definition_hash`, `lineage_hash`, and `certificate_hash` remain distinct commitments.
8. `AMBIGUOUS`/`UNAVAILABLE` fail closed but can recover on later confirmation.
9. `REVOKED`/`SUPERSEDED` are terminal for that source.
10. A bad ancestor makes every descendant ineffective at read time.
11. Consumer may pin both entity definition and current certificate.
12. `AUTHORITATIVE` must never be documented as equivalent to `TRUE`.
13. No private keys, wallet seed phrases, passwords, or secrets in the repo.
14. No frontend.

## Work sequence

### 1. Put the ZIP contents into the empty repository

Use the existing `Ifem1/sourceroot` repository. Preserve the supplied file structure.

### 2. Install current tooling and run every gate

Use Python 3.12+.

```powershell
python -m pip install -r requirements.txt
python scripts/preflight.py
python -m pytest tests/static -q
gltest tests/direct -v -s
genvm-lint check contracts/sourceroot.py
genvm-lint check examples/authoritative_notice_gate.py
```

If the current GenLayer testing/linter versions have advanced incompatibly, update only the tooling pins required for the current official SDK. Do not silently rewrite protocol semantics to make tests pass.

### 3. Fix all real runtime/linter/type issues

Treat the supplied contract as a strong implementation draft, not as automatically perfect. If GenVM rejects a construct, replace it with the closest current official GenLayer pattern while preserving the invariant being implemented.

Pay special attention to:

- storage-compatible dataclass allocation;
- `DynArray`/`TreeMap` usage;
- `Keccak256` availability;
- typed IC interface return annotations;
- event argument types;
- `gl.nondet.web.render` failure behaviour;
- Direct Mode mock patterns;
- validator error handling;
- source evidence membership checks;
- pickling/serialization.

After every fix, rerun the full gate set.

### 4. Expand Direct Mode only where a discovered bug requires regression coverage

The supplied suite has 30 scenarios. Do not pad test count with meaningless tests. Add a regression test for every substantive bug found.

Required adversarial coverage must remain:

- malicious leader `CONFIRMED` vs validator disagreement;
- fabricated evidence;
- scope expansion;
- wrong entity hash;
- stale certificate pin;
- ambiguous revalidation fail-closed/recovery;
- explicit revocation;
- explicit supersession;
- ancestor invalidation of descendants;
- unsafe/private URL forms;
- prompt injection in configured definitions;
- unauthorised graph mutation;
- duplicate source URL;
- invalid relation/scope masks.

### 5. Push a clean pre-deployment commit

Before deployment:

- ensure CI is green;
- ensure working tree is clean;
- record the exact commit SHA;
- run `python scripts/checksums.py`;
- copy the canonical contract SHA-256 into `docs/DEPLOYMENT.md`.

Do not modify `contracts/sourceroot.py` after canonical deployment. If the canonical contract changes, redeploy and update all proof evidence to the new deployment.

### 6. Deploy SourceRoot on StudioNet

Use the already-configured/unlocked GenLayer CLI account. Do not ask for or store a password/private key in the repo.

```powershell
genlayer network set studionet
genlayer account
genlayer deploy --contract contracts/sourceroot.py
```

Record the address, deployment transaction and explorer link.

### 7. Execute the complete authority lifecycle

Follow `docs/LIVE_PROOF.md` exactly.

At minimum prove on the canonical deployment:

- entity create + scopes + seal;
- root proposal + consensus confirmation;
- narrower delegated child confirmation;
- mirror confirmation;
- deterministic scope-expansion revert;
- `is_authoritative` with exact entity/certificate pins;
- one confirmed revalidation that changes the current certificate;
- old certificate pin rejection;
- current certificate acceptance.

### 8. Deploy the consumer IC and prove actual cross-contract reuse

Deploy:

```text
examples/authoritative_notice_gate.py
```

with the SourceRoot address as constructor input.

Then execute a finalized `accept_notice(...)` using an active delegated source and exact pins. Verify that the consumer stores the same certificate returned by SourceRoot.

This proof is essential. Do not leave the example as documentation-only.

### 9. Demonstrate ancestor invalidation

Use the controlled public fixture flow documented in `docs/LIVE_PROOF.md`, preserving the prior Git commit as historical evidence before modifying the mutable `main` fixture.

Obtain an explicit `REVOKED` verdict for the root, then prove:

- root authority is false;
- delegated child authority is false;
- mirror authority is false;
- the consumer rejects a new notice using the descendant.

If the controlled fixture method is awkward in GenVM, use another public immutable + versioned evidence method that still produces a real web fetch and a transparent transition. Do not use a mocked StudioNet result.

### 10. Add one strong third-party real-world authority example if stable evidence exists

Look for a public official page that explicitly designates another URL/source for a narrow scope. The authority must be affirmative and independently fetchable. Do not rely merely on shared domain, logo, branding, or common wording.

If no stable explicit example can be found, do not invent one. The controlled live proof is better than fabricated third-party evidence.

### 11. Final reviewer hardening

Update `docs/DEPLOYMENT.md` and `SUBMISSION.md` with only real evidence:

- final commit SHA;
- source checksum;
- canonical SourceRoot address;
- consumer address;
- all material transaction hashes;
- explorer links;
- exact test count/results;
- lint result;
- successful consumer proof;
- stale pin failure proof;
- descendant invalidation proof.

Remove every `TBD` only when there is real evidence to replace it.

### 12. Final audit before submission

Audit the repo as though you are a hostile GenLayer reviewer. Specifically ask:

- Can a leader fabricate authority without an independent validator reproducing it?
- Can a child gain a scope its parent lacks?
- Can a stale/revoked ancestor still make a descendant authoritative?
- Can a consumer accidentally accept another entity definition?
- Can a consumer accidentally reuse an old certificate?
- Can a page prompt-inject the validator?
- Can a private/local URL be fetched?
- Is any terminal conclusion being inferred from absence rather than affirmative evidence?
- Is there any unproven claim in README/SUBMISSION?
- Does the repo still clearly look like a standalone reusable primitive rather than a Project?

Fix every real issue, add regression coverage, rerun all validation and push the final clean commit.

## Definition of done

Do not call the work finished until all of the following are true:

- no frontend;
- preflight passes;
- static tests pass;
- Direct Mode passes completely;
- GenVM lint passes on both ICs;
- GitHub Actions green;
- SourceRoot has a canonical finalized StudioNet deployment;
- the authority lifecycle has real finalized transaction evidence;
- the consumer IC is deployed and actually consumes SourceRoot on-chain;
- stale certificate rejection is demonstrated;
- ancestor invalidation is demonstrated;
- deployment docs contain no fabricated evidence and no unresolved `TBD` in the final proof section;
- final source matches the deployed source commit exactly.
