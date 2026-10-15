use sovereign_governance_wasm::{Module01NetPositive, Module04Mdve, NodeState, SensorTelemetry};

#[test]
fn mdve_all_pass() {
    let node = NodeState {
        node_id: "NODE_TEST".into(),
        psi_pers: 1,
        lid_hash: "0xabcdef".into(),
        is_markov_isolated: true,
        is_sandboxed: false,
    };

    let telemetry = SensorTelemetry {
        phi_measured: 0.25,
        ds_internal_dt: -0.1,
        planetary_delta: 5.0,
        real_r_systemic: 50.0,
        real_x_extractive: 10.0,
        real_phi_landauer: 2.0,
    };

    let results = Module04Mdve::inspect(&node, &telemetry);
    assert!(results.all_passed, "Expected MDVE to pass for the test input");
}

#[test]
fn net_positive_lock() {
    let telemetry = SensorTelemetry {
        phi_measured: 0.5,
        ds_internal_dt: -0.2,
        planetary_delta: 3.0,
        real_r_systemic: 100.0,
        real_x_extractive: 10.0,
        real_phi_landauer: 1.0,
    };

    let e_net = Module01NetPositive::calculate_e_net(&telemetry);
    let lock = Module01NetPositive::evaluate_lock(e_net);
    assert_eq!(lock, 1, "Expected lock to be engaged (1) when E_net > 0");
}
