#!/usr/bin/env python3
"""
Spiral Governance Lattice Ledger CLI
Command-line interface for creating and verifying cryptographic update blocks.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

from lattice_ledger import initialize_lattice_update, validate_chain_integrity


DEFAULT_LEDGER_PATH = Path("governance_ledger.json")


def load_ledger(ledger_path: Path = DEFAULT_LEDGER_PATH) -> list:
    """Load existing ledger from file, or return empty list if not found."""
    if ledger_path.exists():
        try:
            with open(ledger_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading ledger: {e}", file=sys.stderr)
            return []
    return []


def save_ledger(chain: list, ledger_path: Path = DEFAULT_LEDGER_PATH) -> bool:
    """Save ledger chain to file."""
    try:
        with open(ledger_path, 'w') as f:
            json.dump(chain, f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving ledger: {e}", file=sys.stderr)
        return False


def cmd_create(args) -> int:
    """Create a new update block and append to ledger."""
    ledger = load_ledger(args.ledger)
    
    # Determine previous hash
    if ledger:
        previous_hash = ledger[-1]["current_hash"]
    else:
        # Genesis block
        previous_hash = "0" * 64
        if not args.quiet:
            print("ℹ️  No existing ledger found. Creating genesis block.")
    
    # Prepare payload from CLI arguments
    payload = {
        "update_id": args.update_id,
        "description": args.description,
    }
    
    # Add optional fields
    if args.gate:
        payload["net_positive_gate"] = args.gate
    
    if args.metadata:
        try:
            metadata = json.loads(args.metadata)
            payload["metadata"] = metadata
        except json.JSONDecodeError as e:
            print(f"Error parsing metadata JSON: {e}", file=sys.stderr)
            return 1
    
    # Create new block
    try:
        new_block = initialize_lattice_update(payload, previous_hash)
    except ValueError as e:
        print(f"Error creating block: {e}", file=sys.stderr)
        return 1
    
    # Append to ledger
    ledger.append(new_block)
    
    # Save ledger
    if not save_ledger(ledger, args.ledger):
        return 1
    
    if not args.quiet:
        print(f"✓ Block created and appended to ledger at {args.ledger}")
        print(f"  Block hash: {new_block['current_hash']}")
        print(f"  Update ID: {new_block['payload']['update_id']}")
        print(f"  Timestamp: {new_block['timestamp']}")
    
    # Print full block if requested
    if args.verbose:
        print("\nFull block:")
        print(json.dumps(new_block, indent=2))
    
    return 0


def cmd_verify(args) -> int:
    """Verify integrity of the ledger chain."""
    ledger = load_ledger(args.ledger)
    
    if not ledger:
        print("✗ Ledger is empty", file=sys.stderr)
        return 1
    
    is_valid, error = validate_chain_integrity(ledger)
    
    if is_valid:
        if not args.quiet:
            print(f"✓ Ledger integrity verified ({len(ledger)} blocks)")
    else:
        print(f"✗ Ledger integrity check failed: {error}", file=sys.stderr)
        return 1
    
    return 0


def cmd_view(args) -> int:
    """View ledger contents."""
    ledger = load_ledger(args.ledger)
    
    if not ledger:
        print("Ledger is empty")
        return 0
    
    if args.block is not None:
        # View specific block
        if args.block < 0 or args.block >= len(ledger):
            print(f"Error: Block index {args.block} out of range (0-{len(ledger)-1})", file=sys.stderr)
            return 1
        
        block = ledger[args.block]
        print(f"Block {args.block}:")
        print(json.dumps(block, indent=2))
    else:
        # View summary of all blocks
        print(f"Ledger Summary ({len(ledger)} blocks):\n")
        for i, block in enumerate(ledger):
            print(f"  Block {i}:")
            print(f"    ID: {block['payload'].get('update_id', 'N/A')}")
            print(f"    Hash: {block['current_hash']}")
            print(f"    Timestamp: {block['timestamp']}")
            if args.verbose:
                print(f"    Description: {block['payload'].get('description', 'N/A')}")
            print()
    
    return 0


def cmd_export(args) -> int:
    """Export ledger to file."""
    ledger = load_ledger(args.ledger)
    
    if not ledger:
        print("Ledger is empty", file=sys.stderr)
        return 1
    
    try:
        with open(args.output, 'w') as f:
            json.dump(ledger, f, indent=2)
        if not args.quiet:
            print(f"✓ Ledger exported to {args.output}")
    except IOError as e:
        print(f"Error exporting ledger: {e}", file=sys.stderr)
        return 1
    
    return 0


def cmd_reset(args) -> int:
    """Reset (clear) the ledger."""
    if not args.force:
        response = input(f"Are you sure you want to clear {args.ledger}? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted")
            return 0
    
    try:
        with open(args.ledger, 'w') as f:
            json.dump([], f)
        if not args.quiet:
            print(f"✓ Ledger reset")
    except IOError as e:
        print(f"Error resetting ledger: {e}", file=sys.stderr)
        return 1
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Spiral Governance Lattice Ledger CLI - Manage cryptographic update blocks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new block
  %(prog)s create -id UP-2026-10-11-01 -desc "Initial governance sync"
  
  # Verify ledger integrity
  %(prog)s verify
  
  # View all blocks
  %(prog)s view
  
  # View specific block
  %(prog)s view --block 0
  
  # Export ledger
  %(prog)s export -o ledger_backup.json
  
  # Reset ledger (with confirmation)
  %(prog)s reset
        """
    )
    
    parser.add_argument(
        '-l', '--ledger',
        type=Path,
        default=DEFAULT_LEDGER_PATH,
        help=f"Path to ledger file (default: {DEFAULT_LEDGER_PATH})"
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help="Suppress non-error output"
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Enable verbose output"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    subparsers.required = True
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new update block')
    create_parser.add_argument(
        '-id', '--update-id',
        required=True,
        dest='update_id',
        help="Update ID (e.g., UP-2026-10-11-01)"
    )
    create_parser.add_argument(
        '-desc', '--description',
        required=True,
        help="Description of the update"
    )
    create_parser.add_argument(
        '-gate', '--net-positive-gate',
        dest='gate',
        help="Net positive gate status (e.g., 'PASSED (E > 0)')"
    )
    create_parser.add_argument(
        '-m', '--metadata',
        help="Additional metadata as JSON string"
    )
    create_parser.set_defaults(func=cmd_create)
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify ledger integrity')
    verify_parser.set_defaults(func=cmd_verify)
    
    # View command
    view_parser = subparsers.add_parser('view', help='View ledger contents')
    view_parser.add_argument(
        '--block',
        type=int,
        help="View specific block by index"
    )
    view_parser.set_defaults(func=cmd_view)
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export ledger to file')
    export_parser.add_argument(
        '-o', '--output',
        required=True,
        help="Output file path"
    )
    export_parser.set_defaults(func=cmd_export)
    
    # Reset command
    reset_parser = subparsers.add_parser('reset', help='Clear the ledger')
    reset_parser.add_argument(
        '-f', '--force',
        action='store_true',
        help="Skip confirmation prompt"
    )
    reset_parser.set_defaults(func=cmd_reset)
    
    args = parser.parse_args()
    
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
