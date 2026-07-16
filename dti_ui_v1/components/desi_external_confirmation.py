"""DESI DR2 BAO external provenance-confirmation displays.

The record documents an external DESI Data Q&A response concerning the
identity of the public desi_bao_all measurement and covariance inputs.
It does not represent an independent likelihood computation, posterior
reproduction, or scientific validation by this application.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import altair as alt
import pandas as pd
import streamlit as st


RECORD_RELATIVE_PATH = Path(
    "data/evidence/"
    "desi_dr2_bao_external_confirmation_v1.json"
)

SOURCE_URL = (
    "https://help.desi.lbl.gov/index.php?"
    "qa=182&qa_1=provenance-external-cobaya-likelihood-"
    "public-cosmology-chains&show=183#a183"
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _record_path() -> Path:
    return _repo_root() / RECORD_RELATIVE_PATH


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


@st.cache_data(show_spinner=False)
def load_desi_external_confirmation() -> dict[str, Any]:
    path = _record_path()

    if not path.is_file():
        raise FileNotFoundError(path)

    record = json.loads(path.read_text(encoding="utf-8"))

    required = {
        "record_id",
        "record_date",
        "source_type",
        "question_title",
        "question_id",
        "answer_id",
        "responder",
        "source_url",
        "confirmed",
        "not_claimed",
        "scope",
    }

    missing = sorted(required - set(record))

    if missing:
        raise ValueError(
            "missing external-confirmation fields: "
            + ", ".join(missing)
        )

    return record


def _confirmed_rows(record: dict[str, Any]) -> pd.DataFrame:
    confirmed = record["confirmed"]

    return pd.DataFrame(
        [
            {
                "Item": "Likelihood",
                "Value": confirmed["chain_likelihood_name"],
                "Status": "CONFIRMED",
            },
            {
                "Item": "Public Cobaya binding",
                "Value": confirmed["public_cobaya_likelihood"],
                "Status": "CONFIRMED",
            },
            {
                "Item": "Measurement file",
                "Value": "Byte-identical",
                "Status": "CONFIRMED",
            },
            {
                "Item": "Covariance file",
                "Value": "Byte-identical",
                "Status": "CONFIRMED",
            },
            {
                "Item": "Different YAML paths",
                "Value": "Execution-cluster paths only",
                "Status": "EXPLAINED",
            },
            {
                "Item": "Additional private likelihood",
                "Value": "Not required",
                "Status": "CONFIRMED",
            },
        ]
    )


def _not_claimed_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"Item": "Posterior reproduction", "Status": "NOT CLAIMED"},
            {"Item": "Full-chain identity", "Status": "NOT CLAIMED"},
            {"Item": "Sampler reproduction", "Status": "NOT CLAIMED"},
            {"Item": "Prior configuration identity", "Status": "NOT CLAIMED"},
            {"Item": "Theory configuration identity", "Status": "NOT CLAIMED"},
            {
                "Item": "Independent numerical likelihood reproduction",
                "Status": "NOT CLAIMED",
            },
            {
                "Item": "Scientific/cosmological validation",
                "Status": "NOT CLAIMED",
            },
        ]
    )


def render_desi_external_confirmation(
    *,
    compact: bool = False,
) -> None:
    try:
        record = load_desi_external_confirmation()
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        st.error(f"DESI external-confirmation record unavailable: {exc}")
        return

    if compact:
        confirmed = record["confirmed"]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Likelihood identity", "CONFIRMED")

        with col2:
            st.metric("Measurement", "BYTE-IDENTICAL")

        with col3:
            st.metric("Covariance", "BYTE-IDENTICAL")

        with col4:
            st.metric("Scope", "PROVENANCE")

        st.caption(
            "`desi_y3_cosmo_bindings` desi_bao_all is externally "
            "confirmed as identical to public Cobaya "
            "`bao.desi_dr2.desi_bao_all` at the measurement and "
            "covariance-file level."
        )
        return

    st.subheader("DESI DR2 BAO external confirmation")

    st.caption(
        "External provenance record for the likelihood inputs used by "
        "the public DESI DR2 cosmology chains."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("External response", "RECEIVED")

    with col2:
        st.metric("Measurement", "BYTE-IDENTICAL")

    with col3:
        st.metric("Covariance", "BYTE-IDENTICAL")

    with col4:
        st.metric("Scope", "LIKELIHOOD INPUTS")

    st.dataframe(
        _confirmed_rows(record),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Interpretation")

    st.info(
        "The differing paths recorded in YAML files reflect runs on "
        "different computing clusters. According to the DESI response, "
        "the same input data files were copied to those environments."
    )

    st.markdown("### Scope not extended")

    st.dataframe(
        _not_claimed_rows(),
        use_container_width=True,
        hide_index=True,
    )

    st.link_button(
        "Open DESI Data Q&A answer",
        record["source_url"],
    )

    with st.expander("Record identity"):
        path = _record_path()

        st.code(
            "\n".join(
                [
                    f'record_id={record["record_id"]}',
                    f'record_date={record["record_date"]}',
                    f'question_id={record["question_id"]}',
                    f'answer_id={record["answer_id"]}',
                    f'responder={record["responder"]}',
                    f'scope={record["scope"]}',
                    f'record_path={RECORD_RELATIVE_PATH}',
                    f'record_sha256={_sha256(path)}',
                    "independent_likelihood_run=NO",
                    "posterior_reproduction=NO",
                    "scientific_value_change=NO",
                ]
            ),
            language="text",
        )


def render_desi_evidence_chain() -> None:
    """Render a compact provenance-chain diagram."""

    nodes = pd.DataFrame(
        [
            {"order": 1, "stage": "Public Cobaya\nlikelihood"},
            {"order": 2, "stage": "Measurement +\ncovariance"},
            {"order": 3, "stage": "DESI external\nconfirmation"},
            {"order": 4, "stage": "Local manifest /\nsource record"},
            {"order": 5, "stage": "Loader +\ndiagnostics"},
            {"order": 6, "stage": "Application\nfigures"},
        ]
    )

    chart = (
        alt.Chart(nodes)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "order:O",
                title=None,
                axis=alt.Axis(labels=False, ticks=False),
            ),
            y=alt.value(70),
            tooltip=[
                alt.Tooltip("stage:N", title="Evidence stage"),
            ],
        )
        .properties(height=150)
    )

    labels = (
        alt.Chart(nodes)
        .mark_text(
            align="center",
            baseline="top",
            dy=18,
            lineBreak="\n",
        )
        .encode(
            x=alt.X("order:O", axis=None),
            y=alt.value(70),
            text="stage:N",
        )
    )

    st.altair_chart(
        chart + labels,
        use_container_width=True,
    )

    st.caption(
        "The external confirmation strengthens source provenance. "
        "It does not replace independent numerical reproduction."
    )
