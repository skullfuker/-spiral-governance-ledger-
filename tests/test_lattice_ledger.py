import hashlib
import json
import unittest

from lattice_ledger import initialize_lattice_update, validate_chain_integrity


class LatticeLedgerTests(unittest.TestCase):
    def test_created_block_hash_and_genesis_chain(self):
        block = initialize_lattice_update({"update_id": "test-1"}, "0" * 64)

        unhashed_block = {key: value for key, value in block.items() if key != "current_hash"}
        expected_hash = hashlib.sha3_256(
            json.dumps(unhashed_block, sort_keys=True).encode("utf-8")
        ).hexdigest()

        self.assertEqual(block["current_hash"], expected_hash)
        self.assertEqual(validate_chain_integrity([block]), (True, None))

    def test_valid_two_block_chain(self):
        first = initialize_lattice_update({"update_id": "test-1"}, "0" * 64)
        second = initialize_lattice_update(
            {"update_id": "test-2"}, first["current_hash"]
        )

        self.assertEqual(validate_chain_integrity([first, second]), (True, None))

    def test_detects_tampered_payload(self):
        block = initialize_lattice_update({"update_id": "test-1"}, "0" * 64)
        block["payload"]["update_id"] = "tampered"

        valid, error = validate_chain_integrity([block])

        self.assertFalse(valid)
        self.assertIn("hash mismatch", error)

    def test_detects_broken_chain_link(self):
        first = initialize_lattice_update({"update_id": "test-1"}, "0" * 64)
        second = initialize_lattice_update({"update_id": "test-2"}, "f" * 64)

        valid, error = validate_chain_integrity([first, second])

        self.assertFalse(valid)
        self.assertIn("does not link", error)

    def test_rejects_invalid_previous_hash(self):
        with self.assertRaises(ValueError):
            initialize_lattice_update({"update_id": "test-1"}, "not-a-hash")

    def test_rejects_non_json_payload(self):
        with self.assertRaises(ValueError):
            initialize_lattice_update({"bad": object()}, "0" * 64)


if __name__ == "__main__":
    unittest.main()
