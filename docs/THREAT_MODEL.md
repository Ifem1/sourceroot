# Threat Model

## Assets protected

- entity definition integrity;
- source-authority lineage;
- requested authority scope;
- consensus verdict integrity;
- grounded evidence receipts;
- downstream consumer safety.

## Trust boundaries

### Canonical anchor

The entity creator chooses the canonical anchor URL before sealing. SourceRoot does not claim to discover real-world identity automatically. Consumers should pin the entity `definition_hash` they intend to trust.

### Public web

All fetched page content is untrusted and may be stale, adversarial, prompt-injected, incomplete or temporarily unavailable.

### Leader

The leader may attempt to forge a favourable verdict or fabricated evidence. Validators independently re-fetch and re-derive the verdict.

### Entity creator

The creator controls the scope vocabulary and proposals. The creator cannot force a proposal to become active; consensus must confirm the public authority relation. After sealing, the scope vocabulary and canonical anchor cannot change.

## Threats and mitigations

| Threat | Mitigation |
|---|---|
| fake source with convincing branding | affirmative anchor evidence required; branding/domain similarity is explicitly insufficient |
| child expands delegated authority | deterministic bitmask subset check |
| malicious leader returns `CONFIRMED` | validators independently fetch and re-derive verdict |
| malicious leader fabricates evidence | material excerpt must be present on validator's independently fetched anchor/source |
| prompt injection in fetched page | prompt treats every page as hostile data; page cannot redefine task |
| prompt injection in configured labels/scopes | obvious control markers rejected before sealing/proposal |
| SSRF/private host | HTTPS-only conservative public DNS validation; private/IP-like/ambiguous forms rejected |
| cycle in authority graph | immutable parent pointer always points to an already-existing active node |
| unbounded ancestry | hard `MAX_CHAIN_DEPTH` |
| stale downstream assumption | consumer may pin current certificate hash and entity definition hash |
| parent revoked but child remains stored | `is_authoritative` walks full chain; descendant immediately becomes ineffective |
| page temporarily unavailable | fail-closed `UNAVAILABLE`; active node cannot be consumed until a later `CONFIRMED` review |
| delegation text disappears | not treated as revocation; result is ambiguous unless explicit withdrawal exists |
| old source is stale | not treated as superseded without explicit replacement evidence |
| historical receipt rewriting | review receipts are append-only |

## Non-goals

SourceRoot does not:

- prove the factual truth of content published by an authorised source;
- guarantee that a declared canonical anchor corresponds to a legal entity without an external trust decision by the consumer;
- discover every possible official source on the internet;
- replace domain/DNS security;
- provide legal advice;
- make probabilistic confidence percentages look deterministic.
