from __future__ import annotations

import os

import streamlit as st


PUBLIC_APP_URL = "https://dti-perfect-fit.streamlit.app/"


def _preprint_url() -> str:
    return os.environ.get("DTI_PREPRINT_URL", "").strip()


def render_companion_reference_panel() -> None:
    st.subheader("Companion reference")
    st.caption(
        "Use this panel to understand what the public app claims, how to cite "
        "it, and how to reproduce saved artifacts."
    )

    st.markdown("#### Parameter definitions")
    st.caption(
        "Current public Level 2 runs are single deterministic CLASS/AxiCLASS "
        "forward calculations. They do not run posterior inference or MCMC."
    )
    st.latex(r"f_{\rm EDE}\equiv \max_z \Omega_{\rm EDE}(z)")
    st.caption(
        "f_EDE is the target early-dark-energy fraction forwarded to the "
        "AxiCLASS branch when nonzero."
    )
    st.latex(r"z_c:\quad \Omega_{\rm EDE}(z)\ {\rm peaks\ near}\ z_c")
    st.caption("z_c is the requested critical redshift for the EDE branch.")
    st.latex(r"A_{\rm DTI}:\ {\rm public\ diagnostic\ amplitude}")
    st.caption(
        "A_DTI is recorded in the public artifact as a PERFECT FIT diagnostic "
        "input. In the current General CLASS contract it is not forwarded into "
        "the CLASS/AxiCLASS backend equations."
    )

    preprint = _preprint_url()
    if preprint:
        st.link_button("Open preprint / paper note", preprint)
    else:
        st.info(
            "Preprint link is not configured yet. Set DTI_PREPRINT_URL when an "
            "arXiv or PDF URL is ready."
        )

    st.markdown("#### How to cite")
    bibtex = f"""@misc{{dti_perfect_fit_public_app_2026,
  title = {{DTI PERFECT FIT public companion and artifact viewer}},
  author = {{Fujiki, Junichi}},
  year = {{2026}},
  howpublished = {{Streamlit public companion application}},
  url = {{{PUBLIC_APP_URL}}},
  note = {{Single deterministic CLASS/AxiCLASS runs and saved public artifacts; no posterior or MCMC claim}}
}}"""
    st.code(bibtex, language="bibtex")

    st.markdown("#### Local reproduction quick start")
    st.caption(
        "After downloading a reproduction ZIP from the artifact viewer, use "
        "these commands to inspect the manifest and artifact locally."
    )
    st.code(
        "unzip <downloaded_reproduction.zip> -d dti_reproduction\n"
        "python -m json.tool dti_reproduction/*_manifest.json",
        language="bash",
    )
    st.caption(
        "Full backend replay requires a local CLASS/AxiCLASS environment matching "
        "the artifact manifest and backend contract."
    )

    st.markdown("#### Visualization boundary")
    st.info(
        "The app can display CLASS/AxiCLASS theory CMB spectra from a run. "
        "Planck/DESI observational point overlays are intentionally disabled "
        "until source-identified, redistribution-safe observational data tables "
        "are bundled with the public app."
    )
