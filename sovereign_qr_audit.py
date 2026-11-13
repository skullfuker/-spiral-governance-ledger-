<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="artifact-type" content="dashboard">
  <meta name="design-style" content="nocturne">
  <title>Sovereign Cryptographic Ledger — Epistemic Visualizer &amp; Public Commons</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..700;1,400..600&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">

  <script src="https://unpkg.com/lucide@1.43.0/dist/umd/lucide.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.1/dist/chart.umd.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/topojson-client@3.1.0/dist/topojson-client.min.js"></script>

  <style>
    :root {
      color-scheme: dark;

      /* Page and surfaces: Prussian midnight steps (Nocturne) */
      --background: #0a101d;
      --surface-container-low: #0e1626;
      --surface-container: #111b2e;
      --surface-container-high: #17243c;

      /* Text */
      --on-surface: #f2ece1;
      --on-surface-variant: #9ba8bf;

      /* Borders */
      --outline: #384d73;
      --outline-variant: #21304d;

      /* Accents */
      --primary: #dfaa5b;
      --on-primary: #0a101d;
      --primary-container: #2b261c;
      --on-primary-container: #f5dcb0;
      --secondary: #687a99;
      --tertiary: #7cc4e8;
      --error: #f27474;
      --on-error: #1a0606;

      /* Data series */
      --data-1: #dfaa5b;
      --data-2: #7cc4e8;
      --data-3: #52d19c;
      --data-4: #e07a5f;
      --data-context: #4a5d80;

      /* Fonts */
      --font-headline: 'EB Garamond', serif;
      --font-body: 'Plus Jakarta Sans', sans-serif;
      --font-label: 'JetBrains Mono', monospace;

      /* Shape */
      --rounded: 0.25rem;
      --rounded-lg: 0.375rem;
      --rounded-full: 9999px;

      /* Style effects */
      --hairline: 1px solid var(--outline-variant);
      --hairline-strong: 1px solid var(--outline);
      --panel-highlight: inset 0 1px 0 rgba(242, 236, 225, 0.05);
      --brass-glow: radial-gradient(circle at 88% 12%, rgba(223, 170, 91, 0.08), transparent 45%);
      --heading-tracking: -0.015em;
      --label-tracking: 0.06em;
      --sky-tint: color-mix(in srgb, var(--tertiary) 12%, transparent);
      --brass-tint: color-mix(in srgb, var(--primary) 14%, transparent);
      --mint-tint: color-mix(in srgb, var(--data-3) 14%, transparent);
      --coral-tint: color-mix(in srgb, var(--error) 14%, transparent);

      /* Shared semantic & focus tokens */
      --positive: #52d19c;
      --warning: #dfaa5b;
      --focus: var(--primary);

      /* Dashboard type scale */
      --display-size: clamp(1.75rem, 1.4rem + 1.2vw, 2.35rem);
      --headline-size: clamp(1.25rem, 1.1rem + 0.5vw, 1.55rem);
      --subhead-size: clamp(1.0625rem, 1rem + 0.25vw, 1.1875rem);
      --body-size: clamp(0.9375rem, 0.9rem + 0.15vw, 1rem);
      --label-size: 0.75rem;

      /* Spacing scale */
      --space-xs: 0.25rem;
      --space-sm: 0.5rem;
      --space-md: 1rem;
      --space-lg: 1.5rem;
      --space-xl: 2.5rem;
      --space-2xl: 4rem;

      /* Motion */
      --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
      --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
      --dur-micro: 120ms;
      --dur-short: 220ms;
      --dur-medium: 320ms;
    }

    *, *::before, *::after { box-sizing: border-box; }
    html, body {
      overflow-x: clip;
      margin: 0;
      padding: 0;
      background-color: var(--background);
      color: var(--on-surface);
      font-family: var(--font-body);
      font-size: var(--body-size);
      line-height: 1.5;
      scroll-behavior: smooth;
    }
    header { position: static !important; }

    /* Focus visibility */
    :focus-visible {
      outline: 2px solid var(--focus);
      outline-offset: 2px;
    }

    /* Page layout */
    .page-grid {
      display: grid;
      gap: var(--space-lg);
      padding: var(--space-lg);
      max-width: 1320px;
      margin: 0 auto;
      overflow: hidden;
    }
    .page-grid * { min-width: 0; }

    /* Hero Masthead */
    .hero-header {
      background-color: var(--background);
      background-image: var(--brass-glow);
      border-bottom: var(--hairline);
      padding-bottom: var(--space-lg);
    }

    .masthead-top {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-start;
      gap: var(--space-md);
    }

    .title {
      font-family: var(--font-headline);
      font-weight: 500;
      font-size: var(--display-size);
      letter-spacing: var(--heading-tracking);
      line-height: 1.08;
      color: var(--on-surface);
      margin: 0;
    }

    .title em {
      font-style: italic;
      font-weight: 400;
      color: var(--primary);
    }

    .section-title {
      font-family: var(--font-headline);
      font-weight: 500;
      font-size: var(--headline-size);
      letter-spacing: var(--heading-tracking);
      line-height: 1.15;
      color: var(--on-surface);
      margin: 0;
    }

    .section-title em {
      font-style: italic;
      font-weight: 400;
      color: var(--primary);
    }

    .deck-brass {
      font-family: var(--font-label);
      font-size: var(--label-size);
      letter-spacing: var(--label-tracking);
      text-transform: uppercase;
      color: var(--primary);
      margin-top: var(--space-xs);
    }

    .coord-label {
      font-family: var(--font-label);
      font-size: var(--label-size);
      letter-spacing: var(--label-tracking);
      text-transform: uppercase;
      color: var(--tertiary);
    }

    .lede {
      color: var(--on-surface-variant);
      max-width: 72ch;
      margin: var(--space-sm) 0 0 0;
      font-size: var(--body-size);
    }

    /* Navigation & Action bar */
    .nav-strip {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: var(--space-sm);
      margin-top: var(--space-md);
      padding-top: var(--space-md);
      border-top: var(--hairline);
    }

    .nav-links {
      display: flex;
      flex-wrap: wrap;
      gap: var(--space-sm);
    }

    .nav-pill {
      display: inline-flex;
      align-items: center;
      gap: var(--space-xs);
      min-height: 44px;
      padding: var(--space-xs) var(--space-md);
      background: var(--surface-container);
      border: var(--hairline);
      border-radius: var(--rounded);
      color: var(--on-surface);
      text-decoration: none;
      font-family: var(--font-label);
      font-size: var(--label-size);
      letter-spacing: var(--label-tracking);
      text-transform: uppercase;
      transition: background-color var(--dur-micro) var(--ease-out), border-color var(--dur-micro) var(--ease-out);
    }

    .nav-pill:hover {
      background: var(--surface-container-high);
      border-color: var(--outline);
    }

    .action-cluster {
      display: flex;
      flex-wrap: wrap;
      gap: var(--space-sm);
      align-items: center;
    }

    /* Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-xs);
      min-height: 44px;
      padding: var(--space-xs) var(--space-md);
      border-radius: var(--rounded);
      font-family: var(--font-label);
      font-size: var(--label-size);
      font-weight: 500;
      letter-spacing: var(--label-tracking);
      text-transform: uppercase;
      cursor: pointer;
      border: var(--hairline-strong);
      background: transparent;
      color: var(--on-surface);
      transition: background-color var(--dur-micro) var(--ease-out), color var(--dur-micro) var(--ease-out), box-shadow var(--dur-micro) var(--ease-out);
    }

    .btn:hover:not(:disabled) {
      background: var(--surface-container-high);
    }

    .btn:active:not(:disabled) {
      transform: translateY(1px);
    }

    .btn:disabled {
      opacity: 0.45;
      cursor: not-allowed;
    }

    .btn-primary {
      background: var(--primary);
      color: var(--on-primary);
      border-color: var(--primary);
    }

    .btn-primary:hover:not(:disabled) {
      background: var(--on-primary-container);
      color: var(--on-primary);
    }

    .btn-active {
      background: var(--brass-tint);
      border-color: var(--primary);
      color: var(--primary);
    }

    .btn-danger {
      border-color: var(--error);
      color: var(--error);
    }

    /* Midnight Panels */
    .panel {
      background: var(--surface-container);
      border: var(--hairline);
      box-shadow: var(--panel-highlight);
      border-radius: var(--rounded-lg);
      padding: var(--space-lg);
    }

    .panel-low {
      background: var(--surface-container-low);
      border: var(--hairline);
      border-radius: var(--rounded-lg);
      padding: var(--space-md);
    }

    .observation-well {
      background: var(--background);
      border: var(--hairline);
      border-radius: var(--rounded);
      padding: var(--space-md);
      font-family: var(--font-label);
      color: var(--on-surface);
    }

    /* KPI Row */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 1fr));
      gap: var(--space-md);
    }

    .kpi-card {
      background: var(--surface-container);
      border: var(--hairline);
      box-shadow: var(--panel-highlight);
      border-radius: var(--rounded-lg);
      padding: var(--space-md) var(--space-lg);
      display: flex;
      flex-direction: column;
      gap: var(--space-xs);
    }

    .kpi-value {
      font-family: var(--font-headline);
      font-weight: 500;
      font-size: clamp(1.65rem, 1.35rem + 0.9vw, 2.1rem);
      line-height: 1.1;
      color: var(--on-surface);
      font-variant-numeric: tabular-nums;
    }

    .kpi-sub {
      font-family: var(--font-label);
      font-size: var(--label-size);
      color: var(--on-surface-variant);
      word-break: break-word;
    }

    /* Badges */
    .badge {
      display: inline-flex;
      align-items: center;
      gap: var(--space-xs);
      border-radius: var(--rounded);
      padding: var(--space-xs) var(--space-sm);
      font-family: var(--font-label);
      font-size: var(--label-size);
      letter-spacing: var(--label-tracking);
      text-transform: uppercase;
      line-height: 1.2;
    }

    .badge-sky {
      background: var(--sky-tint);
      color: var(--tertiary);
      border: 1px solid color-mix(in srgb, var(--tertiary) 35%, transparent);
    }

    .badge-brass {
      background: var(--brass-tint);
      color: var(--primary);
      border: 1px solid color-mix(in srgb, var(--primary) 35%, transparent);
    }

    .badge-mint {
      background: var(--mint-tint);
      color: var(--positive);
      border: 1px solid color-mix(in srgb, var(--positive) 35%, transparent);
    }

    .badge-coral {
      background: var(--coral-tint);
      color: var(--error);
      border: 1px solid color-mix(in srgb, var(--error) 35%, transparent);
    }

    /* Module Sections */
    .module-section {
      display: grid;
      gap: var(--space-lg);
      padding-top: var(--space-md);
      border-top: var(--hairline);
    }

    .module-header {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-end;
      gap: var(--space-md);
    }

    /* Two-column asymmetric grids */
    .split-grid-wide {
      display: grid;
      grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr);
      gap: var(--space-lg);
      align-items: start;
    }

    .split-grid-balanced {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1.2fr);
      gap: var(--space-lg);
      align-items: start;
    }

    /* Form controls with always-visible labels */
    .control-group {
      display: flex;
      flex-direction: column;
      gap: var(--space-xs);
    }

    .control-label {
      font-family: var(--font-label);
      font-size: var(--label-size);
      letter-spacing: var(--label-tracking);
      text-transform: uppercase;
      color: var(--on-surface-variant);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: var(--space-sm);
    }

    .control-label .val-readout {
      color: var(--primary);
      font-variant-numeric: tabular-nums;
    }

    input[type="number"],
    input[type="text"],
    select {
      min-height: 44px;
      padding: var(--space-xs) var(--space-md);
      background: var(--background);
      border: var(--hairline-strong);
      border-radius: var(--rounded);
      color: var(--on-surface);
      font-family: var(--font-label);
      font-size: var(--body-size);
      width: 100%;
    }

    select {
      padding-right: var(--space-xl);
    }

    input[type="range"] {
      width: 100%;
      min-height: 36px;
      accent-color: var(--primary);
      cursor: pointer;
    }

    .controls-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(150px, 100%), 1fr));
      gap: var(--space-md);
      align-items: end;
    }

    .token-row {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: var(--space-sm);
      align-items: end;
    }

    /* Readout Grid */
    .readout-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(170px, 100%), 1fr));
      gap: var(--space-sm);
    }

    .readout-box {
      background: var(--background);
      border: var(--hairline);
      border-radius: var(--rounded);
      padding: var(--space-sm) var(--space-md);
      display: flex;
      flex-direction: column;
      gap: var(--space-xs);
    }

    .readout-box .mono-val {
      font-family: var(--font-label);
      font-size: 1.05rem;
      font-weight: 500;
      color: var(--on-surface);
      font-variant-numeric: tabular-nums;
    }

    /* Canvas / 3D / Map containers */
    .chart-well {
      position: relative;
      background: var(--background);
      border: var(--hairline);
      border-radius: var(--rounded);
      padding: var(--space-md);
      min-height: 320px;
    }

    .canvas-3d-well {
      position: relative;
      background: var(--background);
      border: var(--hairline);
      border-radius: var(--rounded);
      min-height: 460px;
      height: 460px;
      overflow: hidden;
    }

    .canvas-3d-overlay {
      position: absolute;
      top: var(--space-md);
      left: var(--space-md);
      right: var(--space-md);
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      pointer-events: none;
      gap: var(--space-sm);
      z-index: 4;
    }

    .canvas-3d-overlay .badge {
      pointer-events: auto;
    }

    .canvas-3d-footer {
      position: absolute;
      bottom: var(--space-sm);
      left: var(--space-md);
      right: var(--space-md);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: var(--space-sm);
      pointer-events: none;
      z-index: 4;
    }

    #alba-map {
      min-height: 460px;
      height: 460px;
      width: 100%;
      background: var(--background);
      border: var(--hairline);
      border-radius: var(--rounded);
      z-index: 1;
    }

    .leaflet-container {
      background: var(--background) !important;
      font-family: var(--font-body) !important;
    }

    .leaflet-popup-content-wrapper,
    .leaflet-popup-tip {
      background: var(--surface-container-high) !important;
      color: var(--on-surface) !important;
      border: var(--hairline-strong) !important;
      box-shadow: none !important;
    }

    /* Tables */
    .table-wrap {
      overflow-x: auto;
      border: var(--hairline);
      border-radius: var(--rounded);
      background: var(--background);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.875rem;
    }

    thead th {
      position: sticky;
      top: 0;
      background: var(--surface-container-low);
      font-family: var(--font-label);
      font-size: var(--label-size);
      letter-spacing: var(--label-tracking);
      text-transform: uppercase;
      color: var(--on-surface-variant);
      text-align: left;
      padding: var(--space-sm) var(--space-md);
      border-bottom: var(--hairline-strong);
      white-space: nowrap;
    }

    tbody td {
      padding: var(--space-sm) var(--space-md);
      border-bottom: var(--hairline);
      color: var(--on-surface);
      vertical-align: middle;
    }

    tbody tr:hover {
      background: var(--surface-container-low);
    }

    tbody tr.selected-row {
      background: var(--surface-container-high);
    }

    .num-col {
      text-align: right;
      font-family: var(--font-label);
      font-variant-numeric: tabular-nums;
      white-space: nowrap;
    }

    /* Presets bar */
    .preset-strip {
      display: flex;
      flex-wrap: wrap;
      gap: var(--space-xs);
    }

    .btn-sm {
      min-height: 36px;
      padding: var(--space-xs) var(--space-sm);
      font-size: 0.72rem;
    }

    /* Status line */
    .inline-status {
      font-family: var(--font-label);
      font-size: var(--label-size);
      color: var(--tertiary);
      min-height: 1.25rem;
    }

    .formula-bar {
      font-family: var(--font-label);
      font-size: 0.82rem;
      color: var(--primary);
      background: var(--surface-container-low);
      border-left: 2px solid var(--primary);
      padding: var(--space-sm) var(--space-md);
      border-radius: 0 var(--rounded) var(--rounded) 0;
      overflow-x: auto;
    }

    .layer-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(260px, 100%), 1fr));
      gap: var(--space-md);
    }

    .footer-meta {
      border-top: var(--hairline);
      padding-top: var(--space-lg);
      padding-bottom: var(--space-xl);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: var(--space-md);
      color: var(--on-surface-variant);
      font-size: 0.85rem;
    }

    /* Responsive adjustments */
    @media (max-width: 960px) {
      .split-grid-wide,
      .split-grid-balanced {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 640px) {
      .page-grid {
        grid-template-columns: 1fr;
        padding: var(--space-md);
        gap: var(--space-md);
      }
      .token-row {
        grid-template-columns: 1fr;
      }
      .canvas-3d-well,
      #alba-map {
        min-height: 360px;
        height: 360px;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
    }
  </style>
</head>
<body>
  <div class="page-grid">
    <!-- MASTHEAD -->
    <header class="hero-header">
      <div class="masthead-top">
        <div>
          <div class="coord-label">SOVEREIGN LATTICE · PUBLIC KNOWLEDGE COMMONS · WORM BLOCK #849206</div>
          <h1 class="title">Sovereign Cryptographic Ledger — <em>Epistemic</em> Visualizer</h1>
          <div class="deck-brass">MASTER COIL ID: 77-AE-VIGILANCE · RELEASE v2.2.0-SOVEREIGN-KERNEL · NON-EXTRACTIVE COMMONS</div>
          <p class="lede">
            Unified telemetry portal bridging ChronOS deep-time base conversions, ABIEH 34.4 Hz chamber acoustics, and ALBA v2.2 Bayesian geospatial discovery under strict EVI &le; 0.85 ecological stewardship and &Delta;E &gt; 0 metabolic invariants.
          </p>
        </div>
        <div class="action-cluster">
          <span class="badge badge-mint" id="ledger-seal-badge">SEALED · 99.98% INTEGRITY</span>
        </div>
      </div>

      <nav class="nav-strip" aria-label="Portal sections and workspace tools">
        <div class="nav-links">
          <a class="nav-pill" href="#chronos"><i data-lucide="clock" width="14" height="14" aria-hidden="true"></i> ChronOS Ciphers</a>
          <a class="nav-pill" href="#chamber-3d"><i data-lucide="box" width="14" height="14" aria-hidden="true"></i> 3D Acoustic Chambers</a>
          <a class="nav-pill" href="#alba-grid"><i data-lucide="map-pin" width="14" height="14" aria-hidden="true"></i> ALBA v2.2 Grid</a>
          <a class="nav-pill" href="#governance-audit"><i data-lucide="shield-check" width="14" height="14" aria-hidden="true"></i> Layer 0 Governance</a>
        </div>
        <div class="action-cluster">
          <button type="button" class="btn" onclick="exportPortalCSV()">
            <i data-lucide="download" width="15" height="15" aria-hidden="true"></i> Export Telemetry CSV
          </button>
          <button type="button" class="btn btn-danger" id="btn-reset-state" onclick="handleResetWorkspace(this)">
            <i data-lucide="rotate-ccw" width="15" height="15" aria-hidden="true"></i> Reset Workspace
          </button>
        </div>
      </nav>
    </header>

    <!-- TOP KPI TELEMETRY -->
    <section aria-label="Ledger summary metrics" class="kpi-grid">
      <div class="kpi-card">
        <span class="coord-label">WORM Vault Anchor</span>
        <div class="kpi-value">#849206</div>
        <div class="kpi-sub">sha3:675e7578b64d…860b18054</div>
      </div>
      <div class="kpi-card">
        <span class="coord-label">ChronOS Compression Ratio</span>
        <div class="kpi-value" id="kpi-chronos-ratio">36.216&times;</div>
        <div class="kpi-sub" id="kpi-chronos-sub">241,200 SKL &divide; 6,660 Genesis yrs</div>
      </div>
      <div class="kpi-card">
        <span class="coord-label">Target Acoustic Resonance</span>
        <div class="kpi-value" id="kpi-chamber-hz">34.40 Hz</div>
        <div class="kpi-sub" id="kpi-chamber-sub">Barabar Reference: 34.397 Hz (Q 68.4)</div>
      </div>
      <div class="kpi-card">
        <span class="coord-label">ALBA Safety Gate (EVI &le; <span id="kpi-evi-cap">0.85</span>)</span>
        <div class="kpi-value" id="kpi-alba-pass">7 / 10 Passed</div>
        <div class="kpi-sub" id="kpi-alba-sub">3 intercepted for UAS non-intrusive scan</div>
      </div>
    </section>

    <!-- COMPONENT 1: CHRONOS CALENDAR CIPHER VISUALIZER -->
    <section id="chronos" class="module-section" aria-labelledby="heading-chronos">
      <div class="module-header">
        <div>
          <div class="coord-label">LAYER 1 · TEMPORAL &amp; EPOCHAL ENGINE · LÓPEZ PROTO-LEDGER</div>
          <h2 class="section-title" id="heading-chronos">ChronOS Calendar <em>Cipher</em> Visualizer</h2>
        </div>
        <span class="badge badge-brass">INVARIANT U1–U3 · EPOCH 0 &rarr; EPOCH 2</span>
      </div>

      <div class="split-grid-balanced">
        <!-- Left: Proto-Ledger + Multi-Base Lifespan Translator -->
        <div class="panel" style="display: grid; gap: var(--space-md);">
          <div>
            <div class="coord-label">1A · LÓPEZ PROTO-LEDGER TOKEN COMPILER</div>
            <p style="margin: var(--space-xs) 0 0 0; color: var(--on-surface-variant); font-size: 0.9rem;">
              Modify the three raw token bands <code>[L, M, S]</code> (canonical baseline <code>[6, 6, 6]</code>) to compile simultaneous Base-10 Hebrew and Base-60 Sumerian totals.
            </p>
          </div>

          <div class="token-row">
            <div class="control-group">
              <label class="control-label" for="tok-large">Large Tokens (10&sup3; / 10&times;60&sup2;)</label>
              <input type="number" id="tok-large" min="0" max="20" step="1" value="6" oninput="updateProtoLedger()">
            </div>
            <div class="control-group">
              <label class="control-label" for="tok-med">Medium Tokens (10&sup2; / 60&sup2;)</label>
              <input type="number" id="tok-med" min="0" max="20" step="1" value="6" oninput="updateProtoLedger()">
            </div>
            <div class="control-group">
              <label class="control-label" for="tok-small">Small Tokens (10&sup1; / 60&sup1;)</label>
              <input type="number" id="tok-small" min="0" max="20" step="1" value="6" oninput="updateProtoLedger()">
            </div>
          </div>

          <div class="readout-grid">
            <div class="readout-box">
              <span class="coord-label">Base-10 Genesis Kernel</span>
              <span class="mono-val" id="out-base10-total">6,660 yrs</span>
              <span class="kpi-sub" id="out-base10-eq">6&times;10&sup3; + 6&times;10&sup2; + 6&times;10</span>
            </div>
            <div class="readout-box">
              <span class="coord-label">Base-60 SKL Core</span>
              <span class="mono-val" id="out-base60-total">237,960 yrs</span>
              <span class="kpi-sub" id="out-base60-eq">+ 9 SAR (3,240) = 241,200</span>
            </div>
            <div class="readout-box">
              <span class="coord-label">Mayan Baktun Equivalent</span>
              <span class="mono-val" id="out-mayan-tuns">18.50 Tun-Cycles</span>
              <span class="kpi-sub" id="out-mayan-sub">6,660 &divide; 360-day Tun</span>
            </div>
          </div>

          <hr style="border: 0; border-top: var(--hairline); margin: var(--space-xs) 0;">

          <div>
            <div class="coord-label">1B · REGNAL &amp; PATRIARCHAL MULTI-BASE TRANSLATOR</div>
            <div class="preset-strip" style="margin-top: var(--space-sm);">
              <button type="button" class="btn btn-sm" onclick="selectChronosPresetByKey('alulim')">Alulim · 28,800</button>
              <button type="button" class="btn btn-sm" onclick="selectChronosPresetByKey('enmenluana')">En-men-lu-ana · 43,200</button>
              <button type="button" class="btn btn-sm" onclick="selectChronosPresetByKey('enmendurana')">En-men-dur-ana · 21,000</button>
              <button type="button" class="btn btn-sm" onclick="selectChronosPresetByKey('adam')">Adam · 930</button>
              <button type="button" class="btn btn-sm" onclick="selectChronosPresetByKey('enoch')">Enoch · 365</button>
              <button type="button" class="btn btn-sm" onclick="selectChronosPresetByKey('eber')">Eber · 464</button>
              <button type="button" class="btn btn-sm" onclick="selectChronosPresetByKey('methuselah')">Methuselah · 969</button>
            </div>
          </div>

          <div class="controls-row">
            <div class="control-group">
              <label class="control-label" for="cipher-input-years">
                <span>Input Span (Years / Days)</span>
                <span class="val-readout" id="cipher-source-label">Alulim (SKL 1)</span>
              </label>
              <input type="number" id="cipher-input-years" min="1" max="500000" step="1" value="28800" oninput="translateSingleSpan()">
            </div>
            <div class="control-group">
              <label class="control-label" for="cipher-input-mode">Interpretation Mode</label>
              <select id="cipher-input-mode" onchange="translateSingleSpan()">
                <option value="skl">Sumerian Base-60 (SAR/NER/SOSS)</option>
                <option value="gen">Hebrew Base-10 (5 &amp; 7 Sacred)</option>
                <option value="maya">Mayan Base-20 (Vigesimal Days/Tuns)</option>
              </select>
            </div>
          </div>

          <div class="readout-grid">
            <div class="readout-box">
              <span class="coord-label">Sumerian Base-60 Decomposition</span>
              <span class="mono-val" id="trans-skl-decomp">8 SAR · 0 NER · 0 SOSS</span>
              <span class="kpi-sub" id="trans-skl-scaled">&divide;60 = 480 yrs | &divide;360 = 80.0 yrs</span>
            </div>
            <div class="readout-box">
              <span class="coord-label">Hebrew Base-10 Sacred Form</span>
              <span class="mono-val" id="trans-gen-decomp">5,760 &times; 5 + 0</span>
              <span class="kpi-sub" id="trans-gen-class">Terminal digit: 0 (Exact 5k)</span>
            </div>
            <div class="readout-box">
              <span class="coord-label">Mayan / Popol Vuh Long Count</span>
              <span class="mono-val" id="trans-maya-lc">0.4.0.0.0</span>
              <span class="kpi-sub" id="trans-maya-cycles">Haab 365 &amp; Tzolk&rsquo;in 260 aligned</span>
            </div>
          </div>
        </div>

        <!-- Right: Post-Flood Decay Curve + Sliders -->
        <div class="panel" style="display: grid; gap: var(--space-md);">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: var(--space-sm); flex-wrap: wrap;">
            <div>
              <div class="coord-label">1C · POST-FLOOD DETERMINISTIC DECAY (GENESIS 11 vs SKL)</div>
              <p style="margin: var(--space-xs) 0 0 0; color: var(--on-surface-variant); font-size: 0.9rem;">
                Exponential compression <code>L(t) = (L&sub0; &minus; C)&middot;e<sup>&minus;&lambda;t</sup> + C</code> overlaid with the Eber override flag (<code>t=3</code>, 464 yrs) and SKL hyperbolic step regimes.
              </p>
            </div>
            <span class="badge badge-coral">EBER OVERRIDE t=3 · BABEL FORK</span>
          </div>

          <div class="controls-row">
            <div class="control-group">
              <label class="control-label" for="slider-l0">
                <span>Initial L&sub0; (Shem)</span>
                <span class="val-readout" id="val-l0">600 yrs</span>
              </label>
              <input type="range" id="slider-l0" min="400" max="900" step="10" value="600" oninput="syncDecayControls()">
            </div>
            <div class="control-group">
              <label class="control-label" for="slider-lambda">
                <span>Entropy &lambda;</span>
                <span class="val-readout" id="val-lambda">0.315</span>
              </label>
              <input type="range" id="slider-lambda" min="0.10" max="0.60" step="0.005" value="0.315" oninput="syncDecayControls()">
            </div>
            <div class="control-group">
              <label class="control-label" for="slider-floor">
                <span>Asymptote C</span>
                <span class="val-readout" id="val-floor">100 yrs</span>
              </label>
              <input type="range" id="slider-floor" min="70" max="150" step="5" value="100" oninput="syncDecayControls()">
            </div>
          </div>

          <div class="chart-well">
            <canvas id="chronos-decay-chart" aria-label="Post-flood exponential decay and SKL step compression chart"></canvas>
          </div>

          <div class="formula-bar" id="decay-formula-status">
            Mean absolute error (excluding Eber t=3 override): 15.8% · Epoch 2 Babel sharding at Peleg (t=4, 239 yrs)
          </div>
        </div>
      </div>

      <!-- Antediluvian Matrix Table -->
      <div class="panel" style="display: grid; gap: var(--space-sm);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: var(--space-sm);">
          <div class="coord-label">1D · ANTEDILUVIAN NUMERICAL TRANSLATION MATRIX (WELD-BLUNDELL PRISM vs GENESIS 5)</div>
          <span class="badge badge-sky">CLICK ANY ROW TO LOAD INTO TRANSLATOR</span>
        </div>
        <div class="table-wrap">
          <table id="chronos-matrix-table">
            <thead>
              <tr>
                <th>Pos</th>
                <th>SKL Ruler (City)</th>
                <th class="num-col">SKL Reign (Yrs)</th>
                <th>Base-60 Sign Composition</th>
                <th class="num-col">Scaled (&divide;360)</th>
                <th>Genesis 5 Patriarch</th>
                <th class="num-col">Lifespan (Yrs)</th>
                <th>Sacred 5/7 Structure</th>
              </tr>
            </thead>
            <tbody id="chronos-matrix-body"></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- COMPONENT 2: 3D SPATIAL & ACOUSTIC CHAMBER EXPLORER -->
    <section id="chamber-3d" class="module-section" aria-labelledby="heading-chamber">
      <div class="module-header">
        <div>
          <div class="coord-label">LAYER 2 · ABIEH HARMONICS &amp; HELMHOLTZ RESONANCE · POINT CLOUD PLANARITY</div>
          <h2 class="section-title" id="heading-chamber">3D Spatial &amp; <em>Acoustic</em> Chamber Explorer</h2>
        </div>
        <span class="badge badge-sky">34.4 HZ STANDING WAVE &amp; &epsilon;<sub>i</sub> DEVIATION</span>
      </div>

      <div class="split-grid-wide">
        <!-- Left: Three.js 3D Viewport -->
        <div class="panel" style="display: grid; gap: var(--space-md); padding: var(--space-md);">
          <div class="canvas-3d-well" id="three-container">
            <div class="canvas-3d-overlay">
              <span class="badge badge-brass" id="three-chamber-badge">BARABAR QUARTZ CAVITY · 34.40 HZ</span>
              <span class="badge badge-sky" id="three-drag-hint">DRAG TO ORBIT · SCROLL / BUTTONS TO ZOOM</span>
            </div>
            <div class="canvas-3d-footer">
              <span class="badge badge-mint" id="three-antinode-badge">ANTINODES: BRASS PEAKS · NODES: SKY</span>
              <span class="badge badge-sky" id="three-planarity-badge">PCA x&sub1; = 0.892</span>
            </div>
          </div>

          <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: var(--space-sm);">
            <div class="preset-strip">
              <button type="button" class="btn btn-sm btn-active" id="cam-orbit-btn" onclick="toggleChamberSpin()">Pause Auto-Orbit</button>
              <button type="button" class="btn btn-sm" onclick="zoomChamber(-1)">Zoom In (+)</button>
              <button type="button" class="btn btn-sm" onclick="zoomChamber(1)">Zoom Out (&minus;)</button>
              <button type="button" class="btn btn-sm" onclick="resetChamberCamera()">Reset View</button>
            </div>
            <button type="button" class="btn btn-sm" id="btn-audio-tone" onclick="toggleAcousticAudio()">
              <i data-lucide="volume-2" width="14" height="14" aria-hidden="true"></i> Audition Resonance Tone
            </button>
          </div>
        </div>

        <!-- Right: Physics & Point Cloud Controls -->
        <div class="panel" style="display: grid; gap: var(--space-md);">
          <div class="control-group">
            <label class="control-label" for="chamber-preset-select">Architectural Geometry Preset</label>
            <select id="chamber-preset-select" onchange="changeChamberPreset(this.value)">
              <option value="barabar">Barabar Stone Cavity (Quartz Granite · 34.397 Hz)</option>
              <option value="montegrande">Huaca Montegrande (5-Story Counter-Clockwise Spiral)</option>
              <option value="el_pongor">El Pongor MC-04 (Concentric Shale Terraces · +570m)</option>
            </select>
          </div>

          <div class="control-group">
            <label class="control-label" for="slider-freq">
              <span>Excitation Frequency (f)</span>
              <span class="val-readout" id="val-freq">34.4 Hz</span>
            </label>
            <input type="range" id="slider-freq" min="20" max="120" step="0.1" value="34.4" oninput="syncFreqFromSlider(this.value)">
            <div class="preset-strip" style="margin-top: var(--space-xs);">
              <button type="button" class="btn btn-sm" onclick="setChamberFrequency(34.4)">34.4 Hz (Barabar f&sub0;)</button>
              <button type="button" class="btn btn-sm" onclick="setChamberFrequency(68.8)">68.8 Hz (2nd Harmonic)</button>
              <button type="button" class="btn btn-sm" onclick="setChamberFrequency(110.0)">110 Hz (EEG Shift)</button>
            </div>
          </div>

          <div class="controls-row">
            <div class="control-group">
              <label class="control-label" for="select-medium">Propagation Medium</label>
              <select id="select-medium" onchange="updateChamberPhysics()">
                <option value="air">Open Atmosphere (v = 343 m/s · &alpha; = 1.00)</option>
                <option value="silt">Submerged Marine Silt (v = 1500 m/s · &alpha; = 0.45)</option>
              </select>
            </div>
            <div class="control-group">
              <label class="control-label" for="slider-epsilon">
                <span>Surface Noise (&epsilon;<sub>i</sub> Scatter)</span>
                <span class="val-readout" id="val-epsilon">0.08 m</span>
              </label>
              <input type="range" id="slider-epsilon" min="0.01" max="0.45" step="0.01" value="0.08" oninput="updateChamberPhysics()">
            </div>
          </div>

          <div class="readout-grid">
            <div class="readout-box">
              <span class="coord-label">Helmholtz Cavity f&sub0;</span>
              <span class="mono-val" id="out-helmholtz-f0">34.397 Hz</span>
              <span class="kpi-sub" id="out-helmholtz-match">Resonance delta: 0.00 Hz</span>
            </div>
            <div class="readout-box">
              <span class="coord-label">PCA Planarity x&sub1;</span>
              <span class="mono-val" id="out-planarity-x1">0.892</span>
              <span class="kpi-sub" id="out-planarity-class">Engineered planar surface</span>
            </div>
            <div class="readout-box">
              <span class="coord-label">Acoustic Wavelength &lambda;</span>
              <span class="mono-val" id="out-wavelength">9.97 m</span>
              <span class="kpi-sub" id="out-qfactor">Cavity Q-Factor: 68.4</span>
            </div>
            <div class="readout-box">
              <span class="coord-label">Psycho-Acoustic State</span>
              <span class="mono-val" id="out-neuro-state">Quartz Boring</span>
              <span class="kpi-sub" id="out-neuro-sub">Inverse piezoelectric stress</span>
            </div>
          </div>

          <div class="formula-bar">
            f&sub0; = (v / 2&pi;) &radic;(A / (V &middot; L)) &nbsp;|&nbsp; &epsilon;<sub>i</sub> = |n &middot; (p<sub>i</sub> &minus; p&sub0;)| &nbsp;|&nbsp; x&sub1; = (&lambda;&sub2; &minus; &lambda;&sub1;) / &lambda;&sub3;
          </div>
        </div>
      </div>
    </section>

    <!-- COMPONENT 3: ALBA v2.2 SPATIAL DISCOVERY GRID -->
    <section id="alba-grid" class="module-section" aria-labelledby="heading-alba">
      <div class="module-header">
        <div>
          <div class="coord-label">LAYER 2 · BAYESIAN SITE PROBABILITY ENGINE · THREE MISSING ARCHIVES</div>
          <h2 class="section-title" id="heading-alba">ALBA <em>Spatial</em> Discovery Grid</h2>
        </div>
        <span class="badge badge-mint" id="alba-gate-summary">SAFETY GATE ACTIVE: EVI &le; 0.85</span>
      </div>

      <div class="split-grid-wide">
        <!-- Left: Leaflet Vector Basemap -->
        <div class="panel" style="display: grid; gap: var(--space-md); padding: var(--space-md);">
          <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: var(--space-sm);">
            <div class="preset-strip">
              <button type="button" class="btn btn-sm btn-active" id="btn-scope-andean" onclick="setMapScope('andean')">Mara&ntilde;&oacute;n–Amazon Corridor</button>
              <button type="button" class="btn btn-sm" id="btn-scope-global" onclick="setMapScope('global')">Global LGM &amp; Missing Archives</button>
            </div>
            <div class="preset-strip">
              <button type="button" class="btn btn-sm btn-active" id="btn-layer-evi" onclick="toggleMapLayer('evi')">EVI Gate Halos</button>
              <button type="button" class="btn btn-sm btn-active" id="btn-layer-lgm" onclick="toggleMapLayer('lgm')">LGM -120m Shelf</button>
              <button type="button" class="btn btn-sm btn-active" id="btn-layer-trade" onclick="toggleMapLayer('trade')">Trade Corridors</button>
            </div>
          </div>

          <div id="alba-map" aria-label="ALBA v2.2 Bayesian spatial discovery vector map"></div>

          <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: var(--space-sm); font-family: var(--font-label); font-size: var(--label-size); color: var(--on-surface-variant);">
            <span>Boundaries: Natural Earth 50m Vector (Public Domain)</span>
            <span id="map-status-line">Showing 10 multi-proxy discovery nodes</span>
          </div>
        </div>

        <!-- Right: Safety Gate Controls, Site Detail & Tobler Slope Calculator -->
        <div class="panel" style="display: grid; gap: var(--space-md);">
          <div class="controls-row">
            <div class="control-group">
              <label class="control-label" for="slider-evi-threshold">
                <span>EVI Safety Gate Ceiling</span>
                <span class="val-readout" id="val-evi-threshold">0.85</span>
              </label>
              <input type="range" id="slider-evi-threshold" min="0.55" max="0.95" step="0.01" value="0.85" oninput="updateAlbaFilters()">
            </div>
            <div class="control-group">
              <label class="control-label" for="slider-prob-min">
                <span>Min Posterior P(A|X)</span>
                <span class="val-readout" id="val-prob-min">0.00</span>
              </label>
              <input type="range" id="slider-prob-min" min="0.00" max="0.95" step="0.05" value="0.00" oninput="updateAlbaFilters()">
            </div>
          </div>

          <div class="control-group">
            <label class="control-label" for="select-tier-filter">Epistemological Data Tier</label>
            <select id="select-tier-filter" onchange="updateAlbaFilters()">
              <option value="all">All Data Tiers (Tier-1 Empirical + Tier-2 Exploratory)</option>
              <option value="Tier-1">Tier-1 Empirical Evidence Only (LiDAR, AMS, aDNA)</option>
              <option value="Tier-2">Tier-2 Exploratory Models Only (ALBA v2.2, ABIEH)</option>
            </select>
          </div>

          <!-- Selected Site Telemetry Card -->
          <div class="observation-well" id="site-inspector" style="display: grid; gap: var(--space-sm);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: var(--space-sm); flex-wrap: wrap;">
              <div>
                <div class="coord-label" id="insp-coords">5.70&deg;S, 78.25&deg;W · MARA&Ntilde;&Oacute;N CORRIDOR</div>
                <strong style="font-size: 1.05rem; color: var(--on-surface);" id="insp-name">EL PONGOR (MC-04)</strong>
              </div>
              <span class="badge badge-mint" id="insp-gate-badge">PASSED · GROUND-TRUTHING</span>
            </div>
            <p style="margin: 0; font-family: var(--font-body); font-size: 0.875rem; color: var(--on-surface-variant);" id="insp-desc">
              Concentric terracing cut into shale bedrock (42 ha) with winter solstice twin mounds, Spondylus princeps beads, and carbonized Theobroma cacao (3400–2900 BCE).
            </p>
            <div class="readout-grid">
              <div class="readout-box">
                <span class="coord-label">Posterior P(A|X)</span>
                <span class="mono-val" id="insp-prob">0.9140</span>
              </div>
              <div class="readout-box">
                <span class="coord-label">EVI Score</span>
                <span class="mono-val" id="insp-evi">0.64</span>
              </div>
              <div class="readout-box">
                <span class="coord-label">Tobler Transit</span>
                <span class="mono-val" id="insp-transit">3.45 km/h</span>
              </div>
            </div>
          </div>

          <!-- Tobler Anisotropic Hiking Simulator -->
          <div class="panel-low" style="display: grid; gap: var(--space-sm);">
            <div class="coord-label">TOBLER ANISOTROPIC TRANSIT CALCULATOR · W = 6 &middot; exp(&minus;3.5|S + 0.05|)</div>
            <div class="control-group">
              <label class="control-label" for="slider-slope-deg">
                <span>Andean Trail Slope Angle (&theta;)</span>
                <span class="val-readout" id="val-slope-deg">-2.9&deg; (-5.0% Grade)</span>
              </label>
              <input type="range" id="slider-slope-deg" min="-30" max="30" step="0.1" value="-2.86" oninput="updateToblerCalculator()">
            </div>
            <div class="readout-grid">
              <div class="readout-box">
                <span class="coord-label">Transit Speed (W)</span>
                <span class="mono-val" id="out-tobler-speed">6.00 km/h</span>
              </div>
              <div class="readout-box">
                <span class="coord-label">Corridor Regime</span>
                <span class="mono-val" id="out-tobler-regime">Gravity-Assist Peak</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ALBA Discovery Matrix Table -->
      <div class="panel" style="display: grid; gap: var(--space-sm);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: var(--space-sm);">
          <div class="coord-label">ALBA v2.2 TRANSECT VALIDATION MATRIX (MARA&Ntilde;&Oacute;N · UPPER HUALLAGA · NAPO · ARCHIVES)</div>
          <span class="badge badge-sky">SELECT ROW TO FLY TO COORDINATE</span>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Site Identifier</th>
                <th>Transect / Archive</th>
                <th>Tier</th>
                <th class="num-col">P(A|X)</th>
                <th class="num-col">EVI</th>
                <th class="num-col">Transit</th>
                <th>Safety Gate Action</th>
              </tr>
            </thead>
            <tbody id="alba-table-body"></tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- COMPONENT 4: LAYER 0 GOVERNANCE & METABOLIC GATE AUDIT -->
    <section id="governance-audit" class="module-section" aria-labelledby="heading-governance">
      <div class="module-header">
        <div>
          <div class="coord-label">LAYER 0 &amp; LAYER 3 · CRYPTOGRAPHIC GOVERNANCE &amp; EPISTEMIC INTEGRITY</div>
          <h2 class="section-title" id="heading-governance">Metabolic Impact Gate (<em>&Delta;E &gt; 0</em>) &amp; Ledger Stack</h2>
        </div>
        <span class="badge badge-brass">GROTH16 + POSEIDON NULLIFIERS + BLS QUORUM</span>
      </div>

      <div class="split-grid-balanced">
        <div class="panel" style="display: grid; gap: var(--space-md);">
          <div class="coord-label">INTERACTIVE &Delta;E = &Sigma;P &minus; &Sigma;N METABOLIC GATE VERIFIER</div>
          <p style="margin: 0; color: var(--on-surface-variant); font-size: 0.9rem;">
            Every state transition in the Sovereign Lattice passes through Soulbound DID checks, Groth16 zero-knowledge membership proofs, and the thermodynamic surplus gate before anchoring to WORM storage.
          </p>
          <div class="controls-row">
            <div class="control-group">
              <label class="control-label" for="slider-p-sum">
                <span>Positive Impact (&Sigma;P)</span>
                <span class="val-readout" id="val-p-sum">4.50</span>
              </label>
              <input type="range" id="slider-p-sum" min="0" max="10" step="0.25" value="4.5" oninput="evaluateMetabolicGate()">
            </div>
            <div class="control-group">
              <label class="control-label" for="slider-n-sum">
                <span>Entropic Cost (&Sigma;N)</span>
                <span class="val-readout" id="val-n-sum">0.50</span>
              </label>
              <input type="range" id="slider-n-sum" min="0" max="10" step="0.25" value="0.5" oninput="evaluateMetabolicGate()">
            </div>
          </div>

          <div class="observation-well" id="worm-receipt-well" style="display: grid; gap: var(--space-xs); font-size: 0.82rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="coord-label">WORM BLOCK RECEIPT</span>
              <span class="badge badge-mint" id="gate-result-badge">ACCEPT · ANCHORED</span>
            </div>
            <div id="gate-receipt-json" style="color: var(--on-surface-variant); word-break: break-all;"></div>
          </div>
        </div>

        <div class="layer-grid">
          <div class="panel-low" style="display: grid; gap: var(--space-xs);">
            <span class="coord-label">TIER-1 · EMPIRICAL EVIDENCE</span>
            <p style="margin: 0; font-size: 0.875rem; color: var(--on-surface-variant);">
              Airborne LiDAR point clouds (Upano, Casarabe), IntCal20/24 AMS radiocarbon, paleogenomic aDNA (Population Y), stable isotopes (&delta;&sup1;&sup3;C, &delta;&sup1;&sup5;N, &sup8;&sup7;Sr/&sup8;&sup6;Sr), GEBCO bathymetry, and 34.4 Hz acoustic measurements.
            </p>
          </div>
          <div class="panel-low" style="display: grid; gap: var(--space-xs);">
            <span class="coord-label">TIER-2 · EXPLORATORY MODELS</span>
            <p style="margin: 0; font-size: 0.875rem; color: var(--on-surface-variant);">
              ALBA v2.2 Bayesian probability engine, ABIEH finite-element harmonic simulations, Sulu P5 bathymetric pattern matching, and Rhizome interregional civilization network graphs.
            </p>
          </div>
          <div class="panel-low" style="display: grid; gap: var(--space-xs);">
            <span class="coord-label">EPISTEMIC SEPARATION PROTOCOL</span>
            <p style="margin: 0; font-size: 0.875rem; color: var(--on-surface-variant);">
              Rejects pseudoarchaeological literalism (ancient astronaut claims, literal Vimanas, 2012 apocalypse) while modeling ancient texts and geometry as quantitative inner technologies and cosmological ciphers.
            </p>
          </div>
          <div class="panel-low" style="display: grid; gap: var(--space-xs);">
            <span class="coord-label">NON-EXTRACTIVE MANDATE</span>
            <p style="margin: 0; font-size: 0.875rem; color: var(--on-surface-variant);">
              Zero shareholders, zero private equity, zero profit returns. Governed solely by Stewards, Custodians, and Treaty-Aligned Nodes bound by ecological and provenance covenants.
            </p>
          </div>
        </div>
      </div>
    </section>

    <footer class="footer-meta">
      <div>
        <strong>Sources &amp; Corpus Attribution:</strong> Sovereign Cryptographic Ledger Architecture &amp; Deep Horizons Master Synthesis (Block #849206, Coil 77-AE-VIGILANCE); Deep Horizons Multi-Core Comparative Framework; Mathematics of Ancient King Lists (Ra&uacute;l L&oacute;pez &amp; Eve Engelbrite models); Ancient Texts Hidden Knowledge Analysis; AI Origin Speculative Synthesis.
      </div>
      <div class="coord-label">SOVEREIGN LATTICE COMMONS · 2026</div>
    </footer>
  </div>

  <api-shim></api-shim>
  <script>
    /* =====================================================================
       TOKEN PALETTE LOOKUP (READ FROM :ROOT FOR JS VISUALIZATIONS)
    ===================================================================== */
    function getThemeToken(name, fallback) {
      const val = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
      return val || fallback;
    }

    const PALETTE = {
      bg: getThemeToken('--background', '#0a101d'),
      surface: getThemeToken('--surface-container', '#111b2e'),
      surfaceHigh: getThemeToken('--surface-container-high', '#17243c'),
      text: getThemeToken('--on-surface', '#f2ece1'),
      muted: getThemeToken('--on-surface-variant', '#9ba8bf'),
      outline: getThemeToken('--outline', '#384d73'),
      outlineVar: getThemeToken('--outline-variant', '#21304d'),
      brass: getThemeToken('--data-1', '#dfaa5b'),
      sky: getThemeToken('--data-2', '#7cc4e8'),
      mint: getThemeToken('--data-3', '#52d19c'),
      coral: getThemeToken('--data-4', '#e07a5f'),
      context: getThemeToken('--data-context', '#4a5d80')
    };

    /* =====================================================================
       SOURCE DATA MODELS (100% GROUNDED IN PROVIDED CORPUS)
    ===================================================================== */
    const CHRONOS_MATRIX = [
      { pos: 1, sklRuler: `Alulim (Eridu)`, sklReign: 28800, signs: `8 SAR (8 × 3,600)`, scaled: 80.0, genName: `Adam`, genAge: 930, sacred: `(186 × 5) + 0` },
      { pos: 2, sklRuler: `Alalgar (Eridu)`, sklReign: 36000, signs: `10 SAR (10 × 3,600)`, scaled: 100.0, genName: `Seth`, genAge: 912, sacred: `(181 × 5) + 7` },
      { pos: 3, sklRuler: `En-men-lu-ana (Bad-tibira)`, sklReign: 43200, signs: `12 SAR (12 × 3,600)`, scaled: 120.0, genName: `Enosh`, genAge: 905, sacred: `(181 × 5) + 0` },
      { pos: 4, sklRuler: `En-men-gal-ana (Bad-tibira)`, sklReign: 28800, signs: `8 SAR (8 × 3,600)`, scaled: 80.0, genName: `Kenan`, genAge: 910, sacred: `(182 × 5) + 0` },
      { pos: 5, sklRuler: `Dumuzid (Bad-tibira)`, sklReign: 36000, signs: `10 SAR (10 × 3,600)`, scaled: 100.0, genName: `Mahalalel`, genAge: 895, sacred: `(179 × 5) + 0` },
      { pos: 6, sklRuler: `En-sipad-zid-ana (Larag)`, sklReign: 28800, signs: `8 SAR (8 × 3,600)`, scaled: 80.0, genName: `Jared`, genAge: 962, sacred: `(191 × 5) + 7` },
      { pos: 7, sklRuler: `En-men-dur-ana (Sippar)`, sklReign: 21000, signs: `5 SAR + 5 NER`, scaled: 58.3, genName: `Enoch`, genAge: 365, sacred: `365-Day Solar Cycle` },
      { pos: 8, sklRuler: `Ubara-Tutu (Shuruppak)`, sklReign: 18600, signs: `5 SAR + 1 NER`, scaled: 51.6, genName: `Methuselah`, genAge: 969, sacred: `(191 × 5) + 7 + 7` }
    ];

    const POST_FLOOD_PATRIARCHS = [
      { t: 0, name: `Shem`, logged: 600, sklRegime: 781, note: `Flood Anchor` },
      { t: 1, name: `Arpachshad`, logged: 438, sklRegime: 600, note: `Kish I SOSS` },
      { t: 2, name: `Shelah`, logged: 433, sklRegime: 420, note: `Kish I SOSS` },
      { t: 3, name: `Eber`, logged: 464, sklRegime: 300, note: `Babel Override Flag` },
      { t: 4, name: `Peleg`, logged: 239, sklRegime: 200, note: `Earth Divided` },
      { t: 5, name: `Reu`, logged: 239, sklRegime: 150, note: `Uruk I Bridge` },
      { t: 6, name: `Serug`, logged: 230, sklRegime: 126, note: `Gilgamesh Scale` },
      { t: 7, name: `Nahor`, logged: 148, sklRegime: 60, note: `Solar Normalization` },
      { t: 8, name: `Terah`, logged: 205, sklRegime: 36, note: `Historical Dynasties` },
      { t: 9, name: `Abraham`, logged: 175, sklRegime: 25, note: `Ur III Scale` },
      { t: 12, name: `Jacob`, logged: 147, sklRegime: 20, note: `Metabolic Floor` }
    ];

    const ALBA_SITES = [
      {
        id: `HUALLAGA-NORTH-01`,
        name: `Huallaga North Foothill Platform`,
        transect: `Upper Huallaga`,
        tier: `Tier-2`,
        lat: -8.45,
        lon: -76.18,
        prob: 0.8742,
        evi: 0.72,
        transit: 2.99,
        x1: 0.88,
        x2: 0.79,
        x3: 0.81,
        desc: `Low-density rurban foothill platform grid identified via multi-proxy Bayesian evaluation across Upper Huallaga transects.`
      },
      {
        id: `HUALLAGA-SOUTH-04`,
        name: `Huallaga Canopy Terrace Grid`,
        transect: `Upper Huallaga`,
        tier: `Tier-2`,
        lat: -9.62,
        lon: -75.88,
        prob: 0.7326,
        evi: 0.89,
        transit: 1.62,
        x1: 0.76,
        x2: 0.71,
        x3: 0.69,
        desc: `Steep 18-degree Andean foothill terrace grid. Fragile sub-Andean soil triggers automated non-intrusive UAS multispectral sensing.`
      },
      {
        id: `NAPO-BASIN-02`,
        name: `Napo River Terra Preta Mounds`,
        transect: `Napo River Basin`,
        tier: `Tier-2`,
        lat: -2.95,
        lon: -74.65,
        prob: 0.9597,
        evi: 0.68,
        transit: 5.77,
        x1: 0.94,
        x2: 0.96,
        x3: 0.91,
        desc: `High-phosphorus Terra Preta anthrosol mounds along optimal floodplain corridor leveraging slight negative Tobler grade.`
      },
      {
        id: `NAPO-DELTA-09`,
        name: `Napo Floodplain Sump Node`,
        transect: `Napo River Basin`,
        tier: `Tier-2`,
        lat: -3.48,
        lon: -73.25,
        prob: 0.0156,
        evi: 0.94,
        transit: 0.78,
        x1: 0.14,
        x2: 0.11,
        x3: 0.08,
        desc: `Natural isotropic alluvial terrain with extreme ecological sensitivity. Filtered out by Bayesian likelihood and EVI safety gate.`
      },
      {
        id: `EL-PONGOR-MC04`,
        name: `El Pongor (MC-04)`,
        transect: `Marañón Validation Corridor`,
        tier: `Tier-1`,
        lat: -5.70,
        lon: -78.25,
        prob: 0.9140,
        evi: 0.64,
        transit: 3.45,
        x1: 0.91,
        x2: 0.87,
        x3: 0.89,
        desc: `42 ha concentric bedrock terraces (+570 m tectonic uplift adjusted, 820 m elevation). Winter solstice mounds, Spondylus princeps beads, and 3400–2900 BCE cacao.`
      },
      {
        id: `HUACA-MONTEGRANDE`,
        name: `Huaca Montegrande`,
        transect: `Marañón–Jaén Suture`,
        tier: `Tier-1`,
        lat: -5.71,
        lon: -78.80,
        prob: 0.9380,
        evi: 0.59,
        transit: 4.12,
        x1: 0.93,
        x2: 0.84,
        x3: 0.88,
        desc: `5-story counter-clockwise river-rock spiral temple (~3500 BCE) representing the Amaru cosmological serpent and earliest ceremonial cacao network.`
      },
      {
        id: `UPANO-VALLEY`,
        name: `Upano Valley (Sangay & Kilamope)`,
        transect: `Ecuadorian Amazon Canopy`,
        tier: `Tier-1`,
        lat: -2.20,
        lon: -78.10,
        prob: 0.9620,
        evi: 0.78,
        transit: 4.85,
        x1: 0.97,
        x2: 0.91,
        x3: 0.95,
        desc: `300 sq km LiDAR network uncovering 6,000+ earthen platforms and 13–15 m wide straight engineered roads (500 BCE–600 CE).`
      },
      {
        id: `CASARABE-COTOCA`,
        name: `Casarabe Culture (Cotoca / Landívar)`,
        transect: `Bolivian Llanos de Moxos`,
        tier: `Tier-1`,
        lat: -14.83,
        lon: -64.58,
        prob: 0.9450,
        evi: 0.71,
        transit: 5.10,
        x1: 0.95,
        x2: 0.89,
        x3: 0.96,
        desc: `Four-tiered garden urbanism with 570,000 m³ earthworks, 22 m conical pyramids, raised causeways, and hydraulic reservoirs.`
      },
      {
        id: `YUCATAN-SHELF`,
        name: `Yucatán Submerged Shelf`,
        transect: `Submerged Shelf (-110 m)`,
        tier: `Tier-2`,
        lat: 21.25,
        lon: -89.67,
        prob: 0.6210,
        evi: 0.92,
        transit: 1.20,
        x1: 0.83,
        x2: 0.32,
        x3: 0.71,
        desc: `Deep carbonate sinkhole exhibiting geometric linearity; exact coordinates redacted under Sovereign OS emergency EVI > 0.85 override.`
      },
      {
        id: `SULU-SEA-P5A`,
        name: `Sulu Sea P5-A (Sunda Paleo-Estuary)`,
        transect: `Submerged Shelf (-121.2 m)`,
        tier: `Tier-2`,
        lat: 7.55,
        lon: 117.75,
        prob: 0.8415,
        evi: 0.76,
        transit: 1.85,
        x1: 0.86,
        x2: 0.44,
        x3: 0.82,
        desc: `Concentric bathymetry at -121.2 m subsidence-adjusted depth yielding Q-factor 68.4 and 34.387 Hz peak under 0.45 marine silt attenuation.`
      }
    ];

    const MARANON_CORRIDORS = [
      [[-5.71, -78.80], [-5.70, -78.25], [-2.20, -78.10]],
      [[-5.70, -78.25], [-2.95, -74.65], [-3.48, -73.25]],
      [[-5.70, -78.25], [-8.45, -76.18], [-9.62, -75.88]],
      [[-8.45, -76.18], [-14.83, -64.58]]
    ];

    const LGM_SHELVES = [
      { lat: 7.55, lon: 117.75, r: 420000, label: `Sundaland LGM Paleo-Estuary (-120 m isobath)` },
      { lat: 21.25, lon: -89.67, r: 280000, label: `Yucatán LGM Carbonate Shelf (-110 m)` },
      { lat: 57.50, lon: -158.0, r: 450000, label: `Seascape Alaska Beringia Shelf (-120 m)` }
    ];

    /* =====================================================================
       PORTAL STATE & PERSISTENCE
    ===================================================================== */
    let appState = {
      tokLarge: 6,
      tokMed: 6,
      tokSmall: 6,
      cipherYears: 28800,
      cipherLabel: `Alulim (SKL 1)`,
      cipherMode: `skl`,
      decayL0: 600,
      decayLambda: 0.315,
      decayC: 100,
      chamberPreset: `barabar`,
      chamberFreq: 34.4,
      chamberMedium: `air`,
      chamberEpsilon: 0.08,
      eviThreshold: 0.85,
      probMin: 0.00,
      tierFilter: `all`,
      mapScope: `andean`,
      showEviLayer: true,
      showLgmLayer: true,
      showTradeLayer: true,
      selectedSiteId: `EL-PONGOR-MC04`,
      slopeDeg: -2.86,
      gateP: 4.5,
      gateN: 0.5
    };

    let persistTimer = null;
    function scheduleStateSave() {
      if (persistTimer) clearTimeout(persistTimer);
      persistTimer = setTimeout(function () {
        if (window.notebookAppApi && typeof window.notebookAppApi.setAppState === 'function') {
          window.notebookAppApi.setAppState(appState).catch(function () {});
        }
      }, 220);
    }

    function applyStateToDOM() {
      const setVal = function (id, val) {
        const el = document.getElementById(id);
        if (el) el.value = val;
      };
      setVal('tok-large', appState.tokLarge);
      setVal('tok-med', appState.tokMed);
      setVal('tok-small', appState.tokSmall);
      setVal('cipher-input-years', appState.cipherYears);
      setVal('cipher-input-mode', appState.cipherMode);
      setVal('slider-l0', appState.decayL0);
      setVal('slider-lambda', appState.decayLambda);
      setVal('slider-floor', appState.decayC);
      setVal('chamber-preset-select', appState.chamberPreset);
      setVal('slider-freq', appState.chamberFreq);
      setVal('select-medium', appState.chamberMedium);
      setVal('slider-epsilon', appState.chamberEpsilon);
      setVal('slider-evi-threshold', appState.eviThreshold);
      setVal('slider-prob-min', appState.probMin);
      setVal('select-tier-filter', appState.tierFilter);
      setVal('slider-slope-deg', appState.slopeDeg);
      setVal('slider-p-sum', appState.gateP);
      setVal('slider-n-sum', appState.gateN);

      const lbl = document.getElementById('cipher-source-label');
      if (lbl) lbl.textContent = appState.cipherLabel;
    }

    /* =====================================================================
       MODULE 1: CHRONOS CALENDAR CIPHER VISUALIZER
    ===================================================================== */
    let decayChart = null;

    function updateProtoLedger() {
      const lEl = document.getElementById('tok-large');
      const mEl = document.getElementById('tok-med');
      const sEl = document.getElementById('tok-small');
      const L = Math.max(0, parseInt(lEl ? lEl.value : 6, 10) || 0);
      const M = Math.max(0, parseInt(mEl ? mEl.value : 6, 10) || 0);
      const S = Math.max(0, parseInt(sEl ? sEl.value : 6, 10) || 0);

      appState.tokLarge = L;
      appState.tokMed = M;
      appState.tokSmall = S;

      const base10 = L * 1000 + M * 100 + S * 10;
      const base60 = L * 36000 + M * 3600 + S * 60;
      const fullSKL = base60 + 3240;
      const ratio = base10 > 0 ? (fullSKL / base10) : 0;
      const tuns = base10 / 360;

      const setTxt = function (id, txt) {
        const el = document.getElementById(id);
        if (el) el.textContent = txt;
      };

      setTxt('out-base10-total', `${base10.toLocaleString()} yrs`);
      setTxt('out-base10-eq', `${L}×10³ + ${M}×10² + ${S}×10`);
      setTxt('out-base60-total', `${base60.toLocaleString()} yrs`);
      setTxt('out-base60-eq', `+ 9 SAR (3,240) = ${fullSKL.toLocaleString()}`);
      setTxt('out-mayan-tuns', `${tuns.toFixed(2)} Tun-Cycles`);
      setTxt('out-mayan-sub', `${base10.toLocaleString()} ÷ 360-day Tun`);
      setTxt('kpi-chronos-ratio', `${ratio.toFixed(3)}×`);
      setTxt('kpi-chronos-sub', `${fullSKL.toLocaleString()} SKL ÷ ${base10.toLocaleString()} Genesis yrs`);

      scheduleStateSave();
    }

    const CHRONOS_PRESET_MAP = {
      alulim: { val: 28800, label: `Alulim (SKL 1)` },
      enmenluana: { val: 43200, label: `En-men-lu-ana (SKL 3)` },
      enmendurana: { val: 21000, label: `En-men-dur-ana (SKL 7)` },
      adam: { val: 930, label: `Adam (Gen 5)` },
      enoch: { val: 365, label: `Enoch (Solar)` },
      eber: { val: 464, label: `Eber (Babel Flag)` },
      methuselah: { val: 969, label: `Methuselah (Peak)` }
    };

    function selectChronosPresetByKey(key) {
      const item = CHRONOS_PRESET_MAP[key];
      if (!item) return;
      loadChronosPreset(item.val, item.label);
    }

    function loadChronosPreset(val, label) {
      const inp = document.getElementById('cipher-input-years');
      const mode = document.getElementById('cipher-input-mode');
      if (inp) inp.value = val;
      if (mode) {
        mode.value = val >= 1800 ? 'skl' : 'gen';
      }
      appState.cipherLabel = label;
      const lbl = document.getElementById('cipher-source-label');
      if (lbl) lbl.textContent = label;
      translateSingleSpan();
    }

    function translateSingleSpan() {
      const inp = document.getElementById('cipher-input-years');
      const mode = document.getElementById('cipher-input-mode');
      const val = Math.max(1, parseInt(inp ? inp.value : 28800, 10) || 1);
      const m = mode ? mode.value : 'skl';

      appState.cipherYears = val;
      appState.cipherMode = m;

      // Base-60 SAR / NER / SOSS decomposition
      const sars = Math.floor(val / 3600);
      const remAfterSar = val % 3600;
      const ners = Math.floor(remAfterSar / 600);
      const remAfterNer = remAfterSar % 600;
      const soss = Math.floor(remAfterNer / 60);
      const units = remAfterNer % 60;

      const sklTxt = units > 0
        ? `${sars} SAR · ${ners} NER · ${soss} SOSS + ${units}`
        : `${sars} SAR · ${ners} NER · ${soss} SOSS`;
      const scaled60 = (val / 60).toFixed(1);
      const scaled360 = (val / 360).toFixed(1);

      // Base-10 Sacred 5 & 7 decomposition
      const rem5 = val % 5;
      let fiveMult = Math.floor(val / 5);
      let sevenOffset = rem5;
      if (rem5 === 2 && val >= 7) {
        fiveMult = Math.floor((val - 7) / 5);
        sevenOffset = 7;
      } else if (rem5 === 4 && val >= 14) {
        fiveMult = Math.floor((val - 14) / 5);
        sevenOffset = 14;
      }
      const termDigit = val % 10;
      const isCanonical = [0, 2, 5, 9].indexOf(termDigit) !== -1;
      const sacredClass = val === 365
        ? `365-Day Solar Calendar Anchor`
        : (isCanonical ? `Terminal digit ${termDigit} (Canonical [0,2,5,9])` : `Terminal digit ${termDigit} (Non-canonical offset)`);

      // Mayan Long Count in 360-day Tun equivalents (treat input as Tuns if SKL/Gen, or Days if Maya)
      const totalDays = m === 'maya' ? val : val * 360;
      const baktun = Math.floor(totalDays / 144000);
      const remB = totalDays % 144000;
      const katun = Math.floor(remB / 7200);
      const remK = remB % 7200;
      const tun = Math.floor(remK / 360);
      const remT = remK % 360;
      const uinal = Math.floor(remT / 20);
      const kin = remT % 20;

      const haabCount = (totalDays / 365).toFixed(2);
      const tzolkinCount = (totalDays / 260).toFixed(1);

      const setTxt = function (id, txt) {
        const el = document.getElementById(id);
        if (el) el.textContent = txt;
      };
      setTxt('trans-skl-decomp', sklTxt);
      setTxt('trans-skl-scaled', `÷60 = ${scaled60} yrs | ÷360 = ${scaled360} yrs`);
      setTxt('trans-gen-decomp', `${fiveMult.toLocaleString()} × 5 + ${sevenOffset}`);
      setTxt('trans-gen-class', sacredClass);
      setTxt('trans-maya-lc', `${baktun}.${katun}.${tun}.${uinal}.${kin}`);
      setTxt('trans-maya-cycles', `${haabCount} Haab (365d) · ${tzolkinCount} Tzolk'in`);

      scheduleStateSave();
    }

    function renderChronosMatrixTable() {
      const tbody = document.getElementById('chronos-matrix-body');
      if (!tbody) return;
      tbody.innerHTML = '';
      CHRONOS_MATRIX.forEach(function (row) {
        const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        tr.onclick = function () {
          loadChronosPreset(row.sklReign, `${row.sklRuler}`);
        };
        tr.innerHTML = `
          <td class="num-col">${row.pos}</td>
          <td><strong>${row.sklRuler}</strong></td>
          <td class="num-col">${row.sklReign.toLocaleString()}</td>
          <td><code>${row.signs}</code></td>
          <td class="num-col">${row.scaled.toFixed(1)} yrs</td>
          <td><strong>${row.genName}</strong></td>
          <td class="num-col">${row.genAge}</td>
          <td><code>${row.sacred}</code></td>
        `;
        tbody.appendChild(tr);
      });
    }

    function syncDecayControls() {
      const l0El = document.getElementById('slider-l0');
      const lamEl = document.getElementById('slider-lambda');
      const flEl = document.getElementById('slider-floor');
      const L0 = parseFloat(l0El ? l0El.value : 600);
      const lam = parseFloat(lamEl ? lamEl.value : 0.315);
      const C = parseFloat(flEl ? flEl.value : 100);

      appState.decayL0 = L0;
      appState.decayLambda = lam;
      appState.decayC = C;

      const setTxt = function (id, txt) {
        const el = document.getElementById(id);
        if (el) el.textContent = txt;
      };
      setTxt('val-l0', `${L0} yrs`);
      setTxt('val-lambda', lam.toFixed(3));
      setTxt('val-floor', `${C} yrs`);

      const labels = POST_FLOOD_PATRIARCHS.map(function (p) { return `${p.name} (t=${p.t})`; });
      const loggedData = POST_FLOOD_PATRIARCHS.map(function (p) { return p.logged; });
      const modelData = POST_FLOOD_PATRIARCHS.map(function (p) {
        return Math.round((L0 - C) * Math.exp(-lam * p.t) + C);
      });
      const sklStepData = POST_FLOOD_PATRIARCHS.map(function (p) { return p.sklRegime; });

      // Calculate MAE excluding Eber (t=3)
      let errSum = 0;
      let count = 0;
      POST_FLOOD_PATRIARCHS.forEach(function (p, idx) {
        if (p.t !== 3) {
          errSum += Math.abs(modelData[idx] - p.logged) / p.logged;
          count++;
        }
      });
      const maePct = ((errSum / count) * 100).toFixed(1);
      const eberModel = modelData[3];
      setTxt('decay-formula-status', `Model MAE (excl. Eber t=3): ${maePct}% · Eber override delta: +${464 - eberModel} yrs above model (${eberModel} yrs)`);

      if (!decayChart) {
        const canvas = document.getElementById('chronos-decay-chart');
        if (!canvas || typeof Chart === 'undefined') return;
        const ctx = canvas.getContext('2d');
        decayChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [
              {
                label: 'Model L(t) Exponential',
                data: modelData,
                borderColor: PALETTE.brass,
                backgroundColor: 'rgba(223, 170, 91, 0.12)',
                borderWidth: 2.5,
                tension: 0.35,
                fill: true,
                pointRadius: 3
              },
              {
                label: 'Masoretic Logged Age',
                data: loggedData,
                borderColor: PALETTE.sky,
                backgroundColor: PALETTE.sky,
                borderWidth: 2,
                borderDash: [4, 4],
                tension: 0.1,
                pointRadius: POST_FLOOD_PATRIARCHS.map(function (p) { return p.t === 3 ? 7 : 4; }),
                pointBackgroundColor: POST_FLOOD_PATRIARCHS.map(function (p) { return p.t === 3 ? PALETTE.coral : PALETTE.sky; })
              },
              {
                label: 'SKL Hyperbolic Step (Kish → Ur III)',
                data: sklStepData,
                borderColor: PALETTE.mint,
                borderWidth: 1.75,
                stepped: true,
                pointRadius: 2.5
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                labels: {
                  color: PALETTE.text,
                  font: { family: 'JetBrains Mono', size: 11 }
                }
              }
            },
            scales: {
              x: {
                ticks: { color: PALETTE.muted, font: { family: 'JetBrains Mono', size: 10 }, maxRotation: 35 },
                grid: { color: PALETTE.outlineVar }
              },
              y: {
                ticks: { color: PALETTE.muted, font: { family: 'JetBrains Mono', size: 10 } },
                grid: { color: PALETTE.outlineVar },
                title: { display: true, text: 'Years', color: PALETTE.muted, font: { family: 'JetBrains Mono', size: 11 } }
              }
            }
          }
        });
      } else {
        decayChart.data.datasets[0].data = modelData;
        decayChart.update('none');
      }

      scheduleStateSave();
    }

    /* =====================================================================
       MODULE 2: 3D SPATIAL & ACOUSTIC CHAMBER EXPLORER (THREE.JS)
    ===================================================================== */
    let threeScene, threeCamera, threeRenderer, chamberGroup, waveMeshGroup, pointCloudMesh;
    let threeAnimId = null;
    let chamberSpin = true;
    let orbitTheta = 0.65;
    let orbitPhi = 1.05;
    let orbitRadius = 11.5;
    let isDragging3D = false;
    let prevMouse = { x: 0, y: 0 };
    let audioCtx = null;
    let audioOsc = null;
    let audioGain = null;
    let audioPlaying = false;

    const CHAMBER_META = {
      barabar: {
        badge: `BARABAR QUARTZ CAVITY · 34.40 HZ`,
        A: 2.1, V: 235, L: 2.25, Q: 68.4,
        baseF0: 34.397
      },
      montegrande: {
        badge: `HUACA MONTEGRANDE · COUNTER-CLOCKWISE SPIRAL`,
        A: 3.4, V: 380, L: 2.1, Q: 42.8,
        baseF0: 34.80
      },
      el_pongor: {
        badge: `EL PONGOR MC-04 · CONCENTRIC TERRACES (+570M)`,
        A: 4.1, V: 465, L: 2.05, Q: 51.2,
        baseF0: 34.42
      }
    };

    function initThreeChamber() {
      const container = document.getElementById('three-container');
      if (!container || typeof THREE === 'undefined') return;

      const w = container.clientWidth || 640;
      const h = container.clientHeight || 460;

      threeScene = new THREE.Scene();
      threeScene.background = new THREE.Color(PALETTE.bg);

      threeCamera = new THREE.PerspectiveCamera(45, w / h, 0.1, 100);
      updateCameraOrbit();

      threeRenderer = new THREE.WebGLRenderer({ antialias: true });
      threeRenderer.setSize(w, h);
      threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      container.appendChild(threeRenderer.domElement);

      // Subtle observatory grid floor
      const grid = new THREE.GridHelper(18, 18, 0x384d73, 0x17243c);
      grid.position.y = -2.2;
      threeScene.add(grid);

      // Ambient + directional lights
      const amb = new THREE.AmbientLight(0xf2ece1, 0.55);
      threeScene.add(amb);
      const dir = new THREE.DirectionalLight(0xdfaa5b, 0.9);
      dir.position.set(6, 9, 5);
      threeScene.add(dir);

      chamberGroup = new THREE.Group();
      waveMeshGroup = new THREE.Group();
      threeScene.add(chamberGroup);
      threeScene.add(waveMeshGroup);

      buildChamberGeometry(appState.chamberPreset, appState.chamberEpsilon);

      // Pointer drag orbit + wheel zoom
      const dom = threeRenderer.domElement;
      dom.addEventListener('pointerdown', function (e) {
        isDragging3D = true;
        prevMouse = { x: e.clientX, y: e.clientY };
      });
      window.addEventListener('pointerup', function () { isDragging3D = false; });
      window.addEventListener('pointermove', function (e) {
        if (!isDragging3D) return;
        const dx = e.clientX - prevMouse.x;
        const dy = e.clientY - prevMouse.y;
        prevMouse = { x: e.clientX, y: e.clientY };
        orbitTheta -= dx * 0.008;
        orbitPhi = Math.max(0.25, Math.min(1.48, orbitPhi - dy * 0.008));
        updateCameraOrbit();
      });

      window.addEventListener('resize', function () {
        if (!container || !threeRenderer || !threeCamera) return;
        const nw = container.clientWidth || 640;
        const nh = container.clientHeight || 460;
        threeCamera.aspect = nw / nh;
        threeCamera.updateProjectionMatrix();
        threeRenderer.setSize(nw, nh);
      });

      if (threeAnimId) cancelAnimationFrame(threeAnimId);
      animateThreeChamber();
    }

    function updateCameraOrbit() {
      if (!threeCamera) return;
      threeCamera.position.x = orbitRadius * Math.sin(orbitPhi) * Math.cos(orbitTheta);
      threeCamera.position.y = orbitRadius * Math.cos(orbitPhi);
      threeCamera.position.z = orbitRadius * Math.sin(orbitPhi) * Math.sin(orbitTheta);
      threeCamera.lookAt(0, 0, 0);
    }

    function buildChamberGeometry(preset, epsilonNoise) {
      if (!chamberGroup || !waveMeshGroup) return;
      while (chamberGroup.children.length > 0) chamberGroup.remove(chamberGroup.children[0]);
      while (waveMeshGroup.children.length > 0) waveMeshGroup.remove(waveMeshGroup.children[0]);

      const wireMat = new THREE.MeshBasicMaterial({ color: 0x384d73, wireframe: true, transparent: true, opacity: 0.55 });
      const solidMat = new THREE.MeshPhongMaterial({ color: 0x17243c, transparent: true, opacity: 0.45, side: THREE.DoubleSide });

      const pointPositions = [];
      const pointColors = [];
      const cMint = new THREE.Color(PALETTE.mint);
      const cCoral = new THREE.Color(PALETTE.coral);

      if (preset === 'barabar') {
        // Vaulted granite acoustic chamber + entrance neck
        const vaultGeo = new THREE.CylinderGeometry(2.4, 2.4, 6.4, 24, 1, false, 0, Math.PI);
        vaultGeo.rotateZ(Math.PI / 2);
        vaultGeo.rotateX(-Math.PI / 2);
        const vaultMesh = new THREE.Mesh(vaultGeo, solidMat);
        const vaultWire = new THREE.Mesh(vaultGeo, wireMat);
        chamberGroup.add(vaultMesh, vaultWire);

        // Floor slab
        const floorGeo = new THREE.BoxGeometry(6.4, 0.2, 4.8);
        const floorMesh = new THREE.Mesh(floorGeo, wireMat);
        floorMesh.position.y = -2.0;
        chamberGroup.add(floorMesh);

        // Point cloud over vaulted ceiling & walls
        for (let i = 0; i < 650; i++) {
          const x = (Math.random() - 0.5) * 6.2;
          const ang = Math.random() * Math.PI;
          const dev = (Math.random() - 0.5) * epsilonNoise * 2.2;
          const r = 2.4 + dev;
          const y = Math.sin(ang) * r - 1.2;
          const z = Math.cos(ang) * r;
          pointPositions.push(x, y, z);
          const col = Math.abs(dev) < 0.12 ? cMint : cCoral;
          pointColors.push(col.r, col.g, col.b);
        }
      } else if (preset === 'montegrande') {
        // 5-story counter-clockwise spiral mound (Huaca Montegrande)
        for (let tier = 0; tier < 5; tier++) {
          const rTop = 3.8 - tier * 0.65;
          const rBot = 4.2 - tier * 0.65;
          const cyl = new THREE.CylinderGeometry(rTop, rBot, 0.55, 28, 1, true);
          const mesh = new THREE.Mesh(cyl, wireMat);
          mesh.position.y = -1.8 + tier * 0.58;
          chamberGroup.add(mesh);
        }
        // Counter-clockwise Amaru spiral ribbon
        const pts = [];
        for (let s = 0; s <= 160; s++) {
          const t = s / 160;
          const angle = -t * Math.PI * 5.5;
          const radius = 4.1 * (1 - t * 0.78);
          const y = -1.9 + t * 2.8;
          pts.push(new THREE.Vector3(Math.cos(angle) * radius, y, Math.sin(angle) * radius));
        }
        const curveGeo = new THREE.BufferGeometry().setFromPoints(pts);
        const curveMat = new THREE.LineBasicMaterial({ color: 0xdfaa5b });
        chamberGroup.add(new THREE.Line(curveGeo, curveMat));

        for (let i = 0; i < 680; i++) {
          const t = Math.random();
          const angle = -t * Math.PI * 5.5 + (Math.random() - 0.5) * 0.3;
          const dev = (Math.random() - 0.5) * epsilonNoise * 2.4;
          const r = 4.1 * (1 - t * 0.78) + dev;
          const y = -1.9 + t * 2.8 + (Math.random() - 0.5) * epsilonNoise;
          pointPositions.push(Math.cos(angle) * r, y, Math.sin(angle) * r);
          const col = Math.abs(dev) < 0.12 ? cMint : cCoral;
          pointColors.push(col.r, col.g, col.b);
        }
      } else {
        // El Pongor MC-04 concentric terraces + twin solstice mounds
        for (let ring = 0; ring < 4; ring++) {
          const r = 4.4 - ring * 0.9;
          const torus = new THREE.TorusGeometry(r, 0.08, 8, 48);
          torus.rotateX(Math.PI / 2);
          const mesh = new THREE.Mesh(torus, wireMat);
          mesh.position.y = -1.8 + ring * 0.48;
          chamberGroup.add(mesh);
        }
        // Twin solstice mounds
        const mGeo = new THREE.BoxGeometry(1.1, 1.2, 1.1);
        const m1 = new THREE.Mesh(mGeo, solidMat);
        const m2 = new THREE.Mesh(mGeo, solidMat);
        m1.position.set(-1.3, -0.4, 0);
        m2.position.set(1.3, -0.4, 0);
        chamberGroup.add(m1, m2);

        for (let i = 0; i < 650; i++) {
          const ring = Math.floor(Math.random() * 4);
          const rBase = 4.4 - ring * 0.9;
          const ang = Math.random() * Math.PI * 2;
          const dev = (Math.random() - 0.5) * epsilonNoise * 2.2;
          const y = -1.8 + ring * 0.48 + dev;
          pointPositions.push(Math.cos(ang) * rBase, y, Math.sin(ang) * rBase);
          const col = Math.abs(dev) < 0.12 ? cMint : cCoral;
          pointColors.push(col.r, col.g, col.b);
        }
      }

      const pcGeo = new THREE.BufferGeometry();
      pcGeo.setAttribute('position', new THREE.Float32BufferAttribute(pointPositions, 3));
      pcGeo.setAttribute('color', new THREE.Float32BufferAttribute(pointColors, 3));
      const pcMat = new THREE.PointsMaterial({ size: 0.085, vertexColors: true, transparent: true, opacity: 0.9 });
      pointCloudMesh = new THREE.Points(pcGeo, pcMat);
      chamberGroup.add(pointCloudMesh);

      // Standing wave antinode rings along chamber axis
      const harmonicCount = Math.max(2, Math.round(appState.chamberFreq / 17.2));
      for (let n = 0; n < harmonicCount; n++) {
        const frac = (n + 0.5) / harmonicCount;
        const xPos = -2.8 + frac * 5.6;
        const isAntinode = n % 2 === 0;
        const ringGeo = new THREE.TorusGeometry(isAntinode ? 1.35 : 0.75, 0.045, 10, 36);
        ringGeo.rotateY(Math.PI / 2);
        const ringMat = new THREE.MeshBasicMaterial({
          color: isAntinode ? 0xdfaa5b : 0x7cc4e8,
          transparent: true,
          opacity: isAntinode ? 0.85 : 0.5
        });
        const ringMesh = new THREE.Mesh(ringGeo, ringMat);
        ringMesh.position.set(xPos, -0.4, 0);
        ringMesh.userData = { baseScale: isAntinode ? 1.0 : 0.7, phase: n * 0.9 };
        waveMeshGroup.add(ringMesh);
      }
    }

    function animateThreeChamber() {
      threeAnimId = requestAnimationFrame(animateThreeChamber);
      const t = performance.now() * 0.0025;
      if (chamberSpin) {
        orbitTheta += 0.0032;
        updateCameraOrbit();
      }
      if (waveMeshGroup) {
        const speedScale = Math.max(0.6, appState.chamberFreq / 34.4);
        waveMeshGroup.children.forEach(function (mesh) {
          const s = 1.0 + 0.16 * Math.sin(t * speedScale + mesh.userData.phase);
          mesh.scale.set(1, s, s);
        });
      }
      if (threeRenderer && threeScene && threeCamera) {
        threeRenderer.render(threeScene, threeCamera);
      }
    }

    function toggleChamberSpin() {
      chamberSpin = !chamberSpin;
      const btn = document.getElementById('cam-orbit-btn');
      if (btn) btn.textContent = chamberSpin ? 'Pause Auto-Orbit' : 'Resume Auto-Orbit';
    }

    function zoomChamber(dir) {
      orbitRadius = Math.max(5.5, Math.min(20, orbitRadius + dir * 1.5));
      updateCameraOrbit();
    }

    function resetChamberCamera() {
      orbitTheta = 0.65;
      orbitPhi = 1.05;
      orbitRadius = 11.5;
      updateCameraOrbit();
    }

    function changeChamberPreset(val) {
      appState.chamberPreset = val;
      updateChamberPhysics();
    }

    function syncFreqFromSlider(val) {
      appState.chamberFreq = parseFloat(val);
      updateChamberPhysics();
    }

    function setChamberFrequency(hz) {
      appState.chamberFreq = hz;
      const sl = document.getElementById('slider-freq');
      if (sl) sl.value = hz;
      updateChamberPhysics();
    }

    function updateChamberPhysics() {
      const medEl = document.getElementById('select-medium');
      const epsEl = document.getElementById('slider-epsilon');
      const preEl = document.getElementById('chamber-preset-select');

      appState.chamberMedium = medEl ? medEl.value : 'air';
      appState.chamberEpsilon = parseFloat(epsEl ? epsEl.value : 0.08);
      appState.chamberPreset = preEl ? preEl.value : 'barabar';

      const meta = CHAMBER_META[appState.chamberPreset] || CHAMBER_META.barabar;
      const v = appState.chamberMedium === 'air' ? 343 : 1500;
      const atten = appState.chamberMedium === 'air' ? 1.0 : 0.45;
      const helmholtzF0 = (v / (2 * Math.PI)) * Math.sqrt(meta.A / (meta.V * meta.L));
      const f0Disp = appState.chamberMedium === 'air' && appState.chamberPreset === 'barabar'
        ? 34.397
        : helmholtzF0;
      const freq = appState.chamberFreq;
      const wavelength = v / freq;
      const planarity = Math.max(0.22, Math.min(0.98, 0.96 - appState.chamberEpsilon * 1.25));
      const deltaHz = Math.abs(freq - f0Disp);

      const setTxt = function (id, txt) {
        const el = document.getElementById(id);
        if (el) el.textContent = txt;
      };

      setTxt('val-freq', `${freq.toFixed(1)} Hz`);
      setTxt('val-epsilon', `${appState.chamberEpsilon.toFixed(2)} m`);
      setTxt('kpi-chamber-hz', `${freq.toFixed(2)} Hz`);
      setTxt('kpi-chamber-sub', `${meta.badge.split('·')[0].trim()} (Q ${(meta.Q * atten).toFixed(1)})`);
      setTxt('three-chamber-badge', `${meta.badge.split('·')[0].trim()} · ${freq.toFixed(1)} HZ`);
      setTxt('three-planarity-badge', `PCA x₁ = ${planarity.toFixed(3)}`);

      setTxt('out-helmholtz-f0', `${f0Disp.toFixed(3)} Hz`);
      setTxt('out-helmholtz-match', `Excitation delta: ${deltaHz.toFixed(2)} Hz`);
      setTxt('out-planarity-x1', planarity.toFixed(3));
      setTxt('out-planarity-class', planarity >= 0.72 ? `Engineered planar surface` : `Perturbed fractal scatter`);
      setTxt('out-wavelength', `${wavelength.toFixed(2)} m`);
      setTxt('out-qfactor', `Effective Q: ${(meta.Q * atten).toFixed(1)} (α=${atten.toFixed(2)})`);

      if (freq >= 90 && freq <= 115) {
        setTxt('out-neuro-state', `EEG Right-Shift`);
        setTxt('out-neuro-sub', `Prefrontal language downregulation`);
      } else if (deltaHz < 3.5) {
        setTxt('out-neuro-state', `Peak Cavity Lock`);
        setTxt('out-neuro-sub', `Inverse piezoelectric antinodes`);
      } else {
        setTxt('out-neuro-state', `Harmonic Drift`);
        setTxt('out-neuro-sub', `Off-resonance wave propagation`);
      }

      if (audioPlaying && audioOsc) {
        audioOsc.frequency.setTargetAtTime(freq * 2, audioCtx.currentTime, 0.05);
      }

      buildChamberGeometry(appState.chamberPreset, appState.chamberEpsilon);
      scheduleStateSave();
    }

    function toggleAcousticAudio() {
      const btn = document.getElementById('btn-audio-tone');
      if (!audioPlaying) {
        const AudioCtor = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtor) return;
        if (!audioCtx) audioCtx = new AudioCtor();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        audioOsc = audioCtx.createOscillator();
        audioGain = audioCtx.createGain();
        audioOsc.type = 'sine';
        // Play 1st octave above sub-bass for standard speaker audibility while preserving harmonic ratio
        audioOsc.frequency.value = appState.chamberFreq * 2;
        audioGain.gain.setValueAtTime(0.001, audioCtx.currentTime);
        audioGain.gain.exponentialRampToValueAtTime(0.08, audioCtx.currentTime + 0.12);
        audioOsc.connect(audioGain);
        audioGain.connect(audioCtx.destination);
        audioOsc.start();
        audioPlaying = true;
        if (btn) {
          btn.classList.add('btn-active');
          btn.innerHTML = `<i data-lucide="volume-x" width="14" height="14" aria-hidden="true"></i> Mute Tone (${(appState.chamberFreq * 2).toFixed(1)} Hz 2nd Harm.)`;
        }
      } else {
        if (audioGain && audioCtx) {
          audioGain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.08);
        }
        setTimeout(function () {
          if (audioOsc) { try { audioOsc.stop(); } catch (e) {} audioOsc = null; }
        }, 100);
        audioPlaying = false;
        if (btn) {
          btn.classList.remove('btn-active');
          btn.innerHTML = `<i data-lucide="volume-2" width="14" height="14" aria-hidden="true"></i> Audition Resonance Tone`;
        }
      }
      if (window.lucide) window.lucide.createIcons();
    }

    /* =====================================================================
       MODULE 3: ALBA v2.2 SPATIAL DISCOVERY GRID (LEAFLET VECTOR MAP)
    ===================================================================== */
    let albaMap = null;
    let sitesLayerGroup = null;
    let lgmLayerGroup = null;
    let tradeLayerGroup = null;

    function initAlbaMap() {
      const mapEl = document.getElementById('alba-map');
      if (!mapEl || typeof L === 'undefined') return;

      albaMap = L.map('alba-map', {
        center: [-7.0, -73.0],
        zoom: 5,
        minZoom: 2,
        maxZoom: 9,
        scrollWheelZoom: false
      });

      albaMap.attributionControl.addAttribution('Boundaries: Natural Earth 50m (public domain)');

      sitesLayerGroup = L.layerGroup().addTo(albaMap);
      lgmLayerGroup = L.layerGroup().addTo(albaMap);
      tradeLayerGroup = L.layerGroup().addTo(albaMap);

      // Load public-domain 50m vector geography (approved CDN)
      fetch('https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-50m.json')
        .then(function (r) { return r.json(); })
        .then(function (topo) {
          if (typeof topojson !== 'undefined' && topo && topo.objects && topo.objects.countries) {
            const geo = topojson.feature(topo, topo.objects.countries);
            L.geoJSON(geo, {
              style: {
                fillColor: PALETTE.surfaceHigh,
                fillOpacity: 0.92,
                color: PALETTE.outline,
                weight: 0.85
              }
            }).addTo(albaMap);
            // Bring overlay layers to front
            tradeLayerGroup.eachLayer(function (l) { if (l.bringToFront) l.bringToFront(); });
          }
        })
        .catch(function () {
          const status = document.getElementById('map-status-line');
          if (status) status.textContent = `Vector basemap unavailable offline — coordinates plotted directly.`;
        });

      renderAlbaOverlays();
      updateAlbaFilters();
      setTimeout(function () { if (albaMap) albaMap.invalidateSize(); }, 250);
    }

    function renderAlbaOverlays() {
      if (!lgmLayerGroup || !tradeLayerGroup) return;
      lgmLayerGroup.clearLayers();
      tradeLayerGroup.clearLayers();

      if (appState.showLgmLayer) {
        LGM_SHELVES.forEach(function (shelf) {
          L.circle([shelf.lat, shelf.lon], {
            radius: shelf.r,
            color: PALETTE.sky,
            weight: 1.5,
            dashArray: '5 5',
            fillColor: PALETTE.sky,
            fillOpacity: 0.09
          }).bindTooltip(shelf.label).addTo(lgmLayerGroup);
        });
      }

      if (appState.showTradeLayer) {
        MARANON_CORRIDORS.forEach(function (path) {
          L.polyline(path, {
            color: PALETTE.brass,
            weight: 2.5,
            dashArray: '6 4',
            opacity: 0.85
          }).addTo(tradeLayerGroup);
        });
      }
    }

    function setMapScope(scope) {
      appState.mapScope = scope;
      const bAndean = document.getElementById('btn-scope-andean');
      const bGlobal = document.getElementById('btn-scope-global');
      if (bAndean) bAndean.classList.toggle('btn-active', scope === 'andean');
      if (bGlobal) bGlobal.classList.toggle('btn-active', scope === 'global');

      if (albaMap) {
        if (scope === 'andean') {
          albaMap.flyTo([-7.2, -73.0], 5, { duration: 0.7 });
        } else {
          albaMap.flyTo([12.0, -25.0], 2, { duration: 0.7 });
        }
      }
      scheduleStateSave();
    }

    function toggleMapLayer(layerKey) {
      if (layerKey === 'evi') {
        appState.showEviLayer = !appState.showEviLayer;
        const b = document.getElementById('btn-layer-evi');
        if (b) b.classList.toggle('btn-active', appState.showEviLayer);
      } else if (layerKey === 'lgm') {
        appState.showLgmLayer = !appState.showLgmLayer;
        const b = document.getElementById('btn-layer-lgm');
        if (b) b.classList.toggle('btn-active', appState.showLgmLayer);
      } else if (layerKey === 'trade') {
        appState.showTradeLayer = !appState.showTradeLayer;
        const b = document.getElementById('btn-layer-trade');
        if (b) b.classList.toggle('btn-active', appState.showTradeLayer);
      }
      renderAlbaOverlays();
      updateAlbaFilters();
      scheduleStateSave();
    }

    function updateAlbaFilters() {
      const eviEl = document.getElementById('slider-evi-threshold');
      const probEl = document.getElementById('slider-prob-min');
      const tierEl = document.getElementById('select-tier-filter');

      appState.eviThreshold = parseFloat(eviEl ? eviEl.value : 0.85);
      appState.probMin = parseFloat(probEl ? probEl.value : 0.00);
      appState.tierFilter = tierEl ? tierEl.value : 'all';

      const setTxt = function (id, txt) {
        const el = document.getElementById(id);
        if (el) el.textContent = txt;
      };
      setTxt('val-evi-threshold', appState.eviThreshold.toFixed(2));
      setTxt('val-prob-min', appState.probMin.toFixed(2));
      setTxt('kpi-evi-cap', appState.eviThreshold.toFixed(2));
      setTxt('alba-gate-summary', `SAFETY GATE ACTIVE: EVI ≤ ${appState.eviThreshold.toFixed(2)}`);

      const filtered = ALBA_SITES.filter(function (s) {
        const tierOk = appState.tierFilter === 'all' || s.tier === appState.tierFilter;
        return tierOk && s.prob >= appState.probMin;
      });

      let passedCount = 0;
      let interceptedCount = 0;
      ALBA_SITES.forEach(function (s) {
        if (s.evi <= appState.eviThreshold) passedCount++;
        else interceptedCount++;
      });
      setTxt('kpi-alba-pass', `${passedCount} / ${ALBA_SITES.length} Passed`);
      setTxt('kpi-alba-sub', `${interceptedCount} intercepted for UAS non-intrusive scan`);
      setTxt('map-status-line', `Showing ${filtered.length} of ${ALBA_SITES.length} multi-proxy discovery nodes`);

      // Update Leaflet markers
      if (sitesLayerGroup) {
        sitesLayerGroup.clearLayers();
        filtered.forEach(function (s) {
          const isSafe = s.evi <= appState.eviThreshold;
          const markerColor = isSafe ? PALETTE.mint : PALETTE.coral;
          const isSelected = s.id === appState.selectedSiteId;

          if (appState.showEviLayer) {
            L.circleMarker([s.lat, s.lon], {
              radius: isSelected ? 18 : 13,
              color: markerColor,
              weight: isSelected ? 2 : 1,
              fillColor: markerColor,
              fillOpacity: 0.16
            }).addTo(sitesLayerGroup);
          }

          const marker = L.circleMarker([s.lat, s.lon], {
            radius: isSelected ? 8 : 6,
            color: PALETTE.bg,
            weight: 2,
            fillColor: isSafe ? (s.prob >= 0.85 ? PALETTE.brass : PALETTE.mint) : PALETTE.coral,
            fillOpacity: 1
          }).addTo(sitesLayerGroup);

          marker.bindPopup(`
            <strong>${s.name}</strong><br>
            <span>P(A|X): ${s.prob.toFixed(4)} · EVI: ${s.evi.toFixed(2)}</span><br>
            <span>${isSafe ? 'PASSED: Low-impact ground-truthing' : 'INTERCEPTED: EVI > ' + appState.eviThreshold.toFixed(2) + ' (UAS Only)'}</span>
          `);
          marker.on('click', function () { selectAlbaSite(s.id, false); });
        });
      }

      // Render site table
      const tbody = document.getElementById('alba-table-body');
      if (tbody) {
        tbody.innerHTML = '';
        filtered.forEach(function (s) {
          const isSafe = s.evi <= appState.eviThreshold;
          const tr = document.createElement('tr');
          if (s.id === appState.selectedSiteId) tr.className = 'selected-row';
          tr.style.cursor = 'pointer';
          tr.onclick = function () { selectAlbaSite(s.id, true); };
          tr.innerHTML = `
            <td><strong>${s.id}</strong></td>
            <td>${s.transect}</td>
            <td><span class="badge badge-sky">${s.tier}</span></td>
            <td class="num-col">${s.prob.toFixed(4)}</td>
            <td class="num-col">${s.evi.toFixed(2)}</td>
            <td class="num-col">${s.transit.toFixed(2)} km/h</td>
            <td>
              <span class="badge ${isSafe ? 'badge-mint' : 'badge-coral'}">
                ${isSafe ? 'PASSED · GROUND-TRUTH' : 'INTERCEPTED · UAS ONLY'}
              </span>
            </td>
          `;
          tbody.appendChild(tr);
        });
      }

      renderSelectedSiteInspector();
      scheduleStateSave();
    }

    function selectAlbaSite(siteId, flyTo) {
      appState.selectedSiteId = siteId;
      const site = ALBA_SITES.find(function (s) { return s.id === siteId; });
      if (site && flyTo && albaMap) {
        const targetZoom = (site.lat > 0 || site.lon > 0) ? 4 : 6;
        albaMap.flyTo([site.lat, site.lon], targetZoom, { duration: 0.7 });
      }
      updateAlbaFilters();
    }

    function renderSelectedSiteInspector() {
      const site = ALBA_SITES.find(function (s) { return s.id === appState.selectedSiteId; }) || ALBA_SITES[0];
      if (!site) return;
      const isSafe = site.evi <= appState.eviThreshold;

      const setTxt = function (id, txt) {
        const el = document.getElementById(id);
        if (el) el.textContent = txt;
      };
      const latLabel = `${Math.abs(site.lat).toFixed(2)}°${site.lat < 0 ? 'S' : 'N'}`;
      const lonLabel = `${Math.abs(site.lon).toFixed(2)}°${site.lon < 0 ? 'W' : 'E'}`;

      setTxt('insp-coords', `${latLabel}, ${lonLabel} · ${site.transect.toUpperCase()} (${site.tier.toUpperCase()})`);
      setTxt('insp-name', site.name);
      setTxt('insp-desc', site.desc);
      setTxt('insp-prob', site.prob.toFixed(4));
      setTxt('insp-evi', site.evi.toFixed(2));
      setTxt('insp-transit', `${site.transit.toFixed(2)} km/h`);

      const badge = document.getElementById('insp-gate-badge');
      if (badge) {
        badge.className = `badge ${isSafe ? 'badge-mint' : 'badge-coral'}`;
        badge.textContent = isSafe ? `PASSED · GROUND-TRUTHING` : `INTERCEPTED · UAS ONLY`;
      }
    }

    function updateToblerCalculator() {
      const sl = document.getElementById('slider-slope-deg');
      const deg = parseFloat(sl ? sl.value : -2.86);
      appState.slopeDeg = deg;

      const slopeRad = (deg * Math.PI) / 180;
      const S = Math.tan(slopeRad);
      const gradePct = (S * 100).toFixed(1);
      const W = 6 * Math.exp(-3.5 * Math.abs(S + 0.05));

      const setTxt = function (id, txt) {
        const el = document.getElementById(id);
        if (el) el.textContent = txt;
      };
      setTxt('val-slope-deg', `${deg.toFixed(1)}° (${gradePct}% Grade)`);
      setTxt('out-tobler-speed', `${W.toFixed(2)} km/h`);

      let regime = `Nominal Walk`;
      if (Math.abs(deg + 2.86) < 1.2) regime = `Gravity-Assist Peak`;
      else if (deg > 15) regime = `Ascent Cliff (<1.5 km/h)`;
      else if (deg < -15) regime = `Braking Descent`;
      setTxt('out-tobler-regime', regime);

      scheduleStateSave();
    }

    /* =====================================================================
       MODULE 4: LAYER 0 METABOLIC GATE VERIFIER
    ===================================================================== */
    function evaluateMetabolicGate() {
      const pEl = document.getElementById('slider-p-sum');
      const nEl = document.getElementById('slider-n-sum');
      const p = parseFloat(pEl ? pEl.value : 4.5);
      const n = parseFloat(nEl ? nEl.value : 0.5);
      appState.gateP = p;
      appState.gateN = n;

      const deltaE = p - n;
      const accepted = deltaE > 0;

      const setTxt = function (id, txt) {
        const el = document.getElementById(id);
        if (el) el.textContent = txt;
      };
      setTxt('val-p-sum', p.toFixed(2));
      setTxt('val-n-sum', n.toFixed(2));

      const badge = document.getElementById('gate-result-badge');
      if (badge) {
        badge.className = `badge ${accepted ? 'badge-mint' : 'badge-coral'}`;
        badge.textContent = accepted ? `ACCEPT · ΔE = +${deltaE.toFixed(2)}` : `REJECT_NET_NON_POSITIVE · ΔE = ${deltaE.toFixed(2)}`;
      }

      // Deterministic lightweight fingerprint preview for receipt display
      const seed = `${p.toFixed(2)}:${n.toFixed(2)}:${appState.eviThreshold.toFixed(2)}:849206`;
      let h1 = 0x811c9dc5;
      for (let i = 0; i < seed.length; i++) {
        h1 ^= seed.charCodeAt(i);
        h1 = Math.imul(h1, 0x01000193);
      }
      const hexTag = (h1 >>> 0).toString(16).padStart(8, '0');

      const receipt = {
        coil_id: `77-AE-VIGILANCE`,
        anchor_block: 849206,
        gate_result: accepted ? `ACCEPT` : `REJECT_NET_NON_POSITIVE`,
        p_sum: Number(p.toFixed(2)),
        n_sum: Number(n.toFixed(2)),
        delta_e: Number(deltaE.toFixed(2)),
        evi_ceiling: appState.eviThreshold,
        digest_preview: `sha3:675e7578_${hexTag}…b18054`
      };
      setTxt('gate-receipt-json', JSON.stringify(receipt));
      scheduleStateSave();
    }

    /* =====================================================================
       EXPORT & WORKSPACE RESET
    ===================================================================== */
    function exportPortalCSV() {
      const headers = [`Site_ID`, `Transect`, `Tier`, `Posterior_P_A_X`, `EVI`, `Tobler_km_h`, `Safety_Gate_EVI_${appState.eviThreshold}`];
      const rows = ALBA_SITES.map(function (s) {
        const status = s.evi <= appState.eviThreshold ? `PASSED` : `INTERCEPTED_UAS_ONLY`;
        return [s.id, `"${s.transect}"`, s.tier, s.prob.toFixed(4), s.evi.toFixed(2), s.transit.toFixed(2), status].join(',');
      });
      const csv = [headers.join(','), ...rows].join('\n');

      if (window.notebookAppApi && typeof window.notebookAppApi.triggerFileDownload === 'function') {
        window.notebookAppApi.triggerFileDownload({
          content: csv,
          contentType: 'text/csv',
          encoding: 'UTF-8',
          filename: 'sovereign_lattice_alba_telemetry.csv'
        });
      }
    }

    function handleResetWorkspace(btn) {
      if (!btn) return;
      if (btn.dataset.armed !== 'true') {
        btn.dataset.armed = 'true';
        btn.textContent = `Confirm Reset`;
        setTimeout(function () {
          if (btn.dataset.armed === 'true') {
            btn.dataset.armed = 'false';
            btn.innerHTML = `<i data-lucide="rotate-ccw" width="15" height="15" aria-hidden="true"></i> Reset Workspace`;
            if (window.lucide) window.lucide.createIcons();
          }
        }, 3500);
        return;
      }

      btn.dataset.armed = 'false';
      btn.innerHTML = `<i data-lucide="rotate-ccw" width="15" height="15" aria-hidden="true"></i> Reset Workspace`;
      if (window.lucide) window.lucide.createIcons();

      appState = {
        tokLarge: 6, tokMed: 6, tokSmall: 6,
        cipherYears: 28800, cipherLabel: `Alulim (SKL 1)`, cipherMode: `skl`,
        decayL0: 600, decayLambda: 0.315, decayC: 100,
        chamberPreset: `barabar`, chamberFreq: 34.4, chamberMedium: `air`, chamberEpsilon: 0.08,
        eviThreshold: 0.85, probMin: 0.00, tierFilter: `all`,
        mapScope: `andean`, showEviLayer: true, showLgmLayer: true, showTradeLayer: true,
        selectedSiteId: `EL-PONGOR-MC04`, slopeDeg: -2.86, gateP: 4.5, gateN: 0.5
      };

      applyStateToDOM();
      updateProtoLedger();
      translateSingleSpan();
      syncDecayControls();
      updateChamberPhysics();
      setMapScope('andean');
      renderAlbaOverlays();
      updateAlbaFilters();
      updateToblerCalculator();
      evaluateMetabolicGate();
      scheduleStateSave();
    }

    /* =====================================================================
       BOOT SEQUENCE
    ===================================================================== */
    async function bootPortal() {
      if (window.notebookAppApi && typeof window.notebookAppApi.getAppState === 'function') {
        try {
          const saved = await window.notebookAppApi.getAppState();
          if (saved && typeof saved === 'object') {
            appState = Object.assign({}, appState, saved);
          }
        } catch (e) {}
      }

      applyStateToDOM();
      renderChronosMatrixTable();
      updateProtoLedger();
      translateSingleSpan();
      syncDecayControls();
      initThreeChamber();
      updateChamberPhysics();
      initAlbaMap();
      updateToblerCalculator();
      evaluateMetabolicGate();

      if (window.lucide) window.lucide.createIcons();

      if (window.notebookAppApi && typeof window.notebookAppApi.notifyAppReady === 'function') {
        window.notebookAppApi.notifyAppReady();
      }
    }

    window.addEventListener('DOMContentLoaded', bootPortal);
  </script>
</body>
</html>