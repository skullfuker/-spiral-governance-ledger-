"""
Sovereign OS Governance Lattice - QR Code Audit Trail Generator
Generates cryptographically-anchored, scannable QR codes for offline verification of chain blocks.
"""

import json
import qrcode
import hashlib
import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional


def calculate_sha3_256(data: str) -> str:
    """Computes SHA-3/256 cryptographic digest for WORM anchoring."""
    digest = hashlib.sha3_256(data.encode("utf-8")).hexdigest()
    return "sha3:" + digest


def generate_block_audit_qr(
    block: Dict[str, Any],
    output_path: str = "output_qr.png",
    include_verification_url: bool = True,
    verification_endpoint: str = "https://governance.lattice.local/verify"
) -> str:
    """
    Generates a scannable QR code containing block height, Merkle root, 
    WORM anchor reference, and auditor roles for offline verification.
    
    Args:
        block: Dictionary containing the sovereign lattice block
        output_path: File path where the QR code PNG will be saved
        include_verification_url: Whether to include a verification endpoint URL
        verification_endpoint: Base URL for chain verification (default: local governance service)
    
    Returns:
        Path to the generated QR code image
    """
    # Extract block metadata
    block_height = block.get("block_height", 0)
    merkle_root = block.get("merkle_root", "0x0")
    epoch_id = block.get("epoch_id", "UNKNOWN")
    sovereign_zone = block.get("sovereign_zone", "ZONE-UNKNOWN")
    timestamp = block.get("timestamp_utc", datetime.now(timezone.utc).isoformat())
    auditor_sigs = block.get("auditor_signatures", [])
    receipts = block.get("receipts", [])
    
    # Construct the audit payload (compact, QR-friendly)
    audit_payload = {
        "sovereign_zone": sovereign_zone,
        "block_height": block_height,
        "merkle_root": merkle_root,
        "epoch_id": epoch_id,
        "signatories_count": len(auditor_sigs),
        "signatories_roles": [sig.get("role", "UNKNOWN") for sig in auditor_sigs],
        "receipt_count": len(receipts),
        "timestamp_utc": timestamp,
        "factual_data": True,
        "verification_url": f"{verification_endpoint}?block={block_height}&root={merkle_root}" if include_verification_url else None
    }
    
    # Serialize payload into compact JSON for QR encoding
    qr_data = json.dumps(audit_payload, sort_keys=True, separators=(',', ':'))
    
    # Compute cryptographic integrity hash of the QR data itself
    qr_integrity_hash = calculate_sha3_256(qr_data)
    
    # Generate QR code with error correction enabled for robustness
    qr = qrcode.QRCode(
        version=1,  # Auto-scale if needed
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create and save QR image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    
    print(f"✓ QR Code generated: {output_path}")
    print(f"  Block Height: {block_height}")
    print(f"  Merkle Root: {merkle_root}")
    print(f"  Epoch ID: {epoch_id}")
    print(f"  QR Integrity Hash: {qr_integrity_hash}")
    print(f"  Signatories: {len(auditor_sigs)} ({', '.join([s.get('role', 'UNKNOWN') for s in auditor_sigs])})")
    
    return output_path


def generate_chain_of_qr_trail(
    chain: list,
    output_dir: str = "qr_audit_trail",
    verification_endpoint: str = "https://governance.lattice.local/verify"
) -> Dict[str, str]:
    """
    Generates a complete audit trail of QR codes for all blocks in the chain.
    Each QR represents a point-in-time verification snapshot.
    
    Args:
        chain: List of blocks from the sovereign lattice
        output_dir: Directory to store all QR code images
        verification_endpoint: Base URL for verification
    
    Returns:
        Dictionary mapping block heights to QR file paths
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    qr_map = {}
    
    for i, block in enumerate(chain):
        block_height = block.get("block_height", i)
        qr_filename = os.path.join(output_dir, f"block_{block_height:04d}_qr.png")
        
        generate_block_audit_qr(
            block=block,
            output_path=qr_filename,
            include_verification_url=True,
            verification_endpoint=verification_endpoint
        )
        
        qr_map[str(block_height)] = qr_filename
        print(f"  Generated QR for block {block_height}")
    
    # Create an index file mapping block heights to QR paths
    index_path = os.path.join(output_dir, "qr_index.json")
    with open(index_path, "w") as f:
        json.dump(qr_map, f, indent=2)
    
    print(f"\n✓ QR audit trail complete: {len(qr_map)} codes in {output_dir}/")
    print(f"  Index file: {index_path}")
    
    return qr_map


def generate_qr_verification_report(
    qr_index: Dict[str, str],
    chain: list,
    report_path: str = "qr_verification_report.json"
) -> str:
    """
    Generates a comprehensive verification report linking QR codes to chain blocks.
    Useful for auditing and compliance documentation.
    
    Args:
        qr_index: Dictionary from generate_chain_of_qr_trail()
        chain: The sovereign lattice chain
        report_path: Output path for the JSON report
    
    Returns:
        Path to the generated report
    """
    report = {
        "report_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_blocks": len(chain),
        "total_qr_codes": len(qr_index),
        "blocks": []
    }
    
    for block in chain:
        block_height = str(block.get("block_height", 0))
        block_entry = {
            "block_height": int(block_height),
            "merkle_root": block.get("merkle_root"),
            "epoch_id": block.get("epoch_id"),
            "timestamp_utc": block.get("timestamp_utc"),
            "signatories_count": len(block.get("auditor_signatures", [])),
            "qr_code_path": qr_index.get(block_height),
            "receipt_count": len(block.get("receipts", []))
        }
        report["blocks"].append(block_entry)
    
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"✓ Verification report generated: {report_path}")
    
    return report_path


def embed_qr_into_html_dashboard(
    qr_path: str,
    block_height: int,
    merkle_root: str,
    epoch_id: str,
    output_html: str = "qr_dashboard.html"
) -> str:
    """
    Embeds a QR code image into an interactive HTML dashboard for real-time verification.
    
    Args:
        qr_path: Path to the generated QR code PNG
        block_height: Block height for display
        merkle_root: Merkle root hash for display
        epoch_id: Epoch identifier
        output_html: Output HTML file path
    
    Returns:
        Path to the generated HTML file
    """
    # Convert QR image to base64 for embedding
    import base64
    
    with open(qr_path, "rb") as qr_file:
        qr_base64 = base64.b64encode(qr_file.read()).decode('utf-8')
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Sovereign Lattice QR Verification - Block {block_height}</title>
        <style>
            :root {{ background-color: #0b0f19; color: #f3f4f6; font-family: system-ui, -apple-system, sans-serif; }}
            body {{ margin: 0; padding: 2rem; }}
            .container {{ max-width: 600px; margin: 0 auto; }}
            h1 {{ color: #38bdf8; text-align: center; }}
            .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 2rem; text-align: center; }}
            .qr-image {{ max-width: 400px; margin: 1.5rem auto; }}
            .qr-image img {{ width: 100%; border: 2px solid #38bdf8; border-radius: 8px; }}
            .block-info {{ text-align: left; margin-top: 1.5rem; }}
            .block-info p {{ margin: 0.5rem 0; font-size: 0.9rem; }}
            .label {{ color: #94a3b8; font-weight: bold; }}
            .value {{ color: #e0f2fe; word-break: break-all; font-family: monospace; font-size: 0.85rem; }}
            .timestamp {{ color: #4ade80; font-size: 0.9rem; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ Sovereign Lattice QR Verification</h1>
            <div class="card">
                <div class="qr-image">
                    <img src="data:image/png;base64,{qr_base64}" alt="QR Code">
                </div>
                <div class="block-info">
                    <p><span class="label">Block Height:</span> <span class="value">{block_height}</span></p>
                    <p><span class="label">Merkle Root:</span> <span class="value">{merkle_root}</span></p>
                    <p><span class="label">Epoch ID:</span> <span class="value">{epoch_id}</span></p>
                    <p><span class="label">Generated:</span> <span class="timestamp">{datetime.now(timezone.utc).isoformat()}</span></p>
                    <p style="margin-top: 1.5rem; font-size: 0.8rem; color: #64748b;">
                        Scan this QR code with any device to verify the block's integrity and audit trail.
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(output_html, "w") as f:
        f.write(html_content)
    
    print(f"✓ QR dashboard generated: {output_html}")
    
    return output_html


if __name__ == "__main__":
    # Example: Generate QR codes for sample blocks
    sample_chain = [
        {
            "block_height": 0,
            "sovereign_zone": "ZONE-ALPHA-STELLAR",
            "merkle_root": "sha3:0000000000000000000000000000000000000000000000000000000000000000",
            "epoch_id": "EPOCH-SOVEREIGN-GENESIS",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "auditor_signatures": [
                {"role": "SUPREME_TRIBUNAL", "signer": "did:glc:sovereign_genesis"},
            ],
            "receipts": []
        },
        {
            "block_height": 1,
            "sovereign_zone": "ZONE-ALPHA-STELLAR",
            "merkle_root": "sha3:abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx1234yzab5678cdef9012",
            "epoch_id": "EPOCH-377.0",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "auditor_signatures": [
                {"role": "SUPREME_TRIBUNAL", "signer": "did:glc:sov01"},
                {"role": "SOVEREIGN_CEA", "signer": "did:glc:sov02"},
                {"role": "ECO_COUNCIL", "signer": "did:glc:sov03"},
            ],
            "receipts": [{"event_id": "evt-test-001"}]
        }
    ]
    
    print("=" * 70)
    print("SOVEREIGN OS QR AUDIT TRAIL GENERATOR")
    print("=" * 70)
    print()
    
    # Generate individual QR codes
    print("1. Generating individual block QR codes...")
    for block in sample_chain:
        generate_block_audit_qr(block, f"block_{block['block_height']}_qr.png")
        print()
    
    # Generate complete audit trail
    print("2. Generating complete chain audit trail...")
    qr_map = generate_chain_of_qr_trail(sample_chain)
    print()
    
    # Generate verification report
    print("3. Generating verification report...")
    report_path = generate_qr_verification_report(qr_map, sample_chain)
    print()
    
    # Embed QR into HTML dashboard
    print("4. Embedding QR into HTML dashboard...")
    html_path = embed_qr_into_html_dashboard(
        qr_path="block_1_qr.png",
        block_height=1,
        merkle_root=sample_chain[1]["merkle_root"],
        epoch_id=sample_chain[1]["epoch_id"]
    )
    
    print()
    print("=" * 70)
    print("✓ QR audit trail generation complete")
    print("=" * 70)
