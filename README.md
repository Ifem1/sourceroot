# SourceRoot

**Consensus-backed source-authority infrastructure for GenLayer Intelligent Contracts.**

SourceRoot answers a question that sits *before* ordinary oracle or evidence logic:

> Is this public source actually authorised for the specific kind of information another contract wants to rely on?

It is a **standalone reusable Intelligent Contract with no frontend**. The primary artifact is `contracts/sourceroot.py`. `examples/authoritative_notice_gate.py` is deliberately tiny and exists only to prove that another Intelligent Contract can consume SourceRoot's authority decision on-chain.

## Why this primitive exists

A validator set can agree perfectly about what a page says and still be relying on the wrong page.

Common failure modes include:

- a convincing unofficial status page;
- an abandoned mirror that still ranks well in search;
- a documentation host that is official for docs but not for security notices;
- a delegated source whose mandate is narrower than a consumer assumes;
- a once-authorised source that has been explicitly revoked or superseded;
- a downstream contract that keeps using an old authority receipt after revalidation changed it.

Corroboration is not authority. Five websites repeating the same statement do not become the canonical regulator, protocol, company, DAO, project owner, or service operator.

SourceRoot therefore models **authority as a bounded, scope-attenuating lineage**.

```text
Declared/evidenced canonical anchor
              |
              | ROOT
              v
       official source
        /           \
DELEGATED_FOR     MIRROR_OF
      /               \
security source     status mirror
```

## What SourceRoot proves — and what it does not

`is_authoritative(...) == true` means:

1. the consumer pinned the intended entity definition;
2. the source belongs to that entity's recorded authority graph;
3. every node in the lineage is still active;
4. every node's latest consensus verdict is `CONFIRMED`;
5. the requested scope is contained within every grant in the lineage; and
6. an optional current certificate pin matches.

It **does not mean the content published by that source is true**. SourceRoot proves a public authority relationship, not factual correctness. A downstream oracle may still need to adjudicate the source's substantive claim.

The initial canonical URL is also an explicit trust boundary. SourceRoot does not magically discover identity from the internet. Instead, it makes the trust anchor visible, immutable after sealing, hash-pinned, and auditable. From that anchor downward, delegation must be positively established by validator consensus and can only narrow scope.

## Protocol design

### 1. Define an entity and its authority vocabulary

The creator registers a canonical entity URL and a bounded set of scope definitions:

```text
SERVICE_STATUS
SECURITY
LEGAL_NOTICES
GOVERNANCE
DOCUMENTATION
...
```

Scopes are assigned deterministic bits. The entity is then sealed, creating an immutable `definition_hash`.

This is intentional: the LLM never decides whether `SECURITY` is a subset of `SERVICE_STATUS`. Scope inheritance is enforced by deterministic bit arithmetic.

### 2. Establish the root

The creator proposes a root source and a scope mask. Validators independently fetch:

- the sealed canonical entity URL; and
- the candidate source URL.

The root is confirmed only when the canonical anchor affirmatively establishes that the candidate is official for **every requested scope**.

Brand similarity, domain similarity, self-assertion, page design, and repeated wording are explicitly insufficient.

### 3. Build narrower delegations

An active parent may have children with one of three relations:

- `OFFICIAL_FOR`
- `DELEGATED_FOR`
- `MIRROR_OF`

A child can never expand authority:

```text
child_scope_mask & ~parent_scope_mask == 0
```

The maximum lineage depth is eight nodes. Parent pointers are immutable, which makes cycles impossible by construction.

### 4. Revalidate

Any active source can be revalidated against its current anchor.

Consensus outcomes are:

- `CONFIRMED`
- `REVOKED`
- `SUPERSEDED`
- `AMBIGUOUS`
- `UNAVAILABLE`

Two epistemic rules are important:

- disappearance from a page is **not** treated as revocation;
- staleness alone is **not** treated as supersession.

Both terminal states require affirmative public evidence.

`AMBIGUOUS` and `UNAVAILABLE` fail closed for consumers without destroying history. A later confirmed revalidation can recover the source. `REVOKED` and `SUPERSEDED` are terminal for that node.

Because descendant authority is evaluated through the complete parent chain, revoking a parent automatically makes every descendant ineffective without rewriting each child record.

## Consensus model

SourceRoot uses `gl.vm.run_nondet` with a custom validator.

The leader:

1. independently renders the anchor and candidate pages;
2. treats both pages as hostile data;
3. asks the LLM for one bounded authority verdict;
4. requires grounded verbatim anchor evidence for material verdicts.

Each validator independently repeats the fetch and authority judgement. It rejects the leader when:

- its own verdict differs;
- the leader uses a verdict that is invalid for the current mode;
- required anchor evidence is empty;
- the leader's evidence is not present in the validator's independently fetched page; or
- the leader supplies evidence for an ambiguous/unavailable result.

Only the bounded decision fields determine consensus. Free-form rationale is stored for auditability but is not trusted as the decision itself.

## Persistent commitments

SourceRoot exposes three distinct commitments:

- `definition_hash`: immutable source definition — entity, URL, parent, relation and scope mask;
- `lineage_hash`: commits the source to the complete authority ancestry;
- `certificate_hash`: commits the latest consensus outcome and grounded evidence.

Consumers can pin both the entity definition and the latest authority certificate to prevent silent policy substitution or stale-receipt reuse.

## Cross-contract interface

```python
@gl.contract_interface
class ISourceRoot:
    class View:
        def is_authoritative(
            self,
            entity_id: u256,
            source_id: u256,
            required_scope_mask: u64,
            expected_entity_hash: str,
            expected_certificate_hash: str,
        ) -> bool: ...

        def authority_certificate(self, source_id: u256) -> str: ...
```

A consumer does not need to understand SourceRoot's prompts or review history. It can ask one deterministic question and pin the exact authority state it expects.

See `examples/authoritative_notice_gate.py` for a complete minimal consumer contract.

## Public API

### Writes

- `create_entity(name, canonical_url)`
- `add_scope(entity_id, name, description)`
- `seal_entity(entity_id)`
- `cancel_entity(entity_id)`
- `propose_root(entity_id, label, source_url, scope_mask)`
- `propose_source(parent_source_id, relation, label, source_url, scope_mask)`
- `resolve_source(source_id)`
- `revalidate_source(source_id)`
- `cancel_pending_source(source_id)`

### Views

- `get_entity(entity_id)`
- `get_scope_dictionary(entity_id)`
- `get_source(source_id)`
- `get_review(review_id)`
- `get_chain(source_id)`
- `get_source_id(entity_id, url)`
- `is_authoritative(...)`
- `authority_certificate(source_id)`

## Status model

### Entity

```text
DRAFT -> SEALED -> ACTIVE
  \        \
   +-------> CANCELLED
```

An entity becomes `ACTIVE` only when its root source reaches consensus `CONFIRMED`.

### Source lifecycle

```text
PENDING -> ACTIVE
   |         | \
   |         |  +-> REVOKED
   |         +----> SUPERSEDED
   +-> REJECTED
   +-> CANCELLED
```

A pending `AMBIGUOUS` or `UNAVAILABLE` resolution remains pending and can be retried.

## Security properties

- HTTPS-only public URLs.
- Local/private/ambiguous host forms are rejected before web access.
- Entity, source labels and scope definitions reject obvious instruction injection.
- Fetched pages are explicitly treated as hostile data in the authority prompt.
- Validators independently re-fetch instead of checking leader output shape only.
- Material verdicts require grounded evidence.
- Scope expansion is impossible by deterministic mask enforcement.
- Authority depth is bounded.
- Parent pointers are immutable; cycles cannot be introduced later.
- Consumers can pin entity and certificate hashes.
- Ambiguous/unavailable revalidation fails closed.
- Revoked/superseded ancestors invalidate descendants at read time.

See `docs/THREAT_MODEL.md` for the complete threat analysis.

## Tests

The repository includes:

- 30 direct-mode protocol/adversarial scenarios;
- dependency-free static invariants;
- pickling validation in Direct Mode;
- a reviewer-facing preflight script;
- CI for AST/preflight, static tests, Direct Mode and GenVM lint.

Direct Mode covers, among other cases:

- forged `CONFIRMED` leader result;
- forged evidence not present on the independent validator fetch;
- scope expansion;
- duplicate authority URL;
- stale certificate pins;
- explicit revocation;
- explicit supersession;
- descendant invalidation;
- ambiguity followed by safe recovery;
- unsafe/private URL forms;
- prompt injection in scope definitions;
- unauthorised mutation attempts.

Run:

```bash
python scripts/preflight.py
pytest tests/static -q
# after installing requirements-test.txt
gltest tests/direct -v -s
```

## StudioNet deployment

The repository intentionally contains **no private key or password material**.

Windows PowerShell:

```powershell
./scripts/deploy_studionet.ps1
```

Bash:

```bash
./scripts/deploy_studionet.sh
```

After SourceRoot is deployed, deploy `examples/authoritative_notice_gate.py` with the SourceRoot address as its constructor argument and execute the lifecycle in `docs/LIVE_PROOF.md`.

## Reproducible public demo fixtures

After this repository is pushed to `Ifem1/sourceroot`, these files become stable public web evidence suitable for a deterministic StudioNet demonstration:

- `fixtures/live/canonical.txt`
- `fixtures/live/status.txt`
- `fixtures/live/security.txt`
- `fixtures/live/mirror.txt`

The intended raw URLs are documented in `docs/LIVE_PROOF.md`.

The fixtures demonstrate the protocol mechanics. For the final reviewer submission, also include at least one third-party real-world authority relationship if a sufficiently explicit, stable public delegation can be found.

## Repository scope

This is not an application and there is **no frontend**. The example consumer is intentionally minimal and does not turn SourceRoot into a product flow.

The reusable primitive is the authority graph and the consumer-safe contract interface.

## Licence

MIT.
