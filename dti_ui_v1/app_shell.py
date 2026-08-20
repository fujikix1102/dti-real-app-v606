"""Task-first navigation shell for the PERFECT FIT APP."""

from __future__ import annotations

from collections.abc import Callable
import importlib
import os

import streamlit as st




from dti_ui_v1.contracts.display_contract import (
    APP_ICON,
    APP_LAYOUT,
    APP_SUBTITLE,
    APP_TITLE,
    DEFAULT_PAGE,
    NAVIGATION_ITEMS,
)


PageRenderer = Callable[[], None]
APP_NAVIGATION = tuple(NAVIGATION_ITEMS[:4]) + ("Atlas", "Consistency", "Audit DTI") + tuple(NAVIGATION_ITEMS[4:])


def page_registry() -> dict[str, tuple[str, str]]:
    return {
        "Workspace": ("dti_ui_v1.pages.dashboard", "render"),
        "Compute": ("dti_ui_v1.pages.run", "render"),
        "Results": ("dti_ui_v1.pages.results", "render"),
        "Compare": ("dti_ui_v1.pages.compare", "render"),
        "Atlas": ("dti_ui_v1.pages.atlas", "render"),
        "Consistency": ("dti_ui_v1.pages.hubble_consistency", "render"),
        "Audit DTI": ("dti_ui_v1.pages.audit_dti", "render"),
        "Figures": ("dti_ui_v1.pages.figures", "render"),
        "Evidence": ("dti_ui_v1.pages.evidence", "render"),
        "Developer": ("dti_ui_v1.pages.developer", "render"),
    }


def resolve_page_renderer(page_name: str) -> PageRenderer:
    module_name, function_name = page_registry()[page_name]

    module = importlib.import_module(module_name)

    return getattr(module, function_name)


def render_sidebar() -> str:
    requested = st.session_state.pop("perfect_fit_navigation_request", None)
    if requested in APP_NAVIGATION:
        st.session_state["perfect_fit_primary_navigation"] = requested

    with st.sidebar:
        st.markdown(f"## {APP_TITLE}")
        st.caption(APP_SUBTITLE)

        from dti_ui_v1.components.deployment_identity import (
            render_deployment_identity
        )

        render_deployment_identity()
        selected = st.radio(
            "Navigation",
            options=APP_NAVIGATION,
            index=APP_NAVIGATION.index(DEFAULT_PAGE),
            label_visibility="collapsed",
            key="perfect_fit_primary_navigation",
        )
        st.divider()
        st.caption("General solver: local CLASS / AxiCLASS")
        st.caption("Joint likelihood: DESI DR2 + Planck 2018 + relative Pantheon+")
        st.caption("Local ladder: overlap-safe summary comparison")
        st.caption("Inference: deterministic single-point scoring; no MCMC")
        with st.expander("Interface boundaries"):
            st.write(
                "General AxiCLASS propagation is evaluated against DESI DR2 BAO; "
                "the fixed baseline remains a separately verified contract. "
                "The General route also evaluates local official Planck and Pantheon+ "
                "assets. Published local-ladder summaries remain comparison-only because "
                "they overlap supernova information. No route is presented as a posterior."
            )
    return selected


def should_exclude_page_view_counter(
    query_params: object,
    *,
    exclude_token: str | None = None,
) -> bool:
    token = (exclude_token or os.getenv("DTI_PAGE_VIEW_EXCLUDE_TOKEN", "")).strip()
    if not token:
        return False
    try:
        audit_view = query_params.get("audit_view")
        supplied_token = query_params.get("token")
    except AttributeError:
        return False
    if isinstance(audit_view, list):
        audit_view = audit_view[-1] if audit_view else None
    if isinstance(supplied_token, list):
        supplied_token = supplied_token[-1] if supplied_token else None
    return str(audit_view) == "1" and str(supplied_token) == token


def render_app() -> None:
    st.set_page_config(
        page_title=f"{APP_TITLE} — {APP_SUBTITLE}",
        page_icon=APP_ICON,
        layout=APP_LAYOUT,
        initial_sidebar_state="expanded",
    )
    selected = render_sidebar()
    try:
        from dti_ui_v1.components.deployment_identity import collect_identity
        from dti_ui_v1.services.run_store import record_anonymous_page_view

        counter_key = f"perfect_fit_page_view_recorded_v1_{selected}"
        if (
            not st.session_state.get(counter_key)
            and not should_exclude_page_view_counter(st.query_params)
        ):
            identity = collect_identity()
            result = record_anonymous_page_view(
                selected,
                app_commit=identity.get("Commit"),
            )
            st.session_state[counter_key] = bool(result.get("recorded")) or bool(
                result.get("configured")
            )
    except Exception:
        pass

    renderer = resolve_page_renderer(selected)
    renderer()



    if selected == "Evidence":
        from dti_ui_v1.components.evidence_layer.gtds_dashboard_entry import (
            render_gtds_dashboard_entry
        )
        render_gtds_dashboard_entry()
