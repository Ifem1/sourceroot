"""Print release checksums for the canonical contract and consumer example."""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
for relative in ("contracts/sourceroot.py", "examples/authoritative_notice_gate.py"):
    path = ROOT / relative
    digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
    print(f"{digest}  {relative}")
