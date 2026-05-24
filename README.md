# DTI-Core Grand Auditor v6.0.6

**DTI-Core Grand Auditor** is a public Streamlit interface for inspecting, comparing, and auditing cosmological parameter profiles.

Public app:

https://dti-real-app-v606.streamlit.app

GitHub repository:

https://github.com/fujikix1102/dti-real-app-v606

---

## 1. What this app is

This app is a **parameter-profile audit interface**.

It helps users inspect and compare cosmological parameter blocks such as:

- H0
- f_EDE
- omega_cdm
- omega_b
- sigma8
- S8
- z_c
- n_s
- ln10_10_As
- tau_reio

The purpose is to make parameter burden, benchmark proximity, and profile-level comparison easier to inspect.

The app includes:

- 100 registered parameter-profile presets
- Candidate / Reference parameter input forms
- text-to-form and form-to-text conversion
- profile-nearest search
- locked AxiCLASS FIX1 benchmark values
- optional exploratory CLASS / AxiCLASS sandbox output

---

## 2. What this app does

The app allows users to:

1. Select a registered cosmological parameter profile.
2. Convert profile text into form fields.
3. Edit candidate and reference values.
4. Convert form values back into a parameter text block.
5. Compare candidate and reference parameter burdens.
6. Inspect registered profile proximity.
7. View locked AxiCLASS FIX1 benchmark references.
8. Run optional exploratory sandbox checks when locally available.

This is intended as a lightweight research interface for inspection, comparison, and reproducibility-oriented review.

---

## 3. What this app does not do

This app does **not** perform:

- likelihood evaluation
- posterior comparison
- Planck likelihood validation
- MCMC sampling
- external chain reanalysis
- final cosmological validation
- claim that the H0 tension is resolved
- claim that the S8 tension is resolved
- claim of a unique physical mechanism

The app should not be interpreted as a replacement for Cobaya, MontePython, CLASS, AxiCLASS, CAMB, or formal Planck likelihood pipelines.

---

## 4. Quick Start

1. Open the public app:

   https://dti-real-app-v606.streamlit.app

2. Select a registered profile from the left sidebar.

3. Inspect the generated parameter block.

4. Use **Text to form** to load the block into the input form.

5. Edit candidate or reference values.

6. Use **Form to text** to regenerate a parameter block.

7. Inspect candidate/reference differences.

8. Check locked AxiCLASS FIX1 benchmark values.

9. Treat live CLASS / AxiCLASS output, if used, as exploratory and non-canonical.

---

## 5. Included presets

The app includes 100 registered parameter-profile presets in:

    app/data/profile_presets_v606.tsv

The preset table has the following columns:

    Model ID
    H0
    f_EDE
    omega_cdm
    omega_b
    sigma8
    S8
    Profile role

The presets include baseline references, EDE-like reference regions, DTI candidate regions, lensing-suppressed regions, high-z growth-stress regions, and extreme-bound stress cases.

These presets are **parameter-profile cartridges**. They are not presented as independent likelihood evaluations.

---

## 6. AxiCLASS FIX1 locked benchmark

The AxiCLASS FIX1 section displays fixed benchmark values copied from a successful checkpoint.

These values are read-only benchmark references.

Changing the active preset or form values does **not** recompute the locked AxiCLASS FIX1 values.

This separation is intentional:

- locked benchmark values are fixed references
- live sandbox calculations are exploratory
- exploratory results are non-canonical
- live results do not overwrite locked checkpoints

---

## 7. Repository structure

    app.py
    requirements.txt
    README.md
    LICENSE
    .gitignore
    .streamlit/config.toml
    app/data/profile_presets_v606.tsv
    app/data/axiclass_fix1_results.tsv
    app/data/axiclass_fix1_delta.tsv

---

## 8. Local run

Clone the repository and run:

    pip install -r requirements.txt
    streamlit run app.py

---

## 9. Streamlit deployment

This repository is designed for Streamlit Community Cloud.

Deployment settings:

    Repository: fujikix1102/dti-real-app-v606
    Branch: main
    Main file path: app.py

---

## 10. Research-use boundary

This app is best understood as a reproducibility-first inspection layer.

It is useful for:

- parameter-profile comparison
- profile burden inspection
- benchmark proximity review
- teaching and exploratory analysis
- pre-likelihood triage
- audit-first communication

It is not a formal statistical inference engine.

---

## 11. Status

Current public version:

    v6.0.6-presets-expanded-inline

The current public app was exported from the local adopted v6.0.6 line and deployed through GitHub + Streamlit Community Cloud.

---

## External CLASS API backend

This public Streamlit app is connected to an external Render-hosted CLASS API backend:

    https://dti-class-api.onrender.com

The compute endpoint is:

    https://dti-class-api.onrender.com/class/compute

The backend repository is:

    https://github.com/fujikix1102/dti-class-api

### What the external backend does

The backend runs exploratory CLASS/PyCLASS propagation outside the Streamlit Community Cloud frontend.

This separation keeps the public Streamlit app lightweight while allowing heavier numerical propagation to run on a dedicated API service.

The current backend returns values such as:

- h
- Omega_m_computed
- A_s
- sigma8_CLASS
- S8_CLASS
- rs_drag_Mpc_CLASS
- age_Gyr_CLASS

### Boundary

The external backend is:

- exploratory
- non-canonical
- not a likelihood evaluation
- not a posterior comparison
- not a Planck validation pipeline
- not a manuscript checkpoint updater

The current backend scope is LCDM-like CLASS propagation. Parameters such as f_EDE and z_c are passed for interface compatibility, but they are not used as AxiCLASS EDE microphysics in the minimal public backend.
