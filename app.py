import json
import math
import re
from pathlib import Path

import numpy as np
import requests


def dom_safe_json_box(obj, label="Result"):

    """Render JSON-like output without st.json to avoid Streamlit removeChild frontend errors."""

    try:

        text = json.dumps(obj, ensure_ascii=False, indent=2, default=str)

    except Exception:

        text = str(obj)

    st.markdown(f"**{label}**")

    st.code(text, language="json")


import pandas as pd
import streamlit as st

# --- DTI_README_DOWNLOAD_AND_8011_GUIDANCE_V3_SAFE ---
# Local-only documentation UI and softer local 8011 unavailable guidance.
_DTI_README_DOWNLOAD_AND_8011_GUIDANCE_V3_SAFE = True

def _dti_readme_text_v3_safe():
    from pathlib import Path
    p = Path(__file__).resolve().parent / "docs" / "README_DTI_LOCAL_8503.md"
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return (
            "# DTI local 8503 app README\n\n"
            "README file was not found on disk.\n\n"
            "This app is local-only and does not perform likelihood evaluation, "
            "posterior comparison, Planck validation, manuscript-value update, "
            "or physics-value update.\n"
        )


# --- DTI_MANUAL_PDF_DOWNLOAD_BUTTON_V1 ---
_DTI_MANUAL_PDF_DOWNLOAD_BUTTON_V1 = True

def _dti_manual_pdf_bytes_v1():
    p = Path(__file__).resolve().parent / "docs" / "DTI_LOCAL_8503_MANUAL_EN.pdf"
    if p.exists():
        return p.read_bytes()
    return b"Manual PDF was not found. Generate docs/DTI_LOCAL_8503_MANUAL_EN.pdf first.\n"

def _dti_render_manual_pdf_download_v1():
    st.download_button(
        "Download English Manual PDF",
        data=_dti_manual_pdf_bytes_v1(),
        file_name="DTI_LOCAL_8503_MANUAL_EN.pdf",
        mime="application/pdf",
        key="download_dti_local_8503_manual_pdf_v1",
        width="stretch",
    )

def _dti_render_readme_download_v3_safe():
    st.download_button(
        "Download local app README",
        data=_dti_readme_text_v3_safe(),
        file_name="README_DTI_LOCAL_8503.md",
        mime="text/markdown",
        key="download_dti_local_8503_readme_v3_safe",
        width="stretch",
    )

def _dti_is_8011_unavailable_error_v3_safe(exc):
    s = str(exc)
    needles = [
        "Connection refused",
        "Max retries exceeded",
        "Failed to establish a new connection",
        "HTTPConnectionPool",
        "127.0.0.1",
        "port=8011",
        "localhost",
    ]
    return any(n in s for n in needles)

def _dti_show_local_probe_error_v3_safe(exc):
    if _dti_is_8011_unavailable_error_v3_safe(exc):
        st.warning(
            "Local 8011 vanilla CLASS endpoint is not running. "
            "This is a local service availability issue, not a physics result. "
            "Start the local 8011 API, then run the live probe again."
        )
    else:
        _dti_show_local_probe_error_v3_safe(exc)


# --- DTI_HIGHLIGHT_ENABLE_CONTROLS_7ABC_V1 ---
# Local-only UI aid: make important 7a/7b/7c Enable gates visually hard to miss.
_DTI_HIGHLIGHT_ENABLE_CONTROLS_7ABC_V1 = True

def _dti_enable_gate_notice_7abc_v1(section_label, purpose):
    st.markdown(
        f"""
        <div style="
            border: 1px solid rgba(250, 204, 21, 0.95);
            background: rgba(250, 204, 21, 0.12);
            border-radius: 10px;
            padding: 0.75rem 0.9rem;
            margin: 0.55rem 0 0.45rem 0;
            color: #facc15;
            font-weight: 700;
        ">
            Enable gate: {section_label}<br>
            <span style="font-weight: 500; color: #fde68a;">
                Turn this on before using the related RUN/probe control. {purpose}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )






# --- DTI_PUBLIC_API_WARMUP_CACHE_HELPERS_7A7B_V2 ---
# Public API warm-up and cached POST helpers for Section 7a/7b.
# This improves UI responsiveness and avoids repeated long fixed-example calls.
# It does not change physics values, does not run likelihood/posterior checks,
# does not validate Planck, and does not reopen graph rendering.
_DTI_PUBLIC_API_WARMUP_CACHE_HELPERS_7A7B_V2 = True

def _dti_endpoint_base_url_v2(endpoint):
    from urllib.parse import urlparse as _dti_urlparse_v2

    s = "" if endpoint is None else str(endpoint).strip()
    try:
        parsed = _dti_urlparse_v2(s)
        if parsed.scheme and parsed.netloc:
            return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        pass
    return ""

def _dti_warmup_urls_for_endpoint_v2(endpoint):
    base = _dti_endpoint_base_url_v2(endpoint)
    if not base:
        return []
    return [
        f"{base}/health",
        f"{base}/axiclass/status",
        f"{base}/axiclass/fixed-example-status",
    ]

def _dti_warmup_public_api_v2(endpoint, timeout_sec=60):
    import time as _dti_time_v2
    import requests as _dti_requests_v2

    rows = []
    for url in _dti_warmup_urls_for_endpoint_v2(endpoint):
        started = _dti_time_v2.time()
        row = {
            "url": url,
            "status_code": None,
            "ok": False,
            "elapsed_sec": None,
            "error": "",
        }
        try:
            response = _dti_requests_v2.get(url, timeout=timeout_sec)
            row["status_code"] = int(response.status_code)
            row["ok"] = bool(response.ok)
        except Exception as exc:
            row["error"] = repr(exc)
        row["elapsed_sec"] = round(_dti_time_v2.time() - started, 3)
        rows.append(row)
    return rows

@st.cache_data(ttl=3600, show_spinner=False)
def _dti_cached_post_json_endpoint_v2(endpoint, payload_json, timeout_sec, cache_label):
    import json as _dti_json_v2
    import time as _dti_time_v2
    import requests as _dti_requests_v2

    payload_text = "" if payload_json is None else str(payload_json)
    payload = None
    if payload_text.strip():
        payload = _dti_json_v2.loads(payload_text)

    started = _dti_time_v2.time()
    response = _dti_requests_v2.post(endpoint, json=payload, timeout=timeout_sec)
    elapsed = round(_dti_time_v2.time() - started, 3)

    try:
        body = response.json()
    except Exception:
        body = {
            "status": "non_json_response",
            "text": response.text[:4000],
        }

    return {
        "status_code": int(response.status_code),
        "body": body,
        "elapsed_sec": elapsed,
        "cache": {
            "streamlit_cache_data": True,
            "ttl_seconds": 3600,
            "cache_label": cache_label,
            "note": "Cached at Streamlit frontend layer only. This does not change the API source response.",
        },
        "boundary": {
            "frontend_cache_only": True,
            "not_likelihood_evaluation": True,
            "not_posterior_comparison": True,
            "not_Planck_validation": True,
            "not_physics_value_update": True,
            "not_manuscript_update": True,
            "graph_rendering_reopened": False,
        },
    }

def _dti_post_json_endpoint_cached_or_uncached_v2(endpoint, payload, timeout_sec, cache_label, use_cache=True):
    import json as _dti_json_v2
    import time as _dti_time_v2
    import requests as _dti_requests_v2

    payload_json = _dti_json_v2.dumps(payload if payload is not None else {}, sort_keys=True)

    if use_cache:
        return _dti_cached_post_json_endpoint_v2(endpoint, payload_json, timeout_sec, cache_label)

    started = _dti_time_v2.time()
    response = _dti_requests_v2.post(endpoint, json=payload if payload is not None else {}, timeout=timeout_sec)
    elapsed = round(_dti_time_v2.time() - started, 3)

    try:
        body = response.json()
    except Exception:
        body = {
            "status": "non_json_response",
            "text": response.text[:4000],
        }

    return {
        "status_code": int(response.status_code),
        "body": body,
        "elapsed_sec": elapsed,
        "cache": {
            "streamlit_cache_data": False,
            "ttl_seconds": 0,
            "cache_label": cache_label,
        },
        "boundary": {
            "frontend_cache_only": False,
            "not_likelihood_evaluation": True,
            "not_posterior_comparison": True,
            "not_Planck_validation": True,
            "not_physics_value_update": True,
            "not_manuscript_update": True,
            "graph_rendering_reopened": False,
        },
    }

# --- DTI_7A_PUBLIC_LOCAL_ENDPOINT_RESOLVER_V1 ---
# Public/local endpoint resolver for Section 7a.
# Local app may use http://127.0.0.1:8010/axiclass/fixed-example-compact.
# Public Streamlit Cloud must not assume that 127.0.0.1 points to the user's Mac.
# Public endpoint should be provided through Streamlit secrets or environment variable:
#   DTI_PUBLIC_FIXED_EXAMPLE_API_URL
_DTI_7A_PUBLIC_LOCAL_ENDPOINT_RESOLVER_V1 = True

def _dti_get_public_fixed_example_endpoint_v1():
    import os as _dti_os_7a_v1

    env_value = _dti_os_7a_v1.environ.get("DTI_PUBLIC_FIXED_EXAMPLE_API_URL", "")
    env_value = "" if env_value is None else str(env_value).strip()
    if env_value:
        return env_value

    try:
        secret_value = st.secrets.get("DTI_PUBLIC_FIXED_EXAMPLE_API_URL", "")
        secret_value = "" if secret_value is None else str(secret_value).strip()
        if secret_value:
            return secret_value
    except Exception:
        pass

    return ""

def _dti_default_7a_fixed_example_endpoint_public_local_v1():
    public_endpoint = _dti_get_public_fixed_example_endpoint_v1()
    if public_endpoint:
        return public_endpoint
    return "http://127.0.0.1:8010/axiclass/fixed-example-compact"

def _dti_is_public_7a_endpoint_configured_v1():
    return bool(_dti_get_public_fixed_example_endpoint_v1())

def _dti_7a_endpoint_mode_notice_v1():
    if _dti_is_public_7a_endpoint_configured_v1():
        st.info(
            "7a endpoint mode: public AxiCLASS fixed-example API endpoint is configured. "
            "This remains bounded: fixed-example only, not likelihood, not posterior, "
            "not Planck validation, and not a manuscript value update."
        )
    else:
        st.info(
            "7a endpoint mode: local fallback endpoint is active. "
            "On Streamlit Cloud, 127.0.0.1 means the cloud container, not the user's Mac. "
            "Configure DTI_PUBLIC_FIXED_EXAMPLE_API_URL for public operation."
        )


# --- DTI_7B_PUBLIC_LOCAL_ENDPOINT_RESOLVER_V1 ---
# Public/local endpoint resolver for Section 7b.
# Local app may use http://127.0.0.1:8011/axiclass/live-vanilla-probe.
# Public Streamlit Cloud must not assume that 127.0.0.1 points to the user's Mac.
# Public endpoint should be provided through Streamlit secrets or environment variable:
#   DTI_PUBLIC_LIVE_VANILLA_API_URL
_DTI_7B_PUBLIC_LOCAL_ENDPOINT_RESOLVER_V1 = True

def _dti_get_public_live_vanilla_endpoint_v1():
    import os as _dti_os_v1

    env_value = _dti_os_v1.environ.get("DTI_PUBLIC_LIVE_VANILLA_API_URL", "")
    env_value = "" if env_value is None else str(env_value).strip()
    if env_value:
        return env_value

    try:
        secret_value = st.secrets.get("DTI_PUBLIC_LIVE_VANILLA_API_URL", "")
        secret_value = "" if secret_value is None else str(secret_value).strip()
        if secret_value:
            return secret_value
    except Exception:
        pass

    return ""

def _dti_default_7b_live_endpoint_public_local_v1():
    public_endpoint = _dti_get_public_live_vanilla_endpoint_v1()
    if public_endpoint:
        return public_endpoint
    return "http://127.0.0.1:8011/axiclass/live-vanilla-probe"

def _dti_is_public_7b_endpoint_configured_v1():
    return bool(_dti_get_public_live_vanilla_endpoint_v1())

def _dti_7b_endpoint_mode_notice_v1():
    if _dti_is_public_7b_endpoint_configured_v1():
        st.info(
            "7b endpoint mode: public vanilla-profile API endpoint is configured. "
            "This public endpoint must still remain bounded: not likelihood, not posterior, "
            "not Planck validation, and not a manuscript value update."
        )
    else:
        st.info(
            "7b endpoint mode: local fallback endpoint is active. "
            "On Streamlit Cloud, 127.0.0.1 means the cloud container, not the user's Mac. "
            "Configure DTI_PUBLIC_LIVE_VANILLA_API_URL for public operation."
        )


# --- DTI_RESTORE_7B_ENDPOINT_WIDGET_ONLY_INDENT_SAFE_V1 ---
_DTI_RESTORE_7B_ENDPOINT_WIDGET_ONLY_INDENT_SAFE_V1 = True

def _dti_default_7b_live_endpoint_widget_only_v1():
    return _dti_default_7b_live_endpoint_public_local_v1()

def _dti_normalize_7b_live_endpoint_widget_only_v1(value):
    s = "" if value is None else str(value).strip()
    if not s or s.startswith("DTI_LOCAL_8011_DISABLED") or s == "8011_REALTIME_DISABLED":
        return _dti_default_7b_live_endpoint_widget_only_v1()
    return s

# --- DTI_GUARD_7B_RUN_BUTTON_MULTILINE_SAFE_V1 ---
# Local-only UI guard:
# 7b Run button must not collapse later sections when 8011 realtime is disabled.
_DTI_GUARD_7B_RUN_BUTTON_MULTILINE_SAFE_V1 = True

def _dti_is_disabled_endpoint_for_7b_run_v1(value):
    s = "" if value is None else str(value).strip()
    disabled_values = {
        "",
        "DTI_LOCAL_8011_DISABLED",
        "8011_REALTIME_DISABLED",
        "DISABLED",
        "disabled",
        "None",
        "none",
        "null",
    }
    return (
        s in disabled_values
        or s.startswith("DTI_LOCAL_8011_DISABLED")
        or s.startswith("8011_REALTIME_DISABLED")
    )

def _dti_7b_run_disabled_notice_v1():
    st.info(
        "Local vanilla CLASS live probe is disabled in this local UI line. "
        "The payload remains available for inspection, but no 8011 realtime call, "
        "likelihood evaluation, posterior comparison, Planck validation, graph rendering, "
        "or physics-value update is executed."
    )

import contextlib

# --- DTI_FIX_7C_SECTION8_INDENT_SAFE_V1 ---
# Local-only UI cleanup:
# - hide obsolete 7c fallback/visual dead block
# - keep 7c controls visible
# - replace Section 8 boundary tab buttons with sequential read-only sections
# - preserve graph/8011 exclusion
_DTI_FIX_7C_SECTION8_INDENT_SAFE_V1 = True

def _dti_noop_context_v1():
    return contextlib.nullcontext()



# --- DTI_SAFE_DEAD_UI_NO_TAB_STRUCTURE_EDIT_V1 ---
# Local-only UI safety patch:
# - soften disabled 8011 endpoint notices
# - avoid red Invalid URL noise for intentionally disabled local probes
# - rename ineffective Section 8 tab labels without changing st.tabs structure
# - do not reopen graph rendering
# - do not reopen 8011 realtime
_DTI_SAFE_DEAD_UI_NO_TAB_STRUCTURE_EDIT_V1 = True

def _dti_local_endpoint_disabled_notice_v1(label="Local vanilla CLASS live probe"):
    st.info(
        f"{label} is disabled in this local UI state. "
        "No 8011 realtime endpoint is opened, and no likelihood/posterior/Planck/physics-value claim is made."
    )

def _dti_is_disabled_endpoint_literal_v1(value):
    try:
        s = str(value).strip()
    except Exception:
        return False
    return s in {
        "DTI_LOCAL_8011_DISABLED",
        "DISABLED",
        "disabled",
        "None",
        "none",
        "null",
        "",
    }

def _dti_boundary_readonly_caption_v1():
    st.caption(
        "Read-only boundary material. These labels organize static explanation/table content only; "
        "they do not trigger likelihood evaluation, posterior comparison, Planck validation, graph rendering, or physics-value updates."
    )

# --- DTI_TIGHTEN_SIDEBAR_NUMBER_INPUT_SPACING_V1 ---
# Local-only UI spacing patch:
# - reduce vertical gaps in Candidate / Reference compact sidebar inputs
# - preserve direct numeric typing
# - preserve +/- step buttons
# - no graph route
# - no 8011 realtime route
_DTI_TIGHTEN_SIDEBAR_NUMBER_INPUT_SPACING_V1 = True

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 0.22rem !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
        gap: 0.35rem !important;
        align-items: center !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stNumberInput"] {
        margin-top: -0.15rem !important;
        margin-bottom: -0.35rem !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stNumberInput"] label {
        display: none !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stNumberInput"] input {
        min-height: 1.85rem !important;
        height: 1.85rem !important;
        padding-top: 0.15rem !important;
        padding-bottom: 0.15rem !important;
        font-size: 0.78rem !important;
    }
    section[data-testid="stSidebar"] button[kind="stepDown"],
    section[data-testid="stSidebar"] button[kind="stepUp"] {
        min-height: 1.85rem !important;
        height: 1.85rem !important;
    }
    section[data-testid="stSidebar"] details {
        margin-bottom: 0.45rem !important;
    }
    section[data-testid="stSidebar"] details [data-testid="stMarkdownContainer"] p {
        margin-bottom: 0.18rem !important;
    }
    .dti-compact-param-label {
        padding-top: 0.18rem;
        font-size: 0.74rem;
        font-weight: 700;
        line-height: 1.0;
        opacity: 0.95;
        white-space: nowrap;
    }
    .dti-compact-param-row-note {
        font-size: 0.72rem;
        opacity: 0.68;
        margin: -0.08rem 0 0.18rem 0;
        line-height: 1.1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- dti_primary_red_button_style_v2 ---
st.markdown(
    """
    <style>
    div.stButton > button[kind="primary"] {
        background: linear-gradient(180deg, #ef4444 0%, #b91c1c 100%) !important;
        border: 1px solid #f87171 !important;
        color: white !important;
        font-weight: 800 !important;
        min-height: 3.05rem !important;
        border-radius: 0.55rem !important;
        box-shadow: 0 0 0 1px rgba(248,113,113,0.25), 0 6px 16px rgba(185,28,28,0.25) !important;
    }
    div.stButton > button[kind="secondary"] {
        min-height: 2.25rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)





# --- dti_sidebar_param_table_editor_v1 ---
def _dti_param_table_rows_v1(prefix, preset_values, preset_name):
    rows = []
    for key in _DTI_UI_PARAM_ORDER_V1:
        fallback = preset_values[preset_name].get(key, 0.0)
        current = _dti_ui_float_v1(st.session_state.get(prefix + key, fallback), fallback)
        rows.append({
            "parameter": key,
            "value": float(current),
        })
    return rows

def _dti_apply_param_table_rows_v1(prefix, edited_rows):
    if edited_rows is None:
        return
    try:
        records = edited_rows.to_dict("records")
    except Exception:
        records = edited_rows
    if not isinstance(records, list):
        return
    for row in records:
        try:
            key = str(row.get("parameter", "")).strip()
            if key not in _DTI_UI_PARAM_ORDER_V1:
                continue
            val = float(row.get("value"))
            st.session_state[prefix + key] = val
        except Exception:
            pass

def _dti_render_param_table_editor_v1(prefix, preset_values, preset_name, editor_key):
    """
    Compact sidebar editor.
    One table replaces many number_input widgets.
    This is UI editing only: no solver, no graph, no 8011 realtime,
    no likelihood, no posterior comparison, no Planck validation.
    """
    import pandas as pd

    df = pd.DataFrame(_dti_param_table_rows_v1(prefix, preset_values, preset_name))

    edited = st.data_editor(
        df,
        key=editor_key,
        hide_index=True,
        use_container_width=True,
        height=300,
        disabled=["parameter"],
        column_config={
            "parameter": st.column_config.TextColumn(
                "parameter",
                width="small",
                help="Parameter name.",
            ),
            "value": st.column_config.NumberColumn(
                "value",
                width="small",
                format="%.6g",
                help="Editable value.",
            ),
        },
    )
    _dti_apply_param_table_rows_v1(prefix, edited)

# --- dti_compact_sidebar_param_rows_v1 ---
def _dti_compact_number_input_row_v1(prefix, key, fallback):
    meta = _DTI_UI_PARAM_META_V1[key]
    label_col, value_col = st.columns([0.34, 0.66], gap="small")
    with label_col:
        st.markdown(
            "<div class='dti-compact-param-label'>"
            + meta["label"]
            + "</div>",
            unsafe_allow_html=True,
        )
    with value_col:
        return st.number_input(
            label=meta["label"],
            value=_dti_ui_float_v1(st.session_state.get(prefix + key, fallback), fallback),
            step=meta["step"],
            format=meta["format"],
            key=prefix + key,
            help=meta["help"],
            label_visibility="collapsed",
        )

def _dti_render_compact_param_rows_v1(prefix, preset_values, preset_name):
    st.markdown(
        "<div class='dti-compact-param-row-note'>Edit values</div>",
        unsafe_allow_html=True,
    )
    for key in _DTI_UI_PARAM_ORDER_V1:
        fallback = preset_values[preset_name].get(key, 0.0)
        _dti_compact_number_input_row_v1(prefix, key, fallback)


# --- DTI_ALL_REGISTERED_PRESETS_FOR_SIDEBAR_V1 ---
# Local-only UI helper:
# Build Candidate / Reference preset options from the app's registered PRESETS.
# This is text/form parsing only:
# - no graph rendering
# - no 8011 realtime
# - no likelihood evaluation
# - no posterior comparison
# - no Planck validation
# - no physics-value update
_DTI_ALL_REGISTERED_PRESETS_FOR_SIDEBAR_V1 = True

def _dti_extract_profile_text_from_preset_obj_v1(obj):
    """Return a readable text block from many possible PRESETS entry shapes."""
    try:
        if isinstance(obj, str):
            return obj
        if isinstance(obj, dict):
            for key in [
                "paper_text_widget",
                "paper_text",
                "profile_text",
                "text",
                "body",
                "content",
                "TARGET_MODEL",
                "target_model",
            ]:
                val = obj.get(key)
                if isinstance(val, str) and val.strip():
                    return val
            parts = []
            for k, v in obj.items():
                if isinstance(v, (int, float, str)):
                    parts.append(f"{k}={v}")
            return "\n".join(parts)
        return str(obj)
    except Exception:
        return ""

def _dti_build_sidebar_preset_values_from_PRESETS_v1():
    """Parse all usable registered PRESETS into numeric Candidate/Reference presets."""
    base = {}
    try:
        base.update(_DTI_UI_PRESET_VALUES_V1)
    except Exception:
        pass

    try:
        registered = PRESETS
    except Exception:
        registered = {}

    if isinstance(registered, dict):
        iterator = registered.items()
    elif isinstance(registered, (list, tuple)):
        iterator = []
        for i, item in enumerate(registered):
            if isinstance(item, dict):
                name = (
                    item.get("name")
                    or item.get("label")
                    or item.get("title")
                    or item.get("id")
                    or f"registered preset {i+1}"
                )
                iterator.append((str(name), item))
            else:
                iterator.append((f"registered preset {i+1}", item))
    else:
        iterator = []

    parsed_count = 0
    for name, obj in iterator:
        try:
            label = str(name).strip() or f"registered preset {parsed_count+1}"
            txt = _dti_extract_profile_text_from_preset_obj_v1(obj)
            parsed = _dti_parse_profile_text_block_v1(txt)
            row = {}
            for key in _DTI_UI_PARAM_ORDER_V1:
                if key in parsed:
                    row[key] = _dti_ui_float_v1(parsed.get(key), None)
                elif isinstance(obj, dict) and key in obj:
                    row[key] = _dti_ui_float_v1(obj.get(key), None)
                else:
                    row[key] = None

            if row.get("H0") is None:
                continue

            fallback_name = "FUJIKI DTI candidate / default"
            fallback = base.get(fallback_name, next(iter(base.values())) if base else {})
            complete = {}
            for key in _DTI_UI_PARAM_ORDER_V1:
                val = row.get(key)
                if val is None:
                    val = fallback.get(key, 0.0)
                complete[key] = float(val)

            candidate_label = label
            if candidate_label in base:
                candidate_label = f"{candidate_label} / registered"
            base[candidate_label] = complete
            parsed_count += 1
        except Exception:
            continue

    # Stable ordering: original important presets first, then registered additions.
    preferred = [
        "FUJIKI DTI candidate / default",
        "Planck2018 LCDM baseline",
        "Ivanov-style EDE reference",
        "High-EDE stress region",
    ]
    ordered = {}
    for key in preferred:
        if key in base:
            ordered[key] = base[key]
    for key in sorted(base.keys()):
        if key not in ordered:
            ordered[key] = base[key]

    return ordered


# --- dti_dynamic_preset_values_from_app_presets_v1 ---
def _dti_parse_profile_text_block_v1(profile_text):
    """
    Parse simple key=value lines from a registered profile text block.
    This is UI parsing only. It does not run solvers, likelihoods, posterior comparison,
    Planck validation, graph rendering, or physics-value updates.
    """
    out = {}
    if not isinstance(profile_text, str):
        return out
    aliases = {
        "H0": "H0",
        "f_EDE": "f_EDE",
        "omega_cdm": "omega_cdm",
        "omega_b": "omega_b",
        "n_s": "n_s",
        "sigma8": "sigma8",
        "S8": "S8",
        "z_c": "z_c",
        "ln10_10_As": "ln10_10_As",
        "ln1010_As": "ln10_10_As",
        "ln10^10_As": "ln10_10_As",
        "ln10_10_A_s": "ln10_10_As",
    }
    for raw in profile_text.splitlines():
        line = raw.strip()
        if not line or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip()
        if k not in aliases:
            continue
        try:
            out[aliases[k]] = float(v)
        except Exception:
            pass
    return out

def _dti_dynamic_preset_values_v1():
    """
    Build UI preset values from existing PRESETS.
    Falls back to the local fixed list only when PRESETS is unavailable or incomplete.
    """
    fallback = dict(_DTI_UI_PRESET_VALUES_V1)
    merged = dict(fallback)

    try:
        preset_obj = PRESETS
    except Exception:
        return merged

    try:
        items = preset_obj.items()
    except Exception:
        return merged

    for name, data in items:
        values = {}
        if isinstance(data, dict):
            if "text" in data:
                values.update(_dti_parse_profile_text_block_v1(data.get("text", "")))
            for k in _DTI_UI_PARAM_ORDER_V1:
                if k in data:
                    try:
                        values[k] = float(data[k])
                    except Exception:
                        pass
        elif isinstance(data, str):
            values.update(_dti_parse_profile_text_block_v1(data))

        if values:
            base = dict(fallback.get("FUJIKI DTI candidate / default", {}))
            base.update(values)
            merged[str(name)] = base

    return merged

def _dti_ui_preset_values_current_v1():
    try:
        vals = _dti_dynamic_preset_values_v1()
        if isinstance(vals, dict) and len(vals) > 0:
            return vals
    except Exception:
        pass
    return dict(_DTI_UI_PRESET_VALUES_V1)

def _dti_safe_preset_name_v1(name, preset_values):
    if name in preset_values:
        return name
    if "FUJIKI DTI candidate / default" in preset_values:
        return "FUJIKI DTI candidate / default"
    return list(preset_values.keys())[0]

def _dti_sidebar_candidate_reference_form_v2():
    st.markdown("### Candidate / Reference input")
    st.caption(
        "ここは常時操作する比較パネルです。まずプリセットを選び、必要なら数値を手で微調整します。"
        "左で編集し、本文側で差分を読みます。"
    )

    preset_values = _dti_build_sidebar_preset_values_from_PRESETS_v1()
    preset_names = list(preset_values.keys())
    if not preset_names:
        st.error("No usable preset profiles were found. Check PRESETS/profile text registration.")
        return

    ccol, rcol = st.columns(2)
    with ccol:
        candidate_preset = st.selectbox(
            "Candidate",
            preset_names,
            index=preset_names.index(_dti_safe_preset_name_v1(st.session_state.get("dti_ui_candidate_preset_v1", preset_names[0]), preset_values)),
            key="dti_ui_candidate_preset_v2",
            help="調べたい候補プロファイルです。まずここを選びます。",
        )
    with rcol:
        default_ref = "Planck2018 LCDM baseline" if "Planck2018 LCDM baseline" in preset_values else preset_names[0]
        reference_preset = st.selectbox(
            "Reference",
            preset_names,
            index=preset_names.index(_dti_safe_preset_name_v1(st.session_state.get("dti_ui_reference_preset_v1", default_ref), preset_values)),
            key="dti_ui_reference_preset_v2",
            help="比較対象の基準プロファイルです。",
        )

    st.caption(
        f"Preset choices available: {len(preset_names)}. "
        "Both Candidate and Reference can use the registered preset list."
    )

    if st.button("Load selected presets", key="dti_ui_load_presets_v2", type="primary"):
        for key, val in preset_values[candidate_preset].items():
            st.session_state["dti_ui_candidate_" + key] = val
        for key, val in preset_values[reference_preset].items():
            st.session_state["dti_ui_reference_" + key] = val
        st.success("Candidate / Reference の入力欄へプリセット値を反映しました。")

    tab_candidate, tab_reference = st.tabs(["Candidate", "Reference"])

    with tab_candidate:
        st.caption("Candidate values.")
        # DTI_TABLE_EDITOR_COMPACT_NOTE_V1
        st.caption("Edit the value column directly. Parameter names stay fixed.")
        _dti_render_param_table_editor_v1("dti_ui_candidate_", preset_values, candidate_preset, "dti_ui_candidate_table_editor_v1")

    with tab_reference:
        st.caption("Reference values.")
        _dti_render_param_table_editor_v1("dti_ui_reference_", preset_values, reference_preset, "dti_ui_reference_table_editor_v1")

    candidate = _dti_ui_get_profile_values_v1("dti_ui_candidate_", candidate_preset)
    reference = _dti_ui_get_profile_values_v1("dti_ui_reference_", reference_preset)
    _dti_ui_sync_existing_keys_v1(candidate, reference)

    rows = _dti_ui_profile_diff_rows_v1(candidate, reference)

    st.markdown("### Current difference")
    diff_lines = []
    for key in ["H0", "omega_cdm", "S8"]:
        row = next((r for r in rows if r["parameter"] == key), None)
        if row:
            diff_lines.append(f"{key}: {row['delta']:+.5g}")
    st.caption(" / ".join(diff_lines))

    st.session_state["dti_ui_candidate_reference_rows_v1"] = rows
    st.session_state["dti_ui_candidate_profile_v1"] = candidate
    st.session_state["dti_ui_reference_profile_v1"] = reference
    st.session_state["dti_ui_candidate_preset_name_v1"] = candidate_preset
    st.session_state["dti_ui_reference_preset_name_v1"] = reference_preset

# --- dti_sidebar_candidate_reference_form_v1 ---
# Local-only UI learning layer.
# Purpose:
# - Give users a persistent left-sidebar operation panel.
# - Let users compare Candidate and Reference parameter profiles.
# - Text/table only.
# - No 8011 realtime.
# - No graph rendering.
# - No likelihood/posterior/Planck claim.
_DTI_UI_PARAM_META_V1 = {
    "H0": {
        "label": "H0",
        "help": "Present-day expansion rate. Larger H0 usually means a faster late-time expansion scale in this comparison panel.",
        "format": "%.3f",
        "step": 0.100,
    },
    "f_EDE": {
        "label": "f_EDE",
        "help": "Early Dark Energy fraction used as a profile descriptor. Here it is an input label for comparison, not a validation result.",
        "format": "%.4f",
        "step": 0.0010,
    },
    "omega_cdm": {
        "label": "omega_cdm",
        "help": "Physical cold-dark-matter density. Useful for seeing how matter-sector burden differs between profiles.",
        "format": "%.5f",
        "step": 0.0010,
    },
    "omega_b": {
        "label": "omega_b",
        "help": "Physical baryon density. Usually changes more narrowly than H0 or omega_cdm in these profile comparisons.",
        "format": "%.5f",
        "step": 0.0001,
    },
    "n_s": {
        "label": "n_s",
        "help": "Scalar spectral index. It describes the tilt of the primordial spectrum in this parameter cartridge.",
        "format": "%.5f",
        "step": 0.0010,
    },
    "ln10_10_As": {
        "label": "ln10_10_As",
        "help": "Log-amplitude notation for primordial scalar amplitude. Kept here as a profile descriptor.",
        "format": "%.4f",
        "step": 0.0010,
    },
    "sigma8": {
        "label": "sigma8",
        "help": "Amplitude of matter clustering on 8 Mpc/h scales. Here it is compared as a recorded/profile value, not recomputed.",
        "format": "%.4f",
        "step": 0.0010,
    },
    "S8": {
        "label": "S8",
        "help": "Common clustering combination. Useful for seeing whether a profile is high-S8 or low-S8 relative to reference.",
        "format": "%.4f",
        "step": 0.0010,
    },
}

_DTI_UI_PRESET_VALUES_V1 = {
    "FUJIKI DTI candidate / default": {
        "H0": 72.90,
        "f_EDE": 0.082,
        "omega_cdm": 0.12700,
        "omega_b": 0.02440,
        "n_s": 0.9847,
        "ln10_10_As": 3.058,
        "sigma8": 0.8229,
        "S8": 0.8019,
    },
    "Planck2018 LCDM baseline": {
        "H0": 67.36,
        "f_EDE": 0.000,
        "omega_cdm": 0.12000,
        "omega_b": 0.02237,
        "n_s": 0.9649,
        "ln10_10_As": 3.044,
        "sigma8": 0.8226,
        "S8": 0.8413,
    },
    "Ivanov-style EDE reference": {
        "H0": 71.15,
        "f_EDE": 0.105,
        "omega_cdm": 0.12999,
        "omega_b": 0.02240,
        "n_s": 0.9850,
        "ln10_10_As": 3.050,
        "sigma8": 0.8314,
        "S8": 0.8340,
    },
}

_DTI_UI_PARAM_ORDER_V1 = [
    "H0",
    "f_EDE",
    "omega_cdm",
    "omega_b",
    "n_s",
    "ln10_10_As",
    "sigma8",
    "S8",
]

def _dti_ui_float_v1(x, default=0.0):
    try:
        if x is None:
            return float(default)
        return float(x)
    except Exception:
        return float(default)

def _dti_ui_get_profile_values_v1(prefix, fallback_name):
    fallback = _DTI_UI_PRESET_VALUES_V1.get(fallback_name, _DTI_UI_PRESET_VALUES_V1["FUJIKI DTI candidate / default"])
    out = {}
    for key in _DTI_UI_PARAM_ORDER_V1:
        out[key] = _dti_ui_float_v1(st.session_state.get(prefix + key, fallback.get(key, 0.0)), fallback.get(key, 0.0))
    return out

def _dti_ui_profile_diff_rows_v1(candidate, reference):
    rows = []
    for key in _DTI_UI_PARAM_ORDER_V1:
        c = _dti_ui_float_v1(candidate.get(key))
        r = _dti_ui_float_v1(reference.get(key))
        d = c - r
        pct = None
        if abs(r) > 1.0e-12:
            pct = 100.0 * d / r
        rows.append({
            "parameter": key,
            "candidate": c,
            "reference": r,
            "delta": d,
            "delta_percent": pct,
        })
    return rows

def _dti_ui_sync_existing_keys_v1(candidate, reference):
    # Keep existing downstream text/table panels aligned with the sidebar values.
    # These assignments only set local UI state. They do not compute likelihoods, posteriors, Planck validation, or physics updates.
    mapping_candidate = {
        "H0": "target_H0",
        "f_EDE": "target_f_EDE",
        "omega_cdm": "target_omega_cdm",
        "omega_b": "target_omega_b",
        "n_s": "target_n_s",
        "ln10_10_As": "target_ln10_10_As",
        "sigma8": "target_sigma8",
        "S8": "target_S8",
    }
    mapping_reference = {
        "H0": "lcdm_H0",
        "omega_cdm": "lcdm_omega_cdm",
        "omega_b": "lcdm_omega_b",
        "n_s": "lcdm_n_s",
        "ln10_10_As": "lcdm_ln10_10_As",
        "sigma8": "lcdm_sigma8",
        "S8": "lcdm_S8",
    }
    for src, dst in mapping_candidate.items():
        try:
            st.session_state[dst] = candidate[src]
        except Exception:
            pass
    for src, dst in mapping_reference.items():
        try:
            st.session_state[dst] = reference[src]
        except Exception:
            pass

def _dti_sidebar_candidate_reference_form_v2():
    st.markdown("### Candidate / Reference input")
    st.caption("Use all registered presets as Candidate / Reference starting points. Edit values below as needed.")
    preset_values = _dti_build_sidebar_preset_values_from_PRESETS_v1()
    preset_names = list(preset_values.keys())

    candidate_preset = st.selectbox(
        "Candidate preset",
        preset_names,
        index=0 if preset_names else 0,
        key="dti_ui_candidate_preset_v1",
        help="Candidate 側の初期値を選びます。手入力で上書きできます。",
    )
    reference_preset = st.selectbox(
        "Reference preset",
        preset_names,
        index=1 if len(preset_names) > 1 else 0,
        key="dti_ui_reference_preset_v1",
        help="Reference 側の初期値を選びます。比較対象の基準値です。",
    )

    st.caption(f"Preset choices available: {len(preset_names)}")

    if st.button("Load selected presets into inputs", key="dti_ui_load_presets_v1"):
        for key, val in preset_values[candidate_preset].items():
            st.session_state["dti_ui_candidate_" + key] = val
        for key, val in preset_values[reference_preset].items():
            st.session_state["dti_ui_reference_" + key] = val

    with st.expander("Candidate profile inputs", expanded=True):
        st.caption("Candidate values: type directly or use +/- buttons.")
        _dti_render_compact_param_rows_v1(
            "dti_ui_candidate_",
            preset_values,
            candidate_preset,
        )

    with st.expander("Reference profile inputs", expanded=True):
        st.caption("Reference values: type directly or use +/- buttons.")
        _dti_render_compact_param_rows_v1(
            "dti_ui_reference_",
            preset_values,
            reference_preset,
        )

    candidate = _dti_ui_get_profile_values_v1("dti_ui_candidate_", candidate_preset)
    reference = _dti_ui_get_profile_values_v1("dti_ui_reference_", reference_preset)
    _dti_ui_sync_existing_keys_v1(candidate, reference)

    rows = _dti_ui_profile_diff_rows_v1(candidate, reference)
    st.markdown("### Current difference")
    for key in ["H0", "omega_cdm", "S8"]:
        row = next((r for r in rows if r["parameter"] == key), None)
        if row:
            st.caption(f"{key}: {row['delta']:+.5g}")

    st.session_state["dti_ui_candidate_reference_rows_v1"] = rows
    st.session_state["dti_ui_candidate_profile_v1"] = candidate
    st.session_state["dti_ui_reference_profile_v1"] = reference

def _dti_main_candidate_reference_panel_v1():
    import pandas as pd

    st.markdown("## Candidate / Reference comparison guide")
    st.markdown(
        "This panel helps users understand how the selected Candidate profile differs from the Reference profile. "
        "It is a text/table learning aid only. It does not run 8011 realtime, does not draw graphs, "
        "and does not compute likelihood, posterior, Planck validation, or physics-value updates."
    )

    candidate = st.session_state.get("dti_ui_candidate_profile_v1")
    reference = st.session_state.get("dti_ui_reference_profile_v1")
    rows = st.session_state.get("dti_ui_candidate_reference_rows_v1")

    if not candidate or not reference or not rows:
        st.info("Use the left sidebar Candidate / Reference input form to populate this comparison.")
        return

    df = pd.DataFrame(rows)
    show_df = df.copy()
    for col in ["candidate", "reference", "delta", "delta_percent"]:
        if col in show_df.columns:
            show_df[col] = show_df[col].map(lambda x: "" if x is None else f"{x:.6g}")
    st.markdown("### Candidate vs Reference")
    st.dataframe(show_df, use_container_width=True, hide_index=True)

    st.markdown("### What changed from the reference?")
    notes = []
    h0_delta = float(candidate["H0"]) - float(reference["H0"])
    om_delta = float(candidate["omega_cdm"]) - float(reference["omega_cdm"])
    s8_delta = float(candidate["S8"]) - float(reference["S8"])

    if abs(h0_delta) > 1.0:
        notes.append(f"- H0 is higher by {h0_delta:+.3f}. This marks a higher-H0 candidate profile relative to the reference.")
    else:
        notes.append(f"- H0 is close to the reference, with delta {h0_delta:+.3f}.")

    if abs(om_delta) > 0.002:
        notes.append(f"- omega_cdm differs by {om_delta:+.5f}. This is the main matter-density comparison lever in this panel.")
    else:
        notes.append(f"- omega_cdm is close to the reference, with delta {om_delta:+.5f}.")

    if abs(s8_delta) > 0.02:
        notes.append(f"- S8 differs by {s8_delta:+.4f}. This helps users see whether the profile is higher- or lower-clustering relative to reference.")
    else:
        notes.append(f"- S8 is close to the reference, with delta {s8_delta:+.4f}.")

    st.markdown("\n".join(notes))

    st.markdown("### Parameter guide")
    guide_rows = []
    for key in _DTI_UI_PARAM_ORDER_V1:
        guide_rows.append({
            "parameter": key,
            "how to read it": _DTI_UI_PARAM_META_V1[key]["help"],
        })
    st.dataframe(pd.DataFrame(guide_rows), use_container_width=True, hide_index=True)

    st.caption(
        "Boundary: comparison guide only. No graph, no 8011 realtime, no likelihood result, "
        "no posterior comparison, no Planck validation, and no physics-value update."
    )




# --- DTI_SAFE_PURGE_GRAPH_VISUAL_ROUTES_NO_INDENT_BREAK_V1 ---
# Local-only closure:
# - 8011 realtime excluded
# - graph rendering excluded
# - graph/audit visualization wording hidden
# - no fallback/global/disabled TSV route route
_DTI_SAFE_PURGE_GRAPH_VISUAL_ROUTES_NO_INDENT_BREAK_V1 = True

def _DTI_DISABLED_GRAPH_CALL(*args, **kwargs):
    return None

_DTI_HIDDEN_VISUAL_PHRASES_V1 = [
    "境界確認",
    "Boundary confirmation",
    "Boundary table",
    "Boundary confirmation",
    "disabled graph route",
    "disabled graph route",
    "disabled visual material",
    "disabled visual route",
    "disabled TSV route",
    "disabled TSV route",
    "static PNG",
    "trade-off visualization",
]

try:
    _dti_orig_markdown_v1 = st.markdown
    _dti_orig_info_v1 = st.info
    _dti_orig_caption_v1 = st.caption
    _dti_orig_button_v1 = st.button
except Exception:
    _dti_orig_markdown_v1 = None
    _dti_orig_info_v1 = None
    _dti_orig_caption_v1 = None
    _dti_orig_button_v1 = None

def _DTI_TEXT_IS_HIDDEN_VISUAL_V1(x):
    try:
        s = str(x)
    except Exception:
        return False
    return any(p in s for p in _DTI_HIDDEN_VISUAL_PHRASES_V1)

def _DTI_MARKDOWN_FILTER_V1(x, *args, **kwargs):
    if _DTI_TEXT_IS_HIDDEN_VISUAL_V1(x):
        return None
    if _dti_orig_markdown_v1 is not None:
        return _dti_orig_markdown_v1(x, *args, **kwargs)
    return None

def _DTI_INFO_FILTER_V1(x, *args, **kwargs):
    if _DTI_TEXT_IS_HIDDEN_VISUAL_V1(x):
        return None
    if _dti_orig_info_v1 is not None:
        return _dti_orig_info_v1(x, *args, **kwargs)
    return None

def _DTI_CAPTION_FILTER_V1(x, *args, **kwargs):
    if _DTI_TEXT_IS_HIDDEN_VISUAL_V1(x):
        return None
    if _dti_orig_caption_v1 is not None:
        return _dti_orig_caption_v1(x, *args, **kwargs)
    return None

def _DTI_BUTTON_FILTER_V1(x, *args, **kwargs):
    if "8011" in str(x) or _DTI_TEXT_IS_HIDDEN_VISUAL_V1(x):
        return False
    if _dti_orig_button_v1 is not None:
        return _dti_orig_button_v1(x, *args, **kwargs)
    return False

try:
    st.markdown = _DTI_MARKDOWN_FILTER_V1
    st.info = _DTI_INFO_FILTER_V1
    st.caption = _DTI_CAPTION_FILTER_V1
    st.button = _DTI_BUTTON_FILTER_V1
except Exception:
    pass
# --- /DTI_SAFE_PURGE_GRAPH_VISUAL_ROUTES_NO_INDENT_BREAK_V1 ---

# --- DTI_LOCAL_FINAL_NOGRAPH_CLEAN_UI_V1 ---
# Local UI closure policy:
# - 8011 realtime probe is disabled.
# - All graph rendering is disabled.
# - Audit visualization material is hidden.
# - Section 8 is payload / boundary confirmation only.
# - Tables and text boundary confirmations may remain.
DTI_LOCAL_FINAL_NOGRAPH_CLEAN_UI_V1 = True
DTI_8011_REALTIME_DISABLED_V1 = True
DTI_ALL_GRAPHS_DISABLED_V1 = True
DTI_AUDIT_VISUAL_ITEMS_HIDDEN_V1 = True
DTI_SECTION8_PAYLOAD_BOUNDARY_ONLY_V1 = True

def _dti_local_final_text_is_visual_noise_v1(x):
    s = str(x)
    noise_terms = [
        "監査可視化レイヤー",
        "Audit visualization",
        "audit visualization",
        "visualization deck",
        "graph API",
        "グラフAPI",
        "グラフは無効",
        "graph disabled",
        "no graph",
        "No graph",
        "8011",
        "live vanilla",
        "ライブプローブ",
        "ローカルのバニラCLASS",
        "disabled visual route",
        "fallback chart",
        "フォールバック",
        "S8 stress",
        "S8応答",
        "stress view",
        "trade-off",
        "トレードオフ",
        "rs_drag",
        "sweep_value",
        "smoothness graph",
        "数値平滑性プロファイル",
        "ヒューリスティック参照領域",
        "Candidate payload / boundary confirmation",
        "reference-distance",
        "基準距離",
    ]
    return any(t in s for t in noise_terms)

try:
    import streamlit as st

    _dti_original_pyplot_v1 = getattr(st, "pyplot", None)
    _dti_original_line_chart_v1 = getattr(st, "line_chart", None)
    _dti_original_area_chart_v1 = getattr(st, "area_chart", None)
    _dti_original_bar_chart_v1 = getattr(st, "bar_chart", None)
    _dti_original_altair_chart_v1 = getattr(st, "altair_chart", None)
    _dti_original_plotly_chart_v1 = getattr(st, "plotly_chart", None)
    _dti_original_graphviz_chart_v1 = getattr(st, "graphviz_chart", None)
    _dti_original_map_v1 = getattr(st, "map", None)
    _dti_original_button_v1 = getattr(st, "button", None)
    _dti_original_text_input_v1 = getattr(st, "text_input", None)
    _dti_original_markdown_v1 = getattr(st, "markdown", None)
    _dti_original_info_v1 = getattr(st, "info", None)
    _dti_original_caption_v1 = getattr(st, "caption", None)
    _dti_original_write_v1 = getattr(st, "write", None)
    _dti_original_header_v1 = getattr(st, "header", None)

    def _dti_silent_chart_v1(*args, **kwargs):
        return None

    def _dti_safe_button_v1(label, *args, **kwargs):
        if _dti_local_final_text_is_visual_noise_v1(label):
            return False
        return _dti_original_button_v1(label, *args, **kwargs)

    def _dti_safe_text_input_v1(label, *args, **kwargs):
        value = kwargs.get("value", None)
        if _dti_local_final_text_is_visual_noise_v1(label) or _dti_local_final_text_is_visual_noise_v1(value):
            return "DTI_LOCAL_8011_DISABLED"
        return _dti_original_text_input_v1(label, *args, **kwargs)

    def _dti_safe_markdown_v1(body, *args, **kwargs):
        if _dti_local_final_text_is_visual_noise_v1(body):
            return None
        return _dti_original_markdown_v1(body, *args, **kwargs)

    def _dti_safe_info_v1(body, *args, **kwargs):
        if _dti_local_final_text_is_visual_noise_v1(body):
            return None
        return _dti_original_info_v1(body, *args, **kwargs)

    def _dti_safe_caption_v1(body, *args, **kwargs):
        if _dti_local_final_text_is_visual_noise_v1(body):
            return None
        return _dti_original_caption_v1(body, *args, **kwargs)

    def _dti_safe_write_v1(*args, **kwargs):
        if args and any(_dti_local_final_text_is_visual_noise_v1(a) for a in args):
            return None
        return _dti_original_write_v1(*args, **kwargs)

    def _dti_safe_header_v1(body, *args, **kwargs):
        s = str(body)
        if "8." in s and ("Heuristic" in s or "ヒューリスティック" in s):
            body = "8. Candidate payload / boundary confirmation"
        return _dti_original_header_v1(body, *args, **kwargs)

    st.pyplot = _dti_silent_chart_v1
    st.line_chart = _dti_silent_chart_v1
    st.area_chart = _dti_silent_chart_v1
    st.bar_chart = _dti_silent_chart_v1
    st.altair_chart = _dti_silent_chart_v1
    st.plotly_chart = _dti_silent_chart_v1
    st.graphviz_chart = _dti_silent_chart_v1
    st.map = _dti_silent_chart_v1
    st.button = _dti_safe_button_v1
    st.text_input = _dti_safe_text_input_v1
    st.markdown = _dti_safe_markdown_v1
    st.info = _dti_safe_info_v1
    st.caption = _dti_safe_caption_v1
    st.write = _dti_safe_write_v1
    st.header = _dti_safe_header_v1
except Exception:
    pass
# --- DTI_LOCAL_FINAL_NOGRAPH_CLEAN_UI_V1_END ---

# --- dti_disable_8011_errors_visual_items_final_fix_v1 ---
# Local-only UI safety patch.
# Policy:
# - 8011 realtime probe is disabled.
# - All graph rendering is disabled.
# - Audit-visualization material blocks are hidden.
# - Section 8 is payload/boundary confirmation only.
# - No likelihood evaluation, posterior comparison, Planck validation, or physics-value update.

DTI_8011_REALTIME_DISABLED_FINAL = True
DTI_ALL_GRAPHS_DISABLED_FINAL = True
DTI_AUDIT_VISUAL_ITEMS_HIDDEN_FINAL = True
DTI_SECTION8_PAYLOAD_BOUNDARY_ONLY_FINAL = True

try:
    import streamlit as _dti_st_final
except Exception:
    _dti_st_final = None

if _dti_st_final is not None:
    def _dti_disabled_graph_notice_final(*args, **kwargs):
        try:
            _dti_st_final.info(
                "No 8011 realtime graph, no disabled visual route, no synthetic graph, "
                "no UI-reference graph, no fixed-reference graph, no disabled TSV route, "
                "and no disabled TSV route is rendered."
            )
        except Exception:
            pass
        return None

    def _dti_silent_visual_item_final(*args, **kwargs):
        return None

    # Disable graph APIs.
    try:
        _dti_st_final.pyplot = _dti_disabled_graph_notice_final
        _dti_st_final.altair_chart = _dti_disabled_graph_notice_final
        _dti_st_final.line_chart = _dti_disabled_graph_notice_final
        _dti_st_final.area_chart = _dti_disabled_graph_notice_final
        _dti_st_final.bar_chart = _dti_disabled_graph_notice_final
        _dti_st_final.plotly_chart = _dti_disabled_graph_notice_final
        _dti_st_final.vega_lite_chart = _dti_disabled_graph_notice_final
    except Exception:
        pass

    # Hide audit-visualization labels/notices that are now out of scope.
    _dti_original_markdown_final = _dti_st_final.markdown
    _dti_original_info_final = _dti_st_final.info
    _dti_original_caption_final = _dti_st_final.caption
    _dti_original_button_final = _dti_st_final.button

    def _dti_text_should_hide_final(x):
        s = str(x)
        hide_tokens = [
            "監査可視化レイヤー",
            "Audit visualization",
            "audit visualization",
            "S8 stress",
            "S8応答",
            "rs_dragとS8",
            "rs_drag と S8",
            "trade-off",
            "トレードオフ",
            "グラフAPI",
            "8011",
            "live vanilla",
            "ライブプローブ",
            "ローカルのバニラCLASSライブプローブ",
            "fallback",
            "フォールバック",
            "visualization panel",
            "可視化",
            "heuristic reference",
            "ヒューリスティック",
            "reference-distance",
            "参照距離",
        ]
        return any(tok in s for tok in hide_tokens)

    def _dti_markdown_filter_final(body, *args, **kwargs):
        if _dti_text_should_hide_final(body):
            return None
        return _dti_original_markdown_final(body, *args, **kwargs)

    def _dti_info_filter_final(body, *args, **kwargs):
        if _dti_text_should_hide_final(body):
            return None
        return _dti_original_info_final(body, *args, **kwargs)

    def _dti_caption_filter_final(body, *args, **kwargs):
        if _dti_text_should_hide_final(body):
            return None
        return _dti_original_caption_final(body, *args, **kwargs)

    def _dti_button_filter_final(label, *args, **kwargs):
        if _dti_text_should_hide_final(label):
            return False
        return _dti_original_button_final(label, *args, **kwargs)

    try:
        _dti_st_final.markdown = _dti_markdown_filter_final
        _dti_st_final.info = _dti_info_filter_final
        _dti_st_final.caption = _dti_caption_filter_final
        _dti_st_final.button = _dti_button_filter_final
    except Exception:
        pass
# --- dti_disable_8011_errors_visual_items_final_fix_v1_end ---


# --- dti_section8_payload_boundary_only_v1 ---
# Local-only UI downgrade:
# Section 8 is not an evaluation, graph, distance-ranking, S8-stress, or reference-region scoring panel.
# It is kept only as a candidate payload / boundary confirmation area.
# This does not perform likelihood evaluation, posterior comparison, Planck validation,
# physics-value update, graph generation, or 8011 realtime probing.
_DTI_SECTION8_PAYLOAD_BOUNDARY_ONLY_V1 = True

try:
    _dti_sec8_orig_header_v1 = st.header
    _dti_sec8_orig_subheader_v1 = st.subheader
    _dti_sec8_orig_markdown_v1 = st.markdown
    _dti_sec8_orig_info_v1 = st.info
    _dti_sec8_orig_caption_v1 = st.caption
    _dti_sec8_orig_write_v1 = st.write
    _dti_sec8_orig_tabs_v1 = st.tabs
except Exception:
    _dti_sec8_orig_header_v1 = None
    _dti_sec8_orig_subheader_v1 = None
    _dti_sec8_orig_markdown_v1 = None
    _dti_sec8_orig_info_v1 = None
    _dti_sec8_orig_caption_v1 = None
    _dti_sec8_orig_write_v1 = None
    _dti_sec8_orig_tabs_v1 = None

_DTI_SECTION8_SUPPRESS_PHRASES_V1 = [
    "監査可視化レイヤー",
    "可視化レイヤー",
    "S8応力",
    "S8 stress",
    "stress view",
    "rs_dragとS8",
    "rs_drag と S8",
    "trade-off",
    "トレードオフ",
    "基準距離",
    "参照距離",
    "heuristic reference distance",
    "heuristic reference-region",
    "Heuristic reference-region",
    "適合領域参照",
    "登録済みの適合領域参照",
    "距離バー",
    "代替UI参照チャート",
    "代表UI参照チャート",
    "fallback",
    "Fallback",
    "フォールバック",
    "graph API",
    "グラフ API",
    "グラフAPI",
    "graph disabled",
    "グラフは無効",
    "グラフが無効",
    "グラフ描画",
    "グラフ表示",
    "プロファイル距離",
    "distance table",
    "distance or trigger score",
    "trigger score",
    "トリガースコア",
]

_DTI_SECTION8_RENAME_MAP_V1 = {
    "8. Candidate payload / boundary confirmation": "8. Candidate payload / boundary confirmation",
    "8. 候補パラメータ送信前の境界確認": "8. 候補パラメータ送信前の境界確認",
}

def _dti_section8_as_text_v1(obj):
    try:
        return str(obj)
    except Exception:
        return ""

def _dti_section8_should_suppress_v1(obj):
    s = _dti_section8_as_text_v1(obj)
    return any(p in s for p in _DTI_SECTION8_SUPPRESS_PHRASES_V1)

def _dti_section8_rewrite_text_v1(obj):
    s = _dti_section8_as_text_v1(obj)
    for old, new in _DTI_SECTION8_RENAME_MAP_V1.items():
        if old in s:
            return s.replace(old, new)
    return obj

def _dti_section8_boundary_notice_v1():
    try:
        _dti_sec8_orig_info_v1(
            "Section 8 is restricted to candidate-payload and boundary confirmation only. "
            "No graph, no 8011 realtime probe, no heuristic distance ranking, no S8 stress review, "
            "no likelihood evaluation, no posterior comparison, no Planck validation, and no physics-value update."
        )
    except Exception:
        pass

def _dti_section8_header_wrapper_v1(*args, **kwargs):
    if args:
        first = _dti_section8_rewrite_text_v1(args[0])
        if _dti_section8_as_text_v1(first).startswith("8. Candidate payload"):
            result = _dti_sec8_orig_header_v1(first, *args[1:], **kwargs)
            _dti_section8_boundary_notice_v1()
            return result
        args = (first,) + args[1:]
    return _dti_sec8_orig_header_v1(*args, **kwargs)

def _dti_section8_text_wrapper_factory_v1(orig_func):
    def wrapper(*args, **kwargs):
        if args and _dti_section8_should_suppress_v1(args[0]):
            return None
        return orig_func(*args, **kwargs)
    return wrapper

class _DTISection8DummyTabV1:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return False

def _dti_section8_tabs_wrapper_v1(labels, *args, **kwargs):
    label_text = " ".join([_dti_section8_as_text_v1(x) for x in labels]) if isinstance(labels, (list, tuple)) else _dti_section8_as_text_v1(labels)
    if _dti_section8_should_suppress_v1(label_text):
        try:
            _dti_sec8_orig_info_v1(
                "Section 8 visualization tabs are hidden. This local line keeps only payload/boundary confirmation."
            )
        except Exception:
            pass
        n = len(labels) if isinstance(labels, (list, tuple)) else 1
        return [_DTISection8DummyTabV1() for _ in range(n)]
    return _dti_sec8_orig_tabs_v1(labels, *args, **kwargs)

try:
    if _dti_sec8_orig_header_v1 is not None:
        st.header = _dti_section8_header_wrapper_v1
    if _dti_sec8_orig_subheader_v1 is not None:
        st.subheader = _dti_section8_text_wrapper_factory_v1(_dti_sec8_orig_subheader_v1)
    if _dti_sec8_orig_markdown_v1 is not None:
        st.markdown = _dti_section8_text_wrapper_factory_v1(_dti_sec8_orig_markdown_v1)
    if _dti_sec8_orig_info_v1 is not None:
        st.info = _dti_section8_text_wrapper_factory_v1(_dti_sec8_orig_info_v1)
    if _dti_sec8_orig_caption_v1 is not None:
        st.caption = _dti_section8_text_wrapper_factory_v1(_dti_sec8_orig_caption_v1)
    if _dti_sec8_orig_write_v1 is not None:
        st.write = _dti_section8_text_wrapper_factory_v1(_dti_sec8_orig_write_v1)
    if _dti_sec8_orig_tabs_v1 is not None:
        st.tabs = _dti_section8_tabs_wrapper_v1
except Exception:
    pass
# --- dti_section8_payload_boundary_only_v1 END ---


# --- DTI_HARD_DISABLE_8011_REALTIME_AND_ALL_GRAPHS_V1 ---
# Policy:
# - 8011 realtime probe is disabled in this local line.
# - All graph rendering is disabled.
# - No fallback, synthetic, illustrative, UI-reference, fixed-reference, or prebuilt graph is drawn.
# - Tables/text may remain visible.
# - This does not change manuscript values, physics values, likelihoods, posteriors, or Planck validation.

DTI_8011_REALTIME_DISABLED = True
DTI_ALL_GRAPHS_DISABLED = True

def _dti_disabled_graph_notice_v1(label="Graph"):
    try:
        st.info(
            f"{label}: graph disabled. 8011 realtime and all graph rendering are intentionally disabled in this local line. "
            "No fallback, synthetic, illustrative, UI-reference, fixed-reference, profile-bound TSV, global TSV, or live 8011 graph is drawn."
        )
    except Exception:
        pass

def _dti_disabled_graph_api_v1(*args, **kwargs):
    return None

def _dti_disabled_8011_realtime_v1(*args, **kwargs):
    raise RuntimeError(
        "8011 realtime probe is disabled by DTI_HARD_DISABLE_8011_REALTIME_AND_ALL_GRAPHS_V1."
    )

# Disable common Streamlit graph APIs globally.
for _dti_graph_api_name in [
    "pyplot",
    "line_chart",
    "bar_chart",
    "area_chart",
    "scatter_chart",
    "altair_chart",
    "vega_lite_chart",
    "plotly_chart",
    "graphviz_chart",
    "bokeh_chart",
    "map",
]:
    if hasattr(st, _dti_graph_api_name):
        setattr(st, _dti_graph_api_name, _dti_disabled_graph_api_v1)

# Disable matplotlib display paths that call pyplot through Streamlit above.
# Do not monkeypatch pandas/tables. Tables remain allowed.
# --- END DTI_HARD_DISABLE_8011_REALTIME_AND_ALL_GRAPHS_V1 ---

# --- DTI_HIDE_AUDIT_VISUALIZATION_ITEMS_V1 ---
# Policy:
# - Hide audit-visualization material blocks.
# - Hide graph API disabled notices.
# - Keep ordinary explanatory text, tables, profile blocks, and boundary text visible.
# - This does not restore graphs, 8011 realtime, likelihood evaluation, posterior comparison, Planck validation, or physics-value updates.

DTI_AUDIT_VISUALIZATION_ITEMS_DISABLED = True

_DTI_HIDDEN_UI_TEXT_TOKENS_V1 = [
    "監査可視化レイヤー",
    "監査可視化 レイヤー",
    "監査可視化は利用できません",
    "可視化の境界",
    "数値平滑性プロファイル",
    "Candidate payload / boundary confirmation",
    "基準距離の概要",
    "S8応力レビュー",
    "Boundary table",
    "rs_dragとS8のトレードオフ比較",
    "Boundary confirmation",
    "グラフAPI：",
    "グラフ API：",
    "graph disabled",
    "all graph rendering",
    "disabled visual route",
    "UI-reference",
    "global TSV",
    "profile-bound TSV",
    "Audit visualization",
    "diagnostic UI aids",
]

def _dti_should_hide_visual_ui_text_v1(obj):
    try:
        s = str(obj)
    except Exception:
        return False
    return any(tok in s for tok in _DTI_HIDDEN_UI_TEXT_TOKENS_V1)

def _dti_make_hidden_ui_wrapper_v1(original_func):
    def _wrapped(*args, **kwargs):
        if args and _dti_should_hide_visual_ui_text_v1(args[0]):
            return None
        if "body" in kwargs and _dti_should_hide_visual_ui_text_v1(kwargs.get("body")):
            return None
        if "label" in kwargs and _dti_should_hide_visual_ui_text_v1(kwargs.get("label")):
            return None
        return original_func(*args, **kwargs)
    return _wrapped

for _dti_ui_api_name in [
    "markdown",
    "info",
    "warning",
    "caption",
    "write",
    "text",
    "subheader",
]:
    if hasattr(st, _dti_ui_api_name):
        setattr(st, _dti_ui_api_name, _dti_make_hidden_ui_wrapper_v1(getattr(st, _dti_ui_api_name)))

# Do not wrap st.header globally. Section headers 7c and 8 should remain visible.
# --- END DTI_HIDE_AUDIT_VISUALIZATION_ITEMS_V1 ---


from scipy.integrate import solve_ivp

# --- GitHub v6.0.6 path compatibility shim ---
from pathlib import Path as _DTIPath
_DTI_APP_ROOT = _DTIPath(__file__).resolve().parent
_DTI_DATA_PRIMARY = _DTI_APP_ROOT / "app" / "data"
_DTI_DATA_FALLBACK = _DTI_APP_ROOT / "data"
# --- end GitHub v6.0.6 path compatibility shim ---

try:
    from classy import Class
    HAS_CLASS = True
except Exception:
    Class = None
    HAS_CLASS = False


APP_VERSION = "v6.0.6-presets-expanded-inline"
APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
AXICLASS_RESULTS = DATA_DIR / "axiclass_fix1_results.tsv"
AXICLASS_DELTA = DATA_DIR / "axiclass_fix1_delta.tsv"

C_LIGHT = 299792458.0
G_CONST = 6.67430e-11
MPC_TO_M = 3.085677581e22
H0_UNIT = 100000.0 / MPC_TO_M

PARAMS = [
    "H0",
    "h",
    "omega_b",
    "omega_cdm",
    "Omega_m",
    "f_EDE",
    "z_c",
    "sigma8",
    "S8",
    "ln10_10_As",
    "n_s",
    "tau_reio",
    "Omega_k",
]

PARAM_PATTERNS = {
    "H0": [
        r"\bH\s*_?\s*0\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bH0\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
    ],
    "h": [
        r"\bh\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
    ],
    "f_EDE": [
        r"\bf\s*_?\s*EDE\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bfEDE\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bfede\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
    ],
    "omega_cdm": [
        r"\bomega\s*_?\s*cdm\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bomega_cdm\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bOmega_c\s*h\^?2\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
    ],
    "omega_b": [
        r"\bomega\s*_?\s*b\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bomega_b\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bOmega_b\s*h\^?2\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
    ],
    "Omega_m": [
        r"\bOmega\s*_?\s*m\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bOmega_m\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bOmegam\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
    ],
    "sigma8": [
        r"\bsigma\s*_?\s*8\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bsigma8\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bσ\s*_?\s*8\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
    ],
    "S8": [
        r"\bS\s*_?\s*8\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bS8\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
    ],
    "ln10_10_As": [
        r"\bln10_10_As\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bln\s*\(?10\^?10\s*A_s\s*\)?\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bln\s*\(?10\^?10\s*As\s*\)?\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
    ],
    "n_s": [
        r"\bn_s\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bns\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
    ],
    "tau_reio": [
        r"\btau_reio\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\btau\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
    ],
    "Omega_k": [
        r"\bOmega\s*_?\s*k\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\bOmega_k\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
    ],
    "z_c": [
        r"\bz_c\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
        r"\blog10z_c\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?)",
    ],
}

PRESETS = {
    "Manual / User model": {
        "text": """TARGET_MODEL block:
H0=72.9
f_EDE=0.082
omega_cdm=0.1270
omega_b=0.0244
sigma8=0.9481
S8=0.9258
z_c=3500

LCDM comparison block:
H0=67.4
omega_cdm=0.120
Omega_m=0.315
sigma8=0.811
S8=0.832""",
        "note": "Initial values for free input.",
    },
    "FUJIKI DTI candidate / default": {
        "text": """TARGET_MODEL block:
H0=72.9
f_EDE=0.082
omega_cdm=0.1270
omega_b=0.0244
sigma8=0.9481
S8=0.9258
z_c=3500
ln10_10_As=3.058
n_s=0.9847
tau_reio=0.0511

LCDM comparison block:
H0=67.4
omega_cdm=0.120
Omega_m=0.315
sigma8=0.811
S8=0.832
ln10_10_As=3.044""",
        "note": "Default registered candidate profile.",
    },
    "Ivanov2020 EDE best-fit style": {
        "text": """TARGET_MODEL block:
H0=71.15
f_EDE=0.105
omega_cdm=0.12999
omega_b=0.02286
Omega_m=0.303
sigma8=0.8322
S8=0.8366
ln10_10_As=3.058
n_s=0.9847
tau_reio=0.0511
z_c=3500

LCDM comparison block:
H0=68.07
omega_cdm=0.11855
omega_b=0.02249
Omega_m=0.306
sigma8=0.808
S8=0.816
ln10_10_As=3.047
n_s=0.9686
tau_reio=0.0566""",
        "note": "Preset for Ivanov-style EDE comparison.",
    },
    "Planck2018 LCDM baseline": {
        "text": """TARGET_MODEL block:
H0=67.36
omega_cdm=0.1200
omega_b=0.02237
Omega_m=0.315
sigma8=0.8111
S8=0.832
ln10_10_As=3.044
n_s=0.9649
tau_reio=0.0544
Omega_k=0.0007

LCDM comparison block:
H0=67.36
omega_cdm=0.1200
omega_b=0.02237
Omega_m=0.315
sigma8=0.8111
S8=0.832
ln10_10_As=3.044
n_s=0.9649
tau_reio=0.0544
Omega_k=0.0""",
        "note": "Planck-like LCDM baseline.",
    },
    "Hill2020 EDE-LSS example": {
        "text": """TARGET_MODEL block:
H0=68.21
f_EDE=0.071
omega_cdm=0.1177
omega_b=0.02253
sigma8=0.806
S8=0.819
ln10_10_As=2.216
n_s=0.968
tau_reio=0.072
z_c=3500

LCDM comparison block:
H0=67.36
omega_cdm=0.1200
omega_b=0.0224
Omega_m=0.315
sigma8=0.8111
S8=0.832
ln10_10_As=3.044""",
        "note": "Practice preset for the EDE-LSS side. Values are treated as input examples for audit.",
    },
    "Poulin2019 EDE example": {
        "text": """TARGET_MODEL block:
H0=72.1
f_EDE=0.122
omega_cdm=0.1306
omega_b=0.0225
ln10_10_As=3.058
n_s=0.9889
tau_reio=0.072
z_c=3500

LCDM comparison block:
H0=67.36
omega_cdm=0.1200
omega_b=0.0224
Omega_m=0.315
sigma8=0.8111
S8=0.832
ln10_10_As=3.044
Omega_k=0.0007""",
        "note": "Practice preset for a Poulin-style EDE example.",
    },
}

# --- v6.0.6 external profile preset expansion ---
def profile_row_to_preset_text_v606(row):
    """Convert one profile row into the app's text cartridge format."""
    model_id = str(row.get("Model ID", "")).strip()
    role = str(row.get("Profile role", "")).strip()

    def val(name):
        raw = row.get(name, "")
        if raw is None:
            return ""
        return str(raw).strip()

    text = "\n".join([
        "TARGET_MODEL block:",
        f"H0={val('H0')}",
        f"f_EDE={val('f_EDE')}",
        f"omega_cdm={val('omega_cdm')}",
        f"omega_b={val('omega_b')}",
        f"sigma8={val('sigma8')}",
        f"S8={val('S8')}",
        "",
        "SOURCE_METADATA block:",
        f"model_id={model_id}",
        f"profile_role={role}",
        "source_type=external_profile_preset_v606",
        "",
        "REFERENCE_NOTE block:",
        "This preset is a parameter-profile cartridge for audit/search/sandbox use.",
        "It is not a likelihood evaluation, posterior comparison, or validation claim.",
    ])
    return text

def load_profile_presets_v606():
    """Load external profile presets from app/data/profile_presets_v606.tsv."""
    from pathlib import Path
    import csv

    path = _DTI_DATA_PRIMARY / "profile_presets_v606.tsv" if (_DTI_DATA_PRIMARY / "profile_presets_v606.tsv").exists() else (_DTI_DATA_FALLBACK / "profile_presets_v606.tsv")
    loaded = {}

    if not path.exists():
        return loaded

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            model_id = str(row.get("Model ID", "")).strip()
            if not model_id:
                continue
            role = str(row.get("Profile role", "profile preset")).strip()
            label = f"{model_id} / {role}"
            loaded[label] = {
                "text": profile_row_to_preset_text_v606(row),
                "note": f"{role}. External profile preset loaded from profile_presets_v606.tsv.",
            }

    return loaded

try:
    PRESETS.update(load_profile_presets_v606())
except Exception:
    pass
# --- end v6.0.6 external profile preset expansion ---

SEARCH_REFERENCE_MODELS = {
    "FUJIKI_DTI_candidate": {
        "H0": 72.9,
        "omega_b": 0.0244,
        "omega_cdm": 0.1270,
        "f_EDE": 0.082,
        "z_c": 3500.0,
        "sigma8": 0.9481,
        "S8": 0.9258,
        "ln10_10_As": 3.058,
        "n_s": 0.9847,
        "tau_reio": 0.0511,
        "source": "app preset",
    },
    "Ivanov_EDE_style": {
        "H0": 71.15,
        "omega_b": 0.02286,
        "omega_cdm": 0.12999,
        "f_EDE": 0.105,
        "z_c": 3500.0,
        "sigma8": 0.8322,
        "S8": 0.8366,
        "ln10_10_As": 3.058,
        "n_s": 0.9847,
        "tau_reio": 0.0511,
        "source": "app preset",
    },
    "Ivanov_LCDM_reference": {
        "H0": 68.07,
        "omega_b": 0.02249,
        "omega_cdm": 0.11855,
        "f_EDE": 0.0,
        "sigma8": 0.808,
        "S8": 0.816,
        "ln10_10_As": 3.047,
        "n_s": 0.9686,
        "tau_reio": 0.0566,
        "source": "app preset",
    },
    "Planck2018_LCDM": {
        "H0": 67.36,
        "omega_b": 0.02237,
        "omega_cdm": 0.1200,
        "Omega_m": 0.315,
        "f_EDE": 0.0,
        "sigma8": 0.8111,
        "S8": 0.832,
        "ln10_10_As": 3.044,
        "n_s": 0.9649,
        "tau_reio": 0.0544,
        "source": "app preset",
    },
    "Hill2020_EDE_LSS_style": {
        "H0": 68.21,
        "omega_b": 0.02253,
        "omega_cdm": 0.1177,
        "f_EDE": 0.071,
        "z_c": 3500.0,
        "sigma8": 0.806,
        "S8": 0.819,
        "ln10_10_As": 2.216,
        "n_s": 0.968,
        "tau_reio": 0.072,
        "source": "app preset",
    },
    "Poulin2019_EDE_style": {
        "H0": 72.1,
        "omega_b": 0.0225,
        "omega_cdm": 0.1306,
        "f_EDE": 0.122,
        "z_c": 3500.0,
        "ln10_10_As": 3.058,
        "n_s": 0.9889,
        "tau_reio": 0.072,
        "source": "app preset",
    },
}

WEIGHTS = {
    "H0": 1.7,
    "omega_cdm": 1.3,
    "omega_b": 1.0,
    "f_EDE": 1.8,
    "z_c": 0.5,
    "sigma8": 1.4,
    "S8": 1.4,
    "ln10_10_As": 0.7,
    "n_s": 0.7,
    "tau_reio": 0.5,
    "Omega_m": 0.8,
}

SCALES = {
    "H0": 5.0,
    "h": 0.05,
    "omega_b": 0.002,
    "omega_cdm": 0.015,
    "Omega_m": 0.04,
    "f_EDE": 0.05,
    "z_c": 1000.0,
    "sigma8": 0.07,
    "S8": 0.07,
    "ln10_10_As": 0.12,
    "n_s": 0.03,
    "tau_reio": 0.03,
    "Omega_k": 0.01,
}


def clean_text(text: str) -> str:
    if not text:
        return ""
    return (
        text.replace("−", "-")
        .replace("ΛCDM", "LCDM")
        .replace("Ω", "Omega")
        .replace("ω", "omega")
        .replace("σ", "sigma")
    )


def to_float_or_nan(value):
    if value is None:
        return np.nan
    if isinstance(value, float) and np.isnan(value):
        return np.nan
    s = str(value).strip()
    if s == "" or s.lower() in {"none", "nan", "null"}:
        return np.nan
    try:
        return float(s)
    except Exception:
        return np.nan


def parse_blocks(text: str) -> pd.DataFrame:
    norm = clean_text(text)
    lines = [line.rstrip() for line in norm.splitlines()]
    blocks = []
    current_label = "UNSPECIFIED"
    current_lines = []

    def flush():
        nonlocal current_lines, current_label, blocks
        if any(x.strip() for x in current_lines):
            blocks.append({"block": current_label, "text": "\n".join(current_lines)})
        current_lines = []

    for line in lines:
        low = line.lower().strip()
        if "target_model" in low or "target model" in low or "candidate" in low:
            flush()
            current_label = "TARGET_MODEL"
            continue
        if "lcdm comparison" in low or "lcdm" == low or "comparison block" in low:
            flush()
            current_label = "LCDM"
            continue
        current_lines.append(line)

    flush()
    if not blocks:
        blocks = [{"block": "TARGET_MODEL", "text": norm}]

    rows = []
    for block in blocks:
        row = {"block": block["block"]}
        btxt = block["text"]
        for param in PARAMS:
            value = None
            for pat in PARAM_PATTERNS.get(param, []):
                m = re.search(pat, btxt, flags=re.IGNORECASE)
                if m:
                    value = m.group(1)
                    break
            row[param] = value
        rows.append(row)

    df = pd.DataFrame(rows)
    for col in PARAMS:
        if col not in df.columns:
            df[col] = None

    if "h" in df.columns:
        for idx, row in df.iterrows():
            h = to_float_or_nan(row.get("h"))
            h0 = to_float_or_nan(row.get("H0"))
            if np.isnan(h0) and not np.isnan(h):
                if h < 10:
                    df.at[idx, "H0"] = f"{100.0*h:.6g}"
            if np.isnan(h) and not np.isnan(h0):
                if h0 > 10:
                    df.at[idx, "h"] = f"{h0/100.0:.6g}"

    return df


def first_block_dict(df: pd.DataFrame, label: str) -> dict:
    if df.empty or "block" not in df.columns:
        return {}
    sub = df[df["block"] == label]
    if sub.empty:
        return {}
    row = sub.iloc[0].to_dict()
    return {k: to_float_or_nan(v) for k, v in row.items() if k != "block"}


def calc_delta_table(df: pd.DataFrame) -> pd.DataFrame:
    target = first_block_dict(df, "TARGET_MODEL")
    lcdm = first_block_dict(df, "LCDM")
    rows = []
    for p in PARAMS:
        tv = target.get(p, np.nan)
        lv = lcdm.get(p, np.nan)
        if not np.isnan(tv) and not np.isnan(lv):
            delta = tv - lv
            direction = "UP" if delta > 0 else "DOWN" if delta < 0 else "SAME"
            rows.append(
                {
                    "parameter": p,
                    "TARGET": tv,
                    "LCDM": lv,
                    "delta": delta,
                    "pct_delta_vs_LCDM": (delta / lv * 100.0) if lv != 0 else np.nan,
                    "direction": direction,
                }
            )
    return pd.DataFrame(rows)


def model_vector_from_target(target: dict) -> dict:
    out = {}
    for p in PARAMS:
        v = target.get(p, np.nan)
        if not np.isnan(v):
            out[p] = float(v)
    if "h" not in out and "H0" in out:
        out["h"] = out["H0"] / 100.0
    if "H0" not in out and "h" in out:
        out["H0"] = out["h"] * 100.0
    return out


def similarity_search(input_model: dict) -> pd.DataFrame:
    rows = []
    for name, ref in SEARCH_REFERENCE_MODELS.items():
        score = 0.0
        used = 0
        details = []
        for p, w in WEIGHTS.items():
            iv = input_model.get(p, np.nan)
            rv = ref.get(p, np.nan)
            if np.isnan(iv) or np.isnan(rv):
                continue
            scale = SCALES.get(p, 1.0)
            d = abs(iv - rv)
            nd = d / scale
            score += w * nd
            used += 1
            details.append(f"{p}:Δ={iv-rv:.5g}")
        if used == 0:
            continue
        similarity = 100.0 / (1.0 + score / max(used, 1))
        rows.append(
            {
                "rank_score": similarity,
                "reference_model": name,
                "used_params": used,
                "source": ref.get("source", ""),
                "difference_notes": "; ".join(details[:8]),
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values("rank_score", ascending=False).reset_index(drop=True)


def safety_class_for_param(param: str, value: float, delta_df: pd.DataFrame) -> tuple:
    if np.isnan(value):
        return ("gray", "missing")

    delta_map = {}
    if not delta_df.empty:
        for _, row in delta_df.iterrows():
            delta_map[str(row["parameter"])] = row

    if param == "H0":
        if value >= 72:
            return ("green", "high-H0 candidate")
        if value >= 70:
            return ("yellow", "mid-H0")
        return ("gray", "near baseline")

    if param == "f_EDE":
        if value <= 0:
            return ("gray", "no EDE")
        if 0.03 <= value <= 0.13:
            return ("yellow", "EDE search range")
        return ("red", "extreme EDE range")

    if param == "omega_cdm":
        row = delta_map.get("omega_cdm")
        if row is not None and float(row["delta"]) > 0.008:
            return ("yellow", "large matter compensation")
        if 0.105 <= value <= 0.135:
            return ("green", "standard search range")
        return ("red", "outlier caution")

    if param == "omega_b":
        if 0.021 <= value <= 0.025:
            return ("green", "standard search range")
        return ("yellow", "check required")

    if param in {"sigma8", "S8"}:
        row = delta_map.get(param)
        if row is not None:
            delta = float(row["delta"])
            if param == "S8" and delta <= 0:
                return ("green", "S8 decrease")
            if delta > 0.05:
                return ("red", "large growth burden")
            if delta > 0:
                return ("yellow", "growth burden")
        if value >= 0.86:
            return ("red", "high growth")
        if value >= 0.83:
            return ("yellow", "moderately high")
        return ("green", "lower / safer")

    if param == "z_c":
        if 2500 <= value <= 4500:
            return ("green", "standard z_c range")
        return ("yellow", "z_ccheck required")

    return ("gray", "reference")


def badge_html(label: str, color: str) -> str:
    palette = {
        "green": ("#0b3d22", "#36d278"),
        "yellow": ("#3f3908", "#ffe15a"),
        "red": ("#4b0d18", "#ff5b6e"),
        "gray": ("#303030", "#bbbbbb"),
    }
    bg, fg = palette.get(color, palette["gray"])
    return f"<span style='display:inline-block;padding:0.25rem 0.6rem;border-radius:999px;background:{bg};color:{fg};font-weight:700;margin:0.15rem;'>{label}</span>"


def card(label: str, value: str, note: str, color: str = "gray") -> str:
    palette = {
        "green": ("#082c1a", "#24d46b"),
        "yellow": ("#363204", "#ffe15a"),
        "red": ("#3c0611", "#ff5b6e"),
        "gray": ("#23252b", "#eeeeee"),
    }
    bg, fg = palette.get(color, palette["gray"])
    return f"""
    <div style="border:1px solid {fg};background:{bg};border-radius:14px;padding:16px;margin-bottom:10px;">
      <div style="font-size:0.82rem;color:#b9b9b9;font-weight:700;">{label}</div>
      <div style="font-size:1.85rem;color:{fg};font-weight:900;line-height:1.25;">{value}</div>
      <div style="font-size:0.85rem;color:#d0d0d0;margin-top:0.4rem;">{note}</div>
    </div>
    """


def load_axiclass_results():
    if not AXICLASS_RESULTS.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(AXICLASS_RESULTS, sep="\t")
    except Exception:
        return pd.DataFrame()


def load_axiclass_delta():
    if not AXICLASS_DELTA.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(AXICLASS_DELTA, sep="\t")
    except Exception:
        return pd.DataFrame()


def compute_background_proxy(h, omega_b, omega_cdm, f_ede, z_c):
    params = {
        "h": h,
        "Omega_b": omega_b / (h * h),
        "Omega_cdm": omega_cdm / (h * h),
        "Omega_g": 5.4e-5,
        "Omega_nu": 3.6e-5,
        "Omega_k": 0.0,
        "f_ede": f_ede,
        "z_c": z_c,
    }

    def derivs(ln_a, y):
        a = np.exp(ln_a)
        H0 = params["h"] * H0_UNIT
        omega_m = params["Omega_b"] + params["Omega_cdm"]
        omega_r = params["Omega_g"] + params["Omega_nu"]
        omega_l = 1.0 - omega_m - omega_r - params["Omega_k"]
        f = params["f_ede"]
        zc = params["z_c"]
        ac = 1.0 / (1.0 + zc) if zc > 0 else 1.0
        if f > 0 and zc > 0:
            w = 0.5
            omega_ede = f * ((ac / a) ** (3.0 * (1.0 + w)) if a > ac else (a / ac) ** 0.5)
        else:
            omega_ede = 0.0
        e_a = np.sqrt(
            params["Omega_g"] * a ** (-4)
            + params["Omega_nu"] * a ** (-4)
            + omega_m * a ** (-3)
            + params["Omega_k"] * a ** (-2)
            + omega_l
            + omega_ede
        )
        return [C_LIGHT / (a * H0 * e_a), 1.0 / (H0 * e_a)]

    sol = solve_ivp(
        derivs,
        (np.log(1e-8), np.log(1.0)),
        [0.0, 0.0],
        t_eval=np.log(np.logspace(-5, 0, 500)),
        method="RK45",
    )
    if not sol.success:
        raise RuntimeError("RK45 background integration failed")

    z_bg = 1.0 / np.exp(sol.t) - 1.0
    eta = sol.y[0]
    r_vals = (3.0 * params["Omega_b"]) / (4.0 * params["Omega_g"]) * np.exp(sol.t)
    c_s = C_LIGHT / np.sqrt(3.0 * (1.0 + r_vals))
    r_s = np.zeros_like(z_bg)
    for i in range(1, len(z_bg)):
        r_s[i] = r_s[i - 1] + (c_s[i] + c_s[i - 1]) / 2.0 * (eta[i] - eta[i - 1]) / C_LIGHT
    r_s = r_s / MPC_TO_M
    z_proxy = 1087.1749
    rs_proxy = float(np.interp(z_proxy, z_bg[::-1], r_s[::-1]))
    return {"z_rec_proxy": z_proxy, "rs_rec_proxy": rs_proxy}


def run_live_class_lcdm_like(h, omega_b, omega_cdm, ln10_10_As, n_s):
    if not HAS_CLASS:
        raise RuntimeError("classy/PyCLASS is not available")
    cosmo = Class()
    params = {
        "output": "mPk",
        "P_k_max_1/Mpc": 3.0,
        "h": float(h),
        "omega_b": float(omega_b),
        "omega_cdm": float(omega_cdm),
        "ln10^{10}A_s": float(ln10_10_As),
        "n_s": float(n_s),
    }
    try:
        cosmo.set(params)
        cosmo.compute()
        derived = cosmo.get_current_derived_parameters(["z_rec", "rs_rec"])
        z_rec = float(derived["z_rec"])
        rs_rec = float(derived["rs_rec"])
        sigma8 = float(cosmo.sigma8())
        omega_m = (float(omega_b) + float(omega_cdm)) / (float(h) * float(h))
        s8 = sigma8 * math.sqrt(omega_m / 0.3)
        return {
            "z_rec": z_rec,
            "rs_rec_Mpc": rs_rec,
            "sigma8": sigma8,
            "S8": s8,
            "Omega_m": omega_m,
            "mode": "LCDM-like CLASS propagation",
        }
    finally:
        try:
            cosmo.struct_cleanup()
            cosmo.empty()
        except Exception:
            pass


def init_session():
    if "selected_preset" not in st.session_state:
        st.session_state.selected_preset = "FUJIKI DTI candidate / default"
    if "paper_text" not in st.session_state:
        st.session_state.pending_paper_text = PRESETS[st.session_state.selected_preset]["text"]
    if "paper_text_widget" not in st.session_state:
        st.session_state.paper_text_widget = st.session_state.get('paper_text', '')
    defaults = {
        "target_H0": 72.9,
        "target_f_EDE": 0.082,
        "target_omega_cdm": 0.1270,
        "target_omega_b": 0.0244,
        "target_sigma8": 0.9481,
        "target_S8": 0.9258,
        "target_z_c": 3500.0,
        "target_ln10_10_As": 3.058,
        "target_n_s": 0.9847,
        "target_tau_reio": 0.0511,
        "lcdm_H0": 67.4,
        "lcdm_omega_cdm": 0.120,
        "lcdm_omega_b": 0.02237,
        "lcdm_Omega_m": 0.315,
        "lcdm_sigma8": 0.811,
        "lcdm_S8": 0.832,
        "lcdm_ln10_10_As": 3.044,
        "lcdm_n_s": 0.9649,
        "lcdm_tau_reio": 0.0544,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def apply_pending_paper_text():
    """Apply deferred text changes before any widget-bound text_area is instantiated."""
    if "pending_paper_text" in st.session_state:
        next_text = st.session_state.pop("pending_paper_text")
        st.session_state.pending_paper_text = next_text
        st.session_state.paper_text_widget = next_text


def sync_form_from_text():
    df = parse_blocks(st.session_state.paper_text)
    target = first_block_dict(df, "TARGET_MODEL")
    lcdm = first_block_dict(df, "LCDM")

    mapping = {
        "H0": "target_H0",
        "f_EDE": "target_f_EDE",
        "omega_cdm": "target_omega_cdm",
        "omega_b": "target_omega_b",
        "sigma8": "target_sigma8",
        "S8": "target_S8",
        "z_c": "target_z_c",
        "ln10_10_As": "target_ln10_10_As",
        "n_s": "target_n_s",
        "tau_reio": "target_tau_reio",
    }
    for p, k in mapping.items():
        v = target.get(p, np.nan)
        if not np.isnan(v):
            st.session_state[k] = float(v)

    lcdm_mapping = {
        "H0": "lcdm_H0",
        "omega_cdm": "lcdm_omega_cdm",
        "omega_b": "lcdm_omega_b",
        "Omega_m": "lcdm_Omega_m",
        "sigma8": "lcdm_sigma8",
        "S8": "lcdm_S8",
        "ln10_10_As": "lcdm_ln10_10_As",
        "n_s": "lcdm_n_s",
        "tau_reio": "lcdm_tau_reio",
    }
    for p, k in lcdm_mapping.items():
        v = lcdm.get(p, np.nan)
        if not np.isnan(v):
            st.session_state[k] = float(v)


def form_to_text():
    return f"""TARGET_MODEL block:
H0={st.session_state.target_H0}
f_EDE={st.session_state.target_f_EDE}
omega_cdm={st.session_state.target_omega_cdm}
omega_b={st.session_state.target_omega_b}
sigma8={st.session_state.target_sigma8}
S8={st.session_state.target_S8}
z_c={st.session_state.target_z_c}
ln10_10_As={st.session_state.target_ln10_10_As}
n_s={st.session_state.target_n_s}
tau_reio={st.session_state.target_tau_reio}

LCDM comparison block:
H0={st.session_state.lcdm_H0}
omega_cdm={st.session_state.lcdm_omega_cdm}
omega_b={st.session_state.lcdm_omega_b}
Omega_m={st.session_state.lcdm_Omega_m}
sigma8={st.session_state.lcdm_sigma8}
S8={st.session_state.lcdm_S8}
ln10_10_As={st.session_state.lcdm_ln10_10_As}
n_s={st.session_state.lcdm_n_s}
tau_reio={st.session_state.lcdm_tau_reio}"""



def ensure_paper_text_state():
    """Initialize paper_text safely before any widget-bound access."""
    default_text = ""
    try:
        default_text = PRESETS.get(st.session_state.get("selected_preset", ""), {}).get("text", "")
    except Exception:
        default_text = ""

    if "paper_text" not in st.session_state:
        st.session_state["paper_text"] = default_text

    if "paper_text_widget" not in st.session_state:
        st.session_state["paper_text_widget"] = st.session_state.get("paper_text", "")

    if "pending_paper_text" in st.session_state:
        st.session_state["paper_text"] = st.session_state.pop("pending_paper_text")
        st.session_state["paper_text_widget"] = st.session_state["paper_text"]

st.set_page_config(page_title="DTI-Core Grand Auditor v6.0", layout="wide")



# --- DTI_RUN_BUTTONS_RED_UI_PATCH_V1 ---
# Local-only UI styling: make RUN-style action buttons visibly red.
_DTI_RUN_BUTTONS_RED_UI_PATCH_V1 = True

st.markdown(
    """
    <style>
    div.stButton > button[kind="primary"] {
        background-color: #d92d20 !important;
        border-color: #d92d20 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #b42318 !important;
        border-color: #b42318 !important;
        color: #ffffff !important;
    }
    div.stButton > button[kind="primary"]:active {
        background-color: #912018 !important;
        border-color: #912018 !important;
        color: #ffffff !important;
    }
    div.stButton > button[kind="primary"]:disabled {
        background-color: #f2b8b5 !important;
        border-color: #f2b8b5 !important;
        color: #ffffff !important;
        opacity: 0.75 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# --- end DTI_RUN_BUTTONS_RED_UI_PATCH_V1 ---


ensure_paper_text_state()

st.markdown(
    """
<style>
.block-container { padding-top: 2rem; max-width: 1320px; }
div[data-testid="stSidebar"] { min-width: 290px; }
h1, h2, h3 { letter-spacing: 0.01em; }
.smallnote { color:#bbbbbb; font-size:0.92rem; }

.boundary-card {
    border: 1px solid rgba(255, 193, 7, 0.55);
    background: rgba(80, 70, 20, 0.35);
    border-radius: 12px;
    padding: 14px 16px;
    margin: 16px 0 22px 0;
    line-height: 1.65;
}
.source-card {
    border: 1px solid rgba(120, 120, 120, 0.35);
    background: rgba(30, 34, 42, 0.72);
    border-radius: 12px;
    padding: 14px 16px;
    margin: 12px 0;
    line-height: 1.55;
}
.metric-card {
    border: 1px solid rgba(76, 175, 80, 0.38);
    background: rgba(15, 50, 30, 0.42);
    border-radius: 12px;
    padding: 14px 16px;
    margin: 12px 0;
    line-height: 1.55;
}
.small-muted {
    color: rgba(220, 220, 220, 0.70);
    font-size: 0.92rem;
}
</style>
""",
    unsafe_allow_html=True,
)



init_session()
apply_pending_paper_text()

st.title("DTI-Core Grand Auditor v6.0.6")
st.caption("Public parameter-profile audit interface for cosmological model comparison, benchmark proximity review, and reproducibility-first inspection.")
st.markdown("""
<div class="card">
<b>Purpose:</b> inspect and compare cosmological parameter profiles using registered presets, candidate/reference forms, and locked benchmark references.<br>
<b>Included:</b> 100 parameter-profile presets, profile search, candidate/reference comparison, AxiCLASS FIX1 locked benchmark values, and an external Render-hosted CLASS API sandbox.<br>
<b>Not included:</b> likelihood evaluation, posterior comparison, Planck validation, or final cosmological conclusion.<br>
<b>Positioning:</b> FUJIKI DTI is included as one registered candidate profile, not as the only supported use case.<br><br>
<b>Public routes:</b><br>
<a href="https://dti-real-app-v606.streamlit.app" target="_blank">Public Streamlit app</a> ·
<a href="https://github.com/fujikix1102/dti-real-app-v606" target="_blank">Frontend GitHub</a> ·
<a href="https://dti-class-api.onrender.com/health" target="_blank">External CLASS API health</a> ·
<a href="https://github.com/fujikix1102/dti-class-api" target="_blank">Backend GitHub</a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<b>How to use this app:</b><br>
1. Select a registered profile from the left sidebar.<br>
2. Inspect the generated parameter block.<br>
3. Use <b>Text to form</b> or <b>Form to text</b> to move between text and editable fields.<br>
4. Compare candidate and reference parameter burdens.<br>
5. Check the locked AxiCLASS FIX1 benchmark values as read-only references.<br>
6. Treat optional live CLASS/AxiCLASS sandbox output as exploratory and non-canonical.
</div>
""", unsafe_allow_html=True)




st.info("DOM-safe rendering mode: live/exploratory outputs are rendered as stable code blocks instead of dynamic JSON widgets.")



st.markdown("""
<div class="boundary-card">
<b>Benchmark boundary:</b> AxiCLASS FIX1 values are read-only benchmark references. Optional live CLASS/AxiCLASS sandbox output is exploratory and non-canonical.
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.header("1. Parameter profile cartridge")

    preset_names = list(PRESETS.keys())
    current_selected = st.session_state.get("selected_preset", preset_names[0] if preset_names else "")
    if current_selected not in preset_names and preset_names:
        current_selected = preset_names[0]
        st.session_state["selected_preset"] = current_selected

    # Hard initial sync: the first visible sidebar text box must contain the active preset text.
    active_preset_text = PRESETS.get(current_selected, {}).get("text", "")
    if active_preset_text:
        if not st.session_state.get("paper_text") or not st.session_state.get("paper_text_widget"):
            st.session_state["paper_text"] = active_preset_text
            st.session_state["paper_text_widget"] = active_preset_text
            st.session_state["pending_paper_text"] = active_preset_text

    selected_preset = st.selectbox(
        "Load registered profile",
        preset_names,
        index=preset_names.index(current_selected) if current_selected in preset_names else 0,
        key="selected_preset_selector_v606",
    )

    if selected_preset and selected_preset != st.session_state.get("selected_preset"):
        selected_text = PRESETS.get(selected_preset, {}).get("text", "")
        st.session_state["selected_preset"] = selected_preset
        st.session_state["paper_text"] = selected_text
        st.session_state["paper_text_widget"] = selected_text
        st.session_state["pending_paper_text"] = selected_text
        st.rerun()

    preset_note = PRESETS.get(st.session_state.get("selected_preset", selected_preset), {}).get("note", "")
    if preset_note:
        st.info(preset_note)

    # Keep the visible text box populated on first load and after reruns.
    active_profile_for_text = st.session_state.get("selected_preset", selected_preset)
    # DTI_SIDEBAR_CANDIDATE_REFERENCE_FORM_CALL_V1
    _dti_sidebar_candidate_reference_form_v2()
    fallback_text = PRESETS.get(active_profile_for_text, {}).get("text", "")
    if not st.session_state.get("paper_text_widget") and fallback_text:
        st.session_state["paper_text_widget"] = fallback_text
    if not st.session_state.get("paper_text") and st.session_state.get("paper_text_widget"):
        st.session_state["paper_text"] = st.session_state.get("paper_text_widget", "")

    st.text_area("Profile text / generated block", key="paper_text_widget", height=270)

    if st.session_state.get("paper_text_widget", "") != st.session_state.get("paper_text", ""):
        st.session_state["paper_text"] = st.session_state.get("paper_text_widget", "")
        st.session_state["pending_paper_text"] = st.session_state.get("paper_text_widget", "")

    col_sidebar_1, col_sidebar_2 = st.columns(2)
    with col_sidebar_1:
        # DTI_PRIMARY_FLOW_TOP_NOTICE_V1
        st.markdown("#### Step 1: apply text to form")
        st.caption("After editing the TARGET_MODEL block, use this button to load the values into the form.")
        # DTI_TEXT_TO_FORM_COMPACT_EN_GUIDE_V1
        st.caption("Step 1: edit the TARGET_MODEL block, then apply it to the form.")
        if st.button("Apply text to form", width="stretch", key="sidebar_text_to_form_v606", type="primary"):
            sync_form_from_text()
            st.rerun()
    with col_sidebar_2:
        if st.button("Form to text", width="stretch", key="sidebar_form_to_text_v606"):
            st.session_state["pending_paper_text"] = form_to_text()
            st.rerun()

    st.markdown("---")
    # DTI_README_SIDEBAR_BEFORE_CURRENT_PROFILE_STATUS_FIX
    _dti_render_readme_download_v3_safe()
    # DTI_MANUAL_PDF_DOWNLOAD_BUTTON_RENDER_CALL_V1
    _dti_render_manual_pdf_download_v1()

    st.subheader("2. Current profile status")

    active_profile_name = st.session_state.get("selected_preset", selected_preset)
    try:
        active_profile_role = PRESETS.get(active_profile_name, {}).get("role", "registered or custom profile")
    except Exception:
        active_profile_role = "registered or custom profile"

    st.markdown(f"**Active profile:** {active_profile_name}")
    st.markdown(f"**Profile role:** {active_profile_role}")
    st.markdown("**Mode:** Candidate / Reference comparison")
    st.success("AxiCLASS FIX1 benchmark: read-only")
    st.caption("Changing presets or form values does not recompute this locked benchmark.")

    st.markdown("---")
    st.subheader("3. Export / share")

    current_block = st.session_state.get("paper_text_widget", st.session_state.get("paper_text", ""))
    st.download_button(
        "Download current parameter block",
        data=str(current_block),
        file_name="current_parameter_block.txt",
        mime="text/plain",
        width="stretch",
        key="sidebar_download_current_parameter_block_v606",
    )

    st.markdown("[Open GitHub](https://github.com/fujikix1102/dti-real-app-v606)")
    st.markdown("[Open public app](https://dti-real-app-v606.streamlit.app)")
st.header("1. Candidate / Reference parameter input form")
st.markdown(
    "Parameter names are fixed. Edit only the values. Use the button to convert form values into text and feed the audit/search engine."
)

with st.expander("TARGET_MODEL form", expanded=True):
    cols = st.columns(5)
    with cols[0]:
        st.number_input("H0", min_value=40.0, max_value=90.0, step=0.01, key="target_H0")
        st.number_input("f_EDE", min_value=0.0, max_value=0.30, step=0.001, key="target_f_EDE")
    with cols[1]:
        st.number_input("omega_cdm", min_value=0.05, max_value=0.20, step=0.0001, format="%.5f", key="target_omega_cdm")
        st.number_input("omega_b", min_value=0.015, max_value=0.035, step=0.0001, format="%.5f", key="target_omega_b")
    with cols[2]:
        st.number_input("sigma8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="target_sigma8")
        st.number_input("S8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="target_S8")
    with cols[3]:
        st.number_input("z_c", min_value=0.0, max_value=10000.0, step=50.0, key="target_z_c")
        st.number_input("ln10_10_As", min_value=1.0, max_value=4.5, step=0.001, format="%.5f", key="target_ln10_10_As")
    with cols[4]:
        st.number_input("n_s", min_value=0.80, max_value=1.20, step=0.0001, format="%.5f", key="target_n_s")
        st.number_input("tau_reio", min_value=0.0, max_value=0.20, step=0.0001, format="%.5f", key="target_tau_reio")

with st.expander("LCDM comparison form", expanded=False):
    cols = st.columns(5)
    with cols[0]:
        st.number_input("LCDM H0", min_value=40.0, max_value=90.0, step=0.01, key="lcdm_H0")
        st.number_input("LCDM Omega_m", min_value=0.10, max_value=0.60, step=0.001, format="%.5f", key="lcdm_Omega_m")
    with cols[1]:
        st.number_input("LCDM omega_cdm", min_value=0.05, max_value=0.20, step=0.0001, format="%.5f", key="lcdm_omega_cdm")
        st.number_input("LCDM omega_b", min_value=0.015, max_value=0.035, step=0.0001, format="%.5f", key="lcdm_omega_b")
    with cols[2]:
        st.number_input("LCDM sigma8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="lcdm_sigma8")
        st.number_input("LCDM S8", min_value=0.50, max_value=1.20, step=0.0001, format="%.5f", key="lcdm_S8")
    with cols[3]:
        st.number_input("LCDM ln10_10_As", min_value=1.0, max_value=4.5, step=0.001, format="%.5f", key="lcdm_ln10_10_As")
        st.number_input("LCDM n_s", min_value=0.80, max_value=1.20, step=0.0001, format="%.5f", key="lcdm_n_s")
    with cols[4]:
        st.number_input("LCDM tau_reio", min_value=0.0, max_value=0.20, step=0.0001, format="%.5f", key="lcdm_tau_reio")

if st.button("Apply form values to text and update search engine", type="primary", width="stretch"):
    st.session_state.pending_paper_text = form_to_text()
    st.rerun()

df_blocks = parse_blocks(st.session_state.paper_text)
delta_df = calc_delta_table(df_blocks)
target_model = model_vector_from_target(first_block_dict(df_blocks, "TARGET_MODEL"))
lcdm_model = model_vector_from_target(first_block_dict(df_blocks, "LCDM"))

st.markdown("---")

st.header("2. Source metadata")

with st.expander("Candidate and reference source metadata", expanded=True):
    st.markdown('<div class="small-muted">These fields are optional, but recommended for public or collaborative use. They do not change the numerical calculation.</div>', unsafe_allow_html=True)
    src_cols = st.columns(2)
    with src_cols[0]:
        candidate_source_paper = st.text_input("Candidate source paper / arXiv / DOI", value="User-entered / candidate parameter block")
        candidate_source_location = st.text_input("Candidate source table / figure / line", value="manual entry")
    with src_cols[1]:
        reference_source_paper = st.text_input("Reference source paper / arXiv / DOI", value="Reference / LCDM comparison block")
        reference_source_location = st.text_input("Reference source table / figure / line", value="manual entry")
    candidate_source_note = st.text_area("Candidate source note", value="Record extraction note, table number, or assumptions.", height=80)
    reference_source_note = st.text_area("Reference source note", value="Record reference extraction note, table number, or assumptions.", height=80)

st.markdown(f"""
<div class="source-card">
<b>Candidate source:</b> {candidate_source_paper}<br>
<b>Candidate location:</b> {candidate_source_location}<br>
<b>Reference source:</b> {reference_source_paper}<br>
<b>Reference location:</b> {reference_source_location}
</div>
""", unsafe_allow_html=True)

st.header("3. Literature text audit")

st.dataframe(df_blocks, width="stretch", hide_index=True)

st.subheader("TARGET_MODEL vs LCDM comparison")
if delta_df.empty:
    st.warning("TARGET_MODEL and LCDM comparison values are incomplete.")
else:
    st.dataframe(delta_df, width="stretch", hide_index=True)

st.markdown("---")
st.header("4. High-precision parameter search engine")

st.markdown("""
<div class="metric-card">
<b>Search metric:</b> weighted normalized distance over available cosmological parameters.<br>
<b>Missing values:</b> ignored pairwise; no value is imputed automatically.<br>
<b>Interpretation:</b> the nearest model is a parameter-space similarity hint, not a likelihood preference.<br>
<b>Recommended use:</b> compare H0 shift, r_s response, omega_cdm compensation, sigma8/S8 burden, and source provenance together.
</div>
""", unsafe_allow_html=True)

st.markdown(
    "The current TARGET_MODEL is compared against registered reference presets using weighted multivariate distance. This is a search/classification aid, not a likelihood evaluation."
)

search_df = similarity_search(target_model)
if search_df.empty:
    st.warning("Not enough parameters are available for search.")
else:
    top = search_df.iloc[0]
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        st.metric("Nearest reference model", top["reference_model"])
    with c2:
        st.metric("Similarity score", f"{top['rank_score']:.2f}")
    with c3:
        st.caption(top["difference_notes"])
    st.dataframe(search_df, width="stretch", hide_index=True)

st.subheader("Current input model safety/readout cards")
card_cols = st.columns(5)
for i, p in enumerate(["H0", "omega_b", "omega_cdm", "f_EDE", "z_c"]):
    v = target_model.get(p, np.nan)
    color, note = safety_class_for_param(p, v, delta_df)
    value = "missing" if np.isnan(v) else f"{v:.5g}"
    with card_cols[i]:
        st.markdown(card(p, value, note, color), unsafe_allow_html=True)

card_cols2 = st.columns(5)
for i, p in enumerate(["sigma8", "S8", "ln10_10_As", "n_s", "tau_reio"]):
    v = target_model.get(p, np.nan)
    color, note = safety_class_for_param(p, v, delta_df)
    value = "missing" if np.isnan(v) else f"{v:.5g}"
    with card_cols2[i]:
        st.markdown(card(p, value, note, color), unsafe_allow_html=True)

st.markdown("---")
# DTI_PRESET_LEARNING_MAIN_PANEL_V1
_dti_main_candidate_reference_panel_v1()

st.header("5. AxiCLASS FIX1 locked benchmark")

st.markdown("""
<div class="boundary-card">
<b>Locked benchmark rule:</b> these values are copied from the successful AxiCLASS FIX1 checkpoint and do not change when the form changes.<br>
<b>Why this matters:</b> researchers can compare a newly entered parameter block against a stable reference without confusing it with a fresh live calculation.<br>
<b>For live calculations:</b> use the exploratory sandbox only, and treat results as non-canonical until separately audited.
</div>
""", unsafe_allow_html=True)

st.markdown(
    """
This section is not a live recomputation.  
It displays the fixed checkpoint values from the successful AxiCLASS FIX1 propagation of Ivanov LCDM / Ivanov EDE / FUJIKI DTI as benchmark references.
Changing presets or form values does not change these locked benchmark values.
"""
)

st.markdown(
    badge_html("Green: propagated / safer", "green")
    + badge_html("Yellow: informative / caution", "yellow")
    + badge_html("Red: cost / tension risk", "red")
    + badge_html("Gray: reference", "gray"),
    unsafe_allow_html=True,
)

axi_results = load_axiclass_results()
axi_delta = load_axiclass_delta()

if axi_results.empty:
    st.warning("AxiCLASS FIX1 results TSV was not found. Check app/data/axiclass_fix1_results.tsv.")
else:
    ok_count = int((axi_results.get("status", pd.Series([])).astype(str) == "OK").sum())
    total_count = len(axi_results)
    st.success(f"FIX1 checkpoint status: {ok_count}/{total_count} models OK")

    tabs = st.tabs(["FUJIKI DTI", "Ivanov EDE", "Ivanov LCDM", "Full table", "Delta table"])
    model_key_map = {
        "FUJIKI DTI": "Fujiki_DTI_candidate_AxiCLASS_FIX1",
        "Ivanov EDE": "Ivanov_EDE_bestfit_AxiCLASS_FIX1",
        "Ivanov LCDM": "Ivanov_LCDM_comparison_AxiCLASS_FIX1",
    }

    for tab, label in zip(tabs[:3], ["FUJIKI DTI", "Ivanov EDE", "Ivanov LCDM"]):
        with tab:
            key = model_key_map[label]
            sub = axi_results[axi_results["model_id"].astype(str) == key]
            if sub.empty:
                st.warning(f"{key} not found.")
            else:
                r = sub.iloc[0]
                cols = st.columns(4)
                status_color = "green" if str(r.get("status", "")) == "OK" else "red"
                with cols[0]:
                    st.markdown(card("H0", f"{float(r.get('H0')):.2f}", "FIX1 locked value", status_color), unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(card("rs_rec [Mpc]", f"{float(r.get('rs_rec_Mpc_AxiCLASS')):.4f}", "AxiCLASS propagated value", "green"), unsafe_allow_html=True)
                with cols[2]:
                    sig = float(r.get("sigma8_AxiCLASS"))
                    sig_color = "green" if sig < 0.83 else "yellow" if sig < 0.86 else "red"
                    st.markdown(card("sigma8", f"{sig:.6f}", "AxiCLASS propagated value", sig_color), unsafe_allow_html=True)
                with cols[3]:
                    s8 = float(r.get("S8_AxiCLASS"))
                    s8_color = "green" if s8 < 0.82 else "yellow" if s8 < 0.85 else "red"
                    st.markdown(card("S8", f"{s8:.6f}", "AxiCLASS propagated value", s8_color), unsafe_allow_html=True)
                st.caption(str(r.get("source_note", "")))

    with tabs[3]:
        st.dataframe(axi_results, width="stretch", hide_index=True)

    with tabs[4]:
        if axi_delta.empty:
            st.warning("AxiCLASS FIX1 delta TSV was not found.")
        else:
            st.dataframe(axi_delta, width="stretch", hide_index=True)

st.markdown("---")
st.header("6. RK45 background-universe proxy")
st.markdown(
    "This is a lightweight background proxy. It is not a substitute for AxiCLASS FIX1 or formal likelihood evaluation. Use it only for quick intuition about the current input model."
)

if st.button("Run RK45 background proxy for current input model", width="stretch", type="primary"):
    try:
        h = target_model.get("h", target_model.get("H0", np.nan) / 100.0)
        ob = target_model.get("omega_b", np.nan)
        oc = target_model.get("omega_cdm", np.nan)
        fe = target_model.get("f_EDE", 0.0)
        zc = target_model.get("z_c", 0.0)
        if np.isnan(h) or np.isnan(ob) or np.isnan(oc):
            st.error("h/H0, omega_b, and omega_cdm are required.")
        else:
            proxy = compute_background_proxy(float(h), float(ob), float(oc), float(fe), float(zc))
            cols = st.columns(2)
            with cols[0]:
                st.metric("z_rec proxy", f"{proxy['z_rec_proxy']:.4f}")
            with cols[1]:
                st.metric("rs_rec proxy", f"{proxy['rs_rec_proxy']:.4f} Mpc")
    except Exception as e:
        st.error(f"RK45 proxy failed: {e}")

st.markdown("---")
def _render_local_axiclass_fixed_example_v606():
    st.header("7. Local experimental probes")
    st.markdown(
        """
    This section groups bounded implementation probes. In the public app, configured endpoints use public Render APIs; in local testing, they may fall back to localhost endpoints.

    These probes are useful for implementation checks, reproducibility inspection, and immediate derived-quantity inspection. They are intentionally separated from the public deployed app, Render services, manuscript checkpoints, and likelihood/posterior analysis.

    **Subsections**

    - **7a. AxiCLASS fixed-example check**: source-locked fixed example, no arbitrary input.
    - **7b. Vanilla-profile API check**: bounded profile payload check, derived proxy quantities only.
        """
    )


    # DTI_PUBLIC_API_WARMUP_UI_7A7B_V2
    st.subheader("7 preflight. Public API warm-up")
    st.caption(
        "Use this before 7a/7b when the public Render API may be asleep. "
        "Warm-up only checks service availability; it is not a likelihood, posterior, Planck, or manuscript calculation."
    )

    warmup_7a_endpoint = _dti_default_7a_fixed_example_endpoint_public_local_v1()
    warmup_7b_endpoint = _dti_default_7b_live_endpoint_public_local_v1()

    with st.expander("Warm up configured API endpoints before 7a/7b", expanded=False):
        st.write("Configured 7a endpoint:")
        st.code(warmup_7a_endpoint, language="text")
        st.write("Configured 7b endpoint:")
        st.code(warmup_7b_endpoint, language="text")
        st.info(
            "Warm-up can reduce first-run delay after Render cold start. "
            "It does not compute new cosmological results."
        )

        if st.button("Warm up public API", key="dti_warmup_public_api_7a7b_v2", width="stretch"):
            rows = []
            rows.extend(_dti_warmup_public_api_v2(warmup_7a_endpoint, timeout_sec=60))
            if _dti_endpoint_base_url_v2(warmup_7b_endpoint) != _dti_endpoint_base_url_v2(warmup_7a_endpoint):
                rows.extend(_dti_warmup_public_api_v2(warmup_7b_endpoint, timeout_sec=60))
            st.session_state["dti_public_api_warmup_rows_7a7b_v2"] = rows

        if "dti_public_api_warmup_rows_7a7b_v2" in st.session_state:
            st.dataframe(st.session_state["dti_public_api_warmup_rows_7a7b_v2"], use_container_width=True)

    st.header("7a. AxiCLASS fixed-example check")

    st.markdown("""
<div class="boundary-card">
<b>Bounded implementation check.</b><br>
This section queries the configured AxiCLASS fixed-example API endpoint.<br>
It is intended for implementation testing and reproducibility inspection only.<br><br>
<b>Scope:</b> one source-locked fixed example only. It does not accept arbitrary user input.<br>
<b>Not included:</b> likelihood evaluation, posterior comparison, Planck validation, MCMC sampling, or manuscript checkpoint updates.<br>
<b>Status:</b> experimental, non-canonical, and not part of the public deployed workflow.
</div>
""", unsafe_allow_html=True)

    st.caption(
        "Use this section only for bounded implementation testing. "
        "In Streamlit Cloud, this should use the configured public Render API; in local testing, it may fall back to a local endpoint."
    )

    # DTI_ENABLE_GATE_NOTICE_INSERTED_FOR: Enable local-only AxiCLASS fixed-example check
    _dti_enable_gate_notice_7abc_v1("7a AxiCLASS fixed-example check", "This prevents the fixed-example check from being skipped by accident.")
    enable_local_axiclass = st.checkbox(
        "Enable AxiCLASS fixed-example check",
        value=False,
        key="enable_local_axiclass_fixed_example_v606",
    )

    if not enable_local_axiclass:
        st.info("Disabled by default. Enable only for bounded implementation testing.")
        return

    _dti_7a_endpoint_mode_notice_v1()

    local_endpoint = st.text_input(
        "Fixed-example API endpoint",
        value=_dti_default_7a_fixed_example_endpoint_public_local_v1(),
        key="local_axiclass_fixed_endpoint_v606",
    )

    # DTI_7A_WAIT_TIME_NOTICE_PUBLIC_UI_V1
    st.info(
        "This fixed-example check may take several minutes, especially after Render cold start. "
        "Please wait for the result and avoid repeated clicks while it is running."
    )


    # DTI_7A_FRONTEND_CACHE_CONTROL_V2
    use_7a_cache = st.checkbox(
        "Use one-hour frontend cache for fixed-example result",
        value=True,
        key="dti_use_7a_frontend_cache_v2",
        help="Recommended. The fixed-example endpoint is source-locked and may take several minutes after Render cold start.",
    )

    with st.expander("How to use the AxiCLASS API endpoint", expanded=False):
        st.markdown(
            """
For public Streamlit use, configure the endpoint through Streamlit Secrets.

DTI_PUBLIC_FIXED_EXAMPLE_API_URL = "https://dti-axiclass-api.onrender.com/axiclass/fixed-example-compact"

For local development, run the AxiCLASS API separately and set the endpoint manually.

Example local command:

cd dti-axiclass-api
bash run_local.sh
            """
        )

    if st.button("Run fixed-example check", key="run_local_axiclass_fixed_example_v606", width="stretch", type="primary"):
        try:
            if _dti_is_disabled_endpoint_literal_v1(local_endpoint):
                _dti_local_endpoint_disabled_notice_v1()
                st.stop()
            cached_result_7a = _dti_post_json_endpoint_cached_or_uncached_v2(
                local_endpoint,
                {},
                240,
                "7a_fixed_example_compact",
                use_cache=use_7a_cache,
            )
            st.session_state["local_axiclass_fixed_result_v606"] = cached_result_7a["body"]
            st.session_state["local_axiclass_fixed_http_status_v606"] = cached_result_7a["status_code"]
            st.session_state["local_axiclass_fixed_elapsed_sec_v606"] = cached_result_7a["elapsed_sec"]
            st.session_state["local_axiclass_fixed_cache_meta_v606"] = cached_result_7a["cache"]
        except Exception as exc:
            st.session_state["local_axiclass_fixed_result_v606"] = {
                "status": "failed",
                "message": repr(exc),
                "boundary": {
                    "experimental": True,
                    "non_canonical": True,
                    "fixed_example_only": True,
                    "arbitrary_user_input": False,
                    "likelihood_evaluation": False,
                    "posterior_comparison": False,
                    "planck_validation": False,
                    "canonical_checkpoint_update": False,
                    "streamlit_frontend_update": False,
                },
                "local_server_start": "For local development: cd dti-axiclass-api && bash run_local.sh",
            }
            st.session_state["local_axiclass_fixed_http_status_v606"] = None

    result = st.session_state.get("local_axiclass_fixed_result_v606")
    http_status = st.session_state.get("local_axiclass_fixed_http_status_v606")

    if not result:
        return

    st.markdown("##### Local fixed-example result")
    st.caption(f"HTTP status: {http_status}")

    if result.get("status") == "ok":
        st.success("Local fixed-example endpoint returned status: ok")
    else:
        st.warning("Local fixed-example endpoint did not return ok. Check that the local API is running.")
        if result.get("local_server_start"):
            st.code(result.get("local_server_start"), language="bash")

    derived = result.get("derived", {})
    if isinstance(derived, dict) and derived:
        derived_rows = []
        for key in ["h", "Omega0_m", "Omega_Lambda", "age", "rs_drag", "sigma8"]:
            if key in derived:
                derived_rows.append({"quantity": key, "value": derived.get(key)})
        if derived_rows:
            st.markdown("##### Derived values")
            st.dataframe(pd.DataFrame(derived_rows), hide_index=True, width="stretch")

    bg = result.get("compact_background_summary", {})
    if isinstance(bg, dict) and bg:
        selected_rows = []
        for key in ["(.)rho_scf", "(.)Omega_scf", "(.)p_scf", "(.)w_scf", "phi_scf", "phi'_scf", "V_scf", "V'_scf", "V''_scf"]:
            item = bg.get(key)
            if isinstance(item, dict):
                selected_rows.append({
                    "field": key,
                    "len": item.get("len"),
                    "first": item.get("first"),
                    "last": item.get("last"),
                })
        if selected_rows:
            st.markdown("##### Selected scalar-field / axion background summary")
            st.dataframe(pd.DataFrame(selected_rows), hide_index=True, width="stretch")

    boundary = result.get("boundary", {})
    if isinstance(boundary, dict) and boundary:
        boundary_rows = [{"flag": k, "value": v} for k, v in boundary.items() if k != "note"]
        if boundary_rows:
            st.markdown("##### Boundary flags")
            st.dataframe(pd.DataFrame(boundary_rows), hide_index=True, width="stretch")

    with st.expander("Raw fixed-example API response", expanded=False):
        st.code(json.dumps(result, indent=2, sort_keys=True), language="json")

_render_local_axiclass_fixed_example_v606()

# ---------------------------------------------------------------------
# Section 7b: Vanilla-profile API check
# ---------------------------------------------------------------------
st.divider()
st.header("7b. Vanilla-profile API check")

st.markdown(
    """
**Purpose.** This subsection accepts local manual real-valued cosmological inputs and sends them to a local vanilla CLASS live derived-parameter endpoint.

The default input source is now the **current sidebar profile where compatible**. This prevents the live probe from silently using an unrelated preset while a different TARGET_MODEL block is selected in the sidebar.

**Compatibility rule.**

- Used by vanilla CLASS probe: `H0`, `omega_cdm`, `omega_b`, `n_s`, `ln(10^10 A_s)`.
- Shown but not used by vanilla CLASS probe: `f_EDE`.
- Treated as reference/display only, not input: `sigma8`, `S8`.

This probe returns CLASS-derived quantities only. It does not compute likelihood, posterior, evidence, MCMC chains, Planck validation, or manuscript values.
    """
)

def _section8b_parse_float_from_text(text, names):
    import re

    if not isinstance(text, str):
        return None

    for name in names:
        escaped = re.escape(name)
        patterns = [
            rf"(?m)^\s*{escaped}\s*=\s*([-+]?[0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?)",
            rf"(?m)^\s*{escaped}\s*:\s*([-+]?[0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?)",
        ]
        for pat in patterns:
            m = re.search(pat, text)
            if m:
                try:
                    return float(m.group(1))
                except Exception:
                    pass
    return None

_active_profile_text_8b = st.session_state.get("paper_text_widget", "")
if not _active_profile_text_8b:
    _active_profile_text_8b = st.session_state.get("paper_text", "")

_active_profile_name_8b = st.session_state.get("selected_preset", "current sidebar profile")

_current_sidebar_values_8b = {
    "H0": _section8b_parse_float_from_text(_active_profile_text_8b, ["H0"]),
    "omega_cdm": _section8b_parse_float_from_text(_active_profile_text_8b, ["omega_cdm", "omch2", "omega_c"]),
    "omega_b": _section8b_parse_float_from_text(_active_profile_text_8b, ["omega_b", "ombh2", "omega_baryon"]),
    "n_s": _section8b_parse_float_from_text(_active_profile_text_8b, ["n_s", "ns"]),
    "ln1010A_s": _section8b_parse_float_from_text(_active_profile_text_8b, ["ln1010A_s", "ln10_10_As", "ln10_10_A_s", "ln_10_10_A_s"]),
    "f_EDE": _section8b_parse_float_from_text(_active_profile_text_8b, ["f_EDE", "fEDE", "f_ede"]),
    "sigma8_reference": _section8b_parse_float_from_text(_active_profile_text_8b, ["sigma8", "sigma_8"]),
    "S8_reference": _section8b_parse_float_from_text(_active_profile_text_8b, ["S8", "S_8"]),
}

_fallback_live_values_8b = {
    "H0": 72.9,
    "omega_cdm": 0.127,
    "omega_b": 0.0244,
    "n_s": 0.9847,
    "ln1010A_s": 3.058,
}

_current_compatible_values_8b = {
    "H0": _current_sidebar_values_8b["H0"] if _current_sidebar_values_8b["H0"] is not None else _fallback_live_values_8b["H0"],
    "omega_cdm": _current_sidebar_values_8b["omega_cdm"] if _current_sidebar_values_8b["omega_cdm"] is not None else _fallback_live_values_8b["omega_cdm"],
    "omega_b": _current_sidebar_values_8b["omega_b"] if _current_sidebar_values_8b["omega_b"] is not None else _fallback_live_values_8b["omega_b"],
    "n_s": _current_sidebar_values_8b["n_s"] if _current_sidebar_values_8b["n_s"] is not None else _fallback_live_values_8b["n_s"],
    "ln1010A_s": _current_sidebar_values_8b["ln1010A_s"] if _current_sidebar_values_8b["ln1010A_s"] is not None else _fallback_live_values_8b["ln1010A_s"],
}

_live_presets_8b = {
    "Use current sidebar profile where compatible": _current_compatible_values_8b,
    "FUJIKI DTI candidate": {
        "H0": 72.9,
        "omega_cdm": 0.127,
        "omega_b": 0.0244,
        "n_s": 0.9847,
        "ln1010A_s": 3.058,
    },
    "Planck-like baseline": {
        "H0": 67.4,
        "omega_cdm": 0.1200,
        "omega_b": 0.0224,
        "n_s": 0.965,
        "ln1010A_s": 3.044,
    },
    "High-H0 vanilla test": {
        "H0": 73.0,
        "omega_cdm": 0.1200,
        "omega_b": 0.0224,
        "n_s": 0.970,
        "ln1010A_s": 3.044,
    },
    "Custom": None,
}

# DTI_ENABLE_GATE_NOTICE_INSERTED_FOR: Enable local-only vanilla CLASS live probe
_dti_enable_gate_notice_7abc_v1("7b vanilla-profile API check", "This prevents the probe RUN button from being mistaken for an active control while disabled.")
enable_live_vanilla_probe = st.checkbox(
    "Enable vanilla-profile API check",
    value=False,
    key="enable_live_vanilla_probe_v606_8d",
)

_dti_7b_endpoint_mode_notice_v1()

live_probe_url = st.text_input(
    "Vanilla-profile API endpoint",
    value=_dti_default_7b_live_endpoint_widget_only_v1(),
    key="live_vanilla_probe_url_v606_8d",
)
# DTI_RESTORE_7B_ENDPOINT_WIDGET_ONLY_NORMALIZE_AFTER_WIDGET
live_probe_url = _dti_normalize_7b_live_endpoint_widget_only_v1(live_probe_url)

# DTI_7B_PUBLIC_API_TRANSIENT_NOTICE_V1
st.info(
    "This API check is usually quick, but a public Render endpoint may take longer after cold start. "
    "This remains a bounded plumbing/profile-response check, not a likelihood or posterior calculation."
)


# DTI_7B_FRONTEND_CACHE_CONTROL_V2
use_7b_cache = st.checkbox(
    "Use one-hour frontend cache for identical vanilla-profile payload",
    value=True,
    key="dti_use_7b_frontend_cache_v2",
    help="Recommended for repeated identical checks. Cache key changes when endpoint or payload changes.",
)

selected_live_input_source_8b = st.selectbox(
    "Input source",
    list(_live_presets_8b.keys()),
    index=0,
    key="live_vanilla_input_source_v606_8d",
)

_selected_defaults_8b = _live_presets_8b.get(selected_live_input_source_8b)
if _selected_defaults_8b is None:
    _selected_defaults_8b = {
        "H0": st.session_state.get("live_vanilla_H0_v606_8d", _fallback_live_values_8b["H0"]),
        "omega_cdm": st.session_state.get("live_vanilla_omega_cdm_v606_8d", _fallback_live_values_8b["omega_cdm"]),
        "omega_b": st.session_state.get("live_vanilla_omega_b_v606_8d", _fallback_live_values_8b["omega_b"]),
        "n_s": st.session_state.get("live_vanilla_ns_v606_8d", _fallback_live_values_8b["n_s"]),
        "ln1010A_s": st.session_state.get("live_vanilla_ln1010As_v606_8d", _fallback_live_values_8b["ln1010A_s"]),
    }

_source_signature_8b = (
    selected_live_input_source_8b,
    _active_profile_name_8b,
    _selected_defaults_8b["H0"],
    _selected_defaults_8b["omega_cdm"],
    _selected_defaults_8b["omega_b"],
    _selected_defaults_8b["n_s"],
    _selected_defaults_8b["ln1010A_s"],
)

if st.session_state.get("live_vanilla_source_signature_v606_8d") != _source_signature_8b:
    st.session_state["live_vanilla_H0_v606_8d"] = float(_selected_defaults_8b["H0"])
    st.session_state["live_vanilla_omega_cdm_v606_8d"] = float(_selected_defaults_8b["omega_cdm"])
    st.session_state["live_vanilla_omega_b_v606_8d"] = float(_selected_defaults_8b["omega_b"])
    st.session_state["live_vanilla_ns_v606_8d"] = float(_selected_defaults_8b["n_s"])
    st.session_state["live_vanilla_ln1010As_v606_8d"] = float(_selected_defaults_8b["ln1010A_s"])
    st.session_state["live_vanilla_source_signature_v606_8d"] = _source_signature_8b

st.markdown("##### Current sidebar profile compatibility readout")

_compat_rows_8b = [
    {"field": "active_profile", "value": str(_active_profile_name_8b), "used_by_vanilla_probe": "context"},
    {"field": "H0", "value": _current_sidebar_values_8b["H0"], "used_by_vanilla_probe": "YES"},
    {"field": "omega_cdm", "value": _current_sidebar_values_8b["omega_cdm"], "used_by_vanilla_probe": "YES"},
    {"field": "omega_b", "value": _current_sidebar_values_8b["omega_b"], "used_by_vanilla_probe": "YES"},
    {"field": "n_s", "value": _current_sidebar_values_8b["n_s"], "used_by_vanilla_probe": "YES if present; fallback otherwise"},
    {"field": "ln1010A_s", "value": _current_sidebar_values_8b["ln1010A_s"], "used_by_vanilla_probe": "YES if present; fallback otherwise"},
    {"field": "f_EDE", "value": _current_sidebar_values_8b["f_EDE"], "used_by_vanilla_probe": "NO; vanilla CLASS probe ignores this"},
    {"field": "sigma8_reference", "value": _current_sidebar_values_8b["sigma8_reference"], "used_by_vanilla_probe": "NO; reference/display only"},
    {"field": "S8_reference", "value": _current_sidebar_values_8b["S8_reference"], "used_by_vanilla_probe": "NO; reference/display only"},
]
st.dataframe(_compat_rows_8b, width="stretch", hide_index=True)

col_live_1, col_live_2, col_live_3 = st.columns(3)

with col_live_1:
    live_H0 = st.number_input(
        "H0",
        min_value=40.0,
        max_value=100.0,
        step=0.1,
        key="live_vanilla_H0_v606_8d",
    )
    live_omega_b = st.number_input(
        "omega_b",
        min_value=0.005,
        max_value=0.080,
        step=0.0001,
        format="%.5f",
        key="live_vanilla_omega_b_v606_8d",
    )

with col_live_2:
    live_omega_cdm = st.number_input(
        "omega_cdm",
        min_value=0.010,
        max_value=0.300,
        step=0.001,
        format="%.5f",
        key="live_vanilla_omega_cdm_v606_8d",
    )
    live_ns = st.number_input(
        "n_s",
        min_value=0.80,
        max_value=1.20,
        step=0.0001,
        format="%.5f",
        key="live_vanilla_ns_v606_8d",
    )

with col_live_3:
    live_ln1010As = st.number_input(
        "ln(10^10 A_s)",
        min_value=1.0,
        max_value=5.0,
        step=0.001,
        format="%.5f",
        key="live_vanilla_ln1010As_v606_8d",
    )

live_payload = {
    "H0": float(live_H0),
    "omega_cdm": float(live_omega_cdm),
    "omega_b": float(live_omega_b),
    "n_s": float(live_ns),
    "ln1010A_s": float(live_ln1010As),
}

st.caption(
    "The JSON below is the actual payload sent to the configured vanilla-profile API endpoint. It should match the compatible current sidebar profile values unless Custom is selected."
)

st.json(live_payload)

import json as _json_section8b
import io as _io_section8b
import csv as _csv_section8b

_payload_json_8b = _json_section8b.dumps(live_payload, indent=2, sort_keys=True)
st.download_button(
    "Download live probe input JSON",
    data=_payload_json_8b,
    file_name="section8b_live_vanilla_input_payload.json",
    mime="application/json",
    key="download_section8b_live_payload_json_v606",
)

_payload_tsv_buf_8b = _io_section8b.StringIO()
_payload_tsv_writer_8b = _csv_section8b.writer(_payload_tsv_buf_8b, delimiter="\t")
_payload_tsv_writer_8b.writerow(["field", "value"])
for _k_8b, _v_8b in live_payload.items():
    _payload_tsv_writer_8b.writerow([_k_8b, _v_8b])

st.download_button(
    "Download live probe input TSV",
    data=_payload_tsv_buf_8b.getvalue(),
    file_name="section8b_live_vanilla_input_payload.tsv",
    mime="text/tab-separated-values",
    key="download_section8b_live_payload_tsv_v606",
)

if st.button(
    "Run vanilla-profile API check",
    key="run_live_vanilla_probe_v606_8d",
    width="stretch",
type="primary",
):
    # DTI_GUARD_7B_RUN_BUTTON_MULTILINE_SAFE_INSERTED
    _dti_7b_endpoint_for_guard_v1 = locals().get('local_endpoint', locals().get('live_probe_url', locals().get('endpoint', None)))
    if _dti_is_disabled_endpoint_for_7b_run_v1(_dti_7b_endpoint_for_guard_v1):
        _dti_7b_run_disabled_notice_v1()
    else:
        if not enable_live_vanilla_probe:
            st.warning("Enable the vanilla-profile API check before running.")
        else:
            try:
                import requests

                if _dti_is_disabled_endpoint_literal_v1(live_probe_url):
                    _dti_local_endpoint_disabled_notice_v1()
                    st.stop()
                cached_result_7b = _dti_post_json_endpoint_cached_or_uncached_v2(
                    live_probe_url,
                    live_payload,
                    240,
                    "7b_vanilla_profile_probe",
                    use_cache=use_7b_cache,
                )
                st.session_state["live_vanilla_probe_result_v606_8d"] = cached_result_7b["body"]
                st.session_state["live_vanilla_probe_http_status_v606_8d"] = cached_result_7b["status_code"]
                st.session_state["live_vanilla_probe_elapsed_sec_v606_8d"] = cached_result_7b["elapsed_sec"]
                st.session_state["live_vanilla_probe_cache_meta_v606_8d"] = cached_result_7b["cache"]

                data = cached_result_7b["body"]
                st.write(f"HTTP status: {cached_result_7b['status_code']}")
                st.caption(
                    "7b frontend cache: "
                    + str(cached_result_7b["cache"])
                    + " | elapsed_sec="
                    + str(cached_result_7b["elapsed_sec"])
                )

                st.markdown("##### Vanilla-profile API check result")
                st.json(data)

                if data.get("status") == "ok":
                    st.success("Local vanilla CLASS live probe returned status: ok")

                    derived = data.get("derived_parameters", {})
                    if isinstance(derived, dict) and derived:
                        rows = []
                        for key in [
                            "h",
                            "Omega0_m",
                            "Omega_Lambda",
                            "age",
                            "rs_drag",
                            "sigma8",
                            "S8",
                        ]:
                            if key in derived:
                                rows.append({"quantity": key, "value": derived[key]})
                        if rows:
                            st.table(rows)

                        result_json = _json_section8b.dumps(data, indent=2, sort_keys=True)
                        st.download_button(
                            "Download live probe result JSON",
                            data=result_json,
                            file_name="section8b_live_vanilla_result.json",
                            mime="application/json",
                            key="download_section8b_live_result_json_v606",
                        )

                        result_tsv_buf = _io_section8b.StringIO()
                        result_tsv_writer = _csv_section8b.writer(result_tsv_buf, delimiter="\t")
                        result_tsv_writer.writerow(["quantity", "value"])
                        for row in rows:
                            result_tsv_writer.writerow([row["quantity"], row["value"]])
                        st.download_button(
                            "Download live probe result TSV",
                            data=result_tsv_buf.getvalue(),
                            file_name="section8b_live_vanilla_result.tsv",
                            mime="text/tab-separated-values",
                            key="download_section8b_live_result_tsv_v606",
                        )

                    st.info(
                        "Interpretation boundary: derived-parameter probe only; f_EDE is not used by vanilla CLASS here; sigma8/S8 from the sidebar are reference values, not inputs; this is not likelihood, posterior, Planck validation, or manuscript values."
                    )
                else:
                    st.warning("Local vanilla CLASS live probe did not return ok. Check that the 8011 API is running.")

            except Exception as exc:
                # DTI_FIX_MSG_DIRECT_BEFORE_USE_V1
                msg = str(exc)
                if "DTI_LOCAL_8011_DISABLED" in msg or "No scheme supplied" in msg or "Invalid URL" in msg:
                    _dti_local_endpoint_disabled_notice_v1()
                else:
                    _dti_show_local_probe_error_v3_safe(exc)


# ---------------------------------------------------------------------
# Section 7c: Continuity / discontinuity examiner
# ---------------------------------------------------------------------
st.divider()


# dti_graph_ui_v607_fallback_v2
# dti_graph_ui_v607_stable_dom_container_patch
# These marker comments identify the local graph UI fallback and stable-DOM repair lane.
# They are audit markers only; they do not change physics values or solver behavior.

# --- dti_graph_ui_v607_audit_visualizations: local-only audit visualization helpers ---
# dti_graph_ui_stable_container_dom_repair_v1: graph UI expanders converted to stable containers where possible.
def _dti_graph_ui_v607_available_frames():
    """Collect dataframe-like objects already present in Streamlit session/global scope.

    This helper is deliberately conservative:
    - It does not run likelihoods.
    - It does not call CLASS.
    - It does not invent data.
    - It only visualizes tables already present in memory/session state.
    """
    try:
        import pandas as _pd_graph_v607
        import streamlit as _st_graph_v607
    except Exception:
        return []

    frames = []

    def _add_frame(name, obj):
        try:
            if isinstance(obj, _pd_graph_v607.DataFrame) and len(obj) > 0:
                frames.append((name, obj.copy()))
            elif isinstance(obj, list) and obj and isinstance(obj[0], dict):
                df = _pd_graph_v607.DataFrame(obj)
                if len(df) > 0:
                    frames.append((name, df))
            elif isinstance(obj, dict):
                for kk, vv in obj.items():
                    if isinstance(vv, _pd_graph_v607.DataFrame) and len(vv) > 0:
                        frames.append((f"{name}.{kk}", vv.copy()))
                    elif isinstance(vv, list) and vv and isinstance(vv[0], dict):
                        df = _pd_graph_v607.DataFrame(vv)
                        if len(df) > 0:
                            frames.append((f"{name}.{kk}", df))
        except Exception:
            return

    try:
        for key in list(_st_graph_v607.session_state.keys()):
            _add_frame(f"session_state.{key}", _st_graph_v607.session_state.get(key))
    except Exception:
        pass

    try:
        for key, val in list(globals().items()):
            if key.startswith("_"):
                continue
            _add_frame(f"global.{key}", val)
    except Exception:
        pass

    dedup = []
    seen = set()
    for name, df in frames:
        sig = (name, tuple(str(c) for c in df.columns), len(df))
        if sig not in seen:
            seen.add(sig)
            dedup.append((name, df))
    return dedup


def _dti_graph_ui_v607_find_numeric_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    lower = {str(c).lower(): c for c in df.columns}
    for c in candidates:
        if c.lower() in lower:
            return lower[c.lower()]
    return None


def _dti_graph_ui_v607_find_frame(required_any=None, required_all=None):
    required_any = required_any or []
    required_all = required_all or []
    frames = _dti_graph_ui_v607_available_frames()
    for name, df in frames:
        cols = {str(c).lower(): c for c in df.columns}
        all_ok = True
        for c in required_all:
            if c.lower() not in cols:
                all_ok = False
                break
        if not all_ok:
            continue
        any_ok = True
        if required_any:
            any_ok = any(c.lower() in cols for c in required_any)
        if any_ok:
            return name, df
    return None, None


def _dti_graph_ui_v607_boundary_notice(section_label):
    import streamlit as st
    st.caption(
        f"{section_label} visualization boundary: audit visualization only; "
        "not a likelihood result, not a posterior comparison, not model validation, "
        "not a formal exclusion rule, not Planck validation, and not a physical-discontinuity proof."
    )


# --- dti_graph_ui_v607_always_visible_fallback_v2 ---
def _dti_graph_ui_v607_fallback_notice(label):
    import streamlit as st
    st.caption(
        f"{label}: graph output is intentionally unavailable until source-of-record data are present. "
        "This is for readability and layout inspection only; it is not solver output, "
        "not a physics-value update, not a likelihood result, not a posterior comparison, "
        "and not Planck validation."
    )


def _dti_graph_ui_v607_fallback_sweep_frame():
    import pandas as pd
    return pd.DataFrame([
        {"sweep_value": 0.105, "S8": 0.805, "sigma8": 0.790, "rs_drag": 147.2, "label": "reference-low"},
        {"sweep_value": 0.112, "S8": 0.820, "sigma8": 0.805, "rs_drag": 146.5, "label": "reference-mid"},
        {"sweep_value": 0.119, "S8": 0.842, "sigma8": 0.827, "rs_drag": 145.7, "label": "reference-high"},
        {"sweep_value": 0.126, "S8": 0.858, "sigma8": 0.844, "rs_drag": 144.8, "label": "reference-extreme"},
    ])


def _dti_graph_ui_v607_fallback_distance_frame():
    import pandas as pd
    return pd.DataFrame([
        {"profile": "LCDM-like reference", "distance": 0.18},
        {"profile": "FUJIKI DTI working reference", "distance": 0.04},
        {"profile": "stress-test profile", "distance": 0.31},
    ])


def _dti_graph_ui_v607_altair_line_with_band(data, xcol, ycol):
    import altair as alt
    base = alt.Chart(data).mark_circle(size=60, opacity=0.7).encode(
        x=alt.X(f"{xcol}:Q", title=xcol),
        y=alt.Y(f"{ycol}:Q", title=ycol),
        tooltip=list(data.columns),
    )
    return base


def _dti_graph_ui_v607_altair_scatter(data, xcol, ycol):
    import altair as alt
    return alt.Chart(data).mark_circle(size=90).encode(
        x=alt.X(f"{xcol}:Q", title=xcol),
        y=alt.Y(f"{ycol}:Q", title=ycol),
        tooltip=list(data.columns),
    )


def _dti_render_section7c_visuals_v607():
    """Section 7c: adjacent response-difference profile."""
    import streamlit as st

    marker = "dti_graph_ui_v607_section7c"
    st.markdown(f"<a id='{marker}'></a>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("##### Audit visualization: numerical smoothness profile")
        _dti_graph_ui_v607_boundary_notice("Section 7c")

        try:
            import pandas as pd
            import altair as alt
        except Exception as exc:
            st.info(f"Graph libraries unavailable: {exc}")
            return

        name, df = _dti_graph_ui_v607_find_frame(
            required_any=["sweep_value", "threshold", "step", "x", "H0", "omega_cdm", "omega_cdm_input"],
            required_all=[],
        )

        if df is None:
            st.info("No compatible sweep table is currently available in session memory. No graph is drawn until source-of-record data are present.")
            _dti_graph_ui_v607_fallback_notice("Section 7c fallback")
            df = _dti_graph_ui_v607_fallback_sweep_frame()
            _DTI_DISABLED_GRAPH_CALL(_dti_graph_ui_v607_altair_line_with_band(df, "sweep_value", "sigma8").properties(height=260), use_container_width=True, key="dti_graph_ui_dom_stable_chart_01")
            st.info(
                "No sweep table is currently available in session memory. "
                "Run or load a sweep/examiner table to draw adjacent response-difference profiles."
            )
            return

        xcol = _dti_graph_ui_v607_find_numeric_col(
            df, ["sweep_value", "threshold", "step", "x", "H0", "omega_cdm", "omega_cdm_input", "fde", "f_EDE"]
        )

        y_candidates = [
            "S8", "s8", "sigma8", "sigma_8", "rs_drag", "theta_s_100", "H0", "omega_cdm", "omega_b"
        ]
        ycols = [c for c in y_candidates if c in df.columns]

        if xcol is None or not ycols:
            st.info(
                f"Found table `{name}`, but it does not contain a recognized sweep axis and response column. "
                "Expected examples: sweep_value with S8/sigma8/rs_drag."
            )
            st.dataframe(df.head(30), use_container_width=True)
            return

        work = df[[xcol] + ycols].copy()
        for c in [xcol] + ycols:
            work[c] = pd.to_numeric(work[c], errors="coerce")
        work = work.dropna(subset=[xcol]).sort_values(xcol)

        rows = []
        for y in ycols:
            tmp = work[[xcol, y]].dropna().copy()
            if len(tmp) >= 2:
                tmp["adjacent_abs_delta"] = tmp[y].diff().abs()
                tmp["quantity"] = y
                tmp = tmp.dropna(subset=["adjacent_abs_delta"])
                rows.append(tmp[[xcol, "quantity", "adjacent_abs_delta"]])

        if not rows:
            st.info("Not enough numeric rows to draw adjacent-difference profile.")
            st.dataframe(work.head(30), use_container_width=True)
            return

        plot_df = pd.concat(rows, ignore_index=True)

        chart = (
            alt.Chart(plot_df)
            .mark_circle(size=60, opacity=0.7)
            .encode(
                x=alt.X(f"{xcol}:Q", title=str(xcol)),
                y=alt.Y("adjacent_abs_delta:Q", title="adjacent absolute difference"),
                color=alt.Color("quantity:N", title="quantity"),
                tooltip=[str(xcol), "quantity", "adjacent_abs_delta"],
            )
            .properties(height=280)
        )
        _DTI_DISABLED_GRAPH_CALL(chart, use_container_width=True, key="dti_graph_ui_dom_stable_chart_02")
        st.caption(
            "Scatter distributions and vertical outliers indicate numerical non-smoothness candidates within the available diagnostic table. "
            "This is not evidence establishing physical discontinuity."
        )


def _dti_render_section8_visuals_v607():
    """Section 8: reference-distance bars, Boundary table, rs_drag-S8 trade-off."""
    import streamlit as st

    st.markdown("<a id='dti_graph_ui_v607_section8'></a>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("##### Audit visualization: heuristic reference-region profile")
        _dti_graph_ui_v607_boundary_notice("Section 8")

        try:
            import pandas as pd
            import altair as alt
        except Exception as exc:
            st.info(f"Graph libraries unavailable: {exc}")
            return

        frames = _dti_graph_ui_v607_available_frames()

        # A. Reference-distance bar chart
        st.markdown("##### Reference-distance overview")
        distance_frame = None
        distance_name = None
        for name, df in frames:
            cols_lower = {str(c).lower(): c for c in df.columns}
            label_col = None
            for c in ["model_id", "profile_id", "name", "label", "reference", "preset"]:
                if c in cols_lower:
                    label_col = cols_lower[c]
                    break
            score_col = None
            for c in ["heuristic_triage_score", "triage_score", "distance", "reference_distance", "weighted_distance", "score"]:
                if c in cols_lower:
                    score_col = cols_lower[c]
                    break
            if label_col is not None and score_col is not None:
                distance_frame = df[[label_col, score_col]].copy()
                distance_name = name
                break

        if distance_frame is not None:
            label_col, score_col = list(distance_frame.columns)
            distance_frame[score_col] = pd.to_numeric(distance_frame[score_col], errors="coerce")
            distance_frame = distance_frame.dropna(subset=[score_col]).sort_values(score_col).head(20)
            chart = (
                alt.Chart(distance_frame)
                .mark_bar()
                .encode(
                    x=alt.X(f"{score_col}:Q", title="heuristic distance / score"),
                    y=alt.Y(f"{label_col}:N", sort="-x", title="registered reference"),
                    tooltip=[str(label_col), str(score_col)],
                )
                .properties(height=max(180, min(520, 24 * len(distance_frame) + 40)))
            )
            _DTI_DISABLED_GRAPH_CALL(chart, use_container_width=True, key="dti_graph_ui_dom_stable_chart_03")
            st.caption(
                f"Source table: `{distance_name}`. Smaller values indicate closer proximity in the registered "
                "parameter-profile space. This is heuristic triage only."
            )
        else:
            st.info("No compatible reference-distance table found in session memory. No graph is drawn until source-of-record data are present.")
            _dti_graph_ui_v607_fallback_notice("Section 8 distance fallback")
            distance_frame = _dti_graph_ui_v607_fallback_distance_frame()
            dist_chart = alt.Chart(distance_frame).mark_bar().encode(
                x=alt.X("distance:Q", title="heuristic reference distance"),
                y=alt.Y("profile:N", sort="-x", title="profile"),
                tooltip=list(distance_frame.columns),
            )
            _DTI_DISABLED_GRAPH_CALL(dist_chart.properties(height=220), use_container_width=True, key="dti_graph_ui_dom_stable_chart_04")
            st.info(
                "No reference-distance table found in session memory. "
                "If a table with model/profile labels and a distance or triage score is available, a bar chart will appear here."
            )

        # B. S8 stress line
        st.markdown("##### S8 response / stress view")
        name_s8, df_s8 = _dti_graph_ui_v607_find_frame(
            required_any=["S8", "s8"],
            required_all=[],
        )
        if df_s8 is not None:
            xcol = _dti_graph_ui_v607_find_numeric_col(
                df_s8, ["sweep_value", "H0", "omega_cdm", "omega_cdm_input", "fde", "f_EDE", "threshold", "step"]
            )
            ycol = _dti_graph_ui_v607_find_numeric_col(df_s8, ["S8", "s8"])
            if xcol is not None and ycol is not None:
                work = df_s8[[xcol, ycol]].copy()
                work[xcol] = pd.to_numeric(work[xcol], errors="coerce")
                work[ycol] = pd.to_numeric(work[ycol], errors="coerce")
                work = work.dropna().sort_values(xcol)
                if len(work) >= 2:
                    band = pd.DataFrame({
                        "ymin": [0.75],
                        "ymax": [0.79],
                        "label": ["S8 reference band disabled until source-of-record data are present"],
                    })
                    base = alt.Chart(work).mark_circle(size=60, opacity=0.7).encode(
                        x=alt.X(f"{xcol}:Q", title=str(xcol)),
                        y=alt.Y(f"{ycol}:Q", title="S8"),
                        tooltip=[str(xcol), str(ycol)],
                    )
                    band_chart = alt.Chart(band).mark_rect(opacity=0.18).encode(
                        y="ymin:Q",
                        y2="ymax:Q",
                    )
                    _DTI_DISABLED_GRAPH_CALL((band_chart + base).properties(height=280), use_container_width=True, key="dti_graph_ui_dom_stable_chart_05")
                    st.caption(
                        "The S8 band display is disabled until source-of-record data are present. "
                        "Crossing it is a diagnostic stress indicator only; it is not a likelihood-based exclusion."
                    )
                else:
                    st.info("S8 table found, but fewer than two numeric rows are available for plotting.")
            else:
                st.info("S8 table found, but no recognized sweep axis was found.")
        else:
            st.info("No compatible S8 response table found in session memory. No graph is drawn until source-of-record data are present.")
            _dti_graph_ui_v607_fallback_notice("Section 8 S8 fallback")
            fallback_s8 = _dti_graph_ui_v607_fallback_sweep_frame()
            chart_s8 = _dti_graph_ui_v607_altair_line_with_band(fallback_s8, "sweep_value", "S8")
            _DTI_DISABLED_GRAPH_CALL(chart_s8.properties(height=280), use_container_width=True, key="dti_graph_ui_dom_stable_chart_06")

        # C. Boundary confirmation scatter
        st.markdown("##### Boundary confirmation view")
        name_trade, df_trade = _dti_graph_ui_v607_find_frame(
            required_any=[],
            required_all=["rs_drag", "S8"],
        )
        if df_trade is None:
            name_trade, df_trade = _dti_graph_ui_v607_find_frame(
                required_any=[],
                required_all=["rs_drag", "s8"],
            )

        if df_trade is not None:
            rs_col = _dti_graph_ui_v607_find_numeric_col(df_trade, ["rs_drag"])
            s8_col = _dti_graph_ui_v607_find_numeric_col(df_trade, ["S8", "s8"])
            color_col = None
            for c in ["model_id", "profile_id", "label", "name", "H0", "f_EDE", "fde"]:
                if c in df_trade.columns:
                    color_col = c
                    break

            work = df_trade[[rs_col, s8_col] + ([color_col] if color_col else [])].copy()
            work[rs_col] = pd.to_numeric(work[rs_col], errors="coerce")
            work[s8_col] = pd.to_numeric(work[s8_col], errors="coerce")
            work = work.dropna(subset=[rs_col, s8_col])

            if len(work) >= 1:
                chart = alt.Chart(work).mark_circle(size=70).encode(
                    x=alt.X(f"{rs_col}:Q", title="rs_drag"),
                    y=alt.Y(f"{s8_col}:Q", title="S8"),
                    tooltip=list(work.columns),
                )
                if color_col is not None:
                    chart = chart.encode(color=alt.Color(f"{color_col}:N", title=str(color_col)))

                vline = alt.Chart(pd.DataFrame({"x": [147.0]})).mark_rule(strokeDash=[4, 4]).encode(x="x:Q")
                hband = alt.Chart(pd.DataFrame({"ymin": [0.75], "ymax": [0.79]})).mark_rect(opacity=0.12).encode(
                    y="ymin:Q", y2="ymax:Q"
                )
                _DTI_DISABLED_GRAPH_CALL((hband + vline + chart).properties(height=300), use_container_width=True, key="dti_graph_ui_dom_stable_chart_07")
                st.caption(
                    "This scatter visualizes a heuristic early-scale / late-clustering trade-off. "
                    "The reference line and band are visual guides only, not a formal exclusion rule regions."
                )
            else:
                st.info("rs_drag/S8 table found, but no numeric rows are available.")
        else:
            st.info("No rs_drag + S8 table found in session memory.")


def _dti_render_section9_visuals_v607():
    """Section 9: sandbox flow diagram."""
    import streamlit as st

    st.markdown("<a id='dti_graph_ui_v607_section9'></a>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("##### Audit visualization: external API sandbox flow")
        _dti_graph_ui_v607_boundary_notice("Section 9")
        st.markdown(
            """
            ```text
            Input parameter profile
                    ↓
            External CLASS API sandbox
                    ↓
            Exploratory derived output
                    ↓
            Not likelihood / not posterior / not Planck validation / not canonical validation
            ```
            """
        )
        st.caption(
            "This diagram clarifies the role of the external API sandbox. "
            "It is a workflow boundary visualization, not a physics result."
        )
# --- end dti_graph_ui_v607_audit_visualizations ---

st.header("7c. Continuity / discontinuity examiner")

# DTI_HIDE_7C_OBSOLETE_VISUAL_FALLBACK_BLOCK_V2
# Hidden: obsolete 7c visual/fallback block in this no-graph local UI line.
# This does not reopen graph rendering or realtime 8011.

st.markdown(
    """
**Purpose.** This local-only examiner tests whether small changes along a selected parameter path produce smooth or non-smooth changes in local vanilla CLASS derived quantities.

It is an **examiner panel**, not a physics-claim engine.

**What this can decide.**

- Whether the tested numerical response is smooth within the chosen grid and tolerance.
- Whether a jump-like candidate appears in the tested derived quantities.
- Whether the result is inconclusive because the grid, endpoint, or solver failed.

**What this cannot decide.**

- It is not evidence establishing physical discontinuity.
- It is not evidence establishing an operator-phase transition.
- It does not compute likelihood, posterior, evidence, MCMC, or Planck validation.
- It does not update manuscript or canonical physics values.

**Local-only endpoint.** This section uses the local vanilla CLASS endpoint, normally:

`8011_REALTIME_DISABLED`
    """
)

# DTI_ENABLE_GATE_NOTICE_INSERTED_FOR: Enable local-only continuity / discontinuity examiner
_dti_enable_gate_notice_7abc_v1("7c continuity / discontinuity examiner", "This prevents the continuity examiner RUN control from being used without enabling the local-only gate.")
enable_continuity_examiner = st.checkbox(
    "Enable local-only continuity / discontinuity examiner",
    value=False,
    key="enable_section7c_continuity_examiner_v606",
)

# DTI_HIDE_7C_BLANK_ENDPOINT_INPUT_V1
# The endpoint text box was visually blank/confusing in Section 7c.
# Keep the examiner local-readonly and do not reopen 8011 realtime.
continuity_endpoint = "DTI_LOCAL_8011_DISABLED"
st.markdown("##### Base profile")

_base_profile_7c = {
    "H0": float(st.session_state.get("live_vanilla_H0_v606_8d", 72.9)),
    "omega_cdm": float(st.session_state.get("live_vanilla_omega_cdm_v606_8d", 0.127)),
    "omega_b": float(st.session_state.get("live_vanilla_omega_b_v606_8d", 0.0244)),
    "n_s": float(st.session_state.get("live_vanilla_ns_v606_8d", 0.9847)),
    "ln1010A_s": float(st.session_state.get("live_vanilla_ln1010As_v606_8d", 3.058)),
}

st.caption(
    "The base values are taken from Section 7b when available. They can be edited below for this examiner run only."
)

col7c_base_1, col7c_base_2, col7c_base_3 = st.columns(3)

with col7c_base_1:
    c7c_base_H0 = st.number_input(
        "7c base H0",
        min_value=40.0,
        max_value=100.0,
        value=_base_profile_7c["H0"],
        step=0.1,
        key="section7c_base_H0_v606",
    )
    c7c_base_omega_b = st.number_input(
        "7c base omega_b",
        min_value=0.005,
        max_value=0.080,
        value=_base_profile_7c["omega_b"],
        step=0.0001,
        format="%.5f",
        key="section7c_base_omega_b_v606",
    )

with col7c_base_2:
    c7c_base_omega_cdm = st.number_input(
        "7c base omega_cdm",
        min_value=0.010,
        max_value=0.300,
        value=_base_profile_7c["omega_cdm"],
        step=0.001,
        format="%.5f",
        key="section7c_base_omega_cdm_v606",
    )
    c7c_base_ns = st.number_input(
        "7c base n_s",
        min_value=0.80,
        max_value=1.20,
        value=_base_profile_7c["n_s"],
        step=0.0001,
        format="%.5f",
        key="section7c_base_ns_v606",
    )

with col7c_base_3:
    c7c_base_ln1010As = st.number_input(
        "7c base ln(10^10 A_s)",
        min_value=1.0,
        max_value=5.0,
        value=_base_profile_7c["ln1010A_s"],
        step=0.001,
        format="%.5f",
        key="section7c_base_ln1010As_v606",
    )

_base_payload_7c = {
    "H0": float(c7c_base_H0),
    "omega_cdm": float(c7c_base_omega_cdm),
    "omega_b": float(c7c_base_omega_b),
    "n_s": float(c7c_base_ns),
    "ln1010A_s": float(c7c_base_ln1010As),
}

st.markdown("##### Sweep design")

col7c_sweep_1, col7c_sweep_2, col7c_sweep_3 = st.columns(3)

with col7c_sweep_1:
    sweep_param_7c = st.selectbox(
        "Parameter to vary",
        ["H0", "omega_cdm", "omega_b", "n_s", "ln1010A_s"],
        index=0,
        key="section7c_sweep_param_v606",
    )
    grid_n_7c = st.number_input(
        "Grid points",
        min_value=3,
        max_value=31,
        value=9,
        step=2,
        key="section7c_grid_n_v606",
    )

with col7c_sweep_2:
    default_center_7c = float(_base_payload_7c[sweep_param_7c])
    default_span_7c = {
        "H0": 1.0,
        "omega_cdm": 0.004,
        "omega_b": 0.001,
        "n_s": 0.01,
        "ln1010A_s": 0.03,
    }.get(sweep_param_7c, 1.0)

    sweep_start_7c = st.number_input(
        "Sweep start",
        value=float(default_center_7c - default_span_7c),
        step=float(default_span_7c / 10.0),
        format="%.6f",
        key="section7c_sweep_start_v606",
    )
    sweep_end_7c = st.number_input(
        "Sweep end",
        value=float(default_center_7c + default_span_7c),
        step=float(default_span_7c / 10.0),
        format="%.6f",
        key="section7c_sweep_end_v606",
    )

with col7c_sweep_3:
    jump_threshold_7c = st.number_input(
        "Relative jump threshold",
        min_value=0.001,
        max_value=20.0,
        value=5.0,
        step=0.1,
        format="%.4f",
        key="section7c_jump_threshold_v606",
    )
    repeat_count_7c = st.number_input(
        "Repeat count per grid point",
        min_value=1,
        max_value=5,
        value=1,
        step=1,
        key="section7c_repeat_count_v606",
    )

st.caption(
    "Relative jump score is a simple local diagnostic: max adjacent finite-difference jump divided by median adjacent finite-difference scale. The default threshold is 5.0 to avoid classifying ordinary smooth finite-difference variation as a jump. It is not a physical-discontinuity proof."
)

st.json(
    {
        "base_payload": _base_payload_7c,
        "sweep": {
            "parameter": sweep_param_7c,
            "start": float(sweep_start_7c),
            "end": float(sweep_end_7c),
            "grid_points": int(grid_n_7c),
            "repeat_count": int(repeat_count_7c),
            "relative_jump_threshold": float(jump_threshold_7c),
        },
        "boundary": {
            "local_only": True,
            "experimental": True,
            "non_canonical": True,
            "likelihood_evaluation": False,
            "posterior_comparison": False,
            "planck_validation": False,
            "physical_discontinuity_proof": False,
        },
    }
)

def _section7c_median(values):
    vals = sorted([float(v) for v in values if v is not None])
    if not vals:
        return None
    n = len(vals)
    if n % 2:
        return vals[n // 2]
    return 0.5 * (vals[n // 2 - 1] + vals[n // 2])

def _section7c_grid(start, end, n):
    n = int(n)
    if n <= 1:
        return [float(start)]
    return [float(start) + (float(end) - float(start)) * i / (n - 1) for i in range(n)]

def _section7c_jump_scores(rows, quantity):
    micro_jitter_abs_delta_threshold_7c = 1.0e-5
    micro_jitter_quantities_7c = {"rs_drag"}

    good = []
    for row in rows:
        val = row.get(quantity)
        x = row.get("sweep_value")
        status = row.get("status")
        if status == "ok" and val is not None and x is not None:
            good.append((float(x), float(val)))
    good.sort()
    if len(good) < 3:
        return {
            "quantity": quantity,
            "n_good": len(good),
            "max_abs_step": None,
            "median_abs_step": None,
            "relative_jump_score": None,
            "micro_jitter_abs_delta_threshold": (
                micro_jitter_abs_delta_threshold_7c
                if quantity in micro_jitter_quantities_7c
                else None
            ),
            "micro_jitter_guard_applied": False,
            "verdict": "insufficient_resolution",
        }

    diffs = []
    for (_, y0), (_, y1) in zip(good[:-1], good[1:]):
        diffs.append(abs(y1 - y0))

    med = _section7c_median(diffs)
    max_step = max(diffs) if diffs else None

    if med is None or med == 0:
        rel = None if max_step is None else float("inf")
    else:
        rel = max_step / med

    micro_jitter_guard_applied = False
    if rel is None:
        verdict = "inconclusive"
    elif rel > float(jump_threshold_7c):
        if (
            quantity in micro_jitter_quantities_7c
            and max_step is not None
            and max_step < micro_jitter_abs_delta_threshold_7c
        ):
            verdict = "micro_jitter_not_jump"
            micro_jitter_guard_applied = True
        else:
            verdict = "jump_candidate"
    else:
        verdict = "continuous_response"

    return {
        "quantity": quantity,
        "n_good": len(good),
        "max_abs_step": max_step,
        "median_abs_step": med,
        "relative_jump_score": rel,
        "micro_jitter_abs_delta_threshold": (
            micro_jitter_abs_delta_threshold_7c
            if quantity in micro_jitter_quantities_7c
            else None
        ),
        "micro_jitter_guard_applied": micro_jitter_guard_applied,
        "verdict": verdict,
    }


if st.button(
    "Run continuity / discontinuity examiner",
    key="run_section7c_continuity_examiner_v606",
    width="stretch",
type="primary",
):
    if not enable_continuity_examiner:
        st.warning("Enable the local-only continuity / discontinuity examiner before running.")
    else:
        try:
            import requests
            import json as _json_section7c
            import io as _io_section7c
            import csv as _csv_section7c

            grid_values_7c = _section7c_grid(sweep_start_7c, sweep_end_7c, int(grid_n_7c))
            result_rows_7c = []
            raw_responses_7c = []

            with st.spinner("Running local continuity / discontinuity examiner..."):
                for sweep_value in grid_values_7c:
                    repeated_derived = []
                    repeated_status = []
                    repeated_error = []

                    for rep in range(int(repeat_count_7c)):
                        payload = dict(_base_payload_7c)
                        payload[sweep_param_7c] = float(sweep_value)

                        try:
                            response = requests.post(
                                continuity_endpoint,
                                json=payload,
                                timeout=240,
                            )
                            try:
                                data = response.json()
                            except Exception:
                                data = {
                                    "status": "error",
                                    "detail": response.text,
                                }

                            raw_responses_7c.append(
                                {
                                    "sweep_value": float(sweep_value),
                                    "repeat": rep,
                                    "http_status": response.status_code,
                                    "payload": payload,
                                    "response": data,
                                }
                            )

                            if response.status_code == 200 and data.get("status") == "ok":
                                repeated_status.append("ok")
                                repeated_derived.append(data.get("derived_parameters", {}))
                            else:
                                repeated_status.append("error")
                                repeated_error.append(str(data.get("detail", data))[:300])

                        except Exception as exc:
                            repeated_status.append("error")
                            repeated_error.append(str(exc)[:300])
                            raw_responses_7c.append(
                                {
                                    "sweep_value": float(sweep_value),
                                    "repeat": rep,
                                    "http_status": None,
                                    "payload": payload,
                                    "response": {
                                        "status": "error",
                                        "detail": str(exc),
                                    },
                                }
                            )

                    row = {
                        "sweep_parameter": sweep_param_7c,
                        "sweep_value": float(sweep_value),
                        "status": "ok" if repeated_status and all(x == "ok" for x in repeated_status) else "error",
                        "repeat_count": int(repeat_count_7c),
                        "error": "; ".join(repeated_error[:2]),
                    }

                    quantities = [
                        "h",
                        "Omega0_m",
                        "Omega_Lambda",
                        "age",
                        "rs_drag",
                        "sigma8",
                        "S8",
                    ]

                    for q in quantities:
                        vals = []
                        for derived in repeated_derived:
                            if isinstance(derived, dict) and q in derived:
                                vals.append(float(derived[q]))
                        row[q] = _section7c_median(vals) if vals else None

                    result_rows_7c.append(row)

            st.markdown("##### Examiner grid output")
            st.dataframe(result_rows_7c, width="stretch", hide_index=True)

            score_rows_7c = []
            for q in [
                "h",
                "Omega0_m",
                "Omega_Lambda",
                "age",
                "rs_drag",
                "sigma8",
                "S8",
            ]:
                score_rows_7c.append(_section7c_jump_scores(result_rows_7c, q))

            st.markdown("##### Continuity / discontinuity score table")
            st.dataframe(score_rows_7c, width="stretch", hide_index=True)

            any_solver_failure = any(row.get("status") != "ok" for row in result_rows_7c)
            jump_candidates = [
                row for row in score_rows_7c if row.get("verdict") == "jump_candidate"
            ]
            micro_jitter_rows = [
                row for row in score_rows_7c if row.get("verdict") == "micro_jitter_not_jump"
            ]

            if any_solver_failure:
                overall_verdict_7c = "solver_failure_or_partial_grid"
                st.warning("Overall bounded verdict: solver_failure_or_partial_grid")
            elif jump_candidates:
                overall_verdict_7c = "jump_candidate"
                st.warning("Overall bounded verdict: jump_candidate")
            elif micro_jitter_rows:
                overall_verdict_7c = "continuous_response_within_tested_grid_after_micro_jitter_guard"
                st.success("Overall bounded verdict: continuous_response_within_tested_grid_after_micro_jitter_guard")
            else:
                overall_verdict_7c = "continuous_response_within_tested_grid"
                st.success("Overall bounded verdict: continuous_response_within_tested_grid")

            examiner_record_7c = {
                "status": "ok",
                "examiner": "7c. Continuity / discontinuity examiner",
                "overall_bounded_verdict": overall_verdict_7c,
                "base_payload": _base_payload_7c,
                "sweep": {
                    "parameter": sweep_param_7c,
                    "start": float(sweep_start_7c),
                    "end": float(sweep_end_7c),
                    "grid_points": int(grid_n_7c),
                    "repeat_count": int(repeat_count_7c),
                    "relative_jump_threshold": float(jump_threshold_7c),
                    "micro_jitter_abs_delta_threshold": 1.0e-5,
                    "micro_jitter_guard_quantities": ["rs_drag"],
                },
                "retained_jump_candidate_count": len(jump_candidates),
                "micro_jitter_not_jump_count": len(micro_jitter_rows),
                "scores": score_rows_7c,
                "boundary": {
                    "local_only": True,
                    "experimental": True,
                    "non_canonical": True,
                    "likelihood_evaluation": False,
                    "posterior_comparison": False,
                    "planck_validation": False,
                    "physical_discontinuity_proof": False,
                },
                "interpretation_warning": "This examiner identifies numerical/statistical continuity-failure candidates only. It is not evidence establishing physical discontinuity, operator-phase transition, likelihood preference, posterior preference, or Planck validation.",
            }

            st.markdown("##### Examiner verdict record")
            st.json(examiner_record_7c)

            grid_tsv_buf_7c = _io_section7c.StringIO()
            grid_fields_7c = list(result_rows_7c[0].keys()) if result_rows_7c else []
            writer_7c = _csv_section7c.DictWriter(
                grid_tsv_buf_7c,
                fieldnames=grid_fields_7c,
                delimiter="\t",
            )
            writer_7c.writeheader()
            for row in result_rows_7c:
                writer_7c.writerow(row)

            score_tsv_buf_7c = _io_section7c.StringIO()
            score_fields_7c = list(score_rows_7c[0].keys()) if score_rows_7c else []
            score_writer_7c = _csv_section7c.DictWriter(
                score_tsv_buf_7c,
                fieldnames=score_fields_7c,
                delimiter="\t",
            )
            score_writer_7c.writeheader()
            for row in score_rows_7c:
                score_writer_7c.writerow(row)

            st.download_button(
                "Download 7c grid output TSV",
                data=grid_tsv_buf_7c.getvalue(),
                file_name="section7c_continuity_grid_output.tsv",
                mime="text/tab-separated-values",
                key="download_section7c_grid_output_tsv_v606",
            )

            st.download_button(
                "Download 7c jump scores TSV",
                data=score_tsv_buf_7c.getvalue(),
                file_name="section7c_continuity_jump_scores.tsv",
                mime="text/tab-separated-values",
                key="download_section7c_jump_scores_tsv_v606",
            )

            st.download_button(
                "Download 7c examiner verdict JSON",
                data=_json_section7c.dumps(examiner_record_7c, indent=2, sort_keys=True),
                file_name="section7c_continuity_examiner_verdict.json",
                mime="application/json",
                key="download_section7c_examiner_verdict_json_v606",
            )

            st.download_button(
                "Download 7c raw response JSON",
                data=_json_section7c.dumps(raw_responses_7c, indent=2, sort_keys=True),
                file_name="section7c_continuity_raw_responses.json",
                mime="application/json",
                key="download_section7c_raw_responses_json_v606",
            )

            st.info(
                "Interpretation boundary: this is a local numerical examiner only. A jump_candidate is not a physical-discontinuity proof."
            )

        except Exception as exc:
            st.error(f"Continuity / discontinuity examiner failed: {exc}")


st.header("8. Candidate payload / boundary confirmation")


# --- dti_graph_ui_v607_section8_visible_fallback_deck_v3 ---
try:
    import altair as _alt_graph_v3
    _fallback_v3 = _dti_graph_ui_v607_fallback_sweep_frame()
    _dti_graph_ui_v607_fallback_notice("Section 8 disabled visual material")
    _dti_boundary_readonly_caption_v1()
    # DTI_SECTION8_REMOVE_INEFFECTIVE_BOUNDARY_TABS_INDENT_SAFE_V2
    _dti_boundary_readonly_caption_v1()
    _tab_s8_v3 = _dti_noop_context_v1()
    _tab_trade_v3 = _dti_noop_context_v1()
    with _tab_s8_v3:
        _DTI_DISABLED_GRAPH_CALL(
            _dti_graph_ui_v607_altair_line_with_band(_fallback_v3, "sweep_value", "S8").properties(height=280),
            use_container_width=True,
        )
    with _tab_trade_v3:
        _DTI_DISABLED_GRAPH_CALL(
            _dti_graph_ui_v607_altair_scatter(_fallback_v3, "rs_drag", "S8").properties(height=280),
            use_container_width=True,
        )
except Exception as _graph_v3_exc:
    st.info(f"Section 8 graph fallback unavailable: {_graph_v3_exc}")

try:
    _dti_render_section8_visuals_v607()
except Exception as _dti_graph_exc_8_v607:
    st.caption(f"Section 8 audit visualization unavailable: {_dti_graph_exc_8_v607}")

st.markdown("""
<div class="boundary-card">
<b>Important:</b> this section is a heuristic reference-region profile, not a Planck likelihood evaluation.<br>
It does not compute Planck likelihoods, Delta chi-square, posterior probabilities, or exclusion levels.<br>
It is designed to help users inspect distance to registered reference rows. It is not a model-validation claim.
</div>
""", unsafe_allow_html=True)

fit_df = pd.DataFrame([
    {
        "Model ID": "Planck 2018 LCDM-like baseline",
        "H0": 67.36,
        "f_EDE": 0.000,
        "omega_cdm": 0.12000,
        "sigma8": 0.8226,
        "S8": 0.8413,
        "Profile role": "baseline reference"
    },
    {
        "Model ID": "Ivanov-style EDE reference",
        "H0": 71.15,
        "f_EDE": 0.105,
        "omega_cdm": 0.12999,
        "sigma8": 0.8314,
        "S8": 0.8340,
        "Profile role": "EDE reference region"
    },
    {
        "Model ID": "FUJIKI DTI working reference",
        "H0": 72.90,
        "f_EDE": 0.082,
        "omega_cdm": 0.12700,
        "sigma8": 0.8229,
        "S8": 0.8019,
        "Profile role": "DTI working reference region"
    },
    {
        "Model ID": "High-EDE stress region",
        "H0": 75.50,
        "f_EDE": 0.160,
        "omega_cdm": 0.14000,
        "sigma8": 0.9000,
        "S8": 0.9000,
        "Profile role": "stress-test region"
    }
])

def _safe_float_from_state(names, default):
    for name in names:
        try:
            value = st.session_state.get(name, None)
            if value is not None and str(value).strip() != "":
                return float(value)
        except Exception:
            pass
    return float(default)

current_h0_val = _safe_float_from_state(["target_H0", "H0", "h_input"], 72.90)
if current_h0_val < 10:
    current_h0_val = current_h0_val * 100.0

current_fede_val = _safe_float_from_state(["target_f_EDE", "f_EDE", "fede_input"], 0.082)
current_ocdm_val = _safe_float_from_state(["target_omega_cdm", "omega_cdm"], 0.127)
current_sig8_val = _safe_float_from_state(["target_sigma8", "sigma8"], 0.8229)
current_s8_val = _safe_float_from_state(["target_S8", "S8"], 0.8019)

profile_weights = {
    "H0": 1.0 / 4.0,
    "f_EDE": 1.0 / 0.08,
    "omega_cdm": 1.0 / 0.015,
    "sigma8": 1.0 / 0.06,
    "S8": 1.0 / 0.06,
}

def profile_distance(row):
    terms = []
    terms.append(((current_h0_val - float(row["H0"])) * profile_weights["H0"]) ** 2)
    terms.append(((current_fede_val - float(row["f_EDE"])) * profile_weights["f_EDE"]) ** 2)
    terms.append(((current_ocdm_val - float(row["omega_cdm"])) * profile_weights["omega_cdm"]) ** 2)
    terms.append(((current_sig8_val - float(row["sigma8"])) * profile_weights["sigma8"]) ** 2)
    terms.append(((current_s8_val - float(row["S8"])) * profile_weights["S8"]) ** 2)
    return float(np.sqrt(sum(terms)))

fit_df["profile_distance"] = fit_df.apply(profile_distance, axis=1)
nearest_row = fit_df.iloc[int(np.argmin(fit_df["profile_distance"].values))]
nearest_distance = float(nearest_row["profile_distance"])

if nearest_distance < 1.25:
    profile_status = "near registered reference region"
    profile_color = "#50c878"
elif nearest_distance < 2.50:
    profile_status = "caution: between registered regions"
    profile_color = "#f57c00"
else:
    profile_status = "outside registered reference region"
    profile_color = "#ff5252"

fit_col1, fit_col2 = st.columns(2)

with fit_col1:
    st.markdown("##### Registered fit-region references")
    st.dataframe(fit_df, hide_index=True, width="stretch")

with fit_col2:
    st.markdown("##### Current input profile position")
    st.markdown(
        f"""
        <div class="source-card">
        <b>Nearest registered region:</b> {nearest_row["Model ID"]}<br>
        <b>Profile role:</b> {nearest_row["Profile role"]}<br>
        <b>Normalized profile distance:</b> {nearest_distance:.3f}<br>
        <b>Status:</b> <span style="color:{profile_color}; font-weight:800;">{profile_status}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="padding:16px; border-radius:10px; border:1px solid {profile_color}; background-color:rgba(120,120,120,0.10); color:{profile_color};">
        <b>Fit-region profile readout</b><br>
        H0={current_h0_val:.3f}, f_EDE={current_fede_val:.4f}, omega_cdm={current_ocdm_val:.5f}, sigma8={current_sig8_val:.5f}, S8={current_s8_val:.5f}<br>
        This is a normalized reference-distance diagnostic, not a Delta-chi-square or likelihood result.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("""
<div class="metric-card">
<b>Fit-profile metric:</b> weighted Euclidean distance to registered reference rows; this is a heuristic triage score.<br>
<b>Weights:</b> H0 scale 4 km/s/Mpc, f_EDE scale 0.08, omega_cdm scale 0.015, sigma8/S8 scale 0.06.<br>
<b>Interpretation:</b> useful for local triage and visualization; not valid as a likelihood result, posterior comparison, model validation, or formal exclusion rule.
</div>
""", unsafe_allow_html=True)



def extract_external_class_api_payload_v606(text):
    import re

    defaults = {
        "H0": 72.9,
        "omega_b": 0.0244,
        "omega_cdm": 0.127,
        "f_EDE": 0.082,
        "z_c": 3500.0,
        "n_s": 0.9847,
        "ln10_10_As": 3.058,
        "tau_reio": 0.0511,
    }

    aliases = {
        "H0": ["H0", "H_0"],
        "omega_b": ["omega_b", "ombh2", "omega_bh2"],
        "omega_cdm": ["omega_cdm", "omch2", "omega_c"],
        "f_EDE": ["f_EDE", "fde", "fEDE"],
        "z_c": ["z_c", "zc"],
        "n_s": ["n_s", "ns"],
        "ln10_10_As": ["ln10_10_As", "ln10^{10}A_s", "ln10_10As"],
        "tau_reio": ["tau_reio", "tau"],
    }

    payload = dict(defaults)
    text = str(text or "")

    for key, names in aliases.items():
        for name in names:
            pattern = rf"(?<![A-Za-z0-9_]){re.escape(name)}\s*[:=]\s*([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)"
            m = re.search(pattern, text)
            if m:
                try:
                    payload[key] = float(m.group(1))
                    break
                except Exception:
                    pass

    return payload


st.header("9. External CLASS API sandbox")
try:
    _dti_render_section9_visuals_v607()
except Exception as _dti_graph_exc_9_v607:
    st.caption(f"Section 9 audit visualization unavailable: {_dti_graph_exc_9_v607}")

st.markdown("""
<div class="boundary-card">
<b>External compute mode:</b> this section sends the current parameter block to the public Render CLASS API backend.<br>
<b>Compute endpoint:</b> <code>https://dti-class-api.onrender.com/class/compute</code><br>
<b>Health endpoint:</b> <code>https://dti-class-api.onrender.com/health</code><br>
<b>Boundary:</b> exploratory, non-canonical, not a likelihood evaluation, not a posterior comparison, and not a Planck validation pipeline.<br>
<b>Current backend scope:</b> LCDM-like CLASS propagation only. <code>f_EDE</code> and <code>z_c</code> are passed for interface compatibility but are not used as AxiCLASS EDE microphysics in this minimal backend.
</div>
""", unsafe_allow_html=True)

external_api_url = st.text_input(
    "External CLASS API endpoint",
    value="https://dti-class-api.onrender.com/class/compute",
    key="external_class_api_endpoint_v606",
)

external_api_text = st.session_state.get("paper_text_widget", st.session_state.get("paper_text", ""))
external_api_payload = extract_external_class_api_payload_v606(external_api_text)

st.markdown("##### Payload sent to external API")
st.dataframe(pd.DataFrame([external_api_payload]), hide_index=True, width="stretch")

if st.button("Run external CLASS API for current input model", key="run_external_class_api_v606", width="stretch", type="primary"):
    try:
        if _dti_is_disabled_endpoint_literal_v1(external_api_url):
            _dti_local_endpoint_disabled_notice_v1()
            st.stop()
        response = requests.post(external_api_url, json=external_api_payload, timeout=90)
        st.session_state["external_class_api_result_v606"] = response.json()
        st.session_state["external_class_api_http_status_v606"] = response.status_code
    except Exception as exc:
        st.session_state["external_class_api_result_v606"] = {
            "status": "failed",
            "message": repr(exc),
            "boundary": {
                "likelihood_evaluation": False,
                "posterior_comparison": False,
                "canonical_checkpoint_update": False,
            },
        }
        st.session_state["external_class_api_http_status_v606"] = None

external_api_result = st.session_state.get("external_class_api_result_v606")
external_api_http_status = st.session_state.get("external_class_api_http_status_v606")

if external_api_result:
    st.markdown("##### External CLASS API result")
    st.caption(f"HTTP status: {external_api_http_status}")

    status_value = str(external_api_result.get("status", "unknown"))
    if status_value == "ok":
        st.success("External CLASS API returned status: ok")
    elif status_value == "unavailable":
        st.warning("External CLASS API is available, but classy/PyCLASS is unavailable on the backend.")
    else:
        st.warning(f"External CLASS API returned status: {status_value}")

    derived = external_api_result.get("derived", {})
    if isinstance(derived, dict) and derived:
        derived_rows = []
        for key in [
            "h",
            "Omega_m_computed",
            "A_s",
            "sigma8_CLASS",
            "S8_CLASS",
            "rs_drag_Mpc_CLASS",
            "age_Gyr_CLASS",
        ]:
            if key in derived:
                derived_rows.append({"quantity": key, "value": derived.get(key)})
        if derived_rows:
            st.dataframe(pd.DataFrame(derived_rows), hide_index=True, width="stretch")

    with st.expander("Raw external API response", expanded=False):
        st.code(json.dumps(external_api_result, indent=2, sort_keys=True), language="json")


st.header("10. Interpretation boundary")

st.markdown("""
<div class="boundary-card">
<b>Explicit boundary:</b> this app is exploratory, local/non-canonical where indicated, and diagnostic only.<br>
<span id="section10_explicit_physical_and_value_boundary_v606"></span>
It is not a likelihood engine, not a posterior sampler, not a Planck validation pipeline, and not a replacement for frozen manuscript artifacts.<br>
It is not evidence establishing physical continuity, physical discontinuity, or an operator-phase transition.<br>
It does not update manuscript values, canonical physics values, likelihood preferences, posterior preferences, or Planck-validation claims.
</div>
""", unsafe_allow_html=True)


audit_summary_text = f"""DTI-Core Grand Auditor v6.0.6 audit summary

Candidate source: {candidate_source_paper}
Candidate source location: {candidate_source_location}
Candidate note: {candidate_source_note}

Reference source: {reference_source_paper}
Reference source location: {reference_source_location}
Reference note: {reference_source_note}

Boundary:
- This is not a likelihood evaluation.
- This is not a posterior comparison.
- AxiCLASS FIX1 is a locked benchmark reference, not a live recomputation.
- Live CLASS sandbox outputs are exploratory and non-canonical.
"""

st.download_button(
    "Download audit summary text",
    data=audit_summary_text,
    file_name="dti_core_audit_summary.txt",
    mime="text/plain",
    width="stretch",
)

st.markdown(
    """
- The search engine helps identify which registered reference model is closest to the input parameters.
- The Section 7a AxiCLASS fixed-example check is a locked local benchmark. It is not recomputed from arbitrary user input.
- The local live CLASS probe in Section 7b is exploratory. A failed run is not a model-level exclusion.
- The continuity / discontinuity examiner in Section 7c detects numerical/statistical non-smoothness candidates only; it is not evidence establishing physical discontinuity.
- This app is not a likelihood evaluation, posterior comparison, Planck likelihood validation, or S8-claim validation.
"""
)
