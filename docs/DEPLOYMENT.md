# Canonical Deployment Record

Status: **DEPLOYED AND LIVE PROOF EXECUTED**

Do not invent or pre-fill transaction evidence.

## Source freeze

- Repository: `https://github.com/Ifem1/sourceroot`
- Canonical contract: `contracts/sourceroot.py`
- Source commit: `ca8a511bf946ca4c226a891660a06d77b36ecd14`
- External SHA-256 checksum: `6133FCB34B43FCCD2032E9C7CCA964C4A5055A0B676059EF581E23C32FDCF8A7`
- GenVM dependency: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

## SourceRoot

- Network: StudioNet
- Address: `0x6eBE7042EbD129EAB6E4972e6716F3C973F9b286`
- Deployment transaction: hash not retained by the CLI output capture; deployment receipt finalized successfully and code/schema are addressable
- Explorer: `https://genlayer-explorer.vercel.app/address/0x6eBE7042EbD129EAB6E4972e6716F3C973F9b286`

## Authority lifecycle

- Entity creation tx: `0x8da58260dac90beb48975c8fc5b2ef712a31fe8a1e0b322a62f17754aeb0d2b7`
- Entity seal tx: `0x3eedf8a69cf282cdd297c4dec6f7e04057ccfc0fba89ed96dcc2dfcc2ba0ca51`
- Root proposal tx: `0xc9c3660229dce945de2baadb2d67421adbe8093303c24e93e42dd75531193086`
- Root resolution tx: `0x135a7d6daa3f591286efafac1a05adaa7b74a35059f896201c81cb3e3b6571c8`
- Security child proposal tx: `0x402a25f2f90b998eae5abc82fc55fdb1e91e3e73b85be5ccbedb11084932e60e`
- Security child resolution tx: `0x09676233e759e0b8e2b1dfd0c696d0c5c587372f04d27b78560e1b1d7619bbce`
- Mirror proposal tx: not part of the executed proof
- Mirror resolution tx: not part of the executed proof

## Consumer proof

- Consumer: `examples/authoritative_notice_gate.py`
- Consumer address: `0x5aa7bA23C3F41f7a2bB8Fc28B568A583E4DCA3E7`
- Deployment tx: `0xc472ab3670702948eb96446fa21cd3b9c9d819b43c6174f21d7bfa70a732498f`
- Successful authority-gated notice tx: `0xac71d5171af45e5e1e23c2a46e2bde93b18d0e07de4813ee86e2246aabb307aa`
- Stored certificate: `98fb43f9da227cd56a37bc55cbfec50a86f78c8b942a3721c70601030d19fd08`
- Stale certificate rejection evidence: `0xfb2867d21c21df806fe499a48d4b9cb5eea5f5441a310e186697d8223c5b0e04`
- Ancestor invalidation rejection evidence: `0x40ed8a3d575cbe0d36468ccf3ab300d57b39aefea835aa87376d978556c73422`

## Validation

- `python scripts/preflight.py`: passed
- `pytest tests/static -q`: 14 passed
- `gltest tests/direct -v -s`: 34 passed
- `genvm-lint check contracts/sourceroot.py`: passed
- `genvm-lint check examples/authoritative_notice_gate.py`: passed
