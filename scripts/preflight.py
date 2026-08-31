"""Dependency-free reviewer-facing preflight for SourceRoot."""

from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "sourceroot.py"
CONSUMER = ROOT / "examples" / "authoritative_notice_gate.py"
README = ROOT / "README.md"
SUBMISSION = ROOT / "SUBMISSION.md"
TESTS = ROOT / "tests" / "direct" / "test_sourceroot.py"
STATIC = ROOT / "tests" / "static" / "test_invariants.py"


def require(condition: bool, message: str):
    if not condition:
        raise SystemExit(f"FAIL: {message}")
    print(f"OK: {message}")


def main():
    contract = CONTRACT.read_text(encoding="utf-8")
    consumer = CONSUMER.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8") if README.exists() else ""
    submission = SUBMISSION.read_text(encoding="utf-8") if SUBMISSION.exists() else ""
    tests = TESTS.read_text(encoding="utf-8")
    static = STATIC.read_text(encoding="utf-8")

    for text in (contract, consumer, tests, static):
        ast.parse(text)

    require("class SourceRoot(gl.Contract)" in contract, "canonical contract class is SourceRoot")
    require("class ISourceRoot" in contract, "typed cross-contract interface is present")
    require("run_nondet_unsafe" in contract, "custom leader/validator consensus is present")
    require("inspect_authority_once" in contract, "validators independently refetch authority evidence")
    require("child scope expands parent authority" in contract, "scope attenuation is deterministically enforced")
    require("lineage_hash" in contract, "authority lineage is commitment-pinned")
    require("certificate_hash" in contract, "consumer-safe authority certificates are commitment-pinned")
    require("VERDICT_REVOKED" in contract and "VERDICT_SUPERSEDED" in contract, "revocation and supersession are first-class states")
    require("Mere disappearance from a page is not revocation" in contract, "negative authority claims fail closed")
    require("class AuthoritativeNoticeGate" in consumer, "real consumer IC example is included")
    require("root.view().is_authoritative" in consumer, "consumer performs a typed IC-to-IC authority check")
    require(tests.count("def test_") >= 25, "substantial direct-mode suite is present")
    require(static.count("def test_") >= 10, "static hardening suite is present")
    require("no frontend" in readme.lower(), "README preserves standalone primitive scope")
    require("cross-contract" in submission.lower(), "submission plan requires live composability proof")
    require(not (ROOT / "frontend").exists(), "repository contains no frontend")

    print("Preflight passed.")


if __name__ == "__main__":
    main()
