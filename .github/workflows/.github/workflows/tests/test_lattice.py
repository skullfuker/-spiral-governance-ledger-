import pytest

from lattice_ledger import initialize_lattice_update, validate_chain_integrity


GENESIS = "0" * 64


def test_create_and_validate_linked_blocks():
    first = initialize_lattice_update({"event": "first"}, GENESIS)
    second = initialize_lattice_update({"event": "second"}, first["current_hash"])

    assert len(first["current_hash"]) == 64
    assert validate_chain_integrity([first, second]) == (True, None)


def test_empty_chain_is_valid():
    assert validate_chain_integrity([]) == (True, None)


def test_invalid_previous_hash_is_rejected():
    with pytest.raises(ValueError, match="Invalid previous_hash format"):
        initialize_lattice_update({"event": "bad"}, "not-a-hash")


def test_non_serializable_payload_is_rejected():
    with pytest.raises(ValueError, match="non-JSON-serializable"):
        initialize_lattice_update({"value": object()}, GENESIS)


def test_missing_block_fields_are_rejected():
    valid, error = validate_chain_integrity([{}])

    assert not valid
    assert "missing fields" in error


def test_tampered_block_fails_hash_validation():
    block = initialize_lattice_update({"event": "original"}, GENESIS)
    block["payload"]["event"] = "tampered"

    valid, error = validate_chain_integrity([block])

    assert not valid
    assert "hash mismatch" in error


def test_non_serializable_block_is_rejected():
    block = initialize_lattice_update({"event": "original"}, GENESIS)
    block["payload"]["unexpected"] = object()

    valid, error = validate_chain_integrity([block])

    assert not valid
    assert "non-serializable data" in error


def test_broken_linkage_is_rejected():
    first = initialize_lattice_update({"event": "first"}, GENESIS)
    second = initialize_lattice_update({"event": "second"}, "1" * 64)

    valid, error = validate_chain_integrity([first, second])

    assert not valid
    assert "does not link" in error