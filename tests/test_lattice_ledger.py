from lattice_ledger import initialize_lattice_update, validate_chain_integrity


def test_create_and_validate_linked_blocks():
    genesis_hash = "0" * 64
    first = initialize_lattice_update({"event": "first"}, genesis_hash)
    second = initialize_lattice_update(
        {"event": "second"}, first["current_hash"]
    )

    assert validate_chain_integrity([first, second]) == (True, None)


def test_empty_chain_is_valid():
    assert validate_chain_integrity([]) == (True, None)


def test_rejects_invalid_previous_hash():
    import pytest

    with pytest.raises(ValueError, match="Invalid previous_hash"):
        initialize_lattice_update({"event": "first"}, "bad-hash")


def test_rejects_non_json_serializable_payload():
    import pytest

    with pytest.raises(ValueError, match="non-JSON-serializable"):
        initialize_lattice_update({"not_json": object()}, "0" * 64)


def test_detects_tampered_payload():
    block = initialize_lattice_update({"event": "original"}, "0" * 64)
    block["payload"]["event"] = "tampered"

    valid, error = validate_chain_integrity([block])

    assert not valid
    assert "hash mismatch" in error


def test_detects_missing_block_fields():
    valid, error = validate_chain_integrity([{"payload": {}}])

    assert not valid
    assert "missing fields" in error


def test_detects_non_json_serializable_block():
    block = initialize_lattice_update({"event": "original"}, "0" * 64)
    block["payload"]["not_json"] = object()
    # Recalculate no hash: validation must report serialization error before hash mismatch.

    valid, error = validate_chain_integrity([block])

    assert not valid
    assert "non-serializable data" in error


def test_detects_broken_previous_hash_link():
    first = initialize_lattice_update({"event": "first"}, "0" * 64)
    second = initialize_lattice_update({"event": "second"}, first["current_hash"])
    second["previous_hash"] = "f" * 64
    # Recompute the second block hash so the chain-link check is reached.
    import hashlib
    import json

    body = {key: value for key, value in second.items() if key != "current_hash"}
    second["current_hash"] = hashlib.sha3_256(
        json.dumps(body, sort_keys=True).encode("utf-8")
    ).hexdigest()

    valid, error = validate_chain_integrity([first, second])

    assert not valid
    assert "does not link" in error
