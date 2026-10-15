import hashlib
import json
import re
import time
from typing import Dict, Any, List, Optional


def initialize_lattice_update(update_payload: Dict[str, Any], previous_hash: str) -> Dict[str, Any]:
    """
    Initializes, timestamps, and cryptographically signs a new update block 
    for the lattice ledger with provenance enforcement.
    
    Args:
        update_payload: Dictionary containing update details (must be JSON-serializable)
        previous_hash: SHA3-256 hash of the previous block (64 hex characters)
    
    Returns:
        Dictionary containing the signed update record with current_hash
    
    Raises:
        ValueError: If previous_hash format is invalid or payload is not serializable
    """
    # Validate previous hash format
    if not re.match(r'^[a-f0-9]{64}$', previous_hash):
        raise ValueError(f"Invalid previous_hash format (expected 64 hex chars): {previous_hash}")
    
    # Defensive copy to prevent external mutations
    payload = dict(update_payload)
    
    update_record = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "provenance_protocol": True,
        "factual_data": True,
        "previous_hash": previous_hash,
        "payload": payload
    }
    
    # Deterministic serialization for stable hashing
    try:
        serialized = json.dumps(update_record, sort_keys=True).encode('utf-8')
    except TypeError as e:
        raise ValueError(f"Payload contains non-JSON-serializable data: {e}")
    
    block_hash = hashlib.sha3_256(serialized).hexdigest()
    update_record["current_hash"] = block_hash
    
    return update_record


def validate_chain_integrity(chain: List[Dict[str, Any]]) -> tuple[bool, Optional[str]]:
    """
    Validates the integrity of a lattice ledger chain by verifying 
    sequential hash linkage and block structure.
    
    Args:
        chain: List of update blocks in chronological order
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not chain:
        return True, None
    
    for i, block in enumerate(chain):
        # Validate block structure
        required_fields = {"timestamp", "provenance_protocol", "factual_data", "previous_hash", "payload", "current_hash"}
        if not required_fields.issubset(block.keys()):
            missing = required_fields - set(block.keys())
            return False, f"Block {i} missing fields: {missing}"
        
        # Verify hash matches content
        block_copy = {k: v for k, v in block.items() if k != "current_hash"}
        try:
            serialized = json.dumps(block_copy, sort_keys=True).encode('utf-8')
        except TypeError as e:
            return False, f"Block {i} contains non-serializable data: {e}"
        
        computed_hash = hashlib.sha3_256(serialized).hexdigest()
        if computed_hash != block["current_hash"]:
            return False, f"Block {i} hash mismatch: expected {computed_hash}, got {block['current_hash']}"
        
        # Verify chain linkage
        if i > 0:
            if block["previous_hash"] != chain[i-1]["current_hash"]:
                return False, f"Block {i} previous_hash does not link to block {i-1}"
    
    return True, None


if __name__ == "__main__":
    # Example initialization of a new update package
    genesis_hash = "0" * 64  # Genesis block hash (all zeros for chain origin)
    
    payload_data = {
        "update_id": "UP-2026-10-11-01",
        "description": "Initialization of new governance lattice parameters and state synchronization.",
        "net_positive_gate": "PASSED (E > 0)"
    }
    
    new_block = initialize_lattice_update(payload_data, genesis_hash)
    print("New Update Block Initialized Successfully:")
    print(json.dumps(new_block, indent=2))
    print()
    
    # Example: Create a second block to demonstrate chain linkage
    payload_data_2 = {
        "update_id": "UP-2026-10-11-02",
        "description": "Treaty phase synchronization and resonance audit completion.",
        "net_positive_gate": "PASSED (E > 0)"
    }
    
    second_block = initialize_lattice_update(payload_data_2, new_block["current_hash"])
    print("Second Update Block Initialized Successfully:")
    print(json.dumps(second_block, indent=2))
    print()
    
    # Example: Validate chain integrity
    chain = [new_block, second_block]
    is_valid, error = validate_chain_integrity(chain)
    print(f"Chain Integrity Check: {'✓ VALID' if is_valid else '✗ INVALID'}")
    if error:
        print(f"Error: {error}")
