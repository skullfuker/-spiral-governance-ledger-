import pytest
from lattice_ledger import LatticeLedger  # Adjust to match actual class/functions

def test_lattice_ledger_initialization():
    """Verify core ledger initialization and initial invariant state."""
    ledger = LatticeLedger(coil_id="77-AE-VIGILANCE")
    assert ledger.coil_id == "77-AE-VIGILANCE"
    assert ledger.is_sealed() is False

def test_net_positive_metabolic_gate():
    """Validate the net-positive metabolic surplus invariant (delta E > 0)."""
    ledger = LatticeLedger(coil_id="77-AE-VIGILANCE")
    # Simulate metabolic surplus calculation
    surplus = ledger.compute_metabolic_surplus(power_inputs=[150], structural_costs=[50])
    assert surplus > 0
