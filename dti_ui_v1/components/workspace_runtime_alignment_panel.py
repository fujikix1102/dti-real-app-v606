from __future__ import annotations

import streamlit as st

from dti_ui_v1.services.posterior_readback_public_viewer import (
    FINAL_HANDOVER_ID,
    FINAL_HANDOVER_ZIP_SHA256,
    POSTERIOR_READBACK_PLOTS,
    public_viewer_rows,
    resolved_asset_path,
)


def _render_posterior_readback_public_viewer() -> None:
    st.markdown("### Public diagnostic viewer")
    st.caption("Asset-gated display only. No posterior inference, no MCMC, no claim promotion.")
    st.dataframe(public_viewer_rows(), hide_index=True, use_container_width=True)

    for asset in POSTERIOR_READBACK_PLOTS:
        with st.expander(f"{asset.plot_id} — {asset.title}", expanded=False):
            st.caption(f"{asset.internal_role} · {asset.boundary}")
            path = resolved_asset_path(asset)
            if path.is_file():
                st.image(str(path), caption=f"{asset.plot_id} · {asset.boundary}", use_container_width=True)
            else:
                st.info(
                    "Public image asset is not bundled in this deployment. "
                    "No substitute image is rendered."
                )
            st.code(
                f"plot={asset.plot_id} role={asset.internal_role} "
                "public_claim=NO posterior=NO mcmc=NO manuscript=NO pointer=NO"
            )


def render_workspace_runtime_alignment_panel() -> None:
    st.subheader("DTI PERFECT FIT Workspace Runtime")

    # DTI_INTERNAL_POSTERIOR_READBACK_PLOT_STATUS_PANEL_PUBLIC_RENDER_LAYER_V1_BEGIN
    with st.expander("Internal posterior-readback plot package status", expanded=False):
        st.caption("FROZEN_INTERNAL_ONLY — audit/status panel; not a plot viewer.")
        st.markdown(
            f"""
    **Final handover gate.**  
    `{FINAL_HANDOVER_ID}`

    **Final handover ZIP SHA256.**  
    `{FINAL_HANDOVER_ZIP_SHA256}`

    **Frozen internal plot count.**  
    `5`

    **Internal role lock.**  
    P1/P2 primary, P3/P4 secondary, P5 reference-only.

    This panel records the frozen internal posterior-readback plot package status only.
            """
        )
        st.markdown(
            """
    | Plot | Internal role | Boundary |
    |---|---|---|
    | P1 | primary | internal diagnostic only; not a public posterior constraint or confidence region |
    | P2 | primary | internal correlation structure only; not model validation or public posterior evidence |
    | P3 | secondary | internal median and quantile readback only; not publication confidence intervals |
    | P4 | secondary | internal component chi2 distribution summary only; not likelihood rerun or model comparison |
    | P5 | reference-only | sampled diagnostic row only; not a global, optimizer, final, or publication best fit |
            """
        )
        st.warning("Internal diagnostic package only. Not public posterior, not publication CI, not global best-fit, not model comparison, not manuscript-ready, and not pointer promotion.")
        _render_posterior_readback_public_viewer()
    # DTI_INTERNAL_POSTERIOR_READBACK_PLOT_STATUS_PANEL_PUBLIC_RENDER_LAYER_V1_END

    st.info(
        "This workspace view represents the deployed Streamlit runtime. "
        "The public runtime and the local development workspace are separate "
        "filesystem environments."
    )

    st.markdown("### Public runtime includes")

    st.markdown(
        "- Runtime status\n"
        "- Artifact viewer\n"
        "- Evidence display\n"
        "- Diagnostic display"
    )

    st.markdown("### Local-only items")

    st.markdown(
        "- Development backups\n"
        "- Review archives\n"
        "- Freeze packages\n"
        "- Temporary patch records"
    )

    st.warning(
        "Public runtime storage is not automatically synchronized with "
        "the local checkout. Local files are not expected to appear here."
    )
