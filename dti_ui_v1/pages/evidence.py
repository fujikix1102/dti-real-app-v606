from __future__ import annotations

import streamlit as st

from dti_ui_v1.services.run_store import list_run_artifacts


def render() -> None:
    st.title("Evidence")
    st.caption("Durable run identities, scientific contracts, and interpretation limits")
    artifacts = list_run_artifacts()
    source_tab, run_tab, boundary_tab = st.tabs(("Source contracts", "Run artifacts", "Boundaries"))
    with source_tab:
        st.dataframe(
            [
                {"Object": "General CLASS / AxiCLASS", "Input": "8 cosmological controls", "Output": "CMB + distances + 3 likelihood families", "Validation": "official data identity + finite outputs"},
                {"Object": "Planck 2018", "Input": "lensed TT/TE/EE", "Output": "Plik-lite + low-T + low-E log L", "Validation": "clipy likelihood self-tests"},
                {"Object": "Pantheon+", "Input": "angular distances", "Output": "marginalized SN chi-square", "Validation": "1701-row source + full covariance"},
                {"Object": "Locked DESI baseline", "Input": "use_locked_baseline=true", "Output": "verified theory vector + DESI likelihood", "Validation": "frozen-vector tolerance"},
                {"Object": "DTI injection/recovery", "Input": "72 transition conditions", "Output": "global 3-sigma recovery rates", "Validation": "10,000 seeded null + 72,000 injected simulations"},
                {"Object": "Catalog-level DTI pilot", "Input": "3 injected H(z) steps × 7 tracers", "Output": "coordinate/reconstruction/correlation/fit/13-value recovery", "Validation": "672 correlation functions + 84 anisotropic BAO fits"},
                {"Object": "Local H0 comparison contract", "Input": "Published SH0ES/CCHP Gaussian summaries", "Output": "Pull and trade-off rail", "Validation": "single-anchor selection + overlap prohibition"},
                {"Object": "Run artifact", "Input": "request + complete response", "Output": "atomic JSON", "Validation": "canonical SHA-256"},
            ], hide_index=True, use_container_width=True,
        )
    with run_tab:
        if artifacts:
            st.dataframe(artifacts, hide_index=True, use_container_width=True)
        else:
            st.info("No durable evidence record exists yet.")
    with boundary_tab:
        st.markdown(
            "- General runs propagate LCDM/AxiCLASS EDE and evaluate DESI DR2, Planck 2018, and Pantheon+.\n"
            "- Locked runs evaluate only the frozen baseline contract.\n"
            "- DESI DR2 BAO is a 13-value, seven-effective-redshift Gaussian compression derived from "
            "template-fitted clustering; it is not a raw-catalog transition likelihood.\n"
            "- Audit-DTI smoothness is conditional on that compression and the scanned AxiCLASS family; "
            "it cannot exclude transitions erased or unrepresented upstream.\n"
            "- The injection/recovery result measures a DESI-like transfer surrogate, not the production "
            "catalog, survey systematics, reconstruction, covariance, template fit, or Ly-alpha pipeline.\n"
            "- The catalog-level pilot executes coordinate conversion, FFT reconstruction, Landy-Szalay "
            "correlations, anisotropic BAO fitting, and 13-value compression on deterministic synthetic "
            "survey-shaped catalogs. It is not an official DESI EZmock/Abacus or production result.\n"
            "- Planck calibration A_planck is fixed to 1.0 in this deterministic view.\n"
            "- SH0ES and CCHP values are published summary coordinates only. They overlap supernova information "
            "with Pantheon+ and are never multiplied into the backend joint likelihood.\n"
            "- A reconciliation claim still requires the raw calibrator likelihood/covariance, declared priors, "
            "a converged posterior, and model comparison.\n"
            "- Posterior/MCMC remains outside scope until priors and convergence criteria are declared.\n"
            "- The toy transition laboratory is mathematical UI validation, not an EDE model."
        )
