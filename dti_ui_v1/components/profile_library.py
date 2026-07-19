"""Small provenance-first profile loader for the executable compute form."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st


_MODULE_DIRECTORY = Path(__file__).resolve().parent
_PROJECT_ROOT = (
    _MODULE_DIRECTORY.parents[1]
    if _MODULE_DIRECTORY.name == "components"
    else _MODULE_DIRECTORY
)
LIBRARY_PATH = _PROJECT_ROOT / "data" / "cosmology_profile_library.json"
if not LIBRARY_PATH.exists():
    LIBRARY_PATH = _PROJECT_ROOT / "cosmology_profile_library.json"

SESSION_KEYS = {
    "H0": "perfect_fit_general_class_H0_v1",
    "omega_b": "perfect_fit_general_class_omega_b_v1",
    "omega_cdm": "perfect_fit_general_class_omega_cdm_v1",
    "n_s": "perfect_fit_general_class_n_s_v1",
    "ln10_10_As": "perfect_fit_general_class_ln10_10_As_v1",
    "tau_reio": "perfect_fit_general_class_tau_reio_v1",
    "f_EDE": "perfect_fit_general_class_f_EDE_v2",
    "z_c": "perfect_fit_general_class_z_c_v2",
}


def load_profile_library(path: Path = LIBRARY_PATH) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    profiles = payload.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        raise ValueError("profile library must contain at least one profile")
    required = set(SESSION_KEYS)
    identifiers: set[str] = set()
    for profile in profiles:
        identifier = str(profile.get("id", ""))
        if not identifier or identifier in identifiers:
            raise ValueError("profile ids must be present and unique")
        identifiers.add(identifier)
        parameters = profile.get("parameters", {})
        if set(parameters) != required:
            raise ValueError(f"profile {identifier} parameter contract changed")
        for value in parameters.values():
            float(value)
    return profiles


def apply_profile(profile: dict[str, Any], state: Any) -> None:
    for parameter, key in SESSION_KEYS.items():
        state[key] = float(profile["parameters"][parameter])
    state["active_cosmology_profile_id_v1"] = profile["id"]
    state["active_cosmology_profile_provenance_v1"] = {
        "label": profile["label"],
        "kind": profile["kind"],
        "source": profile["source"],
    }


def render_profile_library() -> None:
    st.subheader("Quick profile loader")
    st.caption("Choose a starting point, verify its provenance, then apply it to the executable form.")
    profiles = load_profile_library()
    labels = {profile["label"]: profile for profile in profiles}
    selected_label = st.selectbox(
        "Starting profile",
        options=list(labels),
        key="cosmology_profile_library_selection_v1",
    )
    selected = labels[selected_label]
    c1, c2 = st.columns(2)
    c1.metric("Value class", selected["kind"])
    c2.metric("Automatic execution", "NO")
    st.write(selected["note"])
    st.caption(f"Source: {selected['source']}")
    frame = pd.DataFrame(
        [{"Parameter": key, "Value": value, "Value origin": selected["kind"]}
         for key, value in selected["parameters"].items()]
    )
    st.dataframe(frame, hide_index=True, width="stretch")
    if st.button("Apply to CLASS / AxiCLASS form", type="primary", width="stretch"):
        apply_profile(selected, st.session_state)
        st.rerun()
    active = st.session_state.get("active_cosmology_profile_provenance_v1")
    if active:
        st.success(
            f"Loaded: {active['label']} · {active['kind']}. "
            "Review the values below and press the compute button when ready."
        )
