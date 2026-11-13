import runpy
from pathlib import Path

import pytest

import lattice_ledger


GENESIS_HASH = "0" * 64


def test_initialize_lattice_update_creates_signed_block():
    payload = {"update_id": "test-1", "description": "initial update"}

    block = lattice_ledger.initialize_lattice_update(payload, GENESIS_HASH)

    assert block["previous_hash"] == GENESIS_HASH
    assert block["payload"] == payload
    assert block["provenance_protocol"] is True
    assert block["factual_data"] is True
    assert len(block["current_hash"]) == 64
    assert lattice_ledger.validate_chain_integrity([block]) == (True, None)


def test_initialize_rejects_invalid_previous_hash():
    with pytest.raises(ValueError, match="Invalid previous_hash format"):
        lattice_ledger.initialize_lattice_update({}, "not-a-hash")


def test_initialize_rejects_non_json_payload():
    with pytest.raises(ValueError, match="non-JSON-serializable"):
        lattice_ledger.initialize_lattice_update({"invalid": {1, 2}}, GENESIS_HASH)


def test_validate_empty_chain():
    assert lattice_ledger.validate_chain_integrity([]) == (True, None)


def test_validate_rejects_block_with_missing_fields():
    is_valid, error = lattice_ledger.validate_chain_integrity([{}])

    assert not is_valid
    assert "missing fields" in error


def test_validate_rejects_non_json_block_data():
    block = lattice_ledger.initialize_lattice_update({}, GENESIS_HASH)
    block["payload"] = {"invalid": {1, 2}}

    is_valid, error = lattice_ledger.validate_chain_integrity([block])

    assert not is_valid
    assert "non-serializable data" in error


def test_validate_rejects_tampered_block():
    block = lattice_ledger.initialize_lattice_update({}, GENESIS_HASH)
    block["payload"]["tampered"] = True

    is_valid, error = lattice_ledger.validate_chain_integrity([block])

    assert not is_valid
    assert "hash mismatch" in error


def test_validate_rejects_broken_chain_link():
    first = lattice_ledger.initialize_lattice_update({}, GENESIS_HASH)
    second = lattice_ledger.initialize_lattice_update({}, "1" * 64)

    is_valid, error = lattice_ledger.validate_chain_integrity([first, second])

    assert not is_valid
    assert "does not link" in error


def test_script_entrypoint(capsys):
    script_path = Path(lattice_ledger.__file__).resolve()
    runpy.run_path(str(script_path), run_name="__main__")

    output = capsys.readouterr().out
    assert "New Update Block Initialized Successfully:" in output
    assert "Second Update Block Initialized Successfully:" in output
    assert "Chain Integrity Check: ✓ VALID" in output