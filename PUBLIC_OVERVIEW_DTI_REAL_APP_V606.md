# DTI-Core Grand Auditor v6.0.6 — Public overview

## Public app

https://dti-real-app-v606.streamlit.app

## Frontend repository

https://github.com/fujikix1102/dti-real-app-v606

## External CLASS API backend

https://dti-class-api.onrender.com

## Backend repository

https://github.com/fujikix1102/dti-class-api

---

## What this system is

DTI-Core Grand Auditor v6.0.6 is a public parameter-profile audit interface for cosmological model comparison, benchmark proximity review, and reproducibility-first inspection.

The system has three connected parts:

1. **Streamlit public frontend**  
   The user-facing app for loading parameter profiles, editing parameter blocks, comparing candidate/reference profiles, and inspecting benchmark context.

2. **GitHub source repositories**  
   The frontend and backend are versioned publicly through GitHub.

3. **Render CLASS API backend**  
   An external compute service that runs exploratory CLASS/PyCLASS propagation and returns derived quantities to the Streamlit app.

---

## What the Streamlit app does

The Streamlit app provides:

- 100 registered parameter-profile presets
- candidate/reference parameter input forms
- text-to-form and form-to-text conversion
- profile-nearest search
- locked AxiCLASS FIX1 benchmark display
- Planck-like fit-region inspection
- external CLASS API sandbox output

---

## What the external CLASS API does

The external Render backend receives a parameter block from the Streamlit app and runs exploratory CLASS/PyCLASS propagation.

The returned quantities include:

- h
- Omega_m_computed
- A_s
- sigma8_CLASS
- S8_CLASS
- rs_drag_Mpc_CLASS
- age_Gyr_CLASS

---

## Boundary

This system is not:

- a likelihood evaluation
- a posterior comparison
- a Planck validation pipeline
- an MCMC sampler
- a final cosmological validation tool
- a claim that the H0 tension is resolved
- a claim that the S8 tension is resolved
- a claim of a unique physical mechanism

The current external backend performs LCDM-like CLASS propagation only. Parameters such as f_EDE and z_c are passed for interface compatibility but are not used as AxiCLASS EDE microphysics in the minimal public backend.

---

## Intended use

This public system is intended for:

- parameter-profile inspection
- benchmark proximity review
- profile burden comparison
- reproducibility-oriented review
- teaching and exploratory analysis
- pre-likelihood triage

It is best understood as a public audit and inspection layer, not as a formal statistical inference engine.
