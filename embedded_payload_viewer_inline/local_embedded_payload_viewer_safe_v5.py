from pathlib import Path
import json
import pandas as pd
import streamlit as st

BASE = Path(__file__).resolve().parent

st.set_page_config(
    page_title="DTI Local Payload Viewer SAFE V5",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BOUNDARY_TEXT = (
    "Display only. No new MCMC. No CLASS. No likelihood. "
    "No posterior claim. No Planck/CMB validation. No DESI fit. "
    "No physics validation. No Hubble-tension solution claim. "
    "No physical-mechanism proof. No manuscript result. No public app update."
)

FORBIDDEN_COLS = {
    "payload_dir",
    "data_source",
    "source_label_audit",
    "source_payload_root",
    "decision_root",
    "path",
}

PREFERRED_PAYLOAD_FILES = {
    "posterior_payload.json": "metadata",
    "chain_summary.tsv": "summary",
    "diagnostics.tsv": "diagnostics",
    "map_or_bestfit.tsv": "bestfit",
    "parameter_identity.tsv": "parameters",
    "thin_samples.tsv": "thin samples",
    "source_identity.tsv": "source",
    "CLAIM_BOUNDARY.md": "boundary",
    "manifest_sha256.tsv": "manifest",
}


def read_tsv(name: str) -> pd.DataFrame:
    p = BASE / name
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p, sep="\t")


def hide_sensitive_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    cols = [c for c in df.columns if c not in FORBIDDEN_COLS]
    return df[cols].copy()


def short_text(x, max_len=120):
    s = "" if pd.isna(x) else str(x)
    if len(s) <= max_len:
        return s
    return s[: max_len - 1] + "…"


def compact_df(df: pd.DataFrame, max_len=80) -> pd.DataFrame:
    if df.empty:
        return df
    out = hide_sensitive_columns(df)
    for c in out.columns:
        out[c] = out[c].map(lambda v: short_text(v, max_len=max_len))
    return out


def payload_key_label(row: pd.Series) -> str:
    priority = row.get("priority", "")
    key = row.get("payload_key", "")
    cls = row.get("class", "")
    return f"{priority}. {key} — {cls}"


def kv_table(items):
    return pd.DataFrame(items, columns=["item", "value"])


def artifact_status_for_payload(artifact_df: pd.DataFrame, payload_key: str) -> pd.DataFrame:
    if artifact_df.empty or "payload_key" not in artifact_df.columns:
        return pd.DataFrame()
    part = artifact_df[artifact_df["payload_key"] == payload_key].copy()
    if part.empty:
        return pd.DataFrame()

    # UI-safe columns only. No local paths.
    cols = []
    for c in ["artifact", "status", "bytes", "sha256"]:
        if c in part.columns:
            cols.append(c)
    part = part[cols].copy()

    if "sha256" in part.columns:
        part["sha256"] = part["sha256"].map(lambda x: short_text(x, 18))
    return part


def read_payload_artifact(payload_dir_raw: str, filename: str):
    p = Path(str(payload_dir_raw)) / filename
    if not p.exists() or not p.is_file():
        return None
    if filename.endswith(".tsv"):
        try:
            return pd.read_csv(p, sep="\t")
        except Exception as e:
            return f"[read error] {e}"
    if filename.endswith(".json"):
        try:
            return json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception as e:
            return f"[read error] {e}"
    if filename.endswith(".md"):
        try:
            return p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            return f"[read error] {e}"
    return None


selection = read_tsv("LOCAL_VIEWER_SELECTION_LEDGER.tsv")
panel_plan = read_tsv("LOCAL_VIEWER_PANEL_PLAN.tsv")
master = read_tsv("SALVAGED_PAYLOAD_MASTER_LEDGER.tsv")
compact = read_tsv("SALVAGED_PAYLOAD_COMPACT_SUMMARY.tsv")
artifact = read_tsv("SALVAGED_PAYLOAD_ARTIFACT_AUDIT.tsv")

st.title("DTI Local Embedded Payload Viewer — SAFE V5")
st.caption("Compact local viewer. Display-only. No computation.")

st.warning(BOUNDARY_TEXT)

if selection.empty:
    st.error("Selection ledger is missing or empty.")
    st.stop()

payload_count = len(selection)
selectable_count = int((selection.get("selection_status", "") == "SELECTABLE").sum()) if "selection_status" in selection.columns else 0
boundary_count = int((selection.get("boundary_ok", "") == "YES").sum()) if "boundary_ok" in selection.columns else 0
artifact_rows = len(artifact)

m1, m2, m3, m4 = st.columns(4)
m1.metric("payloads", payload_count)
m2.metric("selectable", selectable_count)
m3.metric("boundary OK", boundary_count)
m4.metric("artifact rows", artifact_rows)

payload_options = [payload_key_label(row) for _, row in selection.iterrows()]
selected_label = st.selectbox("Select payload", payload_options, index=0, key="safe_v5_payload_selectbox_1")
selected_idx = payload_options.index(selected_label)
selected = selection.iloc[selected_idx]
payload_key = str(selected.get("payload_key", ""))
payload_dir_raw = str(selected.get("payload_dir", ""))

left, right = st.columns([1.05, 1.4])

with left:
    st.subheader("Selected payload")
    selected_compact = compact_df(pd.DataFrame([selected]), max_len=90)
    st.dataframe(selected_compact, width="stretch", hide_index=True)

    st.subheader("Artifact status")
    art = artifact_status_for_payload(artifact, payload_key)
    if art.empty:
        st.info("No artifact table row found for this payload.")
    else:
        st.dataframe(art, width="stretch", hide_index=True)

with right:
    st.subheader("Role and boundary")
    role_items = [
        ["scientific role", selected.get("scientific_role", "")],
        ["viewer role", selected.get("viewer_role", "")],
        ["caution", selected.get("caution_note", "")],
        ["forbidden claims", selected.get("forbidden_claims", "")],
    ]
    role_df = kv_table(role_items)
    role_df["value"] = role_df["value"].map(lambda v: short_text(v, 180))
    st.dataframe(role_df, width="stretch", hide_index=True)

tabs = st.tabs([
    "Summary",
    "Diagnostics",
    "Bestfit",
    "Parameters",
    "Thin samples",
    "Source",
    "Boundary",
    "Manifest",
    "Hidden ledgers",
])

with tabs[0]:
    st.subheader("Chain summary")
    data = read_payload_artifact(payload_dir_raw, "chain_summary.tsv")
    if isinstance(data, pd.DataFrame):
        st.dataframe(compact_df(data, max_len=100), width="stretch", height=420)
    else:
        st.info("chain_summary.tsv unavailable.")

with tabs[1]:
    st.subheader("Diagnostics")
    data = read_payload_artifact(payload_dir_raw, "diagnostics.tsv")
    if isinstance(data, pd.DataFrame):
        st.dataframe(compact_df(data, max_len=120), width="stretch", height=360)
    else:
        st.info("diagnostics.tsv unavailable.")

with tabs[2]:
    st.subheader("MAP / bestfit candidates")
    data = read_payload_artifact(payload_dir_raw, "map_or_bestfit.tsv")
    if isinstance(data, pd.DataFrame):
        st.dataframe(compact_df(data, max_len=80), width="stretch", height=420)
    else:
        st.info("map_or_bestfit.tsv unavailable.")

with tabs[3]:
    st.subheader("Parameter identity")
    data = read_payload_artifact(payload_dir_raw, "parameter_identity.tsv")
    if isinstance(data, pd.DataFrame):
        st.dataframe(compact_df(data, max_len=100), width="stretch", height=420)
    else:
        st.info("parameter_identity.tsv unavailable.")

with tabs[4]:
    st.subheader("Thin sample preview")
    data = read_payload_artifact(payload_dir_raw, "thin_samples.tsv")
    if isinstance(data, pd.DataFrame):
        st.caption("Preview only. Historical-chain display. Not a posterior claim.")
        st.dataframe(compact_df(data.head(200), max_len=70), width="stretch", height=480)
    else:
        st.info("thin_samples.tsv unavailable.")

with tabs[5]:
    st.subheader("Source identity")
    data = read_payload_artifact(payload_dir_raw, "source_identity.tsv")
    if isinstance(data, pd.DataFrame):
        safe = compact_df(data, max_len=120)
        safe = safe[[c for c in safe.columns if c not in FORBIDDEN_COLS]]
        st.dataframe(safe, width="stretch", height=360)
    else:
        st.info("source_identity.tsv unavailable.")

with tabs[6]:
    st.subheader("Claim boundary")
    data = read_payload_artifact(payload_dir_raw, "CLAIM_BOUNDARY.md")
    if isinstance(data, str):
        st.markdown(data)
    else:
        st.info("CLAIM_BOUNDARY.md unavailable.")

with tabs[7]:
    st.subheader("Payload manifest")
    data = read_payload_artifact(payload_dir_raw, "manifest_sha256.tsv")
    if isinstance(data, pd.DataFrame):
        safe = data.copy()
        if "sha256" in safe.columns:
            safe["sha256"] = safe["sha256"].map(lambda x: short_text(x, 18))
        st.dataframe(safe, width="stretch", height=360)
    else:
        st.info("manifest_sha256.tsv unavailable.")

with tabs[8]:
    st.subheader("Hidden ledgers")
    st.caption("Administrative ledgers are hidden here. Local paths are not displayed.")
    st.markdown("### Compact summary")
    st.dataframe(compact_df(compact, max_len=90), width="stretch", height=260)

    st.markdown("### Selection ledger")
    st.dataframe(compact_df(selection, max_len=80), width="stretch", height=320)

    st.markdown("### Panel plan")
    st.dataframe(compact_df(panel_plan, max_len=80), width="stretch", height=320)

    st.markdown("### Master ledger")
    st.dataframe(compact_df(master, max_len=80), width="stretch", height=320)

st.divider()
st.caption(
    "SAFE V5: compact UI. Absolute Mac paths hidden from UI. "
    "Display-only. No MCMC, CLASS, likelihood, posterior claim, physics validation, manuscript update, public app update, or git action."
)
