use serde::{Deserialize, Serialize};
use wasm_bindgen::prelude::*;

// =====================================================================
// DATA TYPES & DTOS
// =====================================================================

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct NodeState {
    pub node_id: String,
    pub psi_pers: u8,               // 1 = Active Citizen Standing, 0 = Revoked
    pub lid_hash: String,           // ZK-Identity format (e.g. 0x...)
    pub is_markov_isolated: bool,   // Markov Blanket integrity
    pub is_sandboxed: bool,         // Containment status
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct SensorTelemetry {
    pub phi_measured: f64,
    pub ds_internal_dt: f64,
    pub planetary_delta: f64,
    pub real_r_systemic: f64,
    pub real_x_extractive: f64,
    pub real_phi_landauer: f64,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct MdveHookResults {
    pub juris: bool,
    pub info: bool,
    pub thermo: bool,
    pub cyber: bool,
    pub law: bool,
    pub sys: bool,
    pub all_passed: bool,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct MicrokernelEvaluation {
    pub permitted: bool,
    pub e_net: f64,
    pub lock_status: u8,
    pub mdve_hooks: MdveHookResults,
    pub node_id: String,
}

// =====================================================================
// MODULE 04: MULTI-DOMAIN VERIFICATION ENGINE (MDVE)
// =====================================================================

pub struct Module04Mdve;

impl Module04Mdve {
    pub const PHI_THRESHOLD: f64 = 0.10;

    /// Hook 1: Jurisprudence (LID Key Integrity)
    #[inline]
    pub fn verify_jurisprudence(node: &NodeState) -> bool {
        !node.lid_hash.is_empty() && node.lid_hash.starts_with("0x")
    }

    /// Hook 2: Information Theory (Causal Irreducibility Phi)
    #[inline]
    pub fn verify_information_theory(phi: f64) -> bool {
        phi >= Self::PHI_THRESHOLD
    }

    /// Hook 3: Non-Equilibrium Thermodynamics (Free Energy Minimization)
    #[inline]
    pub fn verify_thermodynamics(ds_dt: f64) -> bool {
        ds_dt <= 0.0
    }

    /// Hook 4: Cybernetics (Markov Blanket Isolation)
    #[inline]
    pub fn verify_cybernetics(node: &NodeState) -> bool {
        node.is_markov_isolated
    }

    /// Hook 5: Computational Law (Boolean Citizen Standing Gate)
    #[inline]
    pub fn verify_computational_law(node: &NodeState) -> bool {
        node.psi_pers == 1 && !node.is_sandboxed
    }

    /// Hook 6: Systems Modeling (Planetary Boundary Constraints)
    #[inline]
    pub fn verify_systems_modeling(p_delta: f64) -> bool {
        p_delta >= 0.0
    }

    /// Full 6-Hook Inspection Pipeline
    pub fn inspect(node: &NodeState, telemetry: &SensorTelemetry) -> MdveHookResults {
        let juris = Self::verify_jurisprudence(node);
        let info = Self::verify_information_theory(telemetry.phi_measured);
        let thermo = Self::verify_thermodynamics(telemetry.ds_internal_dt);
        let cyber = Self::verify_cybernetics(node);
        let law = Self::verify_computational_law(node);
        let sys = Self::verify_systems_modeling(telemetry.planetary_delta);

        let all_passed = juris && info && thermo && cyber && law && sys;

        MdveHookResults {
            juris,
            info,
            thermo,
            cyber,
            law,
            sys,
            all_passed,
        }
    }
}

// =====================================================================
// MODULE 01: NET-POSITIVE GATE & ANTI-EXTRACTION LOCK
// =====================================================================

pub struct Module01NetPositive;

impl Module01NetPositive {
    /// Computes systemic yield E_net = Sum(R_systemic) - (Sum(X_extractive) + Phi_landauer)
    #[inline]
    pub fn calculate_e_net(telemetry: &SensorTelemetry) -> f64 {
        telemetry.real_r_systemic - (telemetry.real_x_extractive + telemetry.real_phi_landauer)
    }

    /// Evaluates Anti-Extraction Lock L(alpha): returns 1 if E_net > 0 else 0
    #[inline]
    pub fn evaluate_lock(e_net: f64) -> u8 {
        if e_net > 0.0 { 1 } else { 0 }
    }
}

// =====================================================================
// WASM MICROKERNEL INTERFACE
// =====================================================================

#[wasm_bindgen]
pub struct GovernanceMicrokernel;

#[wasm_bindgen]
impl GovernanceMicrokernel {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Self
    }

    /// Fast evaluation entrypoint accepting JSON strings from JS/Host environment.
    /// Returns a JsValue (JS object) for easier interop with JS consumers.
    #[wasm_bindgen]
    pub fn evaluate(&self, node_json: &str, telemetry_json: &str) -> Result<JsValue, JsValue> {
        let node: NodeState = serde_json::from_str(node_json)
            .map_err(|e| JsValue::from_str(&format!("Invalid NodeState JSON: {}", e)))?;

        let telemetry: SensorTelemetry = serde_json::from_str(telemetry_json)
            .map_err(|e| JsValue::from_str(&format!("Invalid SensorTelemetry JSON: {}", e)))?;

        // 1. Module 04: MDVE Inspection
        let mdve_hooks = Module04Mdve::inspect(&node, &telemetry);

        // 2. Module 01: Net-Positive Gate Evaluation
        let e_net = Module01NetPositive::calculate_e_net(&telemetry);
        let lock_status = Module01NetPositive::evaluate_lock(e_net);

        // Master Kernel Invariant Check
        let permitted = mdve_hooks.all_passed && lock_status == 1 && node.psi_pers == 1;

        let outcome = MicrokernelEvaluation {
            permitted,
            e_net,
            lock_status,
            mdve_hooks,
            node_id: node.node_id,
        };

        JsValue::from_serde(&outcome)
            .map_err(|e| JsValue::from_str(&format!("Serialization Error: {}", e)))
    }
}
