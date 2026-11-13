import base64
import hashlib
import json
import math
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from filelock import FileLock

PROTOCOL_VERSION = "treaty-lattice-audit/2.1-hardened"
MAX_NODE_ID_LENGTH = 64
MAX_IMPACTS = 10_000
MAX_ABS_IMPACT = 1_000_000_000_000.0
MAX_PAYLOAD_BYTES = 1_000_000
DIGEST_PREFIX = "sha3-256:"
DIGEST_RE = re.compile(r"^sha3-256:[0-9a-f]{64}$")


def canonical_json(value: Any) -> str:
    """Python-specific deterministic JSON; not an RFC 8785 implementation."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def normalize_timestamp(value: Optional[str] = None) -> str:
    if value is None:
        parsed = datetime.now(timezone.utc)
    else:
        if not isinstance(value, str) or "T" not in value:
            raise ValueError("timestamp must be an ISO-8601 datetime string")
        try:
            text = value[:-1] + "+00:00" if value.endswith("Z") else value
            parsed = datetime.fromisoformat(text)
        except ValueError as exc:
            raise ValueError("timestamp must be a valid ISO-8601 datetime") from exc
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError("timestamp must include a timezone")
        if parsed.utcoffset().total_seconds() != 0:
            raise ValueError("timestamp must be UTC")
    return parsed.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _validate_json_value(value: Any, path: str = "payload") -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{path} contains a non-finite number")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_json_value(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError(f"{path} object keys must be strings")
            _validate_json_value(item, f"{path}.{key}")
        return
    raise ValueError(f"{path} contains a non-JSON value")


def _validate_impacts(values: List[float], field: str) -> List[float]:
    if not isinstance(values, list):
        raise ValueError(f"{field} must be a list")
    if len(values) > MAX_IMPACTS:
        raise ValueError(f"{field} exceeds the maximum item count")
    normalized = []
    for index, value in enumerate(values):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{field}[{index}] must be a number")
        try:
            number = float(value)
        except (OverflowError, ValueError) as exc:
            raise ValueError(f"{field}[{index}] cannot be represented") from exc
        if not math.isfinite(number):
            raise ValueError(f"{field}[{index}] must be finite")
        if abs(number) > MAX_ABS_IMPACT:
            raise ValueError(f"{field}[{index}] exceeds the permitted magnitude")
        if number < 0:
            raise ValueError(f"{field}[{index}] must be non-negative")
        normalized.append(number)
    return normalized


class TreatyLatticeAuditor:
    """Build and sign hash-bound audit receipts using an explicitly provisioned key."""
    def __init__(self, node_id: str, private_key: ed25519.Ed25519PrivateKey):
        if not isinstance(node_id, str) or not node_id.strip() or len(node_id) > MAX_NODE_ID_LENGTH:
            raise ValueError(f"node_id must be non-empty and at most {MAX_NODE_ID_LENGTH} characters")
        if not isinstance(private_key, ed25519.Ed25519PrivateKey):
            raise TypeError("private_key must be an Ed25519PrivateKey")
        self.node_id = node_id
        self.private_key = private_key
        self.public_key = private_key.public_key()
        self.public_key_hex = self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        ).hex()

    @staticmethod
    def evaluate_impact(positive_impacts: List[float], negative_impacts: List[float]) -> Tuple[float, bool]:
        positives = _validate_impacts(positive_impacts, "positive_impacts")
        negatives = _validate_impacts(negative_impacts, "negative_impacts")
        try:
            positive_sum = math.fsum(positives)
            negative_sum = math.fsum(negatives)
            net_delta = positive_sum - negative_sum
        except (OverflowError, ValueError) as exc:
            raise ValueError("impact calculation failed") from exc
        if not all(math.isfinite(x) for x in (positive_sum, negative_sum, net_delta)):
            raise ValueError("impact calculation produced a non-finite result")
        return net_delta, net_delta > 0.0

    def generate_record(self, payload: Dict[str, Any], positive_impacts: List[float], negative_impacts: List[float], *, timestamp: Optional[str] = None, previous_digest: Optional[str] = None) -> Dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError("payload must be an object")
        _validate_json_value(payload)
        if len(canonical_json(payload).encode("utf-8")) > MAX_PAYLOAD_BYTES:
            raise ValueError("payload exceeds the maximum serialized size")
        if previous_digest is not None and not DIGEST_RE.fullmatch(previous_digest):
            raise ValueError("previous_digest must be a valid sha3-256 digest")
        positives = _validate_impacts(positive_impacts, "positive_impacts")
        negatives = _validate_impacts(negative_impacts, "negative_impacts")
        net_delta, gate_passed = self.evaluate_impact(positives, negatives)
        record = {
            "protocol_version": PROTOCOL_VERSION,
            "node_id": self.node_id,
            "public_key": self.public_key_hex,
            "timestamp": normalize_timestamp(timestamp),
            "previous_digest": previous_digest,
            "payload": payload,
            "objective_evaluation": {
                "positive_sum": math.fsum(positives),
                "negative_sum": math.fsum(negatives),
                "net_delta": net_delta,
                "gate_passed": gate_passed,
            },
            "decision": "ACCEPTED" if gate_passed else "REJECTED_NET_NON_POSITIVE",
        }
        record_bytes = canonical_json(record).encode("utf-8")
        digest = DIGEST_PREFIX + hashlib.sha3_256(record_bytes).hexdigest()
        signature = base64.b64encode(self.private_key.sign(record_bytes)).decode("ascii")
        return {"record": record, "digest": digest, "signature": signature}


def verify_receipt(envelope: Dict[str, Any], trusted_public_key: ed25519.Ed25519PublicKey, *, expected_node_id: Optional[str] = None) -> bool:
    try:
        if not isinstance(envelope, dict) or not isinstance(trusted_public_key, ed25519.Ed25519PublicKey):
            return False
        record, digest, signature_b64 = envelope.get("record"), envelope.get("digest"), envelope.get("signature")
        if not isinstance(record, dict) or not isinstance(digest, str) or not isinstance(signature_b64, str):
            return False
        if not DIGEST_RE.fullmatch(digest):
            return False
        if expected_node_id is not None and record.get("node_id") != expected_node_id:
            return False
        record_bytes = canonical_json(record).encode("utf-8")
        if digest != DIGEST_PREFIX + hashlib.sha3_256(record_bytes).hexdigest():
            return False
        embedded = bytes.fromhex(record["public_key"])
        trusted = trusted_public_key.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        if embedded != trusted:
            return False
        signature = base64.b64decode(signature_b64, validate=True)
        trusted_public_key.verify(signature, record_bytes)
        return True
    except (KeyError, TypeError, ValueError, OverflowError, InvalidSignature):
        return False


def verify_chain(envelopes: List[Dict[str, Any]], trusted_public_key: ed25519.Ed25519PublicKey, *, expected_node_id: Optional[str] = None) -> bool:
    previous_digest = None
    for envelope in envelopes:
        if not verify_receipt(envelope, trusted_public_key, expected_node_id=expected_node_id):
            return False
        if envelope["record"].get("previous_digest") != previous_digest:
            return False
        previous_digest = envelope["digest"]
    return True


class AppendOnlyFileStore:
    """Locked NDJSON append log. This is not OS-enforced WORM storage."""
    def __init__(self, filepath: str, trusted_public_key: ed25519.Ed25519PublicKey, *, expected_node_id: Optional[str] = None):
        self.filepath = Path(filepath)
        self.lock_path = Path(str(self.filepath) + ".lock")
        self.trusted_public_key = trusted_public_key
        self.expected_node_id = expected_node_id
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with FileLock(str(self.lock_path), timeout=10):
            if not self.filepath.exists():
                fd = os.open(self.filepath, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                os.close(fd)
            self._load_and_verify_all()

    def _load_and_verify_all(self) -> List[Dict[str, Any]]:
        if not self.filepath.exists() or self.filepath.stat().st_size == 0:
            return []
        envelopes = []
        with self.filepath.open("r", encoding="utf-8") as stream:
            for line_no, line in enumerate(stream, 1):
                if not line.endswith("\n"):
                    raise ValueError(f"Incomplete ledger entry at line {line_no}")
                try:
                    envelopes.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Corrupted ledger entry at line {line_no}") from exc
        if not verify_chain(envelopes, self.trusted_public_key, expected_node_id=self.expected_node_id):
            raise ValueError("Ledger integrity check failed: signature, digest, or chain link is invalid")
        return envelopes

    def load_all(self) -> List[Dict[str, Any]]:
        with FileLock(str(self.lock_path), timeout=10):
            return self._load_and_verify_all()

    def append(self, envelope: Dict[str, Any]) -> None:
        with FileLock(str(self.lock_path), timeout=10):
            if not verify_receipt(envelope, self.trusted_public_key, expected_node_id=self.expected_node_id):
                raise ValueError("Cannot append an unverified receipt")
            existing = self._load_and_verify_all()
            expected_previous = existing[-1]["digest"] if existing else None
            if envelope["record"].get("previous_digest") != expected_previous:
                raise ValueError("Chain link mismatch: previous_digest does not match ledger tail")
            encoded = (canonical_json(envelope) + "\n").encode("utf-8")
            fd = os.open(self.filepath, os.O_WRONLY | os.O_APPEND)
            try:
                with os.fdopen(fd, "ab", closefd=False) as stream:
                    stream.write(encoded)
                    stream.flush()
                    os.fsync(stream.fileno())
            finally:
                os.close(fd)
