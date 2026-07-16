"""Task-first navigation shell for the PERFECT FIT APP."""

from __future__ import annotations

from collections.abc import Callable

import streamlit as st

from dti_ui_v1.contracts.display_contract import (
    APP_ICON,
    APP_LAYOUT,
    APP_SUBTITLE,
    APP_TITLE,
    DEFAULT_PAGE,
    NAVIGATION_ITEMS,
)
from dti_ui_v1.pages import (
    compare,
    dashboard,
    developer,
    evidence,
    figures,
    results,
    run,
)


PageRenderer = Callable[[], None]


def page_registry() -> dict[str, PageRenderer]:
    return {
        "Workspace": dashboard.render,
        "Compute": run.render,
        "Results": results.render,
        "Compare": compare.render,
        "Figures": figures.render,
        "Evidence": evidence.render,
        "Developer": developer.render,
    }


def render_sidebar() -> str:
    requested = st.session_state.pop(
        "perfect_fit_navigation_request",
        None,
    )

    if requested in NAVIGATION_ITEMS:
        st.session_state[
            "perfect_fit_primary_navigation"
        ] = requested

    with st.sidebar:
        st.markdown(f"## {APP_TITLE}")
        st.caption(APP_SUBTITLE)

        selected = st.radio(
            "Navigation",
            options=NAVIGATION_ITEMS,
            index=NAVIGATION_ITEMS.index(DEFAULT_PAGE),
            label_visibility="collapsed",
            key="perfect_fit_primary_navigation",
        )

        st.divider()

        st.caption("Scientific backend: locked")
        st.caption("Public application: frozen")
        st.caption("Current route: independent clone")

        with st.expander("Interface boundaries"):
            st.write(
                "This workbench reorganizes existing functionality. "
                "Scientific computation remains bound to verified routes."
            )

    return selected


def render_app() -> None:
    st.set_page_config(
        page_title=f"{APP_TITLE} — {APP_SUBTITLE}",
        page_icon=APP_ICON,
        layout=APP_LAYOUT,
        initial_sidebar_state="expanded",
    )

    selected = render_sidebar()
    page_registry()[selected]()
