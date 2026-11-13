from lattice_ledger import initialize_lattice_update, validate_chain_integrity

def test_create_and_validate_linked_blocks():
    genesis_hash = "0" * 64
    first = initialize_lattice_update({"event": "first"}, genesis_hash)
    second = initialize_lattice_update(
        {"event": "second"}, first["current_hash"]
    )

    assert validate_chain_integrity([first, second]) == (True, None)

def test_tampered_block_fails_validation():
    block = initialize_lattice_update({"event": "original"}, "0" * 64)
    block["payload"]["event"] = "tampered"

    valid, error = validate_chain_integrity([block])

    assert not valid
    assert "hash mismatch" in error
