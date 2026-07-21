from __future__ import annotations

import os
import subprocess


def _git_value(args: list[str], fallback: str) -> str:
    try:
        value = subprocess.check_output(
            args,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return value or fallback
    except Exception:
        return fallback


def collect_identity() -> dict[str, str]:
    commit = os.environ.get(
        "DTI_COMMIT_SHA",
        _git_value(
            ["git", "rev-parse", "HEAD"],
            "unknown",
        ),
    )

    branch = os.environ.get(
        "DTI_BRANCH",
        _git_value(
            ["git", "branch", "--show-current"],
            "unknown",
        ),
    )

    return {
        "Application": "DTI PERFECT FIT",
        "Deployment": os.environ.get(
            "DTI_DEPLOYMENT_NAME",
            "dti-perfect-fit",
        ),
        "Branch": branch,
        "Commit": commit[:7],
        "Entrypoint": "app.py",
        "Mode": os.environ.get(
            "DTI_PERFECT_FIT_MODE",
            "perfect-fit",
        ),
    }


def render_deployment_identity() -> None:
    import streamlit as st

    st.caption("Deployment Identity")

    identity = collect_identity()

    for key, value in identity.items():
        st.caption(f"{key}: {value}")
