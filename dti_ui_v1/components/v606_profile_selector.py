from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from dti_ui_v1.services.v606_profile_adapter import (
    V606ProfileAdapterError,
    load_v606_profile_library,
)
from dti_ui_v1.services.v606_profile_runtime_binding import (
    prepare_runtime_binding,
    queue_runtime_binding,
)


DEFAULT_PUBLIC_PROFILE_PATH = Path(
    r"/Users/fujikijunichi/Desktop/MAXOMEGA/_paper_journal/paper_20260305_102018_audit_sensitivity/_OLD_V606_PROFILE_LIBRARY_LAYER_EXPORT_EXECUTE_V1_20260724/export/PUBLIC_PROFILE_LIBRARY_EXPORT.tsv"
)

EXPECTED_PUBLIC_PROFILE_SHA256 = (
    "b6c92579082ee19524db197fd2556fa82371eb2c48aaafe13fa30d9925905485"
)

EXPECTED_PUBLIC_PROFILE_COUNT = 87


def _resolve_public_profile_path() -> Path:
    configured = os.environ.get("DTI_V606_PROFILE_PUBLIC_TSV", "").strip()

    if configured:
        return Path(configured).expanduser()

    return DEFAULT_PUBLIC_PROFILE_PATH


def render_v606_profile_selector() -> None:
    source = _resolve_public_profile_path()

    with st.expander(
        "Legacy v606 profile library — read-only reference",
        expanded=False,
    ):
        st.caption(
            "Loads one of 87 frozen public reference profiles. "
            "Applying a profile changes only H0, omega_b, omega_cdm, "
            "and f_EDE in session state. z_c remains unchanged. "
            "sigma8 and S8 remain reference-only values."
        )

        if not source.is_file():
            st.warning(
                "The frozen v606 public profile source is unavailable. "
                "Set DTI_V606_PROFILE_PUBLIC_TSV to its exact path."
            )
            return

        try:
            library = load_v606_profile_library(
                source,
                expected_sha256=EXPECTED_PUBLIC_PROFILE_SHA256,
                expected_count=EXPECTED_PUBLIC_PROFILE_COUNT,
            )
        except (
            FileNotFoundError,
            V606ProfileAdapterError,
            OSError,
        ) as exc:
            st.error(f"v606 profile library rejected: {exc}")
            return

        categories = library.categories()

        category = st.selectbox(
            "Profile category",
            options=categories,
            key="perfect_fit_v606_profile_category",
        )

        matching = tuple(
            profile
            for profile in library.profiles
            if profile.category == category
        )

        profile_ids = tuple(
            profile.profile_id
            for profile in matching
        )

        profile_id = st.selectbox(
            "Reference profile",
            options=profile_ids,
            key="perfect_fit_v606_profile_id",
        )

        binding = prepare_runtime_binding(
            library,
            profile_id,
        )

        selected = library.by_id(profile_id)

        st.dataframe(
            {
                "field": (
                    "H0",
                    "omega_b",
                    "omega_cdm",
                    "f_EDE",
                    "sigma8",
                    "S8",
                    "z_c",
                ),
                "value": (
                    selected.parameters["H0"],
                    selected.parameters["omega_b"],
                    selected.parameters["omega_cdm"],
                    selected.parameters["f_EDE"],
                    selected.reference_outputs["sigma8"],
                    selected.reference_outputs["S8"],
                    "unchanged",
                ),
                "binding": (
                    "session input",
                    "session input",
                    "session input",
                    "session input",
                    "reference only",
                    "reference only",
                    "optional unbound",
                ),
            },
            use_container_width=True,
            hide_index=True,
        )

        if st.button(
            "Apply frozen reference profile",
            key="perfect_fit_apply_v606_profile",
            type="secondary",
        ):
            queued = queue_runtime_binding(
                st.session_state,
                binding,
            )

            st.session_state[
                "perfect_fit_v606_applied_profile_id"
            ] = binding.profile_id

            st.session_state[
                "perfect_fit_v606_applied_category"
            ] = binding.category

            st.session_state[
                "perfect_fit_v606_reference_sigma8"
            ] = binding.reference_outputs["sigma8"]

            st.session_state[
                "perfect_fit_v606_reference_S8"
            ] = binding.reference_outputs["S8"]

            st.session_state[
                "perfect_fit_v606_source_sha256"
            ] = library.source_sha256

            st.success(
                "Frozen reference profile queued for "
                f"{len(queued)} direct session fields."
            )

            st.rerun()
