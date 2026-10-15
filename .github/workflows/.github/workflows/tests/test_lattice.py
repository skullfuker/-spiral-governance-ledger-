import pytest
from pure_structure import PureStructuralLayer

def test_net_positive_gate_enforcement():
    layer = PureStructuralLayer(
        lattice_zone="ZONE-OMEGA-TEST",
        worm_vault_uri="s3://test-worm-vault"
    )
    agent_did = "did:sos:agent:test_agent_01"
    layer.register_soulbound_agent(agent_did, valid=True)

    # Test 1: Valid Net-Positive Transition (E > 0)
    success_receipt = layer.execute_structural_transition(
        action_id="test_action_01",
        actor_did=agent_did,
        community_id="0x0000000000000000000000000000000000000000000000000000000000000001",
        zk_proof="valid_zk_groth16_proof_string_sample_01",
        positive_impacts=[3.0],
        negative_impacts=[1.0]
    )
    assert success_receipt["gate_result"] == "ACCEPT"
    assert success_receipt["computed_impact"]["delta_e"] == 2.0

    # Test 2: Extractive Rejection (E <= 0)
    rejection_receipt = layer.execute_structural_transition(
        action_id="test_action_02",
        actor_did=agent_did,
        community_id="0x0000000000000000000000000000000000000000000000000000000000000001",
        zk_proof="valid_zk_groth16_proof_string_sample_02",
        positive_impacts=[0.5],
        negative_impacts=[2.0]
    )
    assert rejection_receipt["gate_result"] == "REJECT_NET_NON_POSITIVE"
    assert rejection_receipt["computed_impact"]["delta_e"] == -1.5
