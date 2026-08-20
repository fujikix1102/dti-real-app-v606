from __future__ import annotations

import json
from typing import Any

import streamlit as st


def _safe_st_json(value: Any) -> bool:
    try:
        st.json(value)
        return True
    except Exception as exc:
        st.warning("Display error occurred. No computation was affected.")
        with st.expander("Raw payload", expanded=False):
            st.code(
                json.dumps(
                    {
                        "display_error": type(exc).__name__,
                        "detail": str(exc),
                        "payload": value,
                    },
                    ensure_ascii=False,
                    indent=2,
                    default=str,
                ),
                language="json",
            )
        return False


def render_safe_json(value: Any, *, empty_label: str = "No JSON payload.") -> None:
    if isinstance(value, dict):
        _safe_st_json(value)
        return

    if isinstance(value, list):
        _safe_st_json({"items": value})
        return

    if value is None:
        st.info(empty_label)
        return

    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            st.code(value, language="text")
            return

        if isinstance(parsed, dict):
            _safe_st_json(parsed)
            return

        if isinstance(parsed, list):
            _safe_st_json({"items": parsed})
            return

        st.code(json.dumps(parsed, ensure_ascii=False, indent=2), language="json")
        return

    st.code(str(value), language="text")
