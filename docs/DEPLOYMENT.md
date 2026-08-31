# Canonical Deployment Record

Status: **NOT YET DEPLOYED**

Do not invent or pre-fill transaction evidence.

## Source freeze

- Repository: `https://github.com/Ifem1/sourceroot`
- Canonical contract: `contracts/sourceroot.py`
- Source commit: `TBD`
- External SHA-256 checksum: `TBD`
- GenVM dependency: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

## SourceRoot

- Network: StudioNet
- Address: `TBD`
- Deployment transaction: `TBD`
- Explorer: `TBD`

## Authority lifecycle

- Entity creation tx: `TBD`
- Entity seal tx: `TBD`
- Root proposal tx: `TBD`
- Root resolution tx: `TBD`
- Security child proposal tx: `TBD`
- Security child resolution tx: `TBD`
- Mirror proposal tx: `TBD`
- Mirror resolution tx: `TBD`

## Consumer proof

- Consumer: `examples/authoritative_notice_gate.py`
- Consumer address: `TBD`
- Deployment tx: `TBD`
- Successful authority-gated notice tx: `TBD`
- Stored certificate: `TBD`
- Stale certificate rejection evidence: `TBD`
- Ancestor invalidation rejection evidence: `TBD`

## Validation

- `python scripts/preflight.py`: `TBD`
- `pytest tests/static -q`: `TBD`
- `gltest tests/direct -v -s`: `TBD`
- `genvm-lint check contracts/sourceroot.py`: `TBD`
- `genvm-lint check examples/authoritative_notice_gate.py`: `TBD`
