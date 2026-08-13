from __future__ import annotations

import json
from typing import Any

import streamlit as st


def render_safe_json(value: Any, *, empty_label: str = "No JSON payload.") -> None:
    if isinstance(value, (dict, list)):
        st.json(value)
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

        if isinstance(parsed, (dict, list)):
            st.json(parsed)
            return

        st.code(json.dumps(parsed, ensure_ascii=False, indent=2), language="json")
        return

    st.code(str(value), language="text")
