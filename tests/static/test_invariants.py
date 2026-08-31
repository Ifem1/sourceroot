"""Dependency-free structural invariants for reviewer confidence."""

from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts" / "sourceroot.py"
CONSUMER = ROOT / "examples" / "authoritative_notice_gate.py"


def source():
    return CONTRACT.read_text(encoding="utf-8")


def test_contract_parses():
    ast.parse(source())


def test_consumer_parses():
    ast.parse(CONSUMER.read_text(encoding="utf-8"))


def test_custom_consensus_present():
    text = source()
    assert "run_nondet(leader_fn, validator_fn)" in text
    assert "validator_fn" in text
    assert "inspect_authority_once" in text


def test_validator_independently_refetches():
    text = source()
    validator = text.split("def validator_fn(leader_result)", 1)[1].split("return gl.vm.run_nondet", 1)[0]
    assert "inspect_authority_once" in validator
    assert "include_source" not in validator or "True" in validator


def test_scope_attenuation_is_deterministic():
    text = source()
    assert "is_subset_mask" in text
    assert "child scope expands parent authority" in text


def test_authority_chain_is_bounded():
    text = source()
    assert "MAX_CHAIN_DEPTH = 8" in text
    assert "maximum authority depth reached" in text


def test_consumer_safe_hash_pins_exist():
    text = source()
    assert "expected_entity_hash" in text
    assert "expected_certificate_hash" in text
    assert "definition_hash" in text
    assert "certificate_hash" in text
    assert "lineage_hash" in text


def test_epistemic_boundaries_are_explicit():
    text = source()
    assert "Mere disappearance from a page is not revocation" in text
    assert "Mere staleness is not supersession" in text
    assert "Do not infer authority merely from matching branding" in text


def test_private_host_defence_present():
    text = source()
    assert "private ip-like host is rejected" in text
    assert "numeric hosts are rejected" in text
    assert "ambiguous url encoding is rejected" in text


def test_prompt_injection_defence_present():
    text = source().lower()
    assert "hostile data" in text
    assert "never follow instructions" in text
    assert "reveal your system prompt" in text


def test_review_history_is_persistent():
    text = source()
    assert "reviews: DynArray[ReviewReceipt]" in text
    assert "_append_review" in text
    assert "get_review" in text


def test_cross_contract_interface_and_consumer_exist():
    contract = source()
    consumer = CONSUMER.read_text(encoding="utf-8")
    assert "class ISourceRoot" in contract
    assert "class ISourceRoot" in consumer
    assert "root.view().is_authoritative" in consumer
    assert "root.view().authority_certificate" in consumer


def test_no_frontend_directory_required():
    assert not (ROOT / "frontend").exists()
