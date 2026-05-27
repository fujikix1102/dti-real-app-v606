# DTI Research Dashboard

This repository hosts the DTI research-facing Streamlit app.

The app is a bounded research-navigation dashboard. It helps readers understand locked benchmark references, promising parameter directions, probe value, and safe next controlled tests.

It is not a likelihood engine, posterior comparison, Planck validation, final cosmological claim, or proof of new physics.

## Current public UI state

The current app includes the following research-positive workflow:

1. Visitor Quick Guide
2. Current input model safety/readout cards
3. Readout card detail guide
4. Section 5: AxiCLASS FIX1 locked benchmark
5. Parameter Quality Matrix
6. Probe Result Value Matrix V2
7. Positive Answer Navigator
8. Research Motivation Layer
9. Research Opportunity Engine
10. Discovery Score and Claim Readiness
11. Section 7a: AxiCLASS fixed-example check
12. Section 7b: Vanilla-profile API check
13. Section 7c: continuity/discontinuity examiner remains deferred and disabled

## Recommended reading order

For first-time visitors:

1. Read the Visitor Quick Guide.
2. Check Section 5 for locked benchmark references.
3. Use the Parameter Quality Matrix to identify promising parameter directions.
4. Use the Probe Result Value Matrix V2 to understand what 7a, 7b, and 7c teach.
5. Run 7a if you need a source-locked benchmark check.
6. Run 7b if you need a bounded live-profile probe.
7. Keep 7c deferred unless explicitly approved.

## What this app can help answer

The app can help readers identify:

- which benchmark values are locked
- which parameter directions are promising
- which paths are partial but useful
- which paths are blocked for stronger claims
- what each probe teaches
- what remains bounded
- what next controlled test should be run

## What this app cannot claim

The app does not claim:

- final cosmological truth
- posterior superiority
- Planck validation
- proof of new physics
- likelihood-level model preference
- 7c continuity or discontinuity closure
- manuscript-level scientific conclusion

## Data files

The locked benchmark and profile preset files are expected under:

    app/data/axiclass_fix1_results.tsv
    app/data/axiclass_fix1_delta.tsv
    app/data/profile_presets_v606.tsv

The app now uses a robust DATA_DIR resolver that checks:

    APP_DIR / "app" / "data"
    APP_DIR / "data"
    Path.cwd() / "app" / "data"
    Path.cwd() / "data"

This prevents public/local path-layout drift from hiding the FIX1 benchmark TSV files.

## Key components

### Visitor Quick Guide

A first-reader orientation layer before Section 5. It explains reading order, what the app can answer, what it cannot claim, section flow, and current best next action.

### Current input model safety/readout cards

A lightweight input readout showing the current model parameters and safety labels.

### Readout card detail guide

A clickable explanation layer for current input model readout cards. It explains research role, why each parameter matters, safe interpretation, what not to claim, and next checks.

### AxiCLASS FIX1 locked benchmark

Section 5 displays locked AxiCLASS FIX1 benchmark TSV values. These are read-only reference values, not live recomputation.

### Parameter Quality Matrix

A compact color-coded research triage table.

Meaning:

- GREEN: strong lead
- YELLOW: useful partial
- ORANGE: needs control
- RED: blocked for claim
- GRAY: awaiting data, not zero quality

The compact table keeps the main view readable and moves long details into cards/expanders.

### Probe Result Value Matrix V2

A status-linked positive probe evaluation layer.

It interprets:

- 7a as a source-locked benchmark-value probe
- 7b as a bounded exploratory live-profile probe
- 7c as a deferred high-value future test

V2 reads available 7a / 7b session or API status signals when present and reflects them into actual_status, value_badge, research_score, claim_readiness, what this teaches, what remains blocked, next experiment, safe wording, and session hits.

### Positive Answer Navigator

Reframes app output as:

- PASS
- PARTIAL
- FAIL
- UNRESOLVED

It emphasizes what survives, what remains blocked, and what next test can move the result toward a clearer answer.

### Research Motivation Layer

A constructive research workflow layer that treats partial or unresolved results as useful evidence for designing the next controlled test.

### Research Opportunity Engine

A research opportunity map, next-test composer, and claim-boundary translator.

### Discovery Score and Claim Readiness

A lightweight UI/meta-scoring layer. It is not a likelihood or posterior statistic.

## Section 7 policy

### 7a

7a is available as a source-locked fixed-example check.

### 7b

7b is available as a bounded live-profile API check.

### 7c

7c remains disabled and deferred. It must not be executed unless explicitly approved.

## Hard boundaries

This app does not perform or claim:

- likelihood evaluation
- posterior comparison
- Planck validation
- graph-based scientific result
- 7c execution
- physics-value updates
- manuscript updates
- Render API modification
- Streamlit Secret modification

## Current implementation identity

- Generated docs timestamp: 2026-05-27 07:31:57
- Source HEAD before docs update: 8466d75f069c3810d56be6ee68c029e59dc4eb56
- app.py SHA256 before docs update: 2ba00a74f2704053e93c33342b7dc684dcea0c93f94dd279c3e959b30781c347

## Notes for contributors

Use Bash for copy-paste runs on Mac.

Avoid zsh globbing and quoting pitfalls.

Do not mix app.py changes with docs changes unless explicitly scoped.

Do not commit untracked local artifacts unless the task explicitly says to do so.

<!-- DTI_SHOW_ALL_PROFILES_TABLE_V1F_DOC_START -->
## Show all profiles table V1F

The sidebar profile-category browser includes a preview-only route called **Show all profiles / full TSV inventory**.

When **Show complete profile TSV inventory** is checked, the app now displays the complete TSV inventory as a compact table instead of a raw Python/list-style object.

The table is preview-only and has these columns:

- `no`
- `model_id`
- `category`

The app also separates two counts:

- **TSV profile count:** 100 profiles from `app/data/profile_presets_v606.tsv`
- **Registered PRESETS count:** all profiles currently visible to the app, including default/manual presets and TSV-loaded presets

This distinction is intentional. The TSV is the curated 100-profile source inventory. Registered PRESETS can be larger because the app may include built-in manual/default profiles in addition to the TSV entries.

### Boundary

Show all profiles table V1F does not change the active loader.

It does not replace:

- **Load registered profile — ACTIVE loader**
- **Candidate preset — ACTIVE comparison input**
- **Reference preset — ACTIVE comparison input**

It is a navigation and audit-preview layer only. It does not perform likelihood evaluation, posterior comparison, Planck validation, graph rendering, physics-value updates, 7c execution, or manuscript updates.
<!-- DTI_SHOW_ALL_PROFILES_TABLE_V1F_DOC_END -->
