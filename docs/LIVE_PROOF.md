# Live StudioNet Proof Plan

Do not mark the submission complete until every step below has a finalized transaction/receipt.

## Public fixture URLs after push

```text
ANCHOR
https://raw.githubusercontent.com/Ifem1/sourceroot/main/fixtures/live/canonical.txt

ROOT
https://raw.githubusercontent.com/Ifem1/sourceroot/main/fixtures/live/status.txt

SECURITY CHILD
https://raw.githubusercontent.com/Ifem1/sourceroot/main/fixtures/live/security.txt

STATUS MIRROR
https://raw.githubusercontent.com/Ifem1/sourceroot/main/fixtures/live/mirror.txt
```

These are controlled demonstration evidence, not third-party proof. Add a separate real-world public authority relationship if a stable explicit example is available.

## Phase A — freeze source

1. Run all tests and lint.
2. Commit.
3. Record the commit SHA.
4. Compute an external SHA-256 release checksum of `contracts/sourceroot.py`.
5. Do not edit the canonical contract after deployment. If it changes, redeploy.

## Phase B — deploy SourceRoot

```powershell
genlayer network set studionet
genlayer deploy --contract contracts/sourceroot.py
```

Record address and deployment transaction in `docs/DEPLOYMENT.md`.

## Phase C — establish authority graph

Create entity `SourceRoot Demo Authority` with canonical fixture URL.

Add scopes:

```text
bit 1: SERVICE_STATUS
bit 2: SECURITY
bit 4: LEGAL_NOTICES
```

Seal entity and record `definition_hash`.

Propose root `fixtures/live/status.txt` for mask `7` and resolve it. Verify:

```text
entity = ACTIVE
root = ACTIVE
last_verdict = CONFIRMED
certificate_hash != empty
```

Propose security child with relation `DELEGATED_FOR`, mask `2`, and resolve.

Propose mirror child with relation `MIRROR_OF`, mask `1`, and resolve.

## Phase D — prove deterministic scope attenuation

Attempt a child under the security source with mask `3` (`SECURITY | SERVICE_STATUS`). It must revert before consensus because the child attempts to expand parent authority.

Record the revert evidence.

## Phase E — prove live cross-contract reuse

Deploy:

```text
examples/authoritative_notice_gate.py
```

Constructor:

```text
SourceRootAddress
```

Call `accept_notice(...)` using:

- the security child;
- required mask `2`;
- exact entity definition hash;
- exact current child certificate hash.

The transaction must finalize and `get_notice_certificate(notice_id)` must equal the SourceRoot authority certificate.

This is the key composability proof.

## Phase F — prove stale pin/fail-closed behaviour

Revalidate the security child with a confirmed review. Its certificate should change because the receipt timestamp/review sequence changed.

Attempt another consumer action using the *old* certificate pin. It must fail.

Then use the current certificate pin and prove success.

## Phase G — prove ancestor invalidation

For the controlled transition demo, the entity intentionally uses the mutable `main` raw URL as its canonical anchor. Before changing that fixture, record the current Git commit and its immutable commit-pinned raw URL as historical evidence. Then update `fixtures/live/canonical.txt` so it explicitly revokes the root, commit the change, wait until the public raw `main` URL serves the new content, and call `revalidate_source(root_id)`. This makes the evidence transition transparent and reproducible without pretending the old content never existed.

After the root receives `REVOKED`, show:

```text
is_authoritative(root) == false
is_authoritative(security child) == false
is_authoritative(mirror child) == false
```

Then show `AuthoritativeNoticeGate` rejects the descendant.

## Phase H — third-party authority example

Find one explicit, stable public relationship where an official anchor clearly designates another source for a narrow scope. The wording must be affirmative enough that independent validators can reproduce it.

Avoid examples that rely only on matching domains or branding.

## Final submission evidence

Populate `docs/DEPLOYMENT.md` with:

- commit SHA;
- external source checksum;
- SourceRoot address;
- consumer address;
- deployment tx;
- root resolution tx;
- child resolution tx;
- scope-expansion revert proof;
- successful consumer tx;
- stale-pin rejection proof;
- ancestor invalidation proof;
- explorer links;
- exact final test counts.
