# Architecture

## Core separation

```text
public web evidence
      |
      v
nondeterministic authority judgement
      |
      v
bounded consensus verdict
      |
      v
deterministic graph transition
      |
      v
consumer-safe view interface
```

The model judges only the semantic relation. It does not control scope inheritance, lineage, state transitions, consumer pins, or descendant validity.

## Entity commitment

An entity is created in `DRAFT` with:

- creator;
- human-readable name;
- canonical URL;
- scope vocabulary.

`seal_entity` freezes the authority surface and commits it in `definition_hash`.

## Source definition

Each source has:

- entity ID;
- canonicalized HTTPS URL;
- immutable parent source ID;
- relation type;
- deterministic scope mask;
- `definition_hash`;
- `lineage_hash`.

## Initial resolution

Legal initial verdicts:

```text
CONFIRMED
REJECTED
AMBIGUOUS
UNAVAILABLE
```

`AMBIGUOUS` and `UNAVAILABLE` remain pending and may be retried. `REJECTED` is terminal for that node.

## Revalidation

Legal revalidation verdicts:

```text
CONFIRMED
REVOKED
SUPERSEDED
AMBIGUOUS
UNAVAILABLE
```

For an active source, `AMBIGUOUS` or `UNAVAILABLE` leaves the lifecycle record intact but sets `last_verdict` so consumer reads fail closed. A subsequent `CONFIRMED` review recovers it.

`REVOKED` and `SUPERSEDED` make the node terminal.

## Effective authority

A source is effective only if every node from leaf to root satisfies:

```text
lifecycle_status == ACTIVE
last_verdict == CONFIRMED
required_scope ⊆ node.scope_mask
```

No descendant write is needed when an ancestor becomes invalid.

## Consumer pinning

A downstream contract can pin:

- `expected_entity_hash` to freeze which authority vocabulary and anchor it trusts;
- `expected_certificate_hash` to freeze the exact current authority receipt.

Empty pins are allowed for intentionally looser integrations, but reviewer demos should show the pinned form.
