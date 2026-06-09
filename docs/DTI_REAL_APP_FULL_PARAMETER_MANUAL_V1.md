# DTI Real App — Full Parameter and Usage Manual V1

Created: 2026-06-09 23:21:13 local time  
Public app: https://dti-real-app-v606.streamlit.app/  
Git HEAD / origin target: `fb7970261e2fadc42e2ab673dba108e6262b4b20`  
`app.py` SHA256: `dd0bf188bdb74750a2dc8b6b952a050d51a502add1220bfd77ba9cb5e8a9254f`  
`app.py` line count: `11819`  
Manual file: `docs/DTI_REAL_APP_FULL_PARAMETER_MANUAL_V1.md`

---

## 0. Status and scope of this manual

This manual is a long-form user-facing and reviewer-facing guide for the DTI Real App public Streamlit interface. It is intentionally explicit and repetitive. The purpose is to make each control, parameter, result panel, table, graph, and boundary label readable without relying on informal project memory.

This manual is documentation only. It does not modify the application, run any backend service, execute CLASS or AxiCLASS, recompute chi2, evaluate a likelihood, run MCMC, compare posteriors, validate against Planck, validate against JWST, or update the manuscript.

The app should be read as a diagnostic and audit display system. Unless a specific panel says otherwise, values are bounded, source-locked, display-only, and audit-only. A visible number in the public app is not automatically a physical validation result. A graph in the public app is not automatically a likelihood result. A readiness flag marked `NO` means the capability is unavailable or outside scope in that panel; it is not negative evidence against the model.

---

## 1. Public app access and safe reading order

Open the public app at:

`https://dti-real-app-v606.streamlit.app/`

Recommended reading order:

1. Read the global claim boundary and capability notes first.
2. Use the top-level panels as a map, not as independent proof.
3. Read compact tables before raw data.
4. Treat all warnings, captions, and boundary notes as part of the result.
5. For reviewer use, quote only the bounded wording supplied in the app or in this manual.
6. Do not infer posterior or likelihood meaning from diagnostic displays unless a separately frozen likelihood or posterior package is explicitly cited.

The app contains controls that look computational, but the public interface is intentionally constrained. Some panels are static or frozen readbacks. Some panels call limited backend endpoints. Some panels are diagnostic-only. The manual separates these categories.

---

## 2. Global boundary: what the app is and is not

### What the app is

- A public diagnostic viewer.
- A provenance and audit display interface.
- A bounded interpretation aid.
- A place to inspect source-locked tables, frozen diagnostic values, interface readiness, and selected visual summaries.
- A reviewer-safe companion interface for the DTI / MAXOMEGA audit-first project.

### What the app is not

- Not a full cosmological inference engine.
- Not a live MCMC app.
- Not a public Planck likelihood runner.
- Not a public JWST validation tool.
- Not a full eBOSS LRG likelihood implementation.
- Not a proof that a physical discontinuity has been established.
- Not a claim that DTI is validated.
- Not a claim that the Hubble tension is solved.
- Not a replacement for the manuscript, frozen packages, or source-of-record audit ledgers.

### Required interpretation rule

Every result should be read through one of these statuses:

- **diagnostic:** useful for checking consistency, direction, or display state.
- **audit-only:** useful for provenance and reproducibility checks, not a physics claim by itself.
- **source-locked:** derived from a frozen source package or table whose identity is preserved.
- **bounded:** valid only within the declared scope.
- **display-only:** shown for reading, not recomputed as a full inference result.

---

## 3. Interface map: expanders, tabs, tables, raw data, warnings

The app uses Streamlit UI primitives. The survey detected these major classes:

- `st.expander`: collapsible or default-open sections.
- `st.tabs`: grouped views for related graphs or tables.
- `st.number_input`: numeric parameter controls.
- `st.selectbox`: controlled option selection.
- `st.checkbox`: enable/disable gates.
- `st.text_input`: endpoint or source metadata entry.
- `st.button`: actions such as loading presets, running a boundary check, or applying form values.
- tables and dataframes: compact readouts and raw audit data.
- SVG charts: internal app-rendered graph displays.
- captions and warnings: boundary language and readout constraints.

A closed expander does not mean that the section is irrelevant. It means the section is collapsed for readability. A default-open expander indicates a section that is important for current reading flow. A tab does not create a separate computation; it changes the visible presentation of data already available in that panel.

---

## 4. Current input model cards and preset workflow

The app contains profile and model input panels. Their purpose is to let the reader compare a candidate model profile against reference or LCDM-style comparison entries. These fields are not full posterior controls. They are interface fields for readout, audit, or limited diagnostic calls.

The profile workflow normally follows this pattern:

1. Select a candidate preset.
2. Select a reference preset.
3. Load the selected presets into the form.
4. Inspect the Candidate and Reference tabs.
5. Inspect source metadata, if available.
6. Read boundary warnings before interpreting any difference.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 3579 | selectbox | candidate_preset = st.selectbox( |  |
| 3588 | selectbox | reference_preset = st.selectbox( |  |
| 3601 | button | if st.button("Load selected presets", key="dti_ui_load_presets_v2", type="primary"): | dti_ui_load_presets_v2 |
| 3608 | tabs | tab_candidate, tab_reference = st.tabs(["Candidate", "Reference"]) |  |
| 3832 | selectbox | candidate_preset = st.selectbox( |  |
| 3839 | selectbox | reference_preset = st.selectbox( |  |
| 3849 | button | if st.button("Load selected presets into inputs", key="dti_ui_load_presets_v1"): | dti_ui_load_presets_v1 |
| 3855 | expander | with st.expander("Candidate profile inputs", expanded=True): |  |
| 3863 | expander | with st.expander("Reference profile inputs", expanded=True): |  |
| 8433 | selectbox | _dti_fallback_selected_preset_v2b = st.selectbox( |  |
| 8573 | expander | with st.expander("Candidate and reference source metadata", expanded=True): |  |
| 8577 | text_input | candidate_source_paper = st.text_input("Candidate source paper / arXiv / DOI", value="User-entered / candidate parameter block") |  |
| 8578 | text_input | candidate_source_location = st.text_input("Candidate source table / figure / line", value="manual entry") |  |
| 8580 | text_input | reference_source_paper = st.text_input("Reference source paper / arXiv / DOI", value="Reference / LCDM comparison block") |  |
| 8581 | text_input | reference_source_location = st.text_input("Reference source table / figure / line", value="manual entry") |  |


---

## 5. Parameter Quality Matrix family

The Parameter Quality Matrix panels summarize whether parameter sets are suitable for interpretation, comparison, or further audit. They should be read as quality and readiness indicators, not as posterior evidence.

A typical matrix entry may help answer:

- Is this parameter sufficiently specified?
- Is there a source record?
- Is the comparison safe?
- Is overclaim risk controlled?
- What next test is needed?

The legacy/detail matrices remain useful for audit review, but newer panels may provide more direct reading. When multiple panels overlap, prefer the panel with the clearest current boundary language and provenance.

---

## 6. Probe Result Value Matrix family

Probe Result Value Matrix panels are used to inspect diagnostic quantities and compare readout values. These matrices should not be treated as full likelihood evaluations unless an explicitly frozen likelihood package says so.

Use the matrix as follows:

1. Identify the row or branch.
2. Confirm the source or profile.
3. Check whether the value is direct, derived, static, or proxy.
4. Look for a boundary or claim-readiness label.
5. Avoid quoting the value without its scope.

---

## 7. Profile preset loader and profile comparison forms

The app includes controls for selecting candidate and reference presets. These controls are interface conveniences. They are not proof that the selected values are physically preferred.

Typical controls include:

- Candidate preset selection.
- Reference preset selection.
- Button to load selected presets.
- Candidate profile inputs.
- Reference profile inputs.
- Source metadata fields.

User guidance:

- Use presets to avoid hand-entry errors.
- After loading, inspect the field values.
- If source metadata is editable, record where the parameter block came from.
- Do not claim the app has performed a posterior comparison merely because two profiles are displayed side by side.

---

## 8. Background geometry anchor — local FLRW calculator

The Background geometry anchor is a local FLRW calculator panel. It provides diagnostic background-geometry quantities such as distance or time readouts for selected parameters. It is useful for intuition and audit. It is not a CLASS/AxiCLASS run and not a likelihood evaluation.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 5829 | expander | with st.expander("Background geometry anchor — local FLRW calculator", expanded=False): |  |
| 5836 | number_input | bg_H0 = st.number_input( |  |
| 5846 | number_input | bg_om = st.number_input( |  |
| 5856 | number_input | bg_ov = st.number_input( |  |
| 5866 | number_input | bg_z = st.number_input( |  |
| 6106 | expander | with st.expander("Jump toy comparator — piecewise background geometry", expanded=True): |  |
| 8528 | number_input | st.number_input("H0", min_value=40.0, max_value=90.0, step=0.01, key="target_H0") | target_H0 |
| 8531 | number_input | st.number_input("omega_cdm", min_value=0.05, max_value=0.20, step=0.0001, format="%.5f", key="target_omega_cdm") | target_omega_cdm |
| 8532 | number_input | st.number_input("omega_b", min_value=0.015, max_value=0.035, step=0.0001, format="%.5f", key="target_omega_b") | target_omega_b |
| 8546 | number_input | st.number_input("LCDM H0", min_value=40.0, max_value=90.0, step=0.01, key="lcdm_H0") | lcdm_H0 |
| 8547 | number_input | st.number_input("LCDM Omega_m", min_value=0.10, max_value=0.60, step=0.001, format="%.5f", key="lcdm_Omega_m") | lcdm_Omega_m |
| 8549 | number_input | st.number_input("LCDM omega_cdm", min_value=0.05, max_value=0.20, step=0.0001, format="%.5f", key="lcdm_omega_cdm") | lcdm_omega_cdm |
| 8550 | number_input | st.number_input("LCDM omega_b", min_value=0.015, max_value=0.035, step=0.0001, format="%.5f", key="lcdm_omega_b") | lcdm_omega_b |
| 9204 | number_input | live_H0 = st.number_input( |  |
| 9211 | number_input | live_omega_b = st.number_input( |  |
| 9221 | number_input | live_omega_cdm = st.number_input( |  |
| 9985 | number_input | c7c_base_H0 = st.number_input( |  |
| 9993 | number_input | c7c_base_omega_b = st.number_input( |  |
| 10004 | number_input | c7c_base_omega_cdm = st.number_input( |  |
| 10881 | number_input | h0 = st.number_input("H0", min_value=1.0, max_value=150.0, value=72.6, step=0.1, key="dti_jump_tr_h0_v1") | dti_jump_tr_h0_v1 |
| 10882 | number_input | omega_b = st.number_input("omega_b", min_value=0.0001, max_value=0.2, value=0.02237, step=0.00001, format="%.5f", key="dti_jump_tr_omega_b_v1") | dti_jump_tr_omega_b_v1 |
| 10883 | number_input | omega_cdm = st.number_input("omega_cdm", min_value=0.0001, max_value=1.0, value=0.1200, step=0.0001, format="%.4f", key="dti_jump_tr_omega_cdm_v1") | dti_jump_tr_omega_cdm_v1 |


### H0

- Meaning: Hubble constant input used by the local background-geometry calculator.
- Typical unit: km/s/Mpc.
- What it changes: expansion scaling and derived time/distance quantities in the local calculator.
- What it does not prove: It does not establish model preference, posterior probability, or Planck compatibility.

### Omega_m

- Meaning: matter density fraction used in the local FLRW-style calculation.
- What it changes: expansion history in the local background readout.
- Boundary: It is a diagnostic input, not a fitted nuisance or posterior parameter in this panel.

### Omega_vac

- Meaning: vacuum-energy or cosmological-constant-like density fraction in the local background calculator.
- What it changes: low-redshift expansion contribution and distance/time readouts.
- Boundary: This local parameter should not be overread as the full vacuum-sector claim of the theory.

### Redshift z

- Meaning: redshift at which background quantities are evaluated.
- What it changes: all distance/time outputs that depend on redshift.
- Boundary: A high redshift input can support visualization, but does not turn the panel into a CMB solver.

---

## 9. Jump toy comparator — piecewise background geometry

The Jump toy comparator is a local toy background-geometry comparator. It compares a vanilla background geometry against a piecewise modified expansion history. The current public UI opens this expander by default using `expanded=True`.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 6106 | expander | with st.expander("Jump toy comparator — piecewise background geometry", expanded=True): |  |
| 6111 | button | if st.button("Load jump-toy demonstration values", key="dti_bggeom_load_jump_toy_demo_values_v1"): | dti_bggeom_load_jump_toy_demo_values_v1 |
| 6118 | number_input | z_jump = st.number_input( |  |
| 6128 | number_input | jump_factor = st.number_input( |  |


### Purpose

The panel is designed to show how a simple piecewise modification in `E(z)` can affect local background-geometry readouts. It is a diagnostic visualization and table generator. It is not a physical proof of a discontinuity.

### z_jump

- Meaning: threshold redshift for the toy piecewise rule.
- Internal behavior: the toy modification applies above the selected threshold.
- What changing it does: shifts where the piecewise modification begins.
- What it does not prove: It does not prove that nature has a jump at that redshift.

### jump_factor

- Meaning: multiplier applied to the vanilla `E(z)` above `z_jump` in the toy panel.
- What changing it does: changes the scale of the toy deviation in the background-geometry curves and tables.
- Precision: the public UI uses fine precision for small factors.
- What it does not prove: It does not activate AxiCLASS perturbations or a physical DTI microphysics model.

### Load jump-toy demonstration values

- Button label: `Load jump-toy demonstration values`.
- Internal key: `dti_bggeom_load_jump_toy_demo_values_v1`.
- Loaded values:
  - `z_jump = 2.5`
  - `jump_factor = 1.00001`
- Behavior: the button writes these values into Streamlit session state and reruns the app so the fields update.
- Boundary: the button is a convenience preset for demonstration. It is not a claim that those values are fitted, validated, or physically preferred.

### Default-open behavior

The Jump toy comparator is currently an expander with `expanded=True`. This means the panel is open on first display, but a user may still close it. It is not a permanently always-visible non-expander block.

### Safe interpretation

Reviewer-safe wording:

> The Jump toy comparator is a local background-geometry diagnostic that displays how a simple piecewise toy modification affects selected distance and time readouts. It is not a CLASS/AxiCLASS run, not a likelihood evaluation, not a posterior comparison, and not a proof of a physical discontinuity.

---

## 10. CMB / Likelihood capability matrix

The CMB / Likelihood capability matrix explains which capabilities are available in the app and which are not. A `NO` readiness flag should be read as an availability boundary, not as a negative scientific result.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 7981 | expander | with st.expander("CMB spectra graph — real API arrays only", expanded=False): |  |
| 8233 | expander | with st.expander("CMB array availability audit", expanded=False): |  |
| 10755 | expander | with st.expander("CMB spectra graph — real API arrays only", expanded=True): |  |


### CMB graph readiness

If the app says CMB graph readiness is `NO`, it means the current public path does not have a real compatible CMB spectra array available for that graph. It does not mean the model fails CMB constraints.

### Planck likelihood readiness

If Planck likelihood readiness is `NO`, it means the public app is not running the Planck likelihood. It does not mean a Planck comparison was performed and failed.

### Backend extension required

A backend extension requirement means a future backend implementation would be needed for that capability. It is a roadmap boundary, not a scientific conclusion.

---

## 11. CMB spectra graph panels — real API arrays only

CMB spectra graph panels must use real API arrays only. The app policy rejects fake, synthetic, or placeholder scientific-looking curves. If compatible arrays are not present, the panel should show an unavailability or readiness message rather than inventing a graph.

Safe usage:

- Check array availability first.
- Confirm whether TT, TE, EE, or lensing tabs have data.
- Treat large-array summaries as readability aids.
- Do not infer likelihood values from plotted spectra unless a likelihood panel explicitly computes and freezes them.

---

## 12. TARGET_MODEL and LCDM comparison forms

The TARGET_MODEL form and LCDM comparison form allow the user to edit cosmological parameter blocks for display, comparison, or limited diagnostic calls.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 8525 | expander | with st.expander("TARGET_MODEL form", expanded=True): |  |
| 8528 | number_input | st.number_input("H0", min_value=40.0, max_value=90.0, step=0.01, key="target_H0") | target_H0 |
| 8529 | number_input | st.number_input("f_EDE", min_value=0.0, max_value=0.30, step=0.001, key="target_f_EDE") | target_f_EDE |
| 8531 | number_input | st.number_input("omega_cdm", min_value=0.05, max_value=0.20, step=0.0001, format="%.5f", key="target_omega_cdm") | target_omega_cdm |
| 8532 | number_input | st.number_input("omega_b", min_value=0.015, max_value=0.035, step=0.0001, format="%.5f", key="target_omega_b") | target_omega_b |
| 8534 | number_input | st.number_input("sigma8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="target_sigma8") | target_sigma8 |
| 8535 | number_input | st.number_input("S8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="target_S8") | target_S8 |
| 8537 | number_input | st.number_input("z_c", min_value=0.0, max_value=10000.0, step=50.0, key="target_z_c") | target_z_c |
| 8538 | number_input | st.number_input("ln10_10_As", min_value=1.0, max_value=4.5, step=0.001, format="%.5f", key="target_ln10_10_As") | target_ln10_10_As |
| 8540 | number_input | st.number_input("n_s", min_value=0.80, max_value=1.20, step=0.0001, format="%.5f", key="target_n_s") | target_n_s |
| 8541 | number_input | st.number_input("tau_reio", min_value=0.0, max_value=0.20, step=0.0001, format="%.5f", key="target_tau_reio") | target_tau_reio |
| 8543 | expander | with st.expander("LCDM comparison form", expanded=False): |  |
| 8546 | number_input | st.number_input("LCDM H0", min_value=40.0, max_value=90.0, step=0.01, key="lcdm_H0") | lcdm_H0 |
| 8547 | number_input | st.number_input("LCDM Omega_m", min_value=0.10, max_value=0.60, step=0.001, format="%.5f", key="lcdm_Omega_m") | lcdm_Omega_m |
| 8549 | number_input | st.number_input("LCDM omega_cdm", min_value=0.05, max_value=0.20, step=0.0001, format="%.5f", key="lcdm_omega_cdm") | lcdm_omega_cdm |
| 8550 | number_input | st.number_input("LCDM omega_b", min_value=0.015, max_value=0.035, step=0.0001, format="%.5f", key="lcdm_omega_b") | lcdm_omega_b |
| 8552 | number_input | st.number_input("LCDM sigma8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="lcdm_sigma8") | lcdm_sigma8 |
| 8553 | number_input | st.number_input("LCDM S8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="lcdm_S8") | lcdm_S8 |
| 8555 | number_input | st.number_input("LCDM ln10_10_As", min_value=1.0, max_value=4.5, step=0.001, format="%.5f", key="lcdm_ln10_10_As") | lcdm_ln10_10_As |
| 8556 | number_input | st.number_input("LCDM n_s", min_value=0.80, max_value=1.20, step=0.0001, format="%.5f", key="lcdm_n_s") | lcdm_n_s |
| 8558 | number_input | st.number_input("LCDM tau_reio", min_value=0.0, max_value=0.20, step=0.0001, format="%.5f", key="lcdm_tau_reio") | lcdm_tau_reio |
| 8580 | text_input | reference_source_paper = st.text_input("Reference source paper / arXiv / DOI", value="Reference / LCDM comparison block") |  |
| 8728 | tabs | tabs = st.tabs(["FUJIKI DTI", "Ivanov EDE", "Ivanov LCDM", "Full table", "Delta table"]) |  |


### H0

- **Internal key:** `target_H0 / lcdm_H0`.
- **Default / current displayed value:** User-editable within the app range..
- **Allowed range / step / precision:** 40.0 to 90.0; step usually 0.01..
- **Purpose:** Hubble constant entry for the model block.
- **What changes when the user edits it:** Changes the displayed input block and any diagnostic panel that consumes the form.
- **What it does not establish:** Does not by itself perform a likelihood fit or posterior comparison.
- **Related outputs:** Target model form, LCDM comparison form, text conversion panels.
- **Reviewer-safe wording:** This parameter is used for a bounded, diagnostic, display-only or audit-only readout unless a separately frozen computation package says otherwise.



### f_EDE

- **Internal key:** `target_f_EDE`.
- **Default / current displayed value:** User-editable within the app range..
- **Allowed range / step / precision:** 0.0 to 0.30; step usually 0.001..
- **Purpose:** Early-dark-energy-style fraction entry retained for interface compatibility and comparison.
- **What changes when the user edits it:** Changes the target model input block.
- **What it does not establish:** Does not guarantee an AxiCLASS EDE microphysics run in public UI.
- **Related outputs:** Target model form, profile comparison panels.
- **Reviewer-safe wording:** This parameter is used for a bounded, diagnostic, display-only or audit-only readout unless a separately frozen computation package says otherwise.



### omega_cdm

- **Internal key:** `target_omega_cdm / lcdm_omega_cdm`.
- **Default / current displayed value:** User-editable..
- **Allowed range / step / precision:** 0.05 to 0.20; step usually 0.0001..
- **Purpose:** Physical cold-dark-matter density parameter in the input block.
- **What changes when the user edits it:** Changes the displayed model block and compatible diagnostics.
- **What it does not establish:** Does not imply fitted posterior status.
- **Related outputs:** Target/LCDM forms, backend request payloads if enabled.
- **Reviewer-safe wording:** This parameter is used for a bounded, diagnostic, display-only or audit-only readout unless a separately frozen computation package says otherwise.



### omega_b

- **Internal key:** `target_omega_b / lcdm_omega_b`.
- **Default / current displayed value:** User-editable..
- **Allowed range / step / precision:** 0.015 to 0.035; step usually 0.0001..
- **Purpose:** Physical baryon density parameter in the input block.
- **What changes when the user edits it:** Changes the displayed model block and compatible diagnostics.
- **What it does not establish:** Does not establish BBN, CMB, or likelihood validation by itself.
- **Related outputs:** Target/LCDM forms, backend request payloads if enabled.
- **Reviewer-safe wording:** This parameter is used for a bounded, diagnostic, display-only or audit-only readout unless a separately frozen computation package says otherwise.



### sigma8

- **Internal key:** `target_sigma8 / lcdm_sigma8`.
- **Default / current displayed value:** User-editable..
- **Allowed range / step / precision:** 0.50 to 1.20; step usually 0.0001..
- **Purpose:** Amplitude-related summary parameter in the input block.
- **What changes when the user edits it:** Changes displayed comparison values.
- **What it does not establish:** Does not compute a new structure-growth likelihood in this public panel.
- **Related outputs:** Target/LCDM forms, comparison readouts.
- **Reviewer-safe wording:** This parameter is used for a bounded, diagnostic, display-only or audit-only readout unless a separately frozen computation package says otherwise.



### S8

- **Internal key:** `target_S8 / lcdm_S8`.
- **Default / current displayed value:** User-editable..
- **Allowed range / step / precision:** 0.50 to 1.20; step usually 0.0001..
- **Purpose:** Combined clustering amplitude proxy often used in observational comparisons.
- **What changes when the user edits it:** Changes displayed comparison values.
- **What it does not establish:** Does not establish weak-lensing agreement or tension by itself.
- **Related outputs:** Target/LCDM forms, static diagnostic displays.
- **Reviewer-safe wording:** This parameter is used for a bounded, diagnostic, display-only or audit-only readout unless a separately frozen computation package says otherwise.



### z_c

- **Internal key:** `target_z_c`.
- **Default / current displayed value:** User-editable..
- **Allowed range / step / precision:** 0.0 to 10000.0; step usually 50.0..
- **Purpose:** Characteristic redshift field retained for interface and comparison.
- **What changes when the user edits it:** Changes the target model block.
- **What it does not establish:** Does not activate a full physical transition model unless a backend explicitly implements it.
- **Related outputs:** Target model form.
- **Reviewer-safe wording:** This parameter is used for a bounded, diagnostic, display-only or audit-only readout unless a separately frozen computation package says otherwise.



### ln10_10_As

- **Internal key:** `target_ln10_10_As / lcdm_ln10_10_As`.
- **Default / current displayed value:** User-editable..
- **Allowed range / step / precision:** 1.0 to 4.5; step usually 0.001..
- **Purpose:** Log-amplitude parameter entry.
- **What changes when the user edits it:** Changes the displayed model block and compatible backend payloads.
- **What it does not establish:** Does not compute a posterior amplitude constraint in this app by itself.
- **Related outputs:** Target/LCDM forms, live probe forms.
- **Reviewer-safe wording:** This parameter is used for a bounded, diagnostic, display-only or audit-only readout unless a separately frozen computation package says otherwise.



### n_s

- **Internal key:** `target_n_s / lcdm_n_s`.
- **Default / current displayed value:** User-editable..
- **Allowed range / step / precision:** 0.80 to 1.20; step usually 0.0001..
- **Purpose:** Scalar spectral index entry.
- **What changes when the user edits it:** Changes the displayed model block and compatible backend payloads.
- **What it does not establish:** Does not establish CMB fit quality by itself.
- **Related outputs:** Target/LCDM forms.
- **Reviewer-safe wording:** This parameter is used for a bounded, diagnostic, display-only or audit-only readout unless a separately frozen computation package says otherwise.



### tau_reio

- **Internal key:** `target_tau_reio / lcdm_tau_reio`.
- **Default / current displayed value:** User-editable..
- **Allowed range / step / precision:** 0.0 to 0.20; step usually 0.0001..
- **Purpose:** Reionization optical-depth entry.
- **What changes when the user edits it:** Changes the displayed model block and compatible backend payloads.
- **What it does not establish:** Does not perform Planck low-ell likelihood evaluation.
- **Related outputs:** Target/LCDM forms.
- **Reviewer-safe wording:** This parameter is used for a bounded, diagnostic, display-only or audit-only readout unless a separately frozen computation package says otherwise.



---

## 13. Source metadata fields

Source metadata fields record where parameter values came from. They are important for audit-first usage.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 8573 | expander | with st.expander("Candidate and reference source metadata", expanded=True): |  |
| 8577 | text_input | candidate_source_paper = st.text_input("Candidate source paper / arXiv / DOI", value="User-entered / candidate parameter block") |  |
| 8578 | text_input | candidate_source_location = st.text_input("Candidate source table / figure / line", value="manual entry") |  |
| 8580 | text_input | reference_source_paper = st.text_input("Reference source paper / arXiv / DOI", value="Reference / LCDM comparison block") |  |
| 8581 | text_input | reference_source_location = st.text_input("Reference source table / figure / line", value="manual entry") |  |
| 9151 | selectbox | selected_live_input_source_8b = st.selectbox( |  |
| 11085 | expander | with st.expander("Paper / APJ conversion status", expanded=False): |  |
| 11390 | expander | with st.expander("Source TSV table — G01", expanded=False): |  |
| 11406 | expander | with st.expander("Source TSV table — G02", expanded=False): |  |
| 11422 | expander | with st.expander("Source TSV table — G03", expanded=False): |  |


Use these fields to record:

- Candidate source paper, arXiv identifier, DOI, or note.
- Candidate table, figure, line, or section.
- Reference source paper, arXiv identifier, DOI, or note.
- Reference table, figure, line, or section.

Source metadata does not validate the parameter. It records provenance so the value can be audited.

---

## 14. RK45 background proxy panel

The RK45 background proxy panel is a diagnostic background calculation interface. It should be treated as a proxy or limited calculation, not as a full Boltzmann-code result.

Safe usage:

- Run it only as a diagnostic check.
- Compare direction and consistency, not full likelihood.
- Record whether the output is a proxy, fixed example, live endpoint result, or frozen readback.
- Do not treat proxy success as physical closure.

---

## 15. AxiCLASS fixed-example and local endpoint controls

The app includes controls for limited AxiCLASS or CLASS-related endpoint checks. These controls are boundary-sensitive.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 7981 | expander | with st.expander("CMB spectra graph — real API arrays only", expanded=False): |  |
| 8820 | expander | with st.expander("Warm up configured API endpoints before 7a/7b", expanded=False): |  |
| 8830 | button | if st.button("Warm up public API", key="dti_warmup_public_api_7a7b_v2", width="stretch"): | dti_warmup_public_api_7a7b_v2 |
| 8878 | checkbox | enable_local_axiclass = st.checkbox( |  |
| 8890 | text_input | local_endpoint = st.text_input( |  |
| 8904 | checkbox | use_7a_cache = st.checkbox( |  |
| 8911 | expander | with st.expander("How to use the AxiCLASS API endpoint", expanded=False): |  |
| 8927 | button | if st.button("Run fixed-example check", key="run_local_axiclass_fixed_example_v606", width="stretch", type="primary"): | run_local_axiclass_fixed_example_v606 |
| 9011 | expander | with st.expander("Raw fixed-example API response", expanded=False): |  |
| 10686 | text_input | external_api_url = st.text_input( |  |
| 10698 | button | if st.button("Run external CLASS API for current input model", key="run_external_class_api_v606", width="stretch", type="primary"): | run_external_class_api_v606 |
| 10750 | expander | with st.expander("Raw external API response", expanded=False): |  |
| 10755 | expander | with st.expander("CMB spectra graph — real API arrays only", expanded=True): |  |


### enable_local_axiclass

- Purpose: allows a local endpoint path to be used when configured.
- Boundary: enabling a checkbox does not itself validate a model.
- Risk: endpoint results depend on the endpoint implementation, version, and frozen scope.

### local_endpoint

- Purpose: text field for local endpoint URL.
- Boundary: URL entry does not guarantee endpoint compatibility.
- Safe use: confirm health/status output and boundary flags.

### use_7a_cache

- Purpose: permits cached results for relevant panel.
- Boundary: cache use must be described; cached results are not fresh computation.

### Run fixed-example check

- Purpose: calls or displays a fixed-example status.
- Boundary: fixed-example-only is not arbitrary parameter inference.

---

## 16. Live vanilla CLASS probe controls

The live vanilla CLASS probe controls provide a limited path for vanilla-like backend checks.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 8820 | expander | with st.expander("Warm up configured API endpoints before 7a/7b", expanded=False): |  |
| 8830 | button | if st.button("Warm up public API", key="dti_warmup_public_api_7a7b_v2", width="stretch"): | dti_warmup_public_api_7a7b_v2 |
| 9120 | checkbox | enable_live_vanilla_probe = st.checkbox( |  |
| 9128 | text_input | live_probe_url = st.text_input( |  |
| 9144 | checkbox | use_7b_cache = st.checkbox( |  |
| 9151 | selectbox | selected_live_input_source_8b = st.selectbox( |  |
| 9204 | number_input | live_H0 = st.number_input( |  |
| 9211 | number_input | live_omega_b = st.number_input( |  |
| 9221 | number_input | live_omega_cdm = st.number_input( |  |
| 9229 | number_input | live_ns = st.number_input( |  |
| 9239 | number_input | live_ln1010As = st.number_input( |  |


### enable_live_vanilla_probe

- Purpose: enables the live probe section.
- Boundary: enabling does not run a full model comparison.

### live_probe_url

- Purpose: endpoint URL for the live probe.
- Boundary: endpoint identity and implementation determine scope.

### use_7b_cache

- Purpose: allows cached results.
- Boundary: cache status must be disclosed.

### selected_live_input_source_8b

- Purpose: chooses where live input values come from.
- Boundary: selecting a source is not validation.

### live_H0, live_omega_b, live_omega_cdm, live_ns, live_ln1010As

These fields define input values for a limited live probe. They are not posterior samples and do not imply a Planck likelihood result.

---

## 17. Continuity examiner 7c controls

The continuity examiner 7c section is an audit tool for response continuity across a parameter sweep. It is not a physical discontinuity proof.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 9958 | checkbox | enable_continuity_examiner = st.checkbox( |  |
| 9985 | number_input | c7c_base_H0 = st.number_input( |  |
| 9993 | number_input | c7c_base_omega_b = st.number_input( |  |
| 10004 | number_input | c7c_base_omega_cdm = st.number_input( |  |
| 10013 | number_input | c7c_base_ns = st.number_input( |  |
| 10024 | number_input | c7c_base_ln1010As = st.number_input( |  |
| 10047 | selectbox | sweep_param_7c = st.selectbox( |  |
| 10053 | number_input | grid_n_7c = st.number_input( |  |
| 10072 | number_input | sweep_start_7c = st.number_input( |  |
| 10079 | number_input | sweep_end_7c = st.number_input( |  |
| 10088 | number_input | jump_threshold_7c = st.number_input( |  |
| 10097 | number_input | repeat_count_7c = st.number_input( |  |


### enable_continuity_examiner

- Purpose: enables the 7c continuity audit interface.
- Boundary: enabling does not prove continuity or discontinuity; it allows a configured check.

### c7c_base_H0, c7c_base_omega_b, c7c_base_omega_cdm, c7c_base_ns, c7c_base_ln1010As

- Purpose: baseline parameter values for the sweep.
- Boundary: baseline values define the local audit configuration only.

### sweep_param_7c

- Purpose: chooses which parameter is swept.
- Boundary: only the selected parameter is varied.

### grid_n_7c

- Purpose: number of grid points in the sweep.
- Boundary: grid density affects resolution but does not create proof by itself.

### sweep_start_7c and sweep_end_7c

- Purpose: parameter range for the sweep.
- Boundary: conclusions are bounded to the selected interval.

### jump_threshold_7c

- Purpose: threshold used to flag candidate jumps in the diagnostic.
- Boundary: a threshold crossing is a diagnostic flag, not a physical proof.

### repeat_count_7c

- Purpose: repetition count for stability checks.
- Boundary: repetitions help audit robustness but do not replace formal inference.

---

## 18. External CLASS API controls

External CLASS API controls let the app communicate with a configured external endpoint for selected checks. They are dependency-sensitive and boundary-sensitive.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 8911 | expander | with st.expander("How to use the AxiCLASS API endpoint", expanded=False): |  |
| 10686 | text_input | external_api_url = st.text_input( |  |
| 10698 | button | if st.button("Run external CLASS API for current input model", key="run_external_class_api_v606", width="stretch", type="primary"): | run_external_class_api_v606 |
| 10750 | expander | with st.expander("Raw external API response", expanded=False): |  |


### external_api_url

- Purpose: endpoint URL for external CLASS-like API call.
- Boundary: public URL entry does not establish correctness of the backend.

### Run external CLASS API for current input model

- Purpose: sends the current input model to the configured endpoint.
- Boundary: result interpretation depends on endpoint implementation. It is not automatically a likelihood or posterior result.

---

## 19. Jump parameter translator — backend boundary check

The Jump parameter translator converts or normalizes jump-style parameter inputs for backend boundary checking. It is not a full physical implementation of DTI microphysics.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 6118 | number_input | z_jump = st.number_input( |  |
| 10871 | expander | with st.expander("Jump parameter translator — backend boundary check", expanded=False): |  |
| 10881 | number_input | h0 = st.number_input("H0", min_value=1.0, max_value=150.0, value=72.6, step=0.1, key="dti_jump_tr_h0_v1") | dti_jump_tr_h0_v1 |
| 10882 | number_input | omega_b = st.number_input("omega_b", min_value=0.0001, max_value=0.2, value=0.02237, step=0.00001, format="%.5f", key="dti_jump_tr_omega_b_v1") | dti_jump_tr_omega_b_v1 |
| 10883 | number_input | omega_cdm = st.number_input("omega_cdm", min_value=0.0001, max_value=1.0, value=0.1200, step=0.0001, format="%.4f", key="dti_jump_tr_omega_cdm_v1") | dti_jump_tr_omega_cdm_v1 |
| 10885 | number_input | ln10_10_as = st.number_input("ln10_10_As", min_value=0.1, max_value=10.0, value=3.044, step=0.001, format="%.3f", key="dti_jump_tr_ln10as_v1") | dti_jump_tr_ln10as_v1 |
| 10886 | number_input | n_s = st.number_input("n_s", min_value=0.1, max_value=2.0, value=0.965, step=0.001, format="%.3f", key="dti_jump_tr_ns_v1") | dti_jump_tr_ns_v1 |
| 10887 | number_input | tau_reio = st.number_input("tau_reio", min_value=0.0, max_value=1.0, value=0.054, step=0.001, format="%.3f", key="dti_jump_tr_tau_v1") | dti_jump_tr_tau_v1 |
| 10889 | number_input | a_j = st.number_input("A_J", min_value=-1.0, max_value=1.0, value=-0.00022, step=0.00001, format="%.5f", key="dti_jump_tr_aj_v1") | dti_jump_tr_aj_v1 |
| 10890 | number_input | z_j = st.number_input("z_J", min_value=0.0001, max_value=5000.0, value=1100.0, step=1.0, key="dti_jump_tr_zj_v1") | dti_jump_tr_zj_v1 |
| 10891 | number_input | delta_z = st.number_input("Delta_z", min_value=0.0001, max_value=2000.0, value=30.0, step=1.0, key="dti_jump_tr_dz_v1") | dti_jump_tr_dz_v1 |
| 10893 | selectbox | regime = st.selectbox( |  |
| 10923 | button | if st.button("Run translator boundary check", key="dti_jump_translator_run_v1"): | dti_jump_translator_run_v1 |


### H0

Translator input for the Hubble constant. It is used in the translator payload, not as a posterior parameter.

### omega_b and omega_cdm

Translator inputs for physical baryon and cold-dark-matter densities. They are boundary-check fields.

### ln10_10_As

Translator amplitude input. It does not by itself generate spectra or likelihoods.

### n_s

Translator scalar spectral index input.

### tau_reio

Translator reionization optical depth input.

### A_J

Jump amplitude-style parameter. Boundary: a translator response with `A_J` does not prove a physical jump.

### z_J

Jump redshift-style parameter. Boundary: a selected `z_J` is a model-interface input, not observational proof of a transition.

### Delta_z

Jump width-style parameter. Boundary: controls the interface representation of transition width.

### regime

Translator option controlling the boundary-check regime. It should be documented together with the returned warnings and boundary fields.

### Run translator boundary check

This button runs the translator boundary check. It does not run full CLASS/AxiCLASS physics, CMB spectra, Planck likelihood, or MCMC unless a separate backend implementation explicitly says so.

---

## 20. DTI capability provenance and no-claim boundary

The capability provenance section records which capabilities exist, which are frozen, and which remain unavailable or out of scope. This section should be read before quoting any technical output.

A no-claim boundary is not a weakness. It is a deliberate audit-first constraint. It prevents static diagnostic panels from being mistaken for formal inference.

---

## 21. Embedded posterior viewer — offline BAO chain, audit-only

The embedded posterior viewer is intended for frozen offline chain displays. Its public form should remain lightweight. It is not a live MCMC runner.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 11209 | expander | with st.expander("Embedded posterior viewer — offline BAO chain, audit-only", expanded=True): |  |


Safe interpretation:

- It may display frozen chain summaries or maps.
- It should not run MCMC live in the app.
- It should not claim posterior comparison beyond the frozen audited package.
- It should not imply Planck validation.

---

## 22. Frozen BAO graph viewer

The frozen BAO graph viewer displays source-locked or frozen BAO-related diagnostic visualizations. It is not a full BAO likelihood unless explicitly implemented and frozen.

Graph policy:

- Use only frozen/source-compatible data.
- Do not synthesize scientific-looking curves.
- Keep diagnostic and likelihood language separate.

---

## 23. Route A manual-sanity diagnostic

The Route A manual-sanity diagnostic is a frozen independent lane. It provides a bounded check and helps compare algebraic or diagnostic behavior.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 11489 | expander | with st.expander("Route A manual-sanity diagnostic — frozen independent lane", expanded=False): |  |


Safe wording:

> Route A manual-sanity is an independent diagnostic lane. It is useful for checking a bounded calculation path, but it is not a full BAO/eBOSS likelihood and not a posterior inference.

---

## 24. Route A/B Boundary Matrix

The Route A/B Boundary Matrix separates diagnostic availability from full inference availability.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 11209 | expander | with st.expander("Embedded posterior viewer — offline BAO chain, audit-only", expanded=True): |  |
| 11573 | expander | with st.expander("Route A/B Boundary Matrix — diagnostic available, full inference unavailable", expanded=False): |  |
| 11624 | expander | with st.expander("Route A/B boundary provenance", expanded=False): |  |


Current conceptual interpretation:

- Route B frozen reference: a source-locked diagnostic result.
- Route A derived template: a derived diagnostic template.
- Route A manual-sanity independent lane: an independent diagnostic check.
- Full BAO/eBOSS likelihood: not available in this panel.
- MCMC/posterior inference: not available in this panel.
- Planck validation: not performed here.

The matrix should be read in three layers:

1. Full inference: NO.
2. Frozen diagnostic display: YES, where explicitly shown.
3. Interpretation: bounded.

---

## 25. Route A/B boundary provenance

This section records where the Route A/B matrix values came from and what they do not mean. It is essential for reviewer-safe reading.

Use it to verify:

- Source handoff path.
- Frozen route identity.
- Diagnostic chi2 value identity.
- Non-likelihood boundary.
- Non-posterior boundary.

---

## 26. Likelihood Definition Binder

The Likelihood Definition Binder is an audit-only section for defining what would count as a likelihood, what is currently implemented, and what remains absent.

Relevant extracted UI rows:

_No matching rows were extracted in the survey._


Safe interpretation:

- It clarifies definitions.
- It does not create a likelihood result by being present.
- It helps prevent diagnostic values from being mislabeled as likelihood evidence.

---

## 27. About / Citation / Provenance

The About / Citation / Provenance section identifies the project, author, contact, DOI references, app state, and boundary language.

Relevant extracted UI rows:

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 8577 | text_input | candidate_source_paper = st.text_input("Candidate source paper / arXiv / DOI", value="User-entered / candidate parameter block") |  |
| 8580 | text_input | reference_source_paper = st.text_input("Reference source paper / arXiv / DOI", value="Reference / LCDM comparison block") |  |
| 11053 | expander | with st.expander("DTI capability provenance and no-claim boundary", expanded=False): |  |
| 11243 | expander | with st.expander("Raw embedded tables — provenance / audit readback", expanded=False): |  |
| 11624 | expander | with st.expander("Route A/B boundary provenance", expanded=False): |  |
| 11793 | expander | with st.expander("About / Citation / Provenance", expanded=False): |  |


Use this section when citing the public app. Record:

- Public URL.
- Git HEAD.
- `app.py` SHA.
- Freeze package identity if available.
- DOI or manuscript companion references.
- Boundary status of the quoted panel.

---

## 28. Troubleshooting and cache behavior

### The public app does not show a recent update

Streamlit public reflection can lag after a push. Refresh the browser, clear cache if needed, or wait for the downstream sync.

### A button appears to do nothing

Many Streamlit buttons update session state and trigger a rerun. After pressing the button, inspect whether fields changed.

### A graph is unavailable

If a graph panel requires real API arrays and none are available, the correct behavior is to show an unavailable or readiness message. The app should not invent a scientific-looking graph.

### A readiness flag says NO

Read `NO` as not available in this panel or not implemented in this public route. Do not read it as a failed likelihood result.

### Raw data is large

Use compact tables first. Raw panels exist for audit, not for first-pass reading.

---

## 29. Reviewer-safe language templates

### General app description

> The DTI Real App is a public audit and diagnostic viewer. It displays bounded, source-locked, and diagnostic readouts. It is not a live MCMC app, not a full likelihood engine, and not a Planck or JWST validation interface.

### Background geometry

> The background-geometry panel provides local FLRW-style diagnostic readouts for selected inputs. These outputs are useful for audit and intuition, but they are not a full Boltzmann-code or likelihood result.

### Jump toy comparator

> The Jump toy comparator is a local piecewise background-geometry toy diagnostic. It demonstrates sensitivity of selected distance/time readouts to a toy modification and does not prove a physical discontinuity.

### Route A/B matrix

> The Route A/B Boundary Matrix separates frozen diagnostic displays from unavailable full inference. The shown values are bounded diagnostic readouts and should not be described as a full BAO/eBOSS likelihood or posterior result.

### Embedded posterior viewer

> The embedded posterior viewer is intended for frozen offline chain summaries. It does not run live MCMC in the public app.

### CMB / Likelihood readiness

> Readiness flags identify capability availability. A `NO` flag does not mean a model failed; it means that capability is not available or not implemented in that panel.

---

## 30. Exhaustive parameter glossary

This glossary summarizes the main user-facing parameters and controls extracted in the survey.

| section | group | parameter_or_control | documentation_required |
| --- | --- | --- | --- |
| background_geometry | FLRW anchor | H0 | meaning, units, allowed range, output effect, boundary |
| background_geometry | FLRW anchor | Omega_m | meaning, allowed range, physical caveat, output effect |
| background_geometry | FLRW anchor | Omega_vac | meaning, allowed range, flatness caveat, output effect |
| background_geometry | FLRW anchor | z | redshift meaning, upper limit, graph/table effect |
| jump_toy | comparator | z_jump | threshold redshift for piecewise toy; not physical proof |
| jump_toy | comparator | jump_factor | multiplier for E(z) above z_jump; toy-only |
| jump_toy | comparator | Load jump-toy demonstration values | button behavior, loaded values, rerun behavior |
| jump_toy | comparator | expanded=True | default-open expander behavior; user may still close it |
| cmb_likelihood | readiness flags | CMB graph readiness | explain YES/NO as availability, not evidence |
| cmb_likelihood | readiness flags | Planck likelihood readiness | explain backend requirement and no posterior claim |
| profile_forms | target model | H0,f_EDE,omega_cdm,omega_b,sigma8,S8,z_c,ln10_10_As,n_s,tau_reio | defaults/ranges/meaning/boundary |
| lcdm_forms | comparison model | LCDM H0,LCDM Omega_m,LCDM omega_cdm,LCDM omega_b,LCDM sigma8,LCDM S8,LCDM ln10_10_As,LCDM n_s,LCDM tau_reio | defaults/ranges/meaning/boundary |
| source_metadata | provenance | candidate_source_paper,candidate_source_location,reference_source_paper,reference_source_location | how to record provenance |
| api_controls | local endpoint | enable_local_axiclass,local_endpoint,use_7a_cache | explain fixed-example and cache boundaries |
| live_probe | vanilla probe | enable_live_vanilla_probe,live_probe_url,use_7b_cache,selected_live_input_source_8b | explain live probe boundary |
| live_probe | inputs | live_H0,live_omega_b,live_omega_cdm,live_ns,live_ln1010As | input meaning and no posterior interpretation |
| continuity_7c | examiner | enable_continuity_examiner,c7c_base_H0,c7c_base_omega_b,c7c_base_omega_cdm,c7c_base_ns,c7c_base_ln1010As | explain continuity audit |
| continuity_7c | sweep | sweep_param_7c,grid_n_7c,sweep_start_7c,sweep_end_7c,jump_threshold_7c,repeat_count_7c | explain grid audit and threshold |
| external_api | CLASS endpoint | external_api_url,Run external CLASS API for current input model | explain external dependency and boundary |
| jump_translator | translator | H0,omega_b,omega_cdm,ln10_10_As,n_s,tau_reio,A_J,z_J,Delta_z,regime | explain backend boundary check, not full physics validation |
| route_a_b | diagnostic matrix | Route B frozen reference,Route A derived template,Route A manual-sanity lane | explain chi2 values as diagnostic-only |
| citation | provenance | author,contact,project,DOIs | explain citation block and provenance |


### Additional extracted UI controls

The following table is a direct survey-derived list of UI controls. Some rows are internal or legacy, but they are retained here for audit completeness.

| line | kind | label_or_call | key_hint |
| --- | --- | --- | --- |
| 741 | slider | stability_score = st.slider( |  |
| 752 | slider | signal_score = st.slider( |  |
| 763 | slider | explanation_score = st.slider( |  |
| 774 | slider | next_test_score = st.slider( |  |
| 785 | slider | overclaim_risk = st.slider( |  |
| 2217 | expander | with st.expander(label, expanded=False): |  |
| 2237 | tabs | tabs = st.tabs(["Core branch", "Companion parameters", "Safety / next checks"]) |  |
| 2345 | expander | with st.expander("Boundary note for reviewers and researchers", expanded=False): |  |
| 2935 | expander | with st.expander(title, expanded=False): |  |
| 3325 | number_input | return st.number_input( |  |
| 3579 | selectbox | candidate_preset = st.selectbox( |  |
| 3588 | selectbox | reference_preset = st.selectbox( |  |
| 3601 | button | if st.button("Load selected presets", key="dti_ui_load_presets_v2", type="primary"): | dti_ui_load_presets_v2 |
| 3608 | tabs | tab_candidate, tab_reference = st.tabs(["Candidate", "Reference"]) |  |
| 3832 | selectbox | candidate_preset = st.selectbox( |  |
| 3839 | selectbox | reference_preset = st.selectbox( |  |
| 3849 | button | if st.button("Load selected presets into inputs", key="dti_ui_load_presets_v1"): | dti_ui_load_presets_v1 |
| 3855 | expander | with st.expander("Candidate profile inputs", expanded=True): |  |
| 3863 | expander | with st.expander("Reference profile inputs", expanded=True): |  |
| 5346 | expander | with st.expander("Boundary and claim limits", expanded=False): |  |
| 5425 | expander | with st.expander("Direction summary — static TSV only", expanded=False): |  |
| 5439 | expander | with st.expander("Compact static delta table — audit display only", expanded=False): |  |
| 5447 | expander | with st.expander("Compact static delta table — reader view", expanded=True): |  |
| 5452 | expander | with st.expander("Boundary and safe interpretation", expanded=False): |  |
| 5589 | expander | with st.expander("Raw data — audit view", expanded=False): |  |
| 5620 | expander | with st.expander("Raw data — audit view", expanded=False): |  |
| 5829 | expander | with st.expander("Background geometry anchor — local FLRW calculator", expanded=False): |  |
| 5836 | number_input | bg_H0 = st.number_input( |  |
| 5846 | number_input | bg_om = st.number_input( |  |
| 5856 | number_input | bg_ov = st.number_input( |  |
| 5866 | number_input | bg_z = st.number_input( |  |
| 5880 | expander | with st.expander("Raw data — audit view", expanded=False): |  |
| 6106 | expander | with st.expander("Jump toy comparator — piecewise background geometry", expanded=True): |  |
| 6111 | button | if st.button("Load jump-toy demonstration values", key="dti_bggeom_load_jump_toy_demo_values_v1"): | dti_bggeom_load_jump_toy_demo_values_v1 |
| 6118 | number_input | z_jump = st.number_input( |  |
| 6128 | number_input | jump_factor = st.number_input( |  |
| 6161 | tabs | ttab, dtab, deltab = st.tabs(["Time baseline", "Distance baseline", "Delta"]) |  |
| 6201 | expander | with st.expander("Raw data — audit view", expanded=False): |  |
| 6479 | tabs | tab_time, tab_distance, tab_scale = st.tabs(["Time baseline", "Distance baseline", "Angular scale"]) |  |
| 6514 | expander | with st.expander("Raw data — audit view", expanded=False): |  |
| 6549 | expander | with st.expander("Global claim limits / audit boundary", expanded=False): |  |
| 6576 | expander | return st.expander(title, expanded=False) |  |
| 6628 | expander | with st.expander("Raw data — audit view", expanded=False): |  |
| 6682 | expander | with st.expander("Raw data — audit view", expanded=False): |  |
| 6721 | expander | with st.expander("Raw data — audit view", expanded=False): |  |
| 6765 | expander | with st.expander("Raw data — audit view", expanded=False): |  |
| 7981 | expander | with st.expander("CMB spectra graph — real API arrays only", expanded=False): |  |
| 8233 | expander | with st.expander("CMB array availability audit", expanded=False): |  |
| 8249 | tabs | tab1, tab2, tab3, tab4 = st.tabs(["TT", "TE", "EE", "Lensing"]) |  |
| 8433 | selectbox | _dti_fallback_selected_preset_v2b = st.selectbox( |  |
| 8477 | button | if st.button("Apply text to form", width="stretch", key="sidebar_text_to_form_v606", type="primary"): | sidebar_text_to_form_v606 |
| 8481 | button | if st.button("Form to text", width="stretch", key="sidebar_form_to_text_v606"): | sidebar_form_to_text_v606 |
| 8525 | expander | with st.expander("TARGET_MODEL form", expanded=True): |  |
| 8528 | number_input | st.number_input("H0", min_value=40.0, max_value=90.0, step=0.01, key="target_H0") | target_H0 |
| 8529 | number_input | st.number_input("f_EDE", min_value=0.0, max_value=0.30, step=0.001, key="target_f_EDE") | target_f_EDE |
| 8531 | number_input | st.number_input("omega_cdm", min_value=0.05, max_value=0.20, step=0.0001, format="%.5f", key="target_omega_cdm") | target_omega_cdm |
| 8532 | number_input | st.number_input("omega_b", min_value=0.015, max_value=0.035, step=0.0001, format="%.5f", key="target_omega_b") | target_omega_b |
| 8534 | number_input | st.number_input("sigma8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="target_sigma8") | target_sigma8 |
| 8535 | number_input | st.number_input("S8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="target_S8") | target_S8 |
| 8537 | number_input | st.number_input("z_c", min_value=0.0, max_value=10000.0, step=50.0, key="target_z_c") | target_z_c |
| 8538 | number_input | st.number_input("ln10_10_As", min_value=1.0, max_value=4.5, step=0.001, format="%.5f", key="target_ln10_10_As") | target_ln10_10_As |
| 8540 | number_input | st.number_input("n_s", min_value=0.80, max_value=1.20, step=0.0001, format="%.5f", key="target_n_s") | target_n_s |
| 8541 | number_input | st.number_input("tau_reio", min_value=0.0, max_value=0.20, step=0.0001, format="%.5f", key="target_tau_reio") | target_tau_reio |
| 8543 | expander | with st.expander("LCDM comparison form", expanded=False): |  |
| 8546 | number_input | st.number_input("LCDM H0", min_value=40.0, max_value=90.0, step=0.01, key="lcdm_H0") | lcdm_H0 |
| 8547 | number_input | st.number_input("LCDM Omega_m", min_value=0.10, max_value=0.60, step=0.001, format="%.5f", key="lcdm_Omega_m") | lcdm_Omega_m |
| 8549 | number_input | st.number_input("LCDM omega_cdm", min_value=0.05, max_value=0.20, step=0.0001, format="%.5f", key="lcdm_omega_cdm") | lcdm_omega_cdm |
| 8550 | number_input | st.number_input("LCDM omega_b", min_value=0.015, max_value=0.035, step=0.0001, format="%.5f", key="lcdm_omega_b") | lcdm_omega_b |
| 8552 | number_input | st.number_input("LCDM sigma8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="lcdm_sigma8") | lcdm_sigma8 |
| 8553 | number_input | st.number_input("LCDM S8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="lcdm_S8") | lcdm_S8 |
| 8555 | number_input | st.number_input("LCDM ln10_10_As", min_value=1.0, max_value=4.5, step=0.001, format="%.5f", key="lcdm_ln10_10_As") | lcdm_ln10_10_As |
| 8556 | number_input | st.number_input("LCDM n_s", min_value=0.80, max_value=1.20, step=0.0001, format="%.5f", key="lcdm_n_s") | lcdm_n_s |
| 8558 | number_input | st.number_input("LCDM tau_reio", min_value=0.0, max_value=0.20, step=0.0001, format="%.5f", key="lcdm_tau_reio") | lcdm_tau_reio |
| 8560 | button | if st.button("Apply form values to text and update search engine", type="primary", width="stretch"): |  |
| 8573 | expander | with st.expander("Candidate and reference source metadata", expanded=True): |  |
| 8577 | text_input | candidate_source_paper = st.text_input("Candidate source paper / arXiv / DOI", value="User-entered / candidate parameter block") |  |
| 8578 | text_input | candidate_source_location = st.text_input("Candidate source table / figure / line", value="manual entry") |  |
| 8580 | text_input | reference_source_paper = st.text_input("Reference source paper / arXiv / DOI", value="Reference / LCDM comparison block") |  |
| 8581 | text_input | reference_source_location = st.text_input("Reference source table / figure / line", value="manual entry") |  |
| 8728 | tabs | tabs = st.tabs(["FUJIKI DTI", "Ivanov EDE", "Ivanov LCDM", "Full table", "Delta table"]) |  |
| 8774 | button | if st.button("Run RK45 background proxy for current input model", width="stretch", type="primary"): |  |
| 8820 | expander | with st.expander("Warm up configured API endpoints before 7a/7b", expanded=False): |  |
| 8830 | button | if st.button("Warm up public API", key="dti_warmup_public_api_7a7b_v2", width="stretch"): | dti_warmup_public_api_7a7b_v2 |
| 8878 | checkbox | enable_local_axiclass = st.checkbox( |  |
| 8890 | text_input | local_endpoint = st.text_input( |  |
| 8904 | checkbox | use_7a_cache = st.checkbox( |  |
| 8911 | expander | with st.expander("How to use the AxiCLASS API endpoint", expanded=False): |  |
| 8927 | button | if st.button("Run fixed-example check", key="run_local_axiclass_fixed_example_v606", width="stretch", type="primary"): | run_local_axiclass_fixed_example_v606 |
| 9011 | expander | with st.expander("Raw fixed-example API response", expanded=False): |  |
| 9120 | checkbox | enable_live_vanilla_probe = st.checkbox( |  |
| 9128 | text_input | live_probe_url = st.text_input( |  |
| 9144 | checkbox | use_7b_cache = st.checkbox( |  |
| 9151 | selectbox | selected_live_input_source_8b = st.selectbox( |  |
| 9204 | number_input | live_H0 = st.number_input( |  |
| 9211 | number_input | live_omega_b = st.number_input( |  |
| 9221 | number_input | live_omega_cdm = st.number_input( |  |
| 9229 | number_input | live_ns = st.number_input( |  |
| 9239 | number_input | live_ln1010As = st.number_input( |  |
| 9289 | button | if st.button( |  |
| 9958 | checkbox | enable_continuity_examiner = st.checkbox( |  |
| 9985 | number_input | c7c_base_H0 = st.number_input( |  |
| 9993 | number_input | c7c_base_omega_b = st.number_input( |  |
| 10004 | number_input | c7c_base_omega_cdm = st.number_input( |  |
| 10013 | number_input | c7c_base_ns = st.number_input( |  |
| 10024 | number_input | c7c_base_ln1010As = st.number_input( |  |
| 10047 | selectbox | sweep_param_7c = st.selectbox( |  |
| 10053 | number_input | grid_n_7c = st.number_input( |  |
| 10072 | number_input | sweep_start_7c = st.number_input( |  |
| 10079 | number_input | sweep_end_7c = st.number_input( |  |
| 10088 | number_input | jump_threshold_7c = st.number_input( |  |
| 10097 | number_input | repeat_count_7c = st.number_input( |  |
| 10222 | button | if st.button( |  |
| 10686 | text_input | external_api_url = st.text_input( |  |
| 10698 | button | if st.button("Run external CLASS API for current input model", key="run_external_class_api_v606", width="stretch", type="primary"): | run_external_class_api_v606 |
| 10750 | expander | with st.expander("Raw external API response", expanded=False): |  |
| 10755 | expander | with st.expander("CMB spectra graph — real API arrays only", expanded=True): |  |
| 10871 | expander | with st.expander("Jump parameter translator — backend boundary check", expanded=False): |  |
| 10881 | number_input | h0 = st.number_input("H0", min_value=1.0, max_value=150.0, value=72.6, step=0.1, key="dti_jump_tr_h0_v1") | dti_jump_tr_h0_v1 |
| 10882 | number_input | omega_b = st.number_input("omega_b", min_value=0.0001, max_value=0.2, value=0.02237, step=0.00001, format="%.5f", key="dti_jump_tr_omega_b_v1") | dti_jump_tr_omega_b_v1 |
| 10883 | number_input | omega_cdm = st.number_input("omega_cdm", min_value=0.0001, max_value=1.0, value=0.1200, step=0.0001, format="%.4f", key="dti_jump_tr_omega_cdm_v1") | dti_jump_tr_omega_cdm_v1 |
| 10885 | number_input | ln10_10_as = st.number_input("ln10_10_As", min_value=0.1, max_value=10.0, value=3.044, step=0.001, format="%.3f", key="dti_jump_tr_ln10as_v1") | dti_jump_tr_ln10as_v1 |
| 10886 | number_input | n_s = st.number_input("n_s", min_value=0.1, max_value=2.0, value=0.965, step=0.001, format="%.3f", key="dti_jump_tr_ns_v1") | dti_jump_tr_ns_v1 |
| 10887 | number_input | tau_reio = st.number_input("tau_reio", min_value=0.0, max_value=1.0, value=0.054, step=0.001, format="%.3f", key="dti_jump_tr_tau_v1") | dti_jump_tr_tau_v1 |
| 10889 | number_input | a_j = st.number_input("A_J", min_value=-1.0, max_value=1.0, value=-0.00022, step=0.00001, format="%.5f", key="dti_jump_tr_aj_v1") | dti_jump_tr_aj_v1 |
| 10890 | number_input | z_j = st.number_input("z_J", min_value=0.0001, max_value=5000.0, value=1100.0, step=1.0, key="dti_jump_tr_zj_v1") | dti_jump_tr_zj_v1 |
| 10891 | number_input | delta_z = st.number_input("Delta_z", min_value=0.0001, max_value=2000.0, value=30.0, step=1.0, key="dti_jump_tr_dz_v1") | dti_jump_tr_dz_v1 |
| 10893 | selectbox | regime = st.selectbox( |  |
| 10920 | expander | with st.expander("Request payload preview", expanded=False): |  |
| 10923 | button | if st.button("Run translator boundary check", key="dti_jump_translator_run_v1"): | dti_jump_translator_run_v1 |
| 10960 | expander | with st.expander("Full translator response", expanded=False): |  |
| 11053 | expander | with st.expander("DTI capability provenance and no-claim boundary", expanded=False): |  |
| 11085 | expander | with st.expander("Paper / APJ conversion status", expanded=False): |  |
| 11153 | expander | with st.expander("Boundary / audit status", expanded=True): |  |
| 11209 | expander | with st.expander("Embedded posterior viewer — offline BAO chain, audit-only", expanded=True): |  |
| 11243 | expander | with st.expander("Raw embedded tables — provenance / audit readback", expanded=False): |  |
| 11270 | expander | with st.expander("Claim boundary", expanded=False): |  |
| 11371 | tabs | board_tabs = st.tabs([ |  |
| 11390 | expander | with st.expander("Source TSV table — G01", expanded=False): |  |
| 11406 | expander | with st.expander("Source TSV table — G02", expanded=False): |  |
| 11422 | expander | with st.expander("Source TSV table — G03", expanded=False): |  |
| 11428 | tabs | graph_tabs = st.tabs([ |  |
| 11489 | expander | with st.expander("Route A manual-sanity diagnostic — frozen independent lane", expanded=False): |  |
| 11573 | expander | with st.expander("Route A/B Boundary Matrix — diagnostic available, full inference unavailable", expanded=False): |  |
| 11624 | expander | with st.expander("Route A/B boundary provenance", expanded=False): |  |
| 11658 | expander | with _DTI_st.expander( |  |
| 11770 | expander | with st.expander("Frozen CLAIM_BOUNDARY.md readback", expanded=False): |  |
| 11793 | expander | with st.expander("About / Citation / Provenance", expanded=False): |  |


### Extracted session-state and key-like identifiers

The following identifiers were extracted for audit completeness.

| line | key |
| --- | --- |
| 161 | download_dti_local_8503_manual_pdf_v1 |
| 171 | download_dti_local_8503_readme_v3_safe |
| 748 | dti_discovery_score_stability_v1e |
| 759 | dti_discovery_score_signal_v1e |
| 770 | dti_discovery_score_explainability_v1e |
| 781 | dti_discovery_score_next_test_v1e |
| 792 | dti_discovery_score_overclaim_v1e |
| 3582 | dti_ui_candidate_preset_v1 |
| 3583 | dti_ui_candidate_preset_v2 |
| 3591 | dti_ui_reference_preset_v1 |
| 3592 | dti_ui_reference_preset_v2 |
| 3601 | dti_ui_load_presets_v2 |
| 3614 | dti_ui_candidate_table_editor_v1 |
| 3618 | dti_ui_reference_table_editor_v1 |
| 3634 | dti_ui_candidate_reference_rows_v1 |
| 3635 | dti_ui_candidate_profile_v1 |
| 3636 | dti_ui_reference_profile_v1 |
| 3637 | dti_ui_candidate_preset_name_v1 |
| 3638 | dti_ui_reference_preset_name_v1 |
| 3836 | dti_ui_candidate_preset_v1 |
| 3843 | dti_ui_reference_preset_v1 |
| 3849 | dti_ui_load_presets_v1 |
| 3882 | dti_ui_candidate_reference_rows_v1 |
| 3883 | dti_ui_candidate_profile_v1 |
| 3884 | dti_ui_reference_profile_v1 |
| 3896 | dti_ui_candidate_profile_v1 |
| 3897 | dti_ui_reference_profile_v1 |
| 3898 | dti_ui_candidate_reference_rows_v1 |
| 4745 | dti_active_profile_category_v2b |
| 4765 | dti_active_model_profile_v2b |
| 5088 | dti_profile_category_guide_category_v1_safe_fixindent |
| 5100 | dti_profile_category_guide_model_preview_v1_safe_fixindent |
| 5108 | dti_profile_category_guide_show_archive_counts_v1_safe_fixindent |
| 5843 | dti_bggeom_H0_v1 |
| 5853 | dti_bggeom_omega_m_v1 |
| 5863 | dti_bggeom_omega_vac_v1 |
| 5873 | dti_bggeom_z_v1 |
| 5989 | jump_model |
| 6006 | jump_factor_E_above_zjump |
| 6050 | jump_toy |
| 6051 | delta_jump_minus_vanilla |
| 6058 | jump_toy |
| 6059 | delta_jump_minus_vanilla |
| 6111 | dti_bggeom_load_jump_toy_demo_values_v1 |
| 6112 | dti_bggeom_jump_z_v1b |
| 6113 | dti_bggeom_jump_factor_v1b |
| 6125 | dti_bggeom_jump_z_v1b |
| 6135 | dti_bggeom_jump_factor_v1b |
| 6143 | jump_definition |
| 6145 | jump_factor |
| 6169 | jump_age_at_z_Gyr |
| 6171 | jump_light_travel_time_Gyr |
| 6182 | jump_comoving_radial_distance_Mpc |
| 6184 | jump_luminosity_distance_Mpc |
| 6204 | jump_toy |
| 6652 | relative_jump_threshold |
| 7918 | cmb_graph_readiness |
| 8210 | cmb_array_source |
| 8211 | cmb_array_export_status |
| 8212 | cmb_array_lmax_requested |
| 8830 | dti_warmup_public_api_7a7b_v2 |
| 8835 | dti_public_api_warmup_rows_7a7b_v2 |
| 8837 | dti_public_api_warmup_rows_7a7b_v2 |
| 8838 | dti_public_api_warmup_rows_7a7b_v2 |
| 8907 | dti_use_7a_frontend_cache_v2 |
| 9147 | dti_use_7b_frontend_cache_v2 |
| 9415 | dti_section8_top_restricted_notice_once_v3 |
| 9440 | dti_section8_boundary_notice_once_v1 |
| 9459 | dti_section8_no_source_data_notice_v1 |
| 9640 | dti_graph_ui_v607_section7c |
| 9663 | dti_graph_ui_dom_stable_chart_01 |
| 9719 | dti_graph_ui_dom_stable_chart_02 |
| 9730 | dti_graph_ui_v607_section8 |
| 9780 | dti_graph_ui_dom_stable_chart_03 |
| 9794 | dti_graph_ui_dom_stable_chart_04 |
| 9831 | dti_graph_ui_dom_stable_chart_05 |
| 9845 | dti_graph_ui_dom_stable_chart_06 |
| 9886 | dti_graph_ui_dom_stable_chart_07 |
| 9901 | dti_graph_ui_v607_section9 |
| 10095 | section7c_jump_threshold_v606 |
| 10119 | relative_jump_threshold |
| 10168 | relative_jump_score |
| 10202 | jump_candidate |
| 10211 | relative_jump_score |
| 10345 | jump_candidate |
| 10355 | jump_candidate |
| 10375 | relative_jump_threshold |
| 10379 | retained_jump_candidate_count |
| 10380 | micro_jitter_not_jump_count |
| 10434 | download_section7c_jump_scores_tsv_v606 |
| 10831 | cmb_spectra_generated |
| 10835 | jump_model_active |
| 10836 | jump_background_active |
| 10837 | jump_perturbations_active |
| 10881 | dti_jump_tr_h0_v1 |
| 10882 | dti_jump_tr_omega_b_v1 |
| 10883 | dti_jump_tr_omega_cdm_v1 |
| 10885 | dti_jump_tr_ln10as_v1 |
| 10886 | dti_jump_tr_ns_v1 |
| 10887 | dti_jump_tr_tau_v1 |
| 10889 | dti_jump_tr_aj_v1 |
| 10890 | dti_jump_tr_zj_v1 |
| 10891 | dti_jump_tr_dz_v1 |
| 10894 | jump_regime_label |
| 10897 | dti_jump_tr_regime_v1 |
| 10901 | jump_parameter_translation_only |
| 10908 | jump_model_enabled |
| 10909 | jump_target |
| 10914 | jump_regime_label |
| 10923 | dti_jump_translator_run_v1 |
| 11062 | cmb_generation |
| 11181 | embedded_bao_sdss_dr16cosmo_v1 |
| 11541 | manual_minus_route_b |
| 11545 | full_bao_likelihood |
| 11627 | route_b_frozen_reference_chi2 |
| 11628 | route_a_derived_template_chi2 |
| 11629 | route_a_manual_sanity_independent_lane_chi2 |
| 11630 | manual_minus_route_b |
| 11631 | route_b_scope |
| 11632 | route_a_scope |
| 11634 | full_bao_eboss_likelihood |
| 11766 | embedded_bao_sdss_dr16cosmo_v1 |


---

## 31. Version identity and freeze records

This manual corresponds to the following app identity at patch time:

- Public URL: `https://dti-real-app-v606.streamlit.app/`
- Git HEAD / origin: `fb7970261e2fadc42e2ab673dba108e6262b4b20`
- `app.py` SHA256: `dd0bf188bdb74750a2dc8b6b952a050d51a502add1220bfd77ba9cb5e8a9254f`
- `app.py` line count: `11819`

Important recent state:

- Jump toy comparator public push was completed with `expanded=True`.
- Button label: `Load jump-toy demonstration values`.
- Button key: `dti_bggeom_load_jump_toy_demo_values_v1`.
- Demo values: `z_jump = 2.5`, `jump_factor = 1.00001`.
- The app remains bounded: no backend/API/CLASS/AxiCLASS run is implied by this manual; no chi2 recomputation, likelihood, MCMC, posterior claim, Planck/JWST validation, or manuscript update is performed by the manual.

---

## 32. Prohibited overclaims

Do not use the app or this manual to claim:

- DTI is validated.
- The Hubble tension is solved.
- A full eBOSS LRG likelihood has been implemented where only a diagnostic matrix is shown.
- A physical discontinuity has been proven by the Jump toy comparator.
- A Planck likelihood has been run where readiness says unavailable.
- A posterior comparison has been performed where only frozen or diagnostic displays are shown.
- JWST validates the model.
- A public button or plot is equivalent to a full scientific result.

---

## 33. Closing note

The app is strongest when used exactly as designed: as a conservative, audit-first, provenance-first, reproducibility-first public viewer. Its value is not that every panel makes a strong claim. Its value is that every panel can be read with a clear boundary.
