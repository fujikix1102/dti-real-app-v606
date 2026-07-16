"""Reusable status cards for the PERFECT FIT APP."""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class StatusItem:
    label: str
    value: str
    detail: str = ""


def render_status_row(items: tuple[StatusItem, ...]) -> None:
    """Render compact operational status metrics."""

    columns = st.columns(len(items))

    for column, item in zip(columns, items):
        with column:
            st.metric(item.label, item.value)
            if item.detail:
                st.caption(item.detail)


def render_boundary_card(
    title: str,
    body: str,
    *,
    kind: str = "info",
) -> None:
    """Render one visually consistent boundary notice."""

    content = f"**{title}**\n\n{body}"

    if kind == "warning":
        st.warning(content)
    elif kind == "error":
        st.error(content)
    elif kind == "success":
        st.success(content)
    else:
        st.info(content)
