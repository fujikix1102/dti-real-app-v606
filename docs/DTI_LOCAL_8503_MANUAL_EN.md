# DTI Research Dashboard Manual

Generated: 2026-05-27 07:31:57

## 1. Purpose

This manual describes the current public-facing DTI Streamlit app.

The app is intended as a research-navigation dashboard. It helps readers move from locked benchmark references to parameter triage, probe-value interpretation, and safe next-test planning.

It is not a final cosmological result engine.

## 2. First-time reading flow

Use this order:

1. Visitor Quick Guide
2. Section 5: AxiCLASS FIX1 locked benchmark
3. Parameter Quality Matrix
4. Probe Result Value Matrix V2
5. 7a AxiCLASS fixed-example check
6. 7b Vanilla-profile API check
7. 7c only as deferred future-test context

## 3. Visitor Quick Guide

The Visitor Quick Guide appears before Section 5.

It explains:

- recommended reading order
- what the app can help answer
- what the app cannot claim
- section flow
- current best next action
- reviewer/researcher boundary notes

This is UI explanation only.

## 4. Current input model safety/readout cards

These cards show the current model-input state and lightweight safety labels.

They are for orientation. They are not likelihood results, posterior results, Planck validation, or physics-value claims.

## 5. Readout card detail guide

The detail guide adds explanatory content for the input readout cards.

Each detail explains:

- research role
- why it matters
- safe interpretation
- what not to claim
- next check

This makes the readout cards more useful to researchers without converting them into scientific claims.

## 6. AxiCLASS FIX1 locked benchmark

Section 5 displays locked benchmark references from TSV files.

Required data files:

    app/data/axiclass_fix1_results.tsv
    app/data/axiclass_fix1_delta.tsv
    app/data/profile_presets_v606.tsv

The latest app includes a robust DATA_DIR resolver. It searches:

    APP_DIR / "app" / "data"
    APP_DIR / "data"
    Path.cwd() / "app" / "data"
    Path.cwd() / "data"

Expected healthy display:

    FIX1 checkpoint status: ... models OK

If the TSV files are not found, Section 5 shows a warning. That warning should not appear when app/data is available.

## 7. Parameter Quality Matrix

The Parameter Quality Matrix is a compact color-coded table for research triage.

It helps identify:

- promising parameter directions
- partial but useful zones
- control-needed directions
- claim-blocked routes
- awaiting-data rows
- next-test priority order

Color meaning:

- GREEN: strong lead
- YELLOW: useful partial
- ORANGE: needs control
- RED: blocked for claim
- GRAY: awaiting data, not zero quality

The main table is compact to reduce horizontal clipping.

Detailed fields are moved into cards or expanders:

- positive_signal
- risk_blocker
- next_test
- safe_interpretation

## 8. Probe Result Value Matrix V2

Probe Result Value Matrix V2 evaluates 7a, 7b, and 7c as research-value probes.

It is designed to move away from a simple “result appeared / result did not appear” reading.

It asks:

- what this probe teaches
- what is already useful
- what remains bounded
- what next experiment would make the result stronger

### 7a

7a is treated as a source-locked benchmark-value probe.

### 7b

7b is treated as a bounded exploratory live-profile probe.

### 7c

7c remains disabled and is treated as a deferred high-value future test.

V2 can use available 7a / 7b session or API status signals to update:

- actual_status
- value_badge
- research_score
- claim_readiness
- what this teaches
- what remains blocked
- next experiment
- safe wording
- session hits

## 9. Positive Answer Navigator

The Positive Answer Navigator reframes outputs as:

- PASS
- PARTIAL
- FAIL
- UNRESOLVED

The goal is constructive interpretation:

- what survives the audit
- what remains blocked
- what next test should be run

## 10. Research Motivation Layer

This layer presents the app as a constructive research workflow.

It treats partial and unresolved states as useful evidence for designing better tests.

## 11. Research Opportunity Engine

This layer provides:

- Research Opportunity Map
- Next Test Composer
- Claim Boundary Translator

It helps readers find what is promising without overclaiming.

## 12. Discovery Score and Claim Readiness

This is a lightweight UI/meta-scoring layer.

It is not a likelihood statistic, posterior statistic, Planck validation, or scientific proof.

It is useful only for research planning.

## 13. Boundaries

The app does not perform:

- likelihood evaluation
- posterior comparison
- Planck validation
- graph-based scientific result
- 7c execution
- physics-value updates
- manuscript updates
- Render API modification
- Streamlit Secret modification

## 14. Operational notes

Current app identity before this docs update:

    HEAD: 8466d75f069c3810d56be6ee68c029e59dc4eb56
    app.py SHA256: 2ba00a74f2704053e93c33342b7dc684dcea0c93f94dd279c3e959b30781c347

Recommended maintenance rules:

- use Bash on Mac
- stage only intended files
- keep app.py and docs updates separated unless explicitly scoped
- preserve 7c disabled state
- preserve no-graph-reopening rule
- preserve no-likelihood/posterior/Planck-claim boundary

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


## Static Delta Audit Table V1

The public dashboard includes **AxiCLASS FIX1 static delta audit table**.

This panel reads the local checkpoint file:

- `app/data/axiclass_fix1_delta.tsv`

It displays a bounded audit view of already-recorded static differences:

- row count
- metric count
- comparison-pair count
- direction summary
- compact reader-facing static delta table

The panel is intentionally **display-only**. It does not infer a new model result and does not perform interpolation.

Boundary:

- no interpolation
- no recomputation
- no CLASS execution
- no Render API request
- no 7c execution
- no likelihood evaluation
- no posterior comparison
- no Planck validation
- no model validation
- no physics-value update
- no graph rendering
- no manuscript conclusion

Interpretation:

The panel is useful for checking fixed benchmark-difference structure already present in the repository. It is not a solver, not an emulator, and not a posterior or likelihood object. The earlier read-only interpolation audit found that `axiclass_fix1_delta.tsv` does not contain a clear numeric interpolation axis, so the app presents it as a static audit table rather than an interpolation engine.


## Vanilla-profile API input/result display V1

The vanilla-profile API area now uses a reader-facing display.

The input section shows the configured API payload as a compact table first. Raw input JSON is preserved under an audit-view expander.

The result section shows:

1. PASS / REVIEW summary,
2. HTTP status and endpoint summary,
3. input and derived values in a compact table,
4. raw API response JSON under an audit-view expander.

Missing lightweight endpoint fields such as `sigma8` or `S8` are displayed as `not returned by this lightweight endpoint`.

Boundary:

- display-only UI polish
- no CLASS execution
- no Render API modification
- no 7c execution
- no likelihood evaluation
- no posterior comparison
- no Planck validation
- no physics-value update
- no manuscript update

