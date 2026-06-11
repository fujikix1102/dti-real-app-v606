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
def _dti_arrow_safe_df_v1(*args, **kwargs):
    # DTI_FIX2H_NON_DF_GUARD: avoid DeltaGenerator / nested-render objects
    try:
        import pandas as _pd
        if not isinstance(df, _pd.DataFrame):
            return df
    except Exception:
        return df
    """
    Streamlit dataframe compatibility helper.

    Accepts either:
      _dti_arrow_safe_df_v1(df, ...)
      _dti_arrow_safe_df_v1(container_or_st, df, ...)

    This prevents accidental conversion of Streamlit DeltaGenerator/container
    objects into pandas DataFrames and coerces mixed object columns to string
    before display to avoid Arrow serialization warnings.
    """
    import pandas as pd
    import streamlit as st

    kwargs.pop("hide_index", None)
    kwargs.pop("use_container" + "_width", None)
    width = kwargs.pop("width", "stretch")

    target = st
    df = None

    if len(args) == 0:
        return None

    if len(args) == 1:
        df = args[0]
    else:
        first, second = args[0], args[1]
        if hasattr(first, "dataframe") and not hasattr(first, "columns"):
            target = first
            df = second
        else:
            df = first

    # If a DeltaGenerator/container was accidentally passed as df, do not
    # convert it to pandas. Display a controlled diagnostic instead of crashing.
    if hasattr(df, "dataframe") and not hasattr(df, "columns"):
        return st.warning("Skipped dataframe display: Streamlit container object was passed without a data object.")

    try:
        safe = pd.DataFrame(df).copy()
    except Exception:
        try:
            return target.write(df)
        except Exception:
            return st.write(df)

    for col in safe.columns:
        if str(safe[col].dtype) == "object":
            safe[col] = safe[col].map(lambda x: "" if pd.isna(x) else str(x))

    try:
        return target.dataframe(safe, width=width, **kwargs)
    except TypeError:
        return target.dataframe(safe, **kwargs)

import streamlit as st

def _dti_arrow_safe_df_v1(df, *args, **kwargs):
    """Render dataframe through Streamlit after forcing object columns to safe strings.

    Boundary:
    - UI serialization compatibility only.
    - No scientific value change.
    - No likelihood, CLASS, MCMC, posterior, or validation execution.
    """
    try:
        import pandas as _pd
        if isinstance(df, _pd.DataFrame):
            out = df.copy()
            for col in out.columns:
                if str(out[col].dtype) == "object":
                    out[col] = out[col].map(lambda x: "" if _pd.isna(x) else str(x))
            df = out
    except Exception:
        pass

    kwargs.pop("hide_index", None)
    kwargs.pop("width", None)
    kwargs.setdefault("width", "stretch")
    return st.dataframe(df, *args, **kwargs)


# --- DTI_ORIGINAL_STREAMLIT_MARKDOWN_NO_RECURSION ---
# Keep a stable reference to Streamlit's original markdown function before any wrappers.
_DTI_ORIGINAL_STREAMLIT_MARKDOWN_NO_RECURSION = st.markdown
_DTI_MARKDOWN_RECURSION_FIX_V1 = True
_DTI_DISABLE_MARKDOWN_MONKEYPATCH_PASS_GLOBAL_V1 = True
_DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_GLOBAL_V1 = True
_DTI_DISABLE_REMAINING_HEADER_MONKEYPATCHES_GLOBAL_V1 = True

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



# --- DTI_POSITIVE_ANSWER_NAVIGATOR_V2 ---

# Positive answer-oriented guidance layer.

# UI text only. Does not enable 7c, graph rendering, likelihood, posterior,

# Planck validation, physics-value updates, manuscript updates, Render changes,

# or Streamlit Secret changes.

_DTI_POSITIVE_ANSWER_NAVIGATOR_V2 = True

def _dti_render_positive_answer_navigator_v2():

    import streamlit as st

    st.markdown("### Positive answer navigator")

    st.info(

        "This app is not only a rejection tool. It is designed to identify what already passes, "

        "what remains partial, what fails, and what test is needed next before a clear answer can be claimed."

    )

    col_pass, col_partial, col_next = st.columns(3)

    with col_pass:

        st.markdown(

            """

**Positive output**

- What survives the audit.

- Which branch remains viable.

- Which bounded check passes.

- Which explanation is constrained.

            """

        )

    with col_partial:

        st.markdown(

            """

**Partial output**

Partial is not failure.

It means the signal is informative, but at least one audit layer still blocks a final scientific claim.

            """

        )

    with col_next:

        st.markdown(

            """

**Next test**

The app should always return the next useful test, not only a negative warning.

This keeps the workflow constructive.

            """

        )

    st.markdown("#### Answer format")

    st.code(

        """Answer status:

PASS / PARTIAL / FAIL / UNRESOLVED

Positive content:

What survives the audit?

Blocking content:

What still prevents a final claim?

Next action:

What test would move this from unresolved or partial toward a clear answer?""",

        language="text",

    )

    st.caption(

        "Boundary: this navigator is UI guidance only. It does not perform likelihood evaluation, "

        "posterior comparison, Planck validation, graph rendering, physics-value updates, or manuscript updates."

    )

# --- /DTI_POSITIVE_ANSWER_NAVIGATOR_V2 ---




# --- DTI_RESEARCH_MOTIVATION_LAYER_V1 ---
# Research motivation layer.
# UI text only. This does not enable 7c, graph rendering, likelihood evaluation,
# posterior comparison, Planck validation, physics-value updates, manuscript updates,
# Render API changes, or Streamlit Secret changes.
_DTI_RESEARCH_MOTIVATION_LAYER_V1 = True

def _dti_render_research_motivation_layer_v1():
    import streamlit as st

    st.markdown("### Research motivation layer")

    st.success(
        "Goal: turn each audit result into a constructive research lead. "
        "The app should not only say what fails; it should show what remains promising, "
        "what is already stable, and what the next decisive test should be."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
**Research lead**

Use the app to find:

- a surviving branch
- a stable parameter direction
- a bounded nuisance explanation
- a promising next comparison
- a clean unresolved zone worth testing
            """
        )

    with c2:
        st.markdown(
            """
**Positive interpretation**

A result is useful when it identifies one of these:

- PASS: a bounded check survives
- PARTIAL: a signal is informative but incomplete
- UNRESOLVED: the next test is now clear
- FAIL: a route can be retired safely
            """
        )

    with c3:
        st.markdown(
            """
**Research mindset**

The intended workflow is:

1. keep what survives
2. isolate what blocks the claim
3. define the next test
4. avoid overclaiming
5. convert uncertainty into a research plan
            """
        )

    st.markdown("#### Constructive answer template")
    st.code(
        """Research answer:
What is the most promising surviving result?

Evidence status:
PASS / PARTIAL / FAIL / UNRESOLVED

Why it matters:
What did this audit clarify?

Current blocker:
What still prevents a stronger claim?

Next experiment:
What should be tested next?""",
        language="text",
    )

    st.caption(
        "Boundary: this layer is explanatory UI only. It does not change solver behavior, "
        "physics values, likelihood/posterior interpretation, Planck validation, graph rendering, "
        "7c state, manuscript content, Render API settings, or Streamlit Secrets."
    )
# --- /DTI_RESEARCH_MOTIVATION_LAYER_V1 ---


# --- DTI_RESEARCH_OPPORTUNITY_ENGINE_V1D ---
# Positive research-navigation UI only.
# This does not enable 7c, graph rendering, likelihood evaluation, posterior comparison,
# Planck validation, physics-value updates, manuscript updates, Render API changes,
# or Streamlit Secret changes.
_DTI_RESEARCH_OPPORTUNITY_ENGINE_V1D = True

def _dti_render_research_opportunity_engine_v1d():
    import streamlit as st

    st.markdown("### Research Opportunity Engine")
    st.info(
        "Purpose: convert each audit result into a research opportunity. "
        "The useful output is not only whether something fails, but which direction survives, "
        "which uncertainty is scientifically productive, and what controlled test should be run next."
    )

    st.markdown("#### Research Opportunity Map")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
**Stable lead**

Use when:

- a bounded check passes
- a candidate remains internally consistent
- nuisance drift is not the dominant explanation
- the result is suitable for a stricter follow-up
        """)

    with c2:
        st.markdown("""
**Tension lead**

Use when:

- a mismatch is structured
- the stress has a recognizable direction
- the result exposes a load-bearing parameter
- the tension defines a useful next comparison
        """)

    with c3:
        st.markdown("""
**Missing evidence**

Use when:

- the answer is not yet claimable
- a source-of-record table is absent
- a graph or diagnostic is intentionally disabled
- the next evidence object is clear
        """)

    with c4:
        st.markdown("""
**Retired path**

Use when:

- a route fails under the bounded check
- the failure is reproducible
- pursuing it would add noise
- the result safely narrows the search space
        """)

    st.markdown("#### Next Test Composer")
    st.code(
        """Possible research use:
This result may support a follow-up test of a surviving direction, tension direction, or missing evidence zone.

What to compare next:
Run a controlled comparison while holding the audit boundary, nuisance condition, or source-of-record rule fixed.

What would strengthen the claim:
Show that the same pattern persists under a stricter setting, independent source, or seed-stability check.

What should not be claimed yet:
Do not claim final physics, likelihood dominance, Planck validation, graph-based proof, or a cosmological mechanism unless the required audit layer is present.""",
        language="text",
    )

    st.markdown("#### Claim Boundary Translator")
    safe_col, limit_col = st.columns(2)

    with safe_col:
        st.markdown("""
**Safe positive wording**

- This identifies a bounded research lead.
- This result survives the current audit layer.
- This comparison defines the next controlled test.
- This narrows the viable search space.
- This is a constructive unresolved zone, not a dead end.
        """)

    with limit_col:
        st.markdown("""
**Do not overclaim**

- Do not claim new physics from this UI layer.
- Do not claim likelihood or posterior evidence here.
- Do not claim Planck validation here.
- Do not claim graph-based proof while graphs are disabled.
- Do not turn a useful lead into a final mechanism claim.
        """)

    st.success(
        "Research-positive reading: a strong app does not only reject. "
        "It preserves stable leads, names productive tensions, identifies missing evidence, "
        "and retires weak paths so the next experiment becomes clearer."
    )

    st.caption(
        "Boundary: this engine is explanatory UI only. It does not change solver behavior, "
        "physics values, likelihood/posterior interpretation, Planck validation, graph rendering, "
        "7c state, manuscript content, Render API settings, or Streamlit Secrets."
    )
# --- /DTI_RESEARCH_OPPORTUNITY_ENGINE_V1D ---


# --- DTI_DISCOVERY_SCORE_PANEL_V1E ---
# Lightweight positive research scoring panel.
# UI and meta-scoring only.
# This does not enable 7c, graph rendering, likelihood evaluation,
# posterior comparison, Planck validation, physics-value updates,
# manuscript updates, Render API changes, or Streamlit Secret changes.
_DTI_DISCOVERY_SCORE_PANEL_V1E = True

def _dti_discovery_score_level_v1e(score):
    try:
        value = int(score)
    except Exception:
        value = 0
    if value >= 80:
        return "Strong research lead"
    if value >= 60:
        return "Promising research lead"
    if value >= 40:
        return "Partial but useful lead"
    if value >= 20:
        return "Early-stage lead"
    return "Retired or unresolved path"

def _dti_render_discovery_score_panel_v1e():
    import streamlit as st

    st.markdown("### Discovery Score and Claim Readiness")

    st.info(
        "This panel converts audit status into a constructive research signal. "
        "It does not run new cosmology. It does not change physics values. "
        "It helps decide whether a result is a strong lead, a promising lead, a partial lead, "
        "an early lead, or a route to retire."
    )

    st.markdown("#### Lightweight scoring inputs")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        stability_score = st.slider(
            "Stability",
            min_value=0,
            max_value=20,
            value=12,
            step=1,
            help="Does the result remain stable under the current bounded audit?",
            key="dti_discovery_score_stability_v1e",
        )

    with c2:
        signal_score = st.slider(
            "Signal interest",
            min_value=0,
            max_value=20,
            value=14,
            step=1,
            help="Is the result informative enough to motivate a focused follow-up test?",
            key="dti_discovery_score_signal_v1e",
        )

    with c3:
        explanation_score = st.slider(
            "Explainability",
            min_value=0,
            max_value=20,
            value=12,
            step=1,
            help="Can the result be explained without overclaiming?",
            key="dti_discovery_score_explainability_v1e",
        )

    with c4:
        next_test_score = st.slider(
            "Next-test clarity",
            min_value=0,
            max_value=20,
            value=16,
            step=1,
            help="Is the next controlled test clear?",
            key="dti_discovery_score_next_test_v1e",
        )

    with c5:
        overclaim_risk = st.slider(
            "Overclaim risk",
            min_value=0,
            max_value=20,
            value=8,
            step=1,
            help="Higher means stronger risk of saying more than the audit supports.",
            key="dti_discovery_score_overclaim_v1e",
        )

    raw_score = stability_score + signal_score + explanation_score + next_test_score - overclaim_risk
    discovery_score = max(0, min(100, int(round(raw_score * 100 / 80))))
    readiness_score = max(0, min(7, int(round(discovery_score * 7 / 100))))
    level = _dti_discovery_score_level_v1e(discovery_score)

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Discovery Score",
            f"{discovery_score} / 100",
            help="Lightweight research-lead score. This is not a likelihood or posterior statistic.",
        )

    with m2:
        st.metric(
            "Claim Readiness",
            f"{readiness_score} / 7",
            help="How close the current state is to a claim-ready result.",
        )

    with m3:
        st.metric(
            "Lead Type",
            level,
            help="Interpretive class for research planning only.",
        )

    st.markdown("#### Constructive interpretation")

    if discovery_score >= 80:
        st.success(
            "Positive result: this looks like a strong research lead. "
            "The safe next step is to lock the source data, repeat the bounded comparison, "
            "and test whether the lead survives independent controls."
        )
    elif discovery_score >= 60:
        st.success(
            "Positive result: this is promising. "
            "It is not yet a final scientific claim, but it is strong enough to justify a focused follow-up test."
        )
    elif discovery_score >= 40:
        st.warning(
            "Partial but useful: this result should not be discarded. "
            "It clarifies what is missing and helps define the next controlled experiment."
        )
    elif discovery_score >= 20:
        st.warning(
            "Early-stage lead: useful mainly as a search-direction clue. "
            "Do not claim a physical conclusion yet."
        )
    else:
        st.info(
            "Retired or unresolved path: this route is not currently productive. "
            "The positive value is that it can be safely deprioritized."
        )

    st.markdown("#### Positive finding box")

    st.code(
        f"""Positive finding:
{level}

Discovery Score:
{discovery_score} / 100

Claim Readiness:
{readiness_score} / 7

What survives:
The result is useful as a bounded research lead if it identifies a stable direction, a constrained explanation, or a clear next test.

What remains blocked:
This panel does not add likelihood-level, posterior-level, Planck-level, or manuscript-level evidence.

Next controlled test:
Repeat the relevant comparison under fixed audit boundaries and record whether the result moves from unresolved or partial toward pass.""",
        language="text",
    )

    st.markdown("#### Safe claim translator")

    safe_col, avoid_col = st.columns(2)

    with safe_col:
        st.markdown(
            """
**Safe positive wording**

- This result identifies a bounded research lead.
- The current audit narrows the next controlled test.
- The tested direction remains informative under the present constraints.
- The result is promising but not yet a final physics claim.
            """
        )

    with avoid_col:
        st.markdown(
            """
**Do not claim yet**

- Do not claim a final solution.
- Do not claim proof of new physics from this panel.
- Do not claim Planck validation.
- Do not claim likelihood or posterior superiority.
- Do not claim 7c continuity or discontinuity closure here.
            """
        )

    st.caption(
        "Boundary: this is a lightweight research-planning layer only. "
        "It does not perform likelihood evaluation, posterior comparison, Planck validation, graph rendering, "
        "7c execution, physics-value updates, manuscript updates, Render API modification, or Streamlit Secret modification."
    )
# --- /DTI_DISCOVERY_SCORE_PANEL_V1E ---


# --- DTI_PARAMETER_QUALITY_MATRIX_V1F ---
# Color-coded parameter quality / research triage table.
# UI and meta-scoring only.
# This does not enable 7c, graph rendering, likelihood evaluation,
# posterior comparison, Planck validation, physics-value updates,
# manuscript updates, Render API changes, or Streamlit Secret changes.
_DTI_PARAMETER_QUALITY_MATRIX_V1F = True

def _dti_parameter_quality_label_v1f(score):
    try:
        value = int(score)
    except Exception:
        value = 0
    if value >= 80:
        return "GREEN - promising"
    if value >= 60:
        return "YELLOW - partial but useful"
    if value >= 40:
        return "ORANGE - needs control"
    if value >= 20:
        return "RED - blocked for claim"
    return "GRAY - not evaluated"

def _dti_parameter_quality_score_v1f(stability, signal, control, risk):
    try:
        raw = int(stability) + int(signal) + int(control) - int(risk)
    except Exception:
        raw = 0
    return max(0, min(100, int(round(raw * 100 / 60))))

def _dti_parameter_quality_style_v1f(row):
    score = int(row.get("quality_score", 0))
    if score >= 80:
        color = "background-color: #0f5132; color: #d1e7dd"
    elif score >= 60:
        color = "background-color: #664d03; color: #fff3cd"
    elif score >= 40:
        color = "background-color: #7c2d12; color: #ffedd5"
    elif score >= 20:
        color = "background-color: #842029; color: #f8d7da"
    else:
        color = "background-color: #343a40; color: #dee2e6"
    return [color if col in ["quality_label", "quality_score", "claim_readiness"] else "" for col in row.index]

def _dti_render_parameter_quality_matrix_v1f():
    import streamlit as st
    import pandas as pd

    st.markdown("### Legacy/detail Parameter Quality Matrix 1 — audit view")

    st.info(
        "This matrix color-codes parameter directions so a researcher can see which points look promising, "
        "which are partial, which need controls, and which are blocked for claim-making. "
        "It is a research triage table only, not a likelihood result, posterior comparison, Planck validation, "
        "graph-based proof, or final physics claim."
    )

    st.markdown("#### Parameter direction presets")

    rows = [
        {
            "parameter": "H0",
            "current_value": "sidebar / selected profile",
            "research_role": "branch coordinate",
            "positive_signal": "Can expose branch-level response direction.",
            "risk_blocker": "Not sufficient alone for a cosmological claim.",
            "stability": 12,
            "signal_interest": 16,
            "control_strength": 12,
            "overclaim_risk": 8,
            "next_test": "Compare fixed-H0 branches under the same audit boundary.",
            "safe_interpretation": "Useful branch label and response coordinate.",
        },
        {
            "parameter": "f_EDE",
            "current_value": "sidebar / selected profile",
            "research_role": "early-time scan coordinate",
            "positive_signal": "Can mark a controlled early-time modification direction.",
            "risk_blocker": "Requires source-locked comparison before mechanism language.",
            "stability": 10,
            "signal_interest": 15,
            "control_strength": 10,
            "overclaim_risk": 9,
            "next_test": "Check whether the same pattern persists across adjacent f_EDE values.",
            "safe_interpretation": "Promising controlled scan coordinate.",
        },
        {
            "parameter": "omega_cdm",
            "current_value": "sidebar / selected profile",
            "research_role": "compensating direction",
            "positive_signal": "Can identify a narrow compensating parameter direction.",
            "risk_blocker": "Needs companion-variable and seed-stability checks.",
            "stability": 13,
            "signal_interest": 15,
            "control_strength": 13,
            "overclaim_risk": 7,
            "next_test": "Audit whether the compensating direction remains narrow and sign-stable.",
            "safe_interpretation": "Candidate compensating direction.",
        },
        {
            "parameter": "omega_b",
            "current_value": "sidebar / selected profile",
            "research_role": "baryon-sector control",
            "positive_signal": "Can help separate baryon-sector load from dark-sector load.",
            "risk_blocker": "Usually not sufficient as the main driver.",
            "stability": 10,
            "signal_interest": 9,
            "control_strength": 11,
            "overclaim_risk": 8,
            "next_test": "Hold other parameters fixed and inspect whether the response is load-bearing.",
            "safe_interpretation": "Useful control parameter.",
        },
        {
            "parameter": "n_s",
            "current_value": "sidebar / selected profile",
            "research_role": "spectral-tilt companion",
            "positive_signal": "Can expose spectral-tilt compensation.",
            "risk_blocker": "Needs CMB-shape and companion-variable checks.",
            "stability": 9,
            "signal_interest": 10,
            "control_strength": 10,
            "overclaim_risk": 8,
            "next_test": "Check whether tilt movement is primary or merely a companion shift.",
            "safe_interpretation": "Companion diagnostic.",
        },
        {
            "parameter": "sigma8 / S8",
            "current_value": "derived / reference",
            "research_role": "stress indicator",
            "positive_signal": "Can reveal growth-stress burden and residual tension.",
            "risk_blocker": "A stress indicator is not itself a likelihood exclusion.",
            "stability": 11,
            "signal_interest": 16,
            "control_strength": 9,
            "overclaim_risk": 10,
            "next_test": "Check whether growth stress is reduced without nuisance-driven escape.",
            "safe_interpretation": "Useful diagnostic stress coordinate.",
        },
        {
            "parameter": "A_planck / calibration",
            "current_value": "nuisance / control",
            "research_role": "nuisance-control boundary",
            "positive_signal": "Can test whether a result survives nuisance-control restrictions.",
            "risk_blocker": "Must not be used as a hidden explanation without explicit control.",
            "stability": 12,
            "signal_interest": 12,
            "control_strength": 16,
            "overclaim_risk": 7,
            "next_test": "Repeat under FIX/TIGHT-style nuisance boundaries before stronger wording.",
            "safe_interpretation": "Calibration-control check.",
        },
    ]

    for row in rows:
        score = _dti_parameter_quality_score_v1f(
            row["stability"],
            row["signal_interest"],
            row["control_strength"],
            row["overclaim_risk"],
        )
        row["quality_score"] = score
        row["quality_label"] = _dti_parameter_quality_label_v1f(score)
        row["claim_readiness"] = max(0, min(7, int(round(score * 7 / 100))))

    df = pd.DataFrame(rows)

    st.markdown("#### Total evaluation table")
    st.caption(
        "Color meaning: GREEN is promising, YELLOW is partial but useful, ORANGE needs control, "
        "RED is blocked for claim-making, and GRAY is not evaluated. Scores are UI meta-scores only."
    )

    display_cols = [
        "parameter",
        "research_role",
        "quality_label",
        "quality_score",
        "claim_readiness",
        "positive_signal",
        "risk_blocker",
        "next_test",
        "safe_interpretation",
    ]

    try:
        styled = df[display_cols].style.apply(_dti_parameter_quality_style_v1f, axis=1)
        _dti_arrow_safe_df_v1(styled, width="stretch", hide_index=True)
    except Exception:
        _dti_arrow_safe_df_v1(df[display_cols], width="stretch", hide_index=True)

    st.markdown("#### Best current leads")

    sorted_df = df.sort_values(["quality_score", "claim_readiness"], ascending=False)
    best = sorted_df.head(3)

    for _, row in best.iterrows():
        st.success(
            f"{row['parameter']}: {row['quality_label']} "
            f"(score {row['quality_score']}/100, readiness {row['claim_readiness']}/7). "
            f"Next test: {row['next_test']}"
        )

    st.markdown("#### How to use this table")

    st.code(
        """Use rule:
1. Prefer GREEN/YELLOW rows as research leads.
2. Treat ORANGE rows as control-needed directions.
3. Treat RED rows as blocked for claim-making, not necessarily useless.
4. Never convert this table into a likelihood, posterior, Planck, or final-physics claim.
5. Use the next_test column to design the next bounded comparison.""",
        language="text",
    )

    st.caption(
        "Boundary: this matrix is a research-planning UI layer only. It does not compute likelihoods, "
        "posterior probabilities, Planck validation, graph outputs, 7c continuity closure, physics values, "
        "manuscript values, Render API changes, or Streamlit Secret changes."
    )
# --- /DTI_PARAMETER_QUALITY_MATRIX_V1F ---




# --- DTI_PARAMETER_QUALITY_MATRIX_V1G ---
# Improved color-badge parameter quality / research triage table.
# UI and meta-scoring only.
# This does not enable 7c, graph rendering, likelihood evaluation,
# posterior comparison, Planck validation, physics-value updates,
# manuscript updates, Render API changes, or Streamlit Secret changes.
_DTI_PARAMETER_QUALITY_MATRIX_V1G = True

def _dti_pqm_v1g_session_value(name, fallback):
    try:
        import streamlit as st
        keys = [
            name,
            name.lower(),
            name.upper(),
            "dti_" + name,
            "dti_" + name.lower(),
            "candidate_" + name,
            "candidate_" + name.lower(),
            "current_" + name,
            "current_" + name.lower(),
            "profile_" + name,
            "profile_" + name.lower(),
        ]
        alias = {
            "H0": ["H0", "h0", "H_0", "h"],
            "f_EDE": ["f_EDE", "fede", "f_ede", "fde"],
            "omega_cdm": ["omega_cdm", "omch2", "omega_cdm_h2"],
            "omega_b": ["omega_b", "ombh2", "omega_b_h2"],
            "n_s": ["n_s", "ns"],
            "sigma8 / S8": ["sigma8", "S8", "s8"],
            "A_planck / calibration": ["A_planck", "a_planck", "calibration", "calib_100T"],
        }
        for k in alias.get(name, []):
            keys.append(k)
            keys.append("dti_" + k)
            keys.append("candidate_" + k)
            keys.append("current_" + k)
        for k in keys:
            if k in st.session_state:
                value = st.session_state.get(k)
                if value is not None and str(value).strip() != "":
                    return value
    except Exception:
        pass
    return fallback

def _dti_pqm_v1g_quality_label(score):
    try:
        value = int(score)
    except Exception:
        value = 0
    if value >= 80:
        return "GREEN"
    if value >= 60:
        return "YELLOW"
    if value >= 40:
        return "ORANGE"
    if value >= 20:
        return "RED"
    return "GRAY"

def _dti_pqm_v1g_badge_text(label):
    mapping = {
        "GREEN": "GREEN - promising",
        "YELLOW": "YELLOW - partial but useful",
        "ORANGE": "ORANGE - needs control",
        "RED": "RED - blocked for claim",
        "GRAY": "GRAY - not evaluated",
    }
    return mapping.get(label, "GRAY - not evaluated")

def _dti_pqm_v1g_badge_html(label):
    mapping = {
        "GREEN": ("#064e3b", "#a7f3d0", "GREEN - promising"),
        "YELLOW": ("#713f12", "#fde68a", "YELLOW - partial but useful"),
        "ORANGE": ("#7c2d12", "#fed7aa", "ORANGE - needs control"),
        "RED": ("#7f1d1d", "#fecaca", "RED - blocked for claim"),
        "GRAY": ("#374151", "#e5e7eb", "GRAY - not evaluated"),
    }
    bg, fg, text = mapping.get(label, mapping["GRAY"])
    return (
        "<span style='display:inline-block; padding:4px 10px; border-radius:999px; "
        "font-weight:700; font-size:0.86rem; background:" + bg + "; color:" + fg + ";'>"
        + text +
        "</span>"
    )

def _dti_pqm_v1g_score(stability, signal, control, risk):
    try:
        raw = int(stability) + int(signal) + int(control) - int(risk)
    except Exception:
        raw = 0
    return max(0, min(100, int(round(raw * 100 / 60))))

def _dti_pqm_v1g_styler(df):
    def style_row(row):
        label = str(row.get("quality_group", "GRAY"))
        bg = {
            "GREEN": "#064e3b",
            "YELLOW": "#713f12",
            "ORANGE": "#7c2d12",
            "RED": "#7f1d1d",
            "GRAY": "#374151",
        }.get(label, "#374151")
        fg = {
            "GREEN": "#d1fae5",
            "YELLOW": "#fef3c7",
            "ORANGE": "#ffedd5",
            "RED": "#fee2e2",
            "GRAY": "#f3f4f6",
        }.get(label, "#f3f4f6")
        cells = []
        for col in row.index:
            if col in ["quality_badge", "quality_score", "claim_readiness", "research_role"]:
                cells.append("background-color: " + bg + "; color: " + fg + "; font-weight: 700;")
            else:
                cells.append("")
        return cells
    try:
        return df.style.apply(style_row, axis=1)
    except Exception:
        return df

def _dti_render_parameter_quality_matrix_v1g():
    import streamlit as st
    import pandas as pd

    st.markdown("### Legacy/detail Parameter Quality Matrix 2 — audit view")

    st.info(
        "This matrix color-codes promising parameter directions and blocked regions. "
        "It is a research triage board, not a likelihood result, posterior comparison, Planck validation, "
        "or final physics claim."
    )

    st.markdown("#### Color meaning")

    l1, l2, l3, l4, l5 = st.columns(5)
    with l1:
        st.markdown(_dti_pqm_v1g_badge_html("GREEN"), unsafe_allow_html=True)
        st.caption("Strong lead. Prioritize source-lock and strict follow-up.")
    with l2:
        st.markdown(_dti_pqm_v1g_badge_html("YELLOW"), unsafe_allow_html=True)
        st.caption("Useful partial result. Needs one or more controls.")
    with l3:
        st.markdown(_dti_pqm_v1g_badge_html("ORANGE"), unsafe_allow_html=True)
        st.caption("Control-needed direction. Do not claim yet.")
    with l4:
        st.markdown(_dti_pqm_v1g_badge_html("RED"), unsafe_allow_html=True)
        st.caption("Blocked for claim-making, but useful as a boundary.")
    with l5:
        st.markdown(_dti_pqm_v1g_badge_html("GRAY"), unsafe_allow_html=True)
        st.caption("No evaluation available yet.")

    base_rows = [
        {
            "parameter": "H0",
            "research_role": "branch coordinate",
            "role_group": "Branch geometry",
            "current_value": _dti_pqm_v1g_session_value("H0", "selected profile"),
            "positive_signal": "Can expose branch-level response direction.",
            "risk_blocker": "Not sufficient alone for a cosmological claim.",
            "stability": 12,
            "signal": 16,
            "control": 12,
            "risk": 8,
            "next_test": "Compare fixed-H0 branches under the same audit boundary.",
            "safe_interpretation": "Useful branch label and response coordinate.",
        },
        {
            "parameter": "f_EDE",
            "research_role": "early-time scan coordinate",
            "role_group": "Early-time modification",
            "current_value": _dti_pqm_v1g_session_value("f_EDE", "selected profile"),
            "positive_signal": "Can mark a controlled early-time modification direction.",
            "risk_blocker": "Requires source-locked comparison before mechanism language.",
            "stability": 10,
            "signal": 15,
            "control": 10,
            "risk": 9,
            "next_test": "Check whether the same pattern persists across adjacent f_EDE values.",
            "safe_interpretation": "Promising controlled scan coordinate.",
        },
        {
            "parameter": "omega_cdm",
            "research_role": "compensating direction",
            "role_group": "Matter-sector compensation",
            "current_value": _dti_pqm_v1g_session_value("omega_cdm", "selected profile"),
            "positive_signal": "Can identify a narrow compensating parameter direction.",
            "risk_blocker": "Needs companion-variable and seed-stability checks.",
            "stability": 13,
            "signal": 15,
            "control": 13,
            "risk": 7,
            "next_test": "Audit whether the compensating direction remains narrow and sign-stable.",
            "safe_interpretation": "Candidate compensating parameter direction.",
        },
        {
            "parameter": "omega_b",
            "research_role": "baryon-sector control",
            "role_group": "Control parameter",
            "current_value": _dti_pqm_v1g_session_value("omega_b", "selected profile"),
            "positive_signal": "Can help separate baryon-sector load from dark-sector load.",
            "risk_blocker": "Usually not sufficient as the main driver.",
            "stability": 10,
            "signal": 9,
            "control": 11,
            "risk": 8,
            "next_test": "Hold other parameters fixed and inspect whether the response is load-bearing.",
            "safe_interpretation": "Useful control parameter.",
        },
        {
            "parameter": "n_s",
            "research_role": "spectral-tilt companion",
            "role_group": "Shape compensation",
            "current_value": _dti_pqm_v1g_session_value("n_s", "selected profile"),
            "positive_signal": "Can expose spectral-tilt compensation.",
            "risk_blocker": "Needs CMB-shape and residual checks before stronger wording.",
            "stability": 9,
            "signal": 10,
            "control": 10,
            "risk": 8,
            "next_test": "Check whether tilt movement is a driver or a companion response.",
            "safe_interpretation": "Companion-shift diagnostic.",
        },
        {
            "parameter": "sigma8 / S8",
            "research_role": "stress indicator",
            "role_group": "Growth-stress diagnostic",
            "current_value": _dti_pqm_v1g_session_value("sigma8 / S8", "selected profile"),
            "positive_signal": "Can reveal growth-stress burden and residual tension.",
            "risk_blocker": "A stress indicator is not a likelihood exclusion by itself.",
            "stability": 10,
            "signal": 14,
            "control": 10,
            "risk": 9,
            "next_test": "Use as a diagnostic stress readout, not as final exclusion.",
            "safe_interpretation": "Bounded stress indicator.",
        },
        {
            "parameter": "A_planck / calibration",
            "research_role": "nuisance-control boundary",
            "role_group": "Calibration and nuisance control",
            "current_value": _dti_pqm_v1g_session_value("A_planck / calibration", "selected profile"),
            "positive_signal": "Can test whether a result survives nuisance-control restrictions.",
            "risk_blocker": "Must not become the hidden main explanation without audit.",
            "stability": 13,
            "signal": 13,
            "control": 15,
            "risk": 8,
            "next_test": "Repeat under FIX or TIGHT nuisance boundaries before stronger wording.",
            "safe_interpretation": "Nuisance-boundedness check.",
        },
    ]

    rows = []
    for row in base_rows:
        score = _dti_pqm_v1g_score(
            row["stability"],
            row["signal"],
            row["control"],
            row["risk"],
        )
        readiness = max(0, min(7, int(round(score * 7 / 100))))
        group = _dti_pqm_v1g_quality_label(score)
        row["quality_group"] = group
        row["quality_badge"] = _dti_pqm_v1g_badge_text(group)
        row["quality_score"] = score
        row["claim_readiness"] = readiness
        rows.append(row)

    df = pd.DataFrame(rows)

    st.markdown("#### Total evaluation table")
    st.caption(
        "Sorted by quality score, claim readiness, and control score. "
        "Scores are UI meta-scores only; they are not likelihood or posterior values."
    )

    display_cols = [
        "parameter",
        "research_role",
        "role_group",
        "current_value",
        "quality_badge",
        "quality_score",
        "claim_readiness",
        "positive_signal",
        "risk_blocker",
        "next_test",
        "safe_interpretation",
    ]

    sorted_df = df.sort_values(
        ["quality_score", "claim_readiness", "control"],
        ascending=False,
    ).reset_index(drop=True)

    try:
        _dti_arrow_safe_df_v1(
            _dti_pqm_v1g_styler(sorted_df[display_cols]), width="stretch",
            hide_index=True,
        )
    except Exception:
        _dti_arrow_safe_df_v1(sorted_df[display_cols], width="stretch", hide_index=True)

    st.markdown("#### Next-test priority order")
    st.caption("This section shows the next practical test order, not a scientific ranking of truth.")

    top_rows = sorted_df.head(5).to_dict("records")
    for index, row in enumerate(top_rows, start=1):
        label = row["quality_group"]
        st.markdown(
            "<div style='border:1px solid rgba(255,255,255,0.15); border-radius:12px; padding:12px; margin:8px 0;'>"
            "<div style='font-weight:800;'>"
            + str(index) + ". " + str(row["parameter"]) + " — "
            + _dti_pqm_v1g_badge_html(label)
            + "</div>"
            "<div style='margin-top:6px;'>"
            "<b>Role:</b> " + str(row["research_role"]) + " / " + str(row["role_group"]) + "<br>"
            "<b>Current value:</b> " + str(row["current_value"]) + "<br>"
            "<b>Why it matters:</b> " + str(row["positive_signal"]) + "<br>"
            "<b>Next test:</b> " + str(row["next_test"]) + "<br>"
            "<b>Safe wording:</b> " + str(row["safe_interpretation"])
            + "</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("#### Research-role grouping")

    role_summary = (
        sorted_df.groupby("role_group", as_index=False)
        .agg(
            parameters=("parameter", lambda s: ", ".join(map(str, s))),
            best_score=("quality_score", "max"),
            best_readiness=("claim_readiness", "max"),
        )
        .sort_values(["best_score", "best_readiness"], ascending=False)
    )

    _dti_arrow_safe_df_v1(role_summary, width="stretch", hide_index=True)

    st.markdown("#### How to use this table")
    st.code(
        """Use rule:
1. Start with GREEN or YELLOW rows as research leads.
2. Treat ORANGE rows as control-needed directions.
3. Treat RED rows as blocked for claim-making, not necessarily useless.
4. Read current_value as best-effort UI/session value; if unavailable, it falls back to selected profile.
5. Use role_group to see whether a parameter is acting as branch geometry, compensation, control, stress, or nuisance boundary.
6. Use Next-test priority order to decide what to run next.
7. Do not convert this table into likelihood, posterior, Planck, or final physics evidence.""",
        language="text",
    )

    st.caption(
        "Boundary: Parameter Quality Matrix V1G is a color-coded research triage layer only. "
        "It does not perform likelihood evaluation, posterior comparison, Planck validation, graph rendering, "
        "7c execution, physics-value updates, manuscript updates, Render API modification, or Streamlit Secret modification."
    )
# --- /DTI_PARAMETER_QUALITY_MATRIX_V1G ---


# --- DTI_PARAMETER_QUALITY_MATRIX_VISUAL_V1G ---
# Visual/readability refinement for Parameter Quality Matrix.
# UI and meta-scoring only.
# This does not enable 7c, graph rendering, likelihood evaluation,
# posterior comparison, Planck validation, physics-value updates,
# manuscript updates, Render API changes, or Streamlit Secret changes.
_DTI_PARAMETER_QUALITY_MATRIX_VISUAL_V1G = True

def _dti_parameter_quality_badge_v1g(score):
    try:
        value = int(score)
    except Exception:
        return "GRAY - awaiting data"
    if value >= 80:
        return "GREEN - strong lead"
    if value >= 60:
        return "YELLOW - useful partial"
    if value >= 40:
        return "ORANGE - needs control"
    if value >= 20:
        return "RED - blocked for claim"
    return "GRAY - awaiting data"

def _dti_parameter_quality_badge_style_v1g(label):
    s = "" if label is None else str(label)
    if s.startswith("GREEN"):
        return "background-color: #00A86B; color: #FFFFFF; font-weight: 800; border-radius: 999px;"
    if s.startswith("YELLOW"):
        return "background-color: #FFC400; color: #111111; font-weight: 900; border-radius: 999px;"
    if s.startswith("ORANGE"):
        return "background-color: #FF7A00; color: #FFFFFF; font-weight: 900; border-radius: 999px;"
    if s.startswith("RED"):
        return "background-color: #E53935; color: #FFFFFF; font-weight: 900; border-radius: 999px;"
    if s.startswith("GRAY"):
        return "background-color: #6B7280; color: #FFFFFF; font-weight: 800; border-radius: 999px;"
    return ""

def _dti_parameter_quality_row_style_v1g(row):
    label = str(row.get("quality_badge", ""))
    badge_style = _dti_parameter_quality_badge_style_v1g(label)

    # Avoid the old full-row gray look.
    # Keep normal table readability and color only the evaluation columns.
    normal = ""
    score_style = ""
    readiness_style = ""

    if label.startswith("GREEN"):
        score_style = "background-color: rgba(0, 168, 107, 0.22); color: #FFFFFF; font-weight: 800;"
        readiness_style = score_style
    elif label.startswith("YELLOW"):
        score_style = "background-color: rgba(255, 196, 0, 0.26); color: #FFFFFF; font-weight: 800;"
        readiness_style = score_style
    elif label.startswith("ORANGE"):
        score_style = "background-color: rgba(255, 122, 0, 0.30); color: #FFFFFF; font-weight: 800;"
        readiness_style = score_style
    elif label.startswith("RED"):
        score_style = "background-color: rgba(229, 57, 53, 0.28); color: #FFFFFF; font-weight: 800;"
        readiness_style = score_style
    elif label.startswith("GRAY"):
        score_style = "background-color: rgba(107, 114, 128, 0.20); color: #FFFFFF; font-weight: 700;"
        readiness_style = score_style

    styles = []
    for col in row.index:
        if col == "quality_badge":
            styles.append(badge_style)
        elif col in ["quality_score", "claim_readiness"]:
            styles.append(score_style)
        elif col in ["research_role", "role_group", "parameter"]:
            styles.append("font-weight: 800;")
        else:
            styles.append(normal)
    return styles

def _dti_render_color_meaning_v1g():
    import streamlit as st

    st.markdown("#### Color meaning")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(
            """
<div style="background:#00A86B;color:#FFFFFF;font-weight:900;padding:0.35rem 0.75rem;border-radius:999px;text-align:center;">
GREEN - strong lead
</div>
<p style="font-size:0.85rem;margin-top:0.5rem;">Strong lead. Prioritize source-lock and strict follow-up.</p>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
<div style="background:#FFC400;color:#111111;font-weight:900;padding:0.35rem 0.75rem;border-radius:999px;text-align:center;">
YELLOW - useful partial
</div>
<p style="font-size:0.85rem;margin-top:0.5rem;">Useful partial result. Needs one or more controls.</p>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
<div style="background:#FF7A00;color:#FFFFFF;font-weight:900;padding:0.35rem 0.75rem;border-radius:999px;text-align:center;">
ORANGE - needs control
</div>
<p style="font-size:0.85rem;margin-top:0.5rem;">Control-needed direction. Do not claim yet.</p>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            """
<div style="background:#E53935;color:#FFFFFF;font-weight:900;padding:0.35rem 0.75rem;border-radius:999px;text-align:center;">
RED - blocked for claim
</div>
<p style="font-size:0.85rem;margin-top:0.5rem;">Blocked for claim-making, but useful as a boundary.</p>
            """,
            unsafe_allow_html=True,
        )

    with c5:
        st.markdown(
            """
<div style="background:#6B7280;color:#FFFFFF;font-weight:900;padding:0.35rem 0.75rem;border-radius:999px;text-align:center;">
GRAY - awaiting data
</div>
<p style="font-size:0.85rem;margin-top:0.5rem;">Not scored yet. This is not a zero score.</p>
            """,
            unsafe_allow_html=True,
        )

def _dti_render_parameter_quality_matrix_v1g():
    import streamlit as st
    import pandas as pd

    st.markdown("### Legacy/detail Parameter Quality Matrix 3 — audit view")
    st.info(
        "This matrix highlights promising parameter directions, control-needed zones, and blocked claim paths. "
        "Scores are UI meta-scores for research triage only; they are not likelihood, posterior, Planck, or physics-value results."
    )

    _dti_render_color_meaning_v1g()

    rows = [
        {
            "parameter": "omega_cdm",
            "research_role": "compensating direction",
            "role_group": "Matter-sector compensation",
            "current_value": "selected profile",
            "positive_signal": "Can identify a narrow compensating parameter direction.",
            "risk_blocker": "Needs companion-variable and seed-stability checks.",
            "stability": 13,
            "signal": 15,
            "control": 13,
            "risk": 7,
            "next_test": "Audit whether the compensating direction remains narrow and sign-stable.",
            "safe_interpretation": "Candidate compensating parameter direction.",
        },
        {
            "parameter": "A_planck / calibration",
            "research_role": "nuisance-control boundary",
            "role_group": "Calibration and nuisance control",
            "current_value": "selected profile",
            "positive_signal": "Can test whether a result survives nuisance-control restrictions.",
            "risk_blocker": "Must not be used as a physics mechanism.",
            "stability": 13,
            "signal": 13,
            "control": 14,
            "risk": 7,
            "next_test": "Repeat under FIX or TIGHT nuisance boundaries before stronger wording.",
            "safe_interpretation": "Nuisance-boundedness check.",
        },
        {
            "parameter": "H0",
            "research_role": "branch coordinate",
            "role_group": "Branch geometry",
            "current_value": "selected profile",
            "positive_signal": "Can expose branch-level response direction.",
            "risk_blocker": "Not sufficient alone for a cosmological claim.",
            "stability": 12,
            "signal": 16,
            "control": 12,
            "risk": 8,
            "next_test": "Compare fixed-H0 branches under the same audit boundary.",
            "safe_interpretation": "Useful branch label and response coordinate.",
        },
        {
            "parameter": "f_EDE",
            "research_role": "early-time scan coordinate",
            "role_group": "Early-time modification",
            "current_value": "selected profile",
            "positive_signal": "Can mark a controlled early-time modification direction.",
            "risk_blocker": "Requires source-locked comparison before mechanism language.",
            "stability": 10,
            "signal": 15,
            "control": 10,
            "risk": 9,
            "next_test": "Check whether the same pattern persists across adjacent f_EDE values.",
            "safe_interpretation": "Promising controlled scan coordinate.",
        },
        {
            "parameter": "sigma8 / S8",
            "research_role": "stress indicator",
            "role_group": "Growth-stress diagnostic",
            "current_value": "selected profile",
            "positive_signal": "Can reveal growth-stress burden and residual tension.",
            "risk_blocker": "A stress indicator is not by itself a model proof.",
            "stability": 10,
            "signal": 14,
            "control": 10,
            "risk": 10,
            "next_test": "Separate diagnostic stress from claim-level evidence.",
            "safe_interpretation": "Diagnostic stress coordinate.",
        },
        {
            "parameter": "omega_b",
            "research_role": "baryon-sector control",
            "role_group": "Control parameter",
            "current_value": "selected profile",
            "positive_signal": "Can help separate baryon-sector load from dark-sector load.",
            "risk_blocker": "Usually not sufficient as the main driver.",
            "stability": 10,
            "signal": 9,
            "control": 11,
            "risk": 8,
            "next_test": "Hold other parameters fixed and inspect whether the response is load-bearing.",
            "safe_interpretation": "Useful control parameter.",
        },
        {
            "parameter": "n_s",
            "research_role": "spectral-tilt companion",
            "role_group": "Shape compensation",
            "current_value": "selected profile",
            "positive_signal": "Can expose spectral-tilt compensation.",
            "risk_blocker": "Needs CMB-shape consistency checks before strong interpretation.",
            "stability": 9,
            "signal": 10,
            "control": 9,
            "risk": 9,
            "next_test": "Check whether tilt movement is companion behavior or a primary driver.",
            "safe_interpretation": "Companion shape parameter.",
        },
        {
            "parameter": "unconnected future parameter",
            "research_role": "awaiting data",
            "role_group": "Future source-of-record slot",
            "current_value": "not connected",
            "positive_signal": "Reserved for a future audited parameter direction.",
            "risk_blocker": "No source-of-record input yet.",
            "stability": 0,
            "signal": 0,
            "control": 0,
            "risk": 0,
            "next_test": "Connect audited source data before scoring.",
            "safe_interpretation": "Awaiting data; not a zero score.",
            "force_gray": True,
        },
    ]

    for row in rows:
        if row.get("force_gray"):
            row["quality_score"] = None
            row["claim_readiness"] = None
            row["quality_badge"] = "GRAY - awaiting data"
        else:
            raw = int(row["stability"]) + int(row["signal"]) + int(row["control"]) - int(row["risk"])
            score = max(0, min(100, int(round(raw * 100 / 60))))
            row["quality_score"] = score
            row["claim_readiness"] = max(1, min(7, int(round(score * 7 / 100))))
            row["quality_badge"] = _dti_parameter_quality_badge_v1g(score)

    df = pd.DataFrame(rows)

    display_cols = [
        "parameter",
        "research_role",
        "role_group",
        "current_value",
        "quality_badge",
        "quality_score",
        "claim_readiness",
        "positive_signal",
        "risk_blocker",
        "next_test",
        "safe_interpretation",
    ]

    df_view = df[display_cols].copy()

    sort_df = df.copy()
    sort_df["quality_sort"] = sort_df["quality_score"].fillna(-1)
    sort_df["readiness_sort"] = sort_df["claim_readiness"].fillna(-1)
    sort_df = sort_df.sort_values(["quality_sort", "readiness_sort"], ascending=False)

    st.markdown("#### Legacy total evaluation table")
    st.caption(
        "Sorted by quality score, claim readiness, and control score. "
        "GRAY means awaiting data, not zero quality."
    )

    try:
        styled = df_view.style.apply(_dti_parameter_quality_row_style_v1g, axis=1)
        _dti_arrow_safe_df_v1(styled, width="stretch", hide_index=True)
    except Exception:
        _dti_arrow_safe_df_v1(df_view, width="stretch", hide_index=True)

    st.markdown("#### Legacy next-test priority order")
    st.caption("This is the practical test order, not a scientific ranking of truth.")

    force_gray_mask = sort_df.get("force_gray")
    if force_gray_mask is None:
        force_gray_mask = False
    else:
        force_gray_mask = force_gray_mask.fillna(False).astype(bool)
    priority_rows = sort_df[~force_gray_mask].head(5)

    for idx, row in enumerate(priority_rows.to_dict("records"), start=1):
        badge = row["quality_badge"]
        badge_style = _dti_parameter_quality_badge_style_v1g(badge)
        st.markdown(
            f"""
<div style="border:1px solid rgba(255,255,255,0.18);border-radius:0.75rem;padding:0.85rem;margin:0.65rem 0;">
  <div style="display:flex;gap:0.75rem;align-items:center;flex-wrap:wrap;">
    <strong>{idx}. {row['parameter']}</strong>
    <span style="{badge_style};padding:0.22rem 0.65rem;">{badge}</span>
    <span style="opacity:0.85;">score {row['quality_score']}/100 · readiness {row['claim_readiness']}/7</span>
  </div>
  <div style="margin-top:0.55rem;"><strong>Role:</strong> {row['research_role']} / {row['role_group']}</div>
  <div><strong>Current value:</strong> {row['current_value']}</div>
  <div><strong>Why it matters:</strong> {row['positive_signal']}</div>
  <div><strong>Next test:</strong> {row['next_test']}</div>
  <div><strong>Safe wording:</strong> {row['safe_interpretation']}</div>
</div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### How to read this matrix")
    st.code(
        """Use rule:
1. GREEN and YELLOW are research leads.
2. ORANGE is not bad; it means control is needed before stronger wording.
3. RED is blocked for claim-making, but can still define a useful boundary.
4. GRAY is awaiting data. It is not a zero score.
5. Do not use this matrix as likelihood, posterior, Planck validation, graph proof, or final physics evidence.""",
        language="text",
    )

    st.caption(
        "Boundary: Parameter Quality Matrix V1G is UI/meta-scoring only. "
        "It does not perform likelihood evaluation, posterior comparison, Planck validation, graph rendering, "
        "7c execution, physics-value updates, manuscript updates, Render API modification, or Streamlit Secret modification."
    )
# --- /DTI_PARAMETER_QUALITY_MATRIX_VISUAL_V1G ---




# --- DTI_PROBE_RESULT_VALUE_MATRIX_V1 ---
# Positive probe-result value matrix for 7a / 7b / 7c.
# UI and meta-scoring only.
# This does not execute 7c, enable graph rendering, run likelihood evaluation,
# posterior comparison, Planck validation, physics-value updates, manuscript updates,
# Render API changes, or Streamlit Secret changes.
_DTI_PROBE_RESULT_VALUE_MATRIX_V1 = True

def _dti_probe_value_label_v1(score):
    try:
        value = int(score)
    except Exception:
        value = 0
    if value >= 80:
        return "GREEN - strong research value"
    if value >= 60:
        return "YELLOW - useful research value"
    if value >= 40:
        return "ORANGE - control needed"
    if value >= 20:
        return "RED - blocked for claim"
    return "GRAY - awaiting result"

def _dti_probe_score_v1(positive_value, confidence, next_clarity, boundary_risk):
    try:
        raw = int(positive_value) + int(confidence) + int(next_clarity) - int(boundary_risk)
    except Exception:
        raw = 0
    return max(0, min(100, int(round(raw * 100 / 60))))

def _dti_render_probe_result_value_matrix_v1():
    import streamlit as st
    import pandas as pd

    st.markdown("### Probe Result Value Matrix")

    st.info(
        "This matrix turns 7a / 7b / 7c probe states into a positive research-value summary. "
        "It helps separate what is already useful, what is partial, what is blocked, and what should be tested next. "
        "It is not a likelihood result, posterior comparison, Planck validation, graph result, or physics-value update."
    )

    st.markdown("#### Legacy color meaning")

    color_cols = st.columns(5)

    with color_cols[0]:
        st.markdown(
            "<div style='background:#16a34a;color:white;padding:9px 12px;border-radius:999px;"
            "font-weight:800;text-align:center;'>GREEN - strong value</div>"
            "<div style='font-size:0.85rem;margin-top:6px;'>Reusable result or benchmark. Prioritize source-lock and follow-up.</div>",
            unsafe_allow_html=True,
        )

    with color_cols[1]:
        st.markdown(
            "<div style='background:#facc15;color:#111827;padding:9px 12px;border-radius:999px;"
            "font-weight:800;text-align:center;'>YELLOW - useful value</div>"
            "<div style='font-size:0.85rem;margin-top:6px;'>Constructive partial result. Good for exploratory planning.</div>",
            unsafe_allow_html=True,
        )

    with color_cols[2]:
        st.markdown(
            "<div style='background:#f97316;color:white;padding:9px 12px;border-radius:999px;"
            "font-weight:800;text-align:center;'>ORANGE - control needed</div>"
            "<div style='font-size:0.85rem;margin-top:6px;'>Useful, but needs stricter checks before stronger wording.</div>",
            unsafe_allow_html=True,
        )

    with color_cols[3]:
        st.markdown(
            "<div style='background:#ef4444;color:white;padding:9px 12px;border-radius:999px;"
            "font-weight:800;text-align:center;'>RED - blocked</div>"
            "<div style='font-size:0.85rem;margin-top:6px;'>Blocked for claim-making, but useful as a boundary.</div>",
            unsafe_allow_html=True,
        )

    with color_cols[4]:
        st.markdown(
            "<div style='background:#9ca3af;color:white;padding:9px 12px;border-radius:999px;"
            "font-weight:800;text-align:center;'>GRAY - awaiting</div>"
            "<div style='font-size:0.85rem;margin-top:6px;'>No result yet. This is not a zero score.</div>",
            unsafe_allow_html=True,
        )

    st.markdown("#### Probe value summary")

    rows = [
        {
            "probe": "7a",
            "probe_name": "AxiCLASS fixed-example check",
            "research_role": "locked benchmark",
            "probe_state": "available / source-locked example",
            "positive_value": 18,
            "confidence": 17,
            "next_clarity": 15,
            "boundary_risk": 5,
            "what_it_gives": "A stable reference point for checking that the app and API path can return the expected fixed-example result.",
            "what_it_does_not_give": "It does not prove likelihood preference, posterior dominance, Planck validation, or a new physics mechanism.",
            "best_use": "Use as a confidence anchor before interpreting more exploratory probes.",
            "next_action": "Keep the fixed example source-locked and compare later changes against this benchmark.",
            "safe_positive_wording": "7a provides a useful source-locked benchmark result.",
        },
        {
            "probe": "7b",
            "probe_name": "Vanilla-profile API check",
            "research_role": "live exploratory probe",
            "probe_state": "available / bounded derived quantities",
            "positive_value": 15,
            "confidence": 12,
            "next_clarity": 16,
            "boundary_risk": 8,
            "what_it_gives": "A quick derived-quantity response for the selected profile, useful for intuition and implementation checks.",
            "what_it_does_not_give": "It is not a likelihood evaluation, posterior comparison, Planck validation, or manuscript checkpoint.",
            "best_use": "Use as a fast research-direction clue before deciding whether a stricter audited run is worth doing.",
            "next_action": "Compare whether the selected profile suggests a stable direction worth source-locking.",
            "safe_positive_wording": "7b provides a useful exploratory signal, bounded by non-likelihood interpretation.",
        },
        {
            "probe": "7c",
            "probe_name": "Continuity / discontinuity examiner",
            "research_role": "deferred high-value test",
            "probe_state": "disabled / intentionally bounded",
            "positive_value": 12,
            "confidence": 8,
            "next_clarity": 18,
            "boundary_risk": 10,
            "what_it_gives": "A clearly defined future test target. Disabled status is useful boundary control, not a failure.",
            "what_it_does_not_give": "It does not currently establish continuity, discontinuity, physical transition, or graph-based proof.",
            "best_use": "Use as a future design lane after source-of-record rules and execution boundary are fixed.",
            "next_action": "Design 7c as a controlled local-only or source-locked test before allowing public execution.",
            "safe_positive_wording": "7c is a high-value deferred probe with a clear future-test role.",
        },
    ]

    for row in rows:
        score = _dti_probe_score_v1(
            row["positive_value"],
            row["confidence"],
            row["next_clarity"],
            row["boundary_risk"],
        )
        row["research_score"] = score
        row["value_badge"] = _dti_probe_value_label_v1(score)
        row["claim_readiness"] = max(0, min(7, int(round(score * 7 / 100))))

    df = pd.DataFrame(rows)

    compact_cols = [
        "probe",
        "probe_name",
        "research_role",
        "probe_state",
        "value_badge",
        "research_score",
        "claim_readiness",
    ]

    def style_probe_value_matrix_v1(dataframe):
        def cell_style(value):
            s = "" if value is None else str(value)
            if "GREEN" in s:
                return "background-color:#16a34a;color:white;font-weight:800"
            if "YELLOW" in s:
                return "background-color:#facc15;color:#111827;font-weight:800"
            if "ORANGE" in s:
                return "background-color:#f97316;color:white;font-weight:800"
            if "RED" in s:
                return "background-color:#ef4444;color:white;font-weight:800"
            if "GRAY" in s:
                return "background-color:#9ca3af;color:white;font-weight:800"
            return ""
        return dataframe.style.map(cell_style, subset=["value_badge"])

    _dti_arrow_safe_df_v1(
        style_probe_value_matrix_v1(df[compact_cols]), width="stretch",
        hide_index=True,
    )

    st.markdown("#### Positive probe interpretation")

    sorted_df = df.sort_values(["research_score", "claim_readiness"], ascending=False)

    for index, row in sorted_df.iterrows():
        badge = str(row["value_badge"])
        badge_color = "#9ca3af"
        text_color = "white"
        if "GREEN" in badge:
            badge_color = "#16a34a"
        elif "YELLOW" in badge:
            badge_color = "#facc15"
            text_color = "#111827"
        elif "ORANGE" in badge:
            badge_color = "#f97316"
        elif "RED" in badge:
            badge_color = "#ef4444"

        st.markdown(
            "<div style='border:1px solid #374151;border-radius:12px;padding:12px 14px;margin:10px 0;'>"
            f"<div style='font-weight:800;font-size:1.02rem;'>{row['probe']}. {row['probe_name']} "
            f"<span style='background:{badge_color};color:{text_color};padding:4px 9px;border-radius:999px;"
            f"font-size:0.78rem;margin-left:6px;'>{badge}</span> "
            f"<span style='font-size:0.88rem;'>score {row['research_score']}/100 · readiness {row['claim_readiness']}/7</span></div>"
            f"<div style='margin-top:7px;'><b>Research role:</b> {row['research_role']}</div>"
            f"<div><b>Current state:</b> {row['probe_state']}</div>"
            f"<div><b>Positive value:</b> {row['what_it_gives']}</div>"
            f"<div><b>Boundary:</b> {row['what_it_does_not_give']}</div>"
            f"<div><b>Best use:</b> {row['best_use']}</div>"
            f"<div><b>Next action:</b> {row['next_action']}</div>"
            f"<div><b>Safe wording:</b> {row['safe_positive_wording']}</div>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("#### Research-fun summary")

    st.success(
        "Use this section as a research dashboard: 7a anchors confidence, 7b generates exploratory clues, "
        "and 7c marks a high-value future test. A disabled or partial probe is not automatically negative; "
        "it can clarify the next experiment."
    )

    st.code(
        """Probe result answer:
Which probe is useful now?

Positive value:
What did this probe clarify?

Boundary:
What should not be claimed from this probe?

Next experiment:
What would make this probe more claim-ready?""",
        language="text",
    )

    st.caption(
        "Boundary: this Probe Result Value Matrix is UI/meta-evaluation only. "
        "It does not execute 7c, draw graphs, run likelihood evaluation, compare posteriors, validate Planck, "
        "update physics values, update manuscript content, modify Render API settings, or modify Streamlit Secrets."
    )
# --- /DTI_PROBE_RESULT_VALUE_MATRIX_V1 ---



# --- DTI_READOUT_CARD_DETAIL_GUIDE_V1B ---
# Independent explanation layer for Current input model safety/readout cards.
# Safe insertion policy:
# - Do not modify the existing readout card columns.
# - Do not enter existing button / if / with blocks.
# - Use a separate guide immediately after the readout-card section header.
# - UI explanation only; no likelihood, posterior, Planck validation, graph rendering, 7c execution, physics update, or manuscript update.
_DTI_READOUT_CARD_DETAIL_GUIDE_V1B = True

def _dti_readout_card_detail_rows_v1b():
    return [
        {
            "name": "H0",
            "role": "branch coordinate / fixed-H0 label",
            "why": "H0 identifies which branch-like basin or fixed-H0 representative the current input is probing.",
            "safe": "Treat it as a scenario label or branch coordinate inside the app, not as a standalone cosmological conclusion.",
            "not_claim": "Do not claim that this card alone validates, excludes, or solves a cosmological model.",
            "next": "Compare the same probe under controlled neighboring settings and check whether the response direction is stable.",
        },
        {
            "name": "f_EDE",
            "role": "early-time modification scan coordinate",
            "why": "f_EDE marks the controlled deformation direction used to explore whether the response pattern changes across the scan.",
            "safe": "Useful as a bounded scan coordinate and triage variable.",
            "not_claim": "Do not claim mechanism proof or model validation from this single readout.",
            "next": "Check adjacent f_EDE values and preserve the same source-lock / audit boundary.",
        },
        {
            "name": "omega_cdm",
            "role": "dark-sector compensation direction",
            "why": "omega_cdm can indicate how much compensating burden shifts into the cold-dark-matter sector.",
            "safe": "Use it as a candidate companion direction when interpreting branch response.",
            "not_claim": "Do not claim posterior preference from the card alone.",
            "next": "Inspect sign stability and whether the shift survives fixed nuisance controls.",
        },
        {
            "name": "omega_b",
            "role": "baryon-sector control coordinate",
            "why": "omega_b helps separate baryon-load changes from dark-sector or H0-linked compensation.",
            "safe": "Useful as a control or diagnostic coordinate.",
            "not_claim": "Do not overread it as the main driver unless an audited run supports that.",
            "next": "Compare it against omega_cdm and H0 response under the same profile settings.",
        },
        {
            "name": "n_s",
            "role": "spectral-tilt compensation coordinate",
            "why": "n_s can show whether the current input is relying on tilt-like compensation.",
            "safe": "Read as a compensation indicator, not as a final physical explanation.",
            "not_claim": "Do not claim a validated tilt mechanism from the UI card.",
            "next": "Check whether the same compensation appears in source-locked or run-derived outputs.",
        },
        {
            "name": "z_c",
            "role": "transition / timing coordinate",
            "why": "z_c marks where the early-time feature is placed in the model input.",
            "safe": "Use it to understand timing sensitivity in the current input profile.",
            "not_claim": "Do not infer a detected physical transition from this card.",
            "next": "Test neighboring timing choices only through explicit controlled probes.",
        },
        {
            "name": "theta_i",
            "role": "initial-condition / model-shape coordinate",
            "why": "theta_i affects the model shape and can change the qualitative profile behavior.",
            "safe": "Useful for checking whether the input is exploring the intended family region.",
            "not_claim": "Do not treat it as evidence for a preferred physical initial condition.",
            "next": "Keep it source-locked when comparing profiles.",
        },
        {
            "name": "A_s / ln10^10 A_s",
            "role": "amplitude-side companion coordinate",
            "why": "Amplitude-side movement can matter when interpreting whether the response is broad or narrow.",
            "safe": "Use as a companion readout when checking whether the current profile is internally plausible.",
            "not_claim": "Do not claim Planck validation or likelihood improvement from the card.",
            "next": "Compare only against real run-derived or live API outputs when available.",
        },
        {
            "name": "tau_reio",
            "role": "reionization / amplitude-degeneracy control",
            "why": "tau_reio can signal whether the current profile is relying on a known degeneracy direction.",
            "safe": "Use as a caution flag and control readout.",
            "not_claim": "Do not interpret it as posterior evidence.",
            "next": "Keep the interpretation bounded unless a formal likelihood run is performed.",
        },
        {
            "name": "readout status",
            "role": "safety and usability state",
            "why": "The card labels help decide whether the current input is usable for intuition, needs control, or should be treated as awaiting data.",
            "safe": "Use it for research navigation and next-test design.",
            "not_claim": "Do not convert the label into a model claim.",
            "next": "Use 7a / 7b status-linked probe output and the Parameter Quality Matrix before making any stronger statement.",
        },
    ]

def _dti_render_one_readout_detail_v1b(row):
    import streamlit as st

    label = f"{row['name']} — {row['role']}"

    if hasattr(st, "popover"):
        with st.popover(label, width="stretch"):
            st.markdown(f"**Research role:** {row['role']}")
            st.markdown(f"**Why it matters:** {row['why']}")
            st.markdown(f"**Safe interpretation:** {row['safe']}")
            st.markdown(f"**Do not claim:** {row['not_claim']}")
            st.markdown(f"**Next check:** {row['next']}")
    else:
        with st.expander(label, expanded=False):
            st.markdown(f"**Research role:** {row['role']}")
            st.markdown(f"**Why it matters:** {row['why']}")
            st.markdown(f"**Safe interpretation:** {row['safe']}")
            st.markdown(f"**Do not claim:** {row['not_claim']}")
            st.markdown(f"**Next check:** {row['next']}")

def _dti_render_readout_card_detail_guide_v1b():
    import streamlit as st

    st.markdown("#### Readout card detail guide")
    st.caption(
        "Open a detail item to see what each current-input card means, what it can teach, "
        "what remains bounded, and what the next safe check should be. "
        "This is explanation only, not likelihood evaluation, posterior comparison, Planck validation, "
        "graph rendering, 7c execution, or a physics-value update."
    )

    rows = _dti_readout_card_detail_rows_v1b()

    tabs = st.tabs(["Core branch", "Companion parameters", "Safety / next checks"])

    with tabs[0]:
        for row in rows:
            if row["name"] in ["H0", "f_EDE", "z_c", "theta_i"]:
                _dti_render_one_readout_detail_v1b(row)

    with tabs[1]:
        for row in rows:
            if row["name"] in ["omega_cdm", "omega_b", "n_s", "A_s / ln10^10 A_s", "tau_reio"]:
                _dti_render_one_readout_detail_v1b(row)

    with tabs[2]:
        for row in rows:
            if row["name"] == "readout status":
                _dti_render_one_readout_detail_v1b(row)

        st.info(
            "Reading rule: these cards are navigation aids. They can make the current input easier to understand, "
            "but they do not create a likelihood result, posterior comparison, Planck validation, or model exclusion."
        )
# --- /DTI_READOUT_CARD_DETAIL_GUIDE_V1B ---


# --- DTI_VISITOR_QUICK_GUIDE_V1 ---
# First-visitor orientation layer.
# UI explanation only. This does not enable 7c, graph rendering, likelihood evaluation,
# posterior comparison, Planck validation, physics-value updates, manuscript updates,
# Render API changes, or Streamlit Secret changes.
_DTI_VISITOR_QUICK_GUIDE_V1 = True

def _dti_render_visitor_quick_guide_v1():
    import streamlit as st

    st.markdown("### Visitor Quick Guide")

    st.info(
        "Start here if this is your first time reading the app. "
        "The app is a research-navigation dashboard: it shows locked references, "
        "promising parameter directions, probe value, and safe next tests. "
        "It is not a likelihood engine, posterior comparison, Planck validation, or final physics claim."
    )

    guide_col_1, guide_col_2, guide_col_3 = st.columns(3)

    with guide_col_1:
        st.markdown(
            """
**Recommended reading order**

1. Section 5: locked benchmark values
2. Parameter Quality Matrix
3. Probe Result Value Matrix
4. 7a / 7b live checks
5. Next controlled test
            """
        )

    with guide_col_2:
        st.markdown(
            """
**This app can help answer**

- Which benchmark values are locked
- Which directions look promising
- What each probe teaches
- What remains blocked
- What to test next
            """
        )

    with guide_col_3:
        st.markdown(
            """
**This app cannot claim**

- Final cosmological truth
- Posterior superiority
- Planck validation
- New-physics proof
- 7c closure
            """
        )

    st.markdown("#### Section flow")

    st.code(
        """Locked benchmark
        ↓
Parameter Quality Matrix
        ↓
Probe Result Value Matrix
        ↓
7a / 7b live checks
        ↓
Next controlled test""",
        language="text",
    )

    st.markdown("#### Current best next action")

    st.success(
        "Use Section 5 to anchor the locked benchmark. "
        "Use Parameter Quality Matrix to identify promising directions. "
        "Use Probe Result Value Matrix to interpret what 7a / 7b teach. "
        "Keep 7c deferred unless explicitly approved."
    )

    with st.expander("Boundary note for reviewers and researchers", expanded=False):
        st.markdown(
            """
This guide is an orientation layer only.

It does not change solver behavior, data values, likelihood interpretation,
posterior interpretation, Planck validation, graph rendering, 7c state,
manuscript content, Render API settings, or Streamlit Secrets.

Use it to decide where to look first and how to read the app safely.
            """
        )
# --- /DTI_VISITOR_QUICK_GUIDE_V1 ---


# --- DTI_PROBE_RESULT_VALUE_MATRIX_V2 ---
# Status-linked positive probe evaluation.
# Reads available 7a / 7b session/API status signals when present.
# Keeps 7c disabled and deferred.
# UI/meta-evaluation only. Does not execute 7c, render graphs, evaluate likelihoods,
# compare posteriors, validate Planck, update physics values, update manuscript,
# modify Render API, or modify Streamlit Secrets.
_DTI_PROBE_RESULT_VALUE_MATRIX_V2 = True

def _dti_probe_v2_as_text(obj, limit=900):
    try:
        if obj is None:
            return ""
        if isinstance(obj, str):
            return obj[:limit]
        if isinstance(obj, (int, float, bool)):
            return str(obj)
        if isinstance(obj, dict):
            return " ".join([str(k) + " " + _dti_probe_v2_as_text(v, 180) for k, v in list(obj.items())[:20]])[:limit]
        if isinstance(obj, (list, tuple)):
            return " ".join([_dti_probe_v2_as_text(v, 180) for v in list(obj)[:20]])[:limit]
        return str(obj)[:limit]
    except Exception:
        return ""

def _dti_probe_v2_collect_session_hits(probe_key):
    import streamlit as st

    probe_key = str(probe_key).lower()
    include_terms = []
    if probe_key == "7a":
        include_terms = ["7a", "fixed", "axiclass", "compact"]
    elif probe_key == "7b":
        include_terms = ["7b", "vanilla", "profile"]
    else:
        include_terms = ["7c", "continuity", "discontinuity"]

    hits = []
    try:
        keys = list(st.session_state.keys())
    except Exception:
        keys = []

    for k in keys:
        ks = str(k).lower()
        if any(term in ks for term in include_terms):
            try:
                v = st.session_state.get(k)
            except Exception:
                v = None
            hits.append({"key": str(k), "value_text": _dti_probe_v2_as_text(v)})
    return hits[:16]

def _dti_probe_v2_status_from_hits(probe_key, hits):
    joined = " ".join([(h.get("key", "") + " " + h.get("value_text", "")) for h in hits]).lower()

    if probe_key == "7c":
        return {
            "actual_status": "deferred / disabled",
            "value_badge": "ORANGE - deferred high-value test",
            "research_score": 47,
            "claim_readiness": 3,
            "learned": "7c is not executed. The useful result is a protected boundary: continuity/discontinuity is kept as a future test, not a premature claim.",
            "blocking": "No 7c execution, no continuity closure, no discontinuity proof.",
            "next_experiment": "Only after explicit approval: design a source-locked continuity test with disabled-state provenance preserved.",
            "safe_wording": "7c remains a high-value deferred probe with a clear future-test role.",
        }

    if not joined.strip():
        if probe_key == "7a":
            return {
                "actual_status": "not observed in session",
                "value_badge": "GRAY - awaiting run/status",
                "research_score": 40,
                "claim_readiness": 3,
                "learned": "No current 7a session result was detected. The probe remains useful as a source-locked benchmark lane once executed.",
                "blocking": "No live session status was available to promote the probe value.",
                "next_experiment": "Run or warm 7a, then re-check whether a fixed-example status appears in session state.",
                "safe_wording": "7a is prepared as a benchmark probe, but current status was not observed.",
            }
        return {
            "actual_status": "not observed in session",
            "value_badge": "GRAY - awaiting run/status",
            "research_score": 38,
            "claim_readiness": 2,
            "learned": "No current 7b session result was detected. The probe remains useful as an exploratory bounded-profile lane once executed.",
            "blocking": "No live session status was available to promote the probe value.",
            "next_experiment": "Run or warm 7b, then re-check whether a bounded-profile status appears in session state.",
            "safe_wording": "7b is prepared as an exploratory probe, but current status was not observed.",
        }

    positive_terms = ["ok", "success", "available", "ready", "200", "pass", "completed", "result", "payload", "returned"]
    warning_terms = ["timeout", "pending", "sleep", "warm", "retry", "partial", "none"]
    negative_terms = ["error", "failed", "exception", "traceback", "unavailable", "blocked"]

    pos = sum(1 for t in positive_terms if t in joined)
    warn = sum(1 for t in warning_terms if t in joined)
    neg = sum(1 for t in negative_terms if t in joined)

    if pos >= 2 and neg == 0:
        badge = "GREEN - useful returned value"
        score = 76 if probe_key == "7a" else 68
        readiness = 5 if probe_key == "7a" else 4
        status = "available / returned status detected"
    elif pos >= 1 and neg <= 1:
        badge = "YELLOW - useful partial value"
        score = 64 if probe_key == "7a" else 58
        readiness = 4
        status = "partial / useful status detected"
    elif neg >= 1 and pos == 0:
        badge = "ORANGE - blocked or needs retry"
        score = 43
        readiness = 2
        status = "blocked / retry-needed status detected"
    else:
        badge = "YELLOW - informative session signal"
        score = 55
        readiness = 3
        status = "informative session signal detected"

    if probe_key == "7a":
        learned = "7a can anchor interpretation by checking whether the fixed-example benchmark/API path returns a usable status."
        blocking = "It is still not a likelihood, posterior, Planck validation, or mechanism proof."
        next_experiment = "Use 7a as the benchmark anchor, then compare exploratory 7b signals against this locked reference."
        safe_wording = "7a provides a useful source-locked benchmark signal when available."
    else:
        learned = "7b can identify whether the current vanilla/profile lane returns a bounded exploratory signal."
        blocking = "It is still an exploratory derived-quantity probe, not a posterior or Planck result."
        next_experiment = "Use 7b to identify promising profile directions, then confirm them with stricter source-locked checks."
        safe_wording = "7b provides a useful exploratory signal under bounded non-likelihood interpretation."

    return {
        "actual_status": status,
        "value_badge": badge,
        "research_score": score,
        "claim_readiness": readiness,
        "learned": learned,
        "blocking": blocking,
        "next_experiment": next_experiment,
        "safe_wording": safe_wording,
    }

def _dti_probe_v2_badge_color(badge):
    b = str(badge).upper()
    if "GREEN" in b:
        return "#16a34a"
    if "YELLOW" in b:
        return "#eab308"
    if "ORANGE" in b:
        return "#f97316"
    if "RED" in b:
        return "#ef4444"
    return "#9ca3af"

def _dti_render_probe_result_value_matrix_v2():
    import streamlit as st
    import pandas as pd

    st.markdown("### Probe Result Value Matrix V2")
    st.info(
        "This matrix reads available 7a / 7b session status signals and converts them into a positive research-value summary. "
        "7c remains disabled and deferred. This is still UI/meta-evaluation only, not likelihood, posterior, Planck, graph, or physics-value output."
    )

    rows = []
    for probe_key, probe_name, research_role in [
        ("7a", "AxiCLASS fixed-example check", "locked benchmark anchor"),
        ("7b", "Vanilla-profile API check", "exploratory bounded-profile signal"),
        ("7c", "Continuity / discontinuity examiner", "deferred high-value future test"),
    ]:
        hits = _dti_probe_v2_collect_session_hits(probe_key)
        status = _dti_probe_v2_status_from_hits(probe_key, hits)
        rows.append({
            "probe": probe_key,
            "probe_name": probe_name,
            "research_role": research_role,
            "actual_status": status["actual_status"],
            "value_badge": status["value_badge"],
            "research_score": status["research_score"],
            "claim_readiness": status["claim_readiness"],
            "what_this_teaches": status["learned"],
            "what_remains_blocked": status["blocking"],
            "next_experiment": status["next_experiment"],
            "safe_wording": status["safe_wording"],
            "session_hits": len(hits),
        })

    df = pd.DataFrame(rows)

    st.markdown("#### Probe value summary")
    compact_cols = [
        "probe",
        "probe_name",
        "research_role",
        "actual_status",
        "value_badge",
        "research_score",
        "claim_readiness",
        "session_hits",
    ]
    _dti_arrow_safe_df_v1(df[compact_cols], width="stretch", hide_index=True)

    st.markdown("#### What each probe teaches")

    for _, row in df.iterrows():
        color = _dti_probe_v2_badge_color(row["value_badge"])
        st.markdown(
            f"""
<div style="border:1px solid rgba(255,255,255,0.18); border-radius:12px; padding:14px; margin:12px 0;">
  <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
    <b>{row['probe']}. {row['probe_name']}</b>
    <span style="background:{color}; color:white; border-radius:999px; padding:4px 10px; font-weight:700; font-size:12px;">
      {row['value_badge']}
    </span>
    <span>score {row['research_score']}/100 · readiness {row['claim_readiness']}/7 · session hits {row['session_hits']}</span>
  </div>
  <div style="margin-top:10px;"><b>Actual status:</b> {row['actual_status']}</div>
  <div><b>What this teaches:</b> {row['what_this_teaches']}</div>
  <div><b>What remains blocked:</b> {row['what_remains_blocked']}</div>
  <div><b>Next experiment:</b> {row['next_experiment']}</div>
  <div><b>Safe wording:</b> {row['safe_wording']}</div>
</div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Research-use answer")
    best = df.sort_values(["research_score", "claim_readiness"], ascending=False).iloc[0]
    st.success(
        f"Most useful current probe: {best['probe']} / {best['probe_name']}. "
        f"It is classified as {best['value_badge']} with score {best['research_score']}/100. "
        f"The research value is: {best['what_this_teaches']}"
    )

    st.code(
        "Probe result answer:\n"
        "What did we learn from the probe?\n"
        "- Use 7a as benchmark anchoring when available.\n"
        "- Use 7b as bounded exploratory signal when available.\n"
        "- Keep 7c as deferred high-value future test unless explicitly approved.\n\n"
        "What remains blocked?\n"
        "- No likelihood evaluation.\n"
        "- No posterior comparison.\n"
        "- No Planck validation.\n"
        "- No graph-based proof.\n"
        "- No physics-value or manuscript update.\n\n"
        "Next experiment:\n"
        "- Re-run or warm 7a/7b, then watch whether their actual status moves from awaiting/partial to useful returned value.",
        language="text",
    )

    st.caption(
        "Boundary: Probe Result Value Matrix V2 reads available session/API status signals only. "
        "It does not execute 7c, draw graphs, evaluate likelihoods, compare posteriors, validate Planck, "
        "update physics values, update manuscript text, modify Render API, or modify Streamlit Secrets."
    )
# --- /DTI_PROBE_RESULT_VALUE_MATRIX_V2 ---



# --- DTI_PARAMETER_QUALITY_MATRIX_COMPACT_V1H ---
# Compact Parameter Quality Matrix.
# UI and meta-scoring only.
# This does not enable 7c, graph rendering, likelihood evaluation,
# posterior comparison, Planck validation, physics-value updates,
# manuscript updates, Render API changes, or Streamlit Secret changes.
_DTI_PARAMETER_QUALITY_MATRIX_COMPACT_V1H = True

def _dti_parameter_quality_badge_v1h(score):
    try:
        value = int(score)
    except Exception:
        return "GRAY - awaiting data"
    if value >= 80:
        return "GREEN - strong lead"
    if value >= 60:
        return "YELLOW - useful partial"
    if value >= 40:
        return "ORANGE - needs control"
    if value >= 20:
        return "RED - blocked for claim"
    return "GRAY - awaiting data"

def _dti_parameter_quality_score_v1h(stability, signal, control, risk):
    try:
        raw = int(stability) + int(signal) + int(control) - int(risk)
    except Exception:
        raw = 0
    return max(0, min(100, int(round(raw * 100 / 60))))

def _dti_parameter_quality_badge_style_v1h(row):
    badge = str(row.get("quality_badge", ""))
    styles = []
    for col in row.index:
        color = ""
        if col in ["quality_badge", "quality_score", "claim_readiness"]:
            if badge.startswith("GREEN"):
                color = "background-color: #00A86B; color: white; font-weight: 800;"
            elif badge.startswith("YELLOW"):
                color = "background-color: #FFC400; color: black; font-weight: 900;"
            elif badge.startswith("ORANGE"):
                color = "background-color: #FF7A00; color: white; font-weight: 900;"
            elif badge.startswith("RED"):
                color = "background-color: #E53935; color: white; font-weight: 900;"
            elif badge.startswith("GRAY"):
                color = "background-color: #8B949E; color: white; font-weight: 800;"
        elif col == "parameter":
            color = "font-weight: 900;"
        elif col in ["research_role", "role_group"]:
            color = "font-weight: 700;"
        styles.append(color)
    return styles

def _dti_render_parameter_quality_matrix_v1h():
    import streamlit as st
    import pandas as pd

    st.markdown("### Parameter Quality Matrix")

    st.info(
        "This compact matrix highlights promising parameter directions, control-needed zones, "
        "and blocked claim paths. Scores are UI meta-scores for research triage only; "
        "they are not likelihood, posterior, Planck, or physics-value results."
    )

    st.markdown("#### Color meaning")

    legend_cols = st.columns(5)
    legend_items = [
        ("GREEN - strong lead", "#00A86B", "Strong lead. Prioritize source-lock and strict follow-up."),
        ("YELLOW - useful partial", "#FFC400", "Useful partial result. Needs one or more controls."),
        ("ORANGE - needs control", "#FF7A00", "Control-needed direction. Do not claim yet."),
        ("RED - blocked for claim", "#E53935", "Blocked for claim-making, but useful as a boundary."),
        ("GRAY - awaiting data", "#8B949E", "Not scored yet. This is not a zero score."),
    ]
    for col, item in zip(legend_cols, legend_items):
        label, color, note = item
        with col:
            st.markdown(
                f"""
<div style="background:{color}; color:{'black' if 'YELLOW' in label else 'white'}; padding:8px 10px; border-radius:999px; text-align:center; font-weight:900; font-size:0.86rem;">
{label}
</div>
<div style="font-size:0.78rem; margin-top:6px; line-height:1.35;">
{note}
</div>
                """,
                unsafe_allow_html=True,
            )

    base_rows = [
        {
            "parameter": "omega_cdm",
            "research_role": "compensating direction",
            "role_group": "Matter-sector compensation",
            "current_value": "selected profile",
            "positive_signal": "Can identify a narrow compensating parameter direction.",
            "risk_blocker": "Needs companion-variable and seed-stability checks.",
            "stability": 13,
            "signal": 15,
            "control": 13,
            "risk": 7,
            "next_test": "Audit whether the compensating direction remains narrow and sign-stable.",
            "safe_interpretation": "Candidate compensating parameter direction.",
        },
        {
            "parameter": "A_planck / calibration",
            "research_role": "nuisance-control boundary",
            "role_group": "Calibration and nuisance control",
            "current_value": "selected profile",
            "positive_signal": "Can test whether a result survives nuisance-control restrictions.",
            "risk_blocker": "Must not be treated as a physical mechanism.",
            "stability": 12,
            "signal": 13,
            "control": 15,
            "risk": 7,
            "next_test": "Repeat under FIX / TIGHT nuisance boundaries before stronger wording.",
            "safe_interpretation": "Nuisance-boundedness check.",
        },
        {
            "parameter": "H0",
            "research_role": "branch coordinate",
            "role_group": "Branch geometry",
            "current_value": "selected profile",
            "positive_signal": "Can expose branch-level response direction.",
            "risk_blocker": "Not sufficient alone for a cosmological claim.",
            "stability": 12,
            "signal": 16,
            "control": 12,
            "risk": 8,
            "next_test": "Compare fixed-H0 branches under the same audit boundary.",
            "safe_interpretation": "Useful branch label and response coordinate.",
        },
        {
            "parameter": "f_EDE",
            "research_role": "early-time scan coordinate",
            "role_group": "Early-time modification",
            "current_value": "selected profile",
            "positive_signal": "Can mark a controlled early-time modification direction.",
            "risk_blocker": "Requires source-locked comparison before mechanism language.",
            "stability": 10,
            "signal": 15,
            "control": 10,
            "risk": 9,
            "next_test": "Check whether the same pattern persists across adjacent f_EDE values.",
            "safe_interpretation": "Promising controlled scan coordinate.",
        },
        {
            "parameter": "sigma8 / S8",
            "research_role": "stress indicator",
            "role_group": "Growth-stress diagnostic",
            "current_value": "selected profile",
            "positive_signal": "Can reveal growth-stress burden and residual tension.",
            "risk_blocker": "A stress indicator is not a likelihood exclusion.",
            "stability": 9,
            "signal": 14,
            "control": 9,
            "risk": 8,
            "next_test": "Use as a diagnostic stress row only after source-of-record data exist.",
            "safe_interpretation": "Growth-stress diagnostic only.",
        },
        {
            "parameter": "omega_b",
            "research_role": "baryon-sector control",
            "role_group": "Control parameter",
            "current_value": "selected profile",
            "positive_signal": "Can help separate baryon-sector load from dark-sector load.",
            "risk_blocker": "Usually not sufficient as the main driver.",
            "stability": 10,
            "signal": 9,
            "control": 11,
            "risk": 8,
            "next_test": "Hold other parameters fixed and inspect whether the response is load-bearing.",
            "safe_interpretation": "Useful control parameter.",
        },
        {
            "parameter": "n_s",
            "research_role": "spectral-tilt companion",
            "role_group": "Shape compensation",
            "current_value": "selected profile",
            "positive_signal": "Can expose spectral-tilt compensation.",
            "risk_blocker": "Needs CMB-shape context before interpretation.",
            "stability": 8,
            "signal": 10,
            "control": 9,
            "risk": 8,
            "next_test": "Check whether tilt movement is secondary or load-bearing.",
            "safe_interpretation": "Companion shape-control parameter.",
        },
        {
            "parameter": "unconnected future parameter",
            "research_role": "awaiting data",
            "role_group": "Future source-of-record slot",
            "current_value": "not connected",
            "positive_signal": "Reserved for a future audited parameter direction.",
            "risk_blocker": "No evaluation available yet.",
            "stability": None,
            "signal": None,
            "control": None,
            "risk": None,
            "next_test": "Attach source-of-record data before scoring.",
            "safe_interpretation": "Awaiting data, not zero quality.",
            "force_gray": True,
        },
    ]

    rows = []
    for row in base_rows:
        row = dict(row)
        if row.get("force_gray"):
            row["quality_score"] = None
            row["claim_readiness"] = None
            row["quality_badge"] = "GRAY - awaiting data"
        else:
            score = _dti_parameter_quality_score_v1h(
                row.get("stability", 0),
                row.get("signal", 0),
                row.get("control", 0),
                row.get("risk", 0),
            )
            row["quality_score"] = score
            row["claim_readiness"] = max(1, min(7, int(round(score * 7 / 100))))
            row["quality_badge"] = _dti_parameter_quality_badge_v1h(score)
        rows.append(row)

    df = pd.DataFrame(rows)

    st.markdown("#### Compact total evaluation table")
    st.caption(
        "Compact view: long explanatory fields are moved below into detail cards to avoid horizontal clipping."
    )

    compact_cols = [
        "parameter",
        "research_role",
        "role_group",
        "current_value",
        "quality_badge",
        "quality_score",
        "claim_readiness",
    ]

    compact_df = df[compact_cols].copy()

    try:
        compact_styled = compact_df.style.apply(_dti_parameter_quality_badge_style_v1h, axis=1)
        _dti_arrow_safe_df_v1(
            compact_styled, width="stretch",
            hide_index=True,
            height=330,
        )
    except Exception:
        _dti_arrow_safe_df_v1(
            compact_df, width="stretch",
            hide_index=True,
            height=330,
        )

    st.markdown("#### Next-test priority order")
    st.caption("This is the practical test order, not a scientific ranking of truth.")

    sort_df = df.copy()
    sort_df["sort_score"] = sort_df["quality_score"].fillna(-1)
    sort_df["sort_readiness"] = sort_df["claim_readiness"].fillna(-1)
    sort_df["sort_control"] = sort_df["control"].fillna(-1)
    sort_df = sort_df.sort_values(
        ["sort_score", "sort_readiness", "sort_control"],
        ascending=False,
    )

    force_gray_mask = sort_df.get("force_gray")
    if force_gray_mask is None:
        force_gray_mask = False
    else:
        force_gray_mask = force_gray_mask.fillna(False).astype(bool)

    priority_rows = sort_df[~force_gray_mask].head(5)

    for idx, row in enumerate(priority_rows.to_dict(orient="records"), start=1):
        badge = str(row.get("quality_badge", ""))
        badge_color = "#8B949E"
        badge_text_color = "white"
        if badge.startswith("GREEN"):
            badge_color = "#00A86B"
        elif badge.startswith("YELLOW"):
            badge_color = "#FFC400"
            badge_text_color = "black"
        elif badge.startswith("ORANGE"):
            badge_color = "#FF7A00"
        elif badge.startswith("RED"):
            badge_color = "#E53935"

        st.markdown(
            f"""
<div style="border:1px solid rgba(255,255,255,0.18); border-radius:12px; padding:12px 14px; margin:10px 0;">
  <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
    <b>{idx}. {row.get('parameter')}</b>
    <span style="background:{badge_color}; color:{badge_text_color}; padding:4px 10px; border-radius:999px; font-weight:900; font-size:0.80rem;">{badge}</span>
    <span>score {row.get('quality_score')}/100 · readiness {row.get('claim_readiness')}/7</span>
  </div>
  <div style="margin-top:8px;"><b>Role:</b> {row.get('research_role')} / {row.get('role_group')}</div>
  <div><b>Current value:</b> {row.get('current_value')}</div>
  <div><b>Why it matters:</b> {row.get('positive_signal')}</div>
  <div><b>Next test:</b> {row.get('next_test')}</div>
  <div><b>Safe wording:</b> {row.get('safe_interpretation')}</div>
</div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Full detail rows")
    st.caption("Use these expanders for the long fields removed from the compact table.")

    for row in df.to_dict(orient="records"):
        title = f"{row.get('parameter')} — {row.get('quality_badge')}"
        with st.expander(title, expanded=False):
            st.markdown(f"**Research role:** {row.get('research_role')}")
            st.markdown(f"**Role group:** {row.get('role_group')}")
            st.markdown(f"**Current value:** {row.get('current_value')}")
            st.markdown(f"**Positive signal:** {row.get('positive_signal')}")
            st.markdown(f"**Risk / blocker:** {row.get('risk_blocker')}")
            st.markdown(f"**Next test:** {row.get('next_test')}")
            st.markdown(f"**Safe interpretation:** {row.get('safe_interpretation')}")

    st.markdown("#### Use rule")
    st.code(
        """1. Use GREEN and YELLOW as research leads.
2. Use ORANGE as a control-needed direction.
3. Use RED as a claim boundary, not necessarily useless data.
4. Use GRAY as awaiting data, not zero quality.
5. Do not treat this matrix as likelihood, posterior, Planck validation, graph evidence, or physics-value update.""",
        language="text",
    )

    st.caption(
        "Boundary: this is a compact UI triage matrix only. It does not perform likelihood evaluation, "
        "posterior comparison, Planck validation, graph rendering, 7c execution, physics-value updates, "
        "manuscript updates, Render API modification, or Streamlit Secret modification."
    )
# --- /DTI_PARAMETER_QUALITY_MATRIX_COMPACT_V1H ---


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
        hide_index=True, width="stretch",
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
    "FUJIKI DTI BG z1100 jump 0.99778": {
        "H0": 72.900,
        "f_EDE": 0.0,
        "omega_cdm": 0.12700,
        "omega_b": 0.02440,
        "n_s": 0.9840,
        "ln10_10_As": 3.0589,
        "logAmod": 0.2223,
        "S8": 0.8019,
        "Geometry_Omega_M": 0.286,
        "Geometry_Omega_vac": 0.714,
        "Geometry_redshift_z": 1100.000,
        "Jump_redshift_z_jump": 3.500,
        "Jump_factor_E_above_z_jump": 0.99778,
        "boundary": "UI/profile preset only; not CLASS, likelihood, posterior, Planck, JWST, physics-value, or manuscript update",
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
        "Candidate preset — ACTIVE comparison input",
        preset_names,
        index=0 if preset_names else 0,
        key="dti_ui_candidate_preset_v1",
        help="Candidate 側の初期値を選びます。手入力で上書きできます。",
    )
    reference_preset = st.selectbox(
        "Reference preset — ACTIVE comparison input",
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
    _dti_arrow_safe_df_v1(show_df, width="stretch", hide_index=True)

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
    _dti_arrow_safe_df_v1(pd.DataFrame(guide_rows), width="stretch", hide_index=True)

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
    pass  # DTI_DISABLE_MARKDOWN_MONKEYPATCH_PASS_V1: disabled recursive markdown monkey patch; was markdown = _DTI_MARKDOWN_FILTER_V1
    pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled st.info assignment; was = _DTI_INFO_FILTER_V1
    pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled st.caption assignment; was = _DTI_CAPTION_FILTER_V1
    pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled st.button assignment; was = _DTI_BUTTON_FILTER_V1
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
    pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled st.button assignment; was = _dti_safe_button_v1
    pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled st.text_input assignment; was = _dti_safe_text_input_v1
    pass  # DTI_DISABLE_MARKDOWN_MONKEYPATCH_PASS_V1: disabled recursive markdown monkey patch; was markdown = _dti_safe_markdown_v1
    pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled st.info assignment; was = _dti_safe_info_v1
    pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled st.caption assignment; was = _dti_safe_caption_v1
    pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled st.write assignment; was = _dti_safe_write_v1
    pass  # DTI_DISABLE_REMAINING_HEADER_MONKEYPATCHES_V1: disabled st.header assignment
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
        pass  # DTI_DISABLE_MARKDOWN_MONKEYPATCH_PASS_V1: disabled recursive markdown monkey patch; was markdown = _dti_markdown_filter_final
        pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled _dti_st_final.info assignment; was = _dti_info_filter_final
        pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled _dti_st_final.caption assignment; was = _dti_caption_filter_final
        pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled _dti_st_final.button assignment; was = _dti_button_filter_final
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
        _dti_section8_top_restricted_notice_once_v3()
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
        pass  # DTI_DISABLE_REMAINING_HEADER_MONKEYPATCHES_V1: disabled st.header assignment
    if _dti_sec8_orig_subheader_v1 is not None:
        pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled st.subheader assignment; was = _dti_section8_text_wrapper_factory_v1(_dti_sec8_orig_subheader_v1)
    if _dti_sec8_orig_markdown_v1 is not None:
        pass  # DTI_DISABLE_MARKDOWN_MONKEYPATCH_PASS_V1: disabled recursive markdown monkey patch; was markdown = _dti_section8_text_wrapper_factory_v1(_dti_sec8_orig_markdown_v1)
    if _dti_sec8_orig_info_v1 is not None:
        pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled st.info assignment; was = _dti_section8_text_wrapper_factory_v1(_dti_sec8_orig_info_v1)
    if _dti_sec8_orig_caption_v1 is not None:
        pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled st.caption assignment; was = _dti_section8_text_wrapper_factory_v1(_dti_sec8_orig_caption_v1)
    if _dti_sec8_orig_write_v1 is not None:
        pass  # DTI_DISABLE_ALL_STREAMLIT_MONKEYPATCHES_V1: disabled st.write assignment; was = _dti_section8_text_wrapper_factory_v1(_dti_sec8_orig_write_v1)
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

# --- DTI_AXICLASS_FIX1_DATA_DIR_RESOLVER_V1 ---
# Robust data path resolver for local/public Streamlit layouts.
# The public repo stores benchmark TSV files under app/data, while some local
# layouts may expose them under data. This resolver only selects a readable
# source-of-record path. It does not run likelihoods, posteriors, Planck
# validation, graph rendering, 7c, physics-value updates, or manuscript edits.
_DTI_AXICLASS_FIX1_DATA_DIR_RESOLVER_V1 = True
_DTI_FIX1_REQUIRED_TSV_V1 = "axiclass_fix1_results.tsv"
_DTI_DATA_DIR_CANDIDATES_V1 = [
    APP_DIR / "app" / "data",
    APP_DIR / "data",
    Path.cwd() / "app" / "data",
    Path.cwd() / "data",
]
DATA_DIR = next(
    (
        _dti_data_dir
        for _dti_data_dir in _DTI_DATA_DIR_CANDIDATES_V1
        if (_dti_data_dir / _DTI_FIX1_REQUIRED_TSV_V1).exists()
    ),
    _DTI_DATA_DIR_CANDIDATES_V1[0],
)
AXICLASS_RESULTS = DATA_DIR / "axiclass_fix1_results.tsv"
AXICLASS_DELTA = DATA_DIR / "axiclass_fix1_delta.tsv"
# --- /DTI_AXICLASS_FIX1_DATA_DIR_RESOLVER_V1 ---



# --- DTI_CATEGORIZED_ACTIVE_PROFILE_LOADER_V2B_LINEPATCH ---
# Category-linked ACTIVE profile loader.
# This avoids huge regex patching and keeps the legacy loader as fallback.
_DTI_CATEGORIZED_ACTIVE_PROFILE_LOADER_V2B_LINEPATCH = True

_DTI_ACTIVE_PROFILE_CATEGORY_ORDER_V2B = [
    "Fujiki DTI Current",
    "DTI 5H Framework",
    "Baseline Anchors",
    "Local H0 & Lensed Catalogs",
    "LSS & Cosmic Shear",
    "Competing EDE / New Physics",
    "Fujiki DTI Historical Archive",
    "Misfit Calibration References",
    "Show all profiles / full TSV inventory",
    "Other / Review queue",
]

_DTI_ACTIVE_PROFILE_CATEGORY_NOTES_V2B = {
    "Fujiki DTI Current": "Current Fujiki DTI working profiles. Recommended default entry point.",
    "DTI 5H Framework": "Five-level DTI triage / inference / stress-test framework profiles.",
    "Baseline Anchors": "CMB and baseline reference profiles.",
    "Local H0 & Lensed Catalogs": "Local-H0 and strong-lensing anchor profiles.",
    "LSS & Cosmic Shear": "Large-scale-structure and S8-sensitive constraint profiles.",
    "Competing EDE / New Physics": "Mainstream EDE and adjacent new-physics comparison profiles.",
    "Fujiki DTI Historical Archive": "Earlier Fujiki DTI development snapshots.",
    "Misfit Calibration References": "Calibration and audit-reference profiles.",
    "Show all profiles / full TSV inventory": "Audit escape hatch: all registered profiles are selectable.",
    "Other / Review queue": "Profiles not yet mapped into a front-facing category.",
}

def _dti_profile_category_for_model_v2b(model_id):
    s = str(model_id)

    if s in {
        "FUJIKI_DTI_Candidate_v6",
        "DTI_AxiCLASS_HighH0",
        "Empirical_Misfit_Bounds",
        "Theoretical_Horizon_Lim",
    }:
        return "Fujiki DTI Current"

    if s.startswith("DTI_5H_"):
        return "DTI 5H Framework"

    if s.startswith("FUJIKI_DTI_v6_0_"):
        return "Fujiki DTI Historical Archive"

    if s.startswith("Misfit_Calibration_Ref"):
        return "Misfit Calibration References"

    if s.startswith((
        "Planck_",
        "ACT_DR4",
        "SPT_3G_2024",
        "SPT_3G_2022",
        "SPT_Pol",
        "WMAP",
        "Combined_CMB",
        "BICEP",
    )):
        return "Baseline Anchors"

    if s.startswith((
        "Riess",
        "CCHP",
        "Megamaser",
        "Pantheon",
        "Agnello",
        "H0LiCOW",
        "TDCOSMO",
        "STRIDES",
        "Mortsell",
    )):
        return "Local H0 & Lensed Catalogs"

    if s.startswith((
        "Hill_",
        "DES_",
        "KiDS",
        "HSC_",
        "ACT_DR6_Cosmic",
        "SPT_3G_Y3_Cosmic",
        "SDSS",
        "BOSS",
        "DESI_DR",
        "Euclid",
        "Vera_Rubin",
        "Roman",
    )):
        return "LSS & Cosmic Shear"

    if any(token in s for token in [
        "EDE",
        "Axi",
        "Niedermann",
        "Poulin",
        "Ivanov",
        "Smith",
        "Lin_",
        "Gomez",
        "Allali",
        "Ye_Piao",
        "Braglia",
        "Abellan",
        "Seto",
        "He_Piao",
        "Wang_Piao",
        "Freese",
        "Kamionkowski",
        "Knox",
        "Vagnozzi",
        "Efstathiou",
        "Spergel",
        "Silk",
        "Verde",
        "Di_Valentino",
        "JWST",
        "Karwal",
        "Moss",
        "K_essence",
        "High_EDE",
    ]):
        return "Competing EDE / New Physics"

    return "Other / Review queue"

def _dti_group_profile_presets_v2b(preset_names):
    grouped = {cat: [] for cat in _DTI_ACTIVE_PROFILE_CATEGORY_ORDER_V2B}
    for name in preset_names:
        cat = _dti_profile_category_for_model_v2b(name)
        grouped.setdefault(cat, []).append(name)
    grouped["Show all profiles / full TSV inventory"] = list(preset_names)
    return grouped

def _dti_render_categorized_active_profile_loader_v2b(preset_names, current_default=None):
    st.sidebar.markdown("### Profile category → ACTIVE loader")
    st.sidebar.caption(
        "Use this two-step loader for normal use. The selected model becomes the active profile. "
        "The older loader below is retained only as fallback."
    )

    if not preset_names:
        st.sidebar.warning("No registered profile presets are available.")
        return None

    grouped = _dti_group_profile_presets_v2b(preset_names)
    available_categories = [
        cat for cat in _DTI_ACTIVE_PROFILE_CATEGORY_ORDER_V2B
        if grouped.get(cat)
    ]

    default_category = "Fujiki DTI Current"
    if current_default and current_default in preset_names:
        default_category = _dti_profile_category_for_model_v2b(current_default)
    if default_category not in available_categories:
        default_category = available_categories[0]

    category_index = available_categories.index(default_category)

    selected_category = st.sidebar.selectbox(
        "Profile category — ACTIVE",
        available_categories,
        index=category_index,
        key="dti_active_profile_category_v2b",
    )

    st.sidebar.caption(_DTI_ACTIVE_PROFILE_CATEGORY_NOTES_V2B.get(selected_category, ""))

    model_options = grouped.get(selected_category, [])
    if not model_options:
        st.sidebar.warning("No profiles found in this category.")
        return current_default if current_default in preset_names else preset_names[0]

    default_model = current_default if current_default in model_options else None
    if default_model is None and "FUJIKI_DTI_Candidate_v6" in model_options:
        default_model = "FUJIKI_DTI_Candidate_v6"
    if default_model is None:
        default_model = model_options[0]

    selected_model = st.sidebar.selectbox(
        "Model profile — ACTIVE",
        model_options,
        index=model_options.index(default_model),
        key="dti_active_model_profile_v2b",
    )

    st.sidebar.success(f"ACTIVE profile selected: {selected_model}")

    if selected_category == "Show all profiles / full TSV inventory":
        st.sidebar.caption("SHOW ALL is for audit and full inventory access. It still loads only the selected model.")

    with st.sidebar.expander("Active loader category counts", expanded=False):
        rows = [{"category": cat, "count": len(grouped.get(cat, []))} for cat in available_categories]
        try:
            _dti_arrow_safe_df_v1(pd.DataFrame(rows), width="stretch", hide_index=True)
        except Exception:
            st.write(rows)

    return selected_model
# --- /DTI_CATEGORIZED_ACTIVE_PROFILE_LOADER_V2B_LINEPATCH ---

# --- DTI_PROFILE_CATEGORY_GUIDE_V1_SAFE_FIXINDENT ---
# Sidebar profile category guide.
# UI organization only. It does not modify profile_presets_v606.tsv.
# It does not replace the existing active profile selector.
# It does not enable 7c, graph rendering, likelihood evaluation,
# posterior comparison, Planck validation, physics-value updates,
# manuscript updates, Render API changes, or Streamlit Secret changes.
_DTI_PROFILE_CATEGORY_GUIDE_V1_SAFE_FIXINDENT = True

_DTI_PROFILE_CATEGORY_ORDER_V1_SAFE_FIXINDENT = [
    "Baseline Anchors",
    "Local H0 & Lensed Catalogs",
    "LSS & Cosmic Shear",
    "Competing EDE / New Physics",
    "Fujiki DTI Current",
    "DTI 5H Framework",
    "Fujiki DTI Historical Archive",
    "Misfit Calibration References",
    "Other / Review queue",
]

_DTI_PROFILE_CATEGORY_NOTES_V1_SAFE_FIXINDENT = {
    "Baseline Anchors": "CMB / baseline reference profiles used as starting anchors.",
    "Local H0 & Lensed Catalogs": "Local expansion and strong-lensing H0 reference profiles.",
    "LSS & Cosmic Shear": "S8 / growth / large-scale-structure pressure profiles.",
    "Competing EDE / New Physics": "Mainstream EDE and new-physics comparison profiles.",
    "Fujiki DTI Current": "Current FUJIKI DTI front-facing candidate/reference profiles.",
    "DTI 5H Framework": "5H triage, inference, canonical, and stress profiles.",
    "Fujiki DTI Historical Archive": "Earlier FUJIKI DTI development versions; hidden from first-pass focus.",
    "Misfit Calibration References": "Calibration and audit-reference profiles.",
    "Show all profiles / full TSV inventory": [
        "Full unfiltered TSV inventory. Use this when auditing coverage or searching for a specific model ID.",
    ],
    "Other / Review queue": "Profiles not yet mapped into a front-facing category.",
}

def _dti_profile_category_for_model_v1_safe_fixindent(model_id):
    mid = str(model_id)

    baseline_exact = {
        "Planck_2018_LCDM_Base",
        "Planck_2018_no_lensing",
        "Planck_2018_CamSpec",
        "ACT_DR4_LCDM_Baseline",
        "ACT_DR4_no_lensing",
        "ACT_DR4_plus_WMAP9",
        "SPT_3G_2024_CMB_Only",
        "SPT_3G_2022_TE_EE",
        "SPT_Pol_Final_Baseline",
        "WMAP_9Year_Final_Re",
        "Combined_CMB_Lens_2025",
        "Planck_2018_Alternative",
        "BICEP_Keck_2021_BMode",
    }

    local_h0_exact = {
        "Riess_2022_SHOES_Anchor",
        "CCHP_2023_TRGB_Anchor",
        "Megamaser_MCP_Final",
        "Pantheon_Plus_SN_Only",
        "Agnello_2025_StrongLens",
        "H0LiCOW_6_Clusters_Max",
        "TDCOSMO_2024_Lensing",
        "STRIDES_Strong_Lens_H0",
        "Mortsell_2024_SNIa_Lensed",
    }

    lss_exact = {
        "Hill_2020_S8_Growth_Lim",
        "DES_Y1_3x2pt_Baseline",
        "DES_Y3_3x2pt_Optimal",
        "DES_Y3_Shear_Baseline",
        "DES_Y5_Combined_2026",
        "DES_Y5_Dovekie_2026_Lim",
        "KiDS_1000_Cosmic_Shear",
        "KiDS_1000_Full_3x2pt",
        "KiDS_VIKING_450_Shear",
        "HSC_Y3_Cosmic_Shear_1",
        "HSC_Y3_Cosmic_Shear_2",
        "ACT_DR6_Cosmic_Shear_1",
        "SPT_3G_Y3_Cosmic_Shear",
        "SDSS_DR16_eBOSS_Max",
        "BOSS_DR12_Full_Shape",
        "DESI_DR1_BAO_Planck_1",
        "DESI_DR1_BAO_Planck_2",
        "DESI_DR2_BAO_2026_Pref",
        "Euclid_2025_First_FS_1",
        "Euclid_2026_Joint_LSS",
        "Vera_Rubin_LSST_2025_P",
        "Roman_Space_Telescope_1",
        "DESI_DR1_Om0_Evolution",
    }

    ede_exact = {
        "Poulin_2019_EDE_Planck",
        "Ivanov_2020_EDE_Joint",
        "Smith_2020_EDE_ACT",
        "Poulin_2021_EDE_ACT_DR4",
        "Smith_2022_EDE_SPT3G",
        "Lin_2021_AxiCLASS_Max",
        "Gomez_Valent_2024_Axi",
        "Niedermann_Sloth_2020",
        "Niedermann_2022_Cold1",
        "Niedermann_2024_Cold2",
        "Allali_2023_Early_Quint",
        "Ye_Piao_2020_AdS_EDE_1",
        "Ye_Piao_2022_AdS_EDE_2",
        "Braglia_2021_Enhanced",
        "Abellan_2022_Mirror_DM",
        "Seto_Takahashi_2023_Axi",
        "DESI_2024_Thawing_EDE",
        "Cold_New_EDE_2025_Fit",
        "Freese_2024_Natural_EDE",
        "He_Piao_2024_V_Coupled",
        "Wang_Piao_2025_Pre_Rec",
        "JWST_Massive_Galaxy_z10",
        "Karwal_2024_Fractional",
        "Moss_2025_DM_Decay_EDE",
        "K_essence_Reconstructed",
        "High_EDE_Overcomp_Max",
        "Kamionkowski_2023_Rev1",
        "Kamionkowski_2025_Rev2",
        "Knox_Millea_2020_Hubble",
        "Vagnozzi_2021_Critique",
        "Efstathiou_2021_H0_LSS",
        "Spergel_2024_Complement",
        "Silk_2025_High_z_Anom",
        "Verde_2023_Tension_Review",
        "Di_Valentino_2021_Mega",
    }

    current_dti_exact = {
        "FUJIKI_DTI_Candidate_v6",
        "DTI_AxiCLASS_HighH0",
        "Empirical_Misfit_Bounds",
        "Theoretical_Horizon_Lim",
    }

    dti_5h_exact = {
        "DTI_5H_Level1_Triage",
        "DTI_5H_Level2_Inference",
        "DTI_5H_Level3_Canonical",
        "DTI_5H_Level4_Stress_1",
        "DTI_5H_Level5_Stress_2",
        "DTI_5H_Max_Strain_End",
    }

    historical_exact = {
        "FUJIKI_DTI_v6_0_1_tuned",
        "FUJIKI_DTI_v6_0_2_widget",
        "FUJIKI_DTI_v6_0_3_labels",
        "FUJIKI_DTI_v6_0_4_likel",
        "FUJIKI_DTI_v6_0_5_fixed",
    }

    calibration_exact = {
        "Misfit_Calibration_Ref1",
        "Misfit_Calibration_Ref2",
        "Misfit_Calibration_Ref3",
        "Misfit_Calibration_Ref4",
        "Misfit_Calibration_Ref5",
    }

    if mid in baseline_exact:
        return "Baseline Anchors"
    if mid in local_h0_exact:
        return "Local H0 & Lensed Catalogs"
    if mid in lss_exact:
        return "LSS & Cosmic Shear"
    if mid in ede_exact:
        return "Competing EDE / New Physics"
    if mid in current_dti_exact:
        return "Fujiki DTI Current"
    if mid in dti_5h_exact:
        return "DTI 5H Framework"
    if mid in historical_exact:
        return "Fujiki DTI Historical Archive"
    if mid in calibration_exact:
        return "Misfit Calibration References"

    if mid.startswith("FUJIKI_DTI_v6_0_"):
        return "Fujiki DTI Historical Archive"
    if mid.startswith("DTI_5H_"):
        return "DTI 5H Framework"
    if mid.startswith("Misfit_Calibration_"):
        return "Misfit Calibration References"
    if "Shear" in mid or "DES_" in mid or "KiDS" in mid or "HSC_" in mid or "BOSS" in mid or "eBOSS" in mid:
        return "LSS & Cosmic Shear"
    if "EDE" in mid or "Axi" in mid or "Quint" in mid or "Mirror" in mid or "Fractional" in mid:
        return "Competing EDE / New Physics"
    if "H0" in mid or "Lens" in mid or "SHOES" in mid or "TRGB" in mid or "SNIa" in mid:
        return "Local H0 & Lensed Catalogs"
    if "Planck" in mid or "ACT" in mid or "SPT" in mid or "WMAP" in mid or "CMB" in mid or "BICEP" in mid:
        return "Baseline Anchors"

    return "Other / Review queue"

def _dti_profile_role_for_model_v1_safe_fixindent(model_id):
    category = _dti_profile_category_for_model_v1_safe_fixindent(model_id)
    role_map = {
        "Baseline Anchors": "baseline reference",
        "Local H0 & Lensed Catalogs": "high-H0 / local-distance reference",
        "LSS & Cosmic Shear": "S8 / growth-pressure constraint",
        "Competing EDE / New Physics": "comparison / stress-test target",
        "Fujiki DTI Current": "front-facing DTI candidate/reference",
        "DTI 5H Framework": "5H triage / inference / stress profile",
        "Fujiki DTI Historical Archive": "historical DTI archive",
        "Misfit Calibration References": "calibration reference",
        "Other / Review queue": "unclassified review item",
    }
    return role_map.get(category, "unclassified review item")

def _dti_build_profile_category_map_v1_safe_fixindent(presets):
    grouped = {cat: [] for cat in _DTI_PROFILE_CATEGORY_ORDER_V1_SAFE_FIXINDENT}
    try:
        model_ids = list(presets.keys())
    except Exception:
        model_ids = []
    for model_id in model_ids:
        category = _dti_profile_category_for_model_v1_safe_fixindent(model_id)
        grouped.setdefault(category, []).append(model_id)
    for category in grouped:
        grouped[category] = sorted(grouped[category], key=lambda x: str(x).lower())
    return grouped

def _dti_render_profile_category_guide_v1_safe_fixindent(presets):
    import streamlit as st

    grouped = _dti_build_profile_category_map_v1_safe_fixindent(presets)

    st.sidebar.markdown("### Profile category browser / preview only")
    st.sidebar.caption("SHOW ALL is an audit escape hatch: it previews the complete TSV inventory without changing the active loader.")
    st.sidebar.caption("When SHOW ALL is selected, the browser preview is intended for full inventory audit. Use ACTIVE loader below to load a model.")

    if st.sidebar.checkbox("Show complete profile TSV inventory", value=False, key="show_complete_profile_tsv_inventory_v1e"):
        # DTI_SHOW_ALL_PROFILES_TABLE_V1F
        # Preview-only full inventory table. This does not change the active loader.
        try:
            _dti_tsv_path_v1f = DATA_DIR / "profile_presets_v606.tsv"
            if _dti_tsv_path_v1f.exists():
                _dti_all_df_v1f = pd.read_csv(_dti_tsv_path_v1f, sep="\t")
                _dti_model_col_v1f = "Model ID" if "Model ID" in _dti_all_df_v1f.columns else _dti_all_df_v1f.columns[0]
                _dti_models_v1f = [str(x) for x in _dti_all_df_v1f[_dti_model_col_v1f].dropna().tolist()]
                _dti_source_label_v1f = "profile_presets_v606.tsv"
            else:
                _dti_models_v1f = [str(x) for x in PRESETS.keys()]
                _dti_source_label_v1f = "registered PRESETS fallback"
    
            _dti_registered_count_v1f = len(list(PRESETS.keys()))
            _dti_tsv_count_v1f = len(_dti_models_v1f)
    
            st.sidebar.caption(
                f"Full inventory preview: {_dti_tsv_count_v1f} TSV profiles. "
                f"Registered PRESETS currently visible to the app: {_dti_registered_count_v1f}. "
                "Preview only; active loader unchanged."
            )
    
            _dti_inventory_rows_v1f = []
            for _dti_i_v1f, _dti_model_id_v1f in enumerate(_dti_models_v1f, start=1):
                try:
                    _dti_cat_v1f = _dti_profile_category_for_model_v1_safe_fixindent(_dti_model_id_v1f)
                except Exception:
                    _dti_cat_v1f = "Unclassified"
                _dti_inventory_rows_v1f.append({
                    "no": _dti_i_v1f,
                    "model_id": _dti_model_id_v1f,
                    "category": _dti_cat_v1f,
                })
    
            _dti_inventory_df_v1f = pd.DataFrame(_dti_inventory_rows_v1f)
            with st.sidebar.expander("Full profile TSV inventory — table preview only", expanded=False):
                st.caption(f"Source: {_dti_source_label_v1f}. This table is not an active selection control.")
                _dti_arrow_safe_df_v1(
                    _dti_inventory_df_v1f,
                    width="stretch",
                    hide_index=True,
                )
        except Exception as _dti_show_all_err_v1f:
            st.sidebar.warning(f"Full TSV inventory preview could not be rendered: {_dti_show_all_err_v1f}")
    st.sidebar.caption(
        "The full preset inventory is grouped for readability. "
        "This guide does not change the underlying TSV or run new cosmology."
    )

    visible_first_pass = [
        "Baseline Anchors",
        "Local H0 & Lensed Catalogs",
        "LSS & Cosmic Shear",
        "Competing EDE / New Physics",
        "Fujiki DTI Current",
        "DTI 5H Framework",
    ]

    available = [cat for cat in visible_first_pass if grouped.get(cat)]
    if not available:
        available = [cat for cat in _DTI_PROFILE_CATEGORY_ORDER_V1_SAFE_FIXINDENT if grouped.get(cat)]

    default_index = 0
    if "Fujiki DTI Current" in available:
        default_index = available.index("Fujiki DTI Current")

    selected_category = st.sidebar.selectbox(
        "Profile category browser / preview only",
        available,
        index=default_index,
        key="dti_profile_category_guide_category_v1_safe_fixindent",
        help="Use this guide to understand the large profile inventory before using the existing active profile selector.",
    )

    st.sidebar.caption(_DTI_PROFILE_CATEGORY_NOTES_V1_SAFE_FIXINDENT.get(selected_category, ""))

    model_ids = grouped.get(selected_category, [])
    if model_ids:
        preview_model = st.sidebar.selectbox(
            "Category model preview — not loaded yet",
            model_ids,
            index=0,
            key="dti_profile_category_guide_model_preview_v1_safe_fixindent",
            help="Preview profiles in this category. The existing active profile selector remains unchanged.",
        )
        st.sidebar.caption(f"Role: {_dti_profile_role_for_model_v1_safe_fixindent(preview_model)}")

    show_archive = st.sidebar.checkbox(
        "Show archive category counts",
        value=False,
        key="dti_profile_category_guide_show_archive_counts_v1_safe_fixindent",
        help="Shows counts for historical, calibration, and review-queue profiles.",
    )

    with st.sidebar.expander("Profile category counts", expanded=False):
        for category in _DTI_PROFILE_CATEGORY_ORDER_V1_SAFE_FIXINDENT:
            if not show_archive and category in {
                "Fujiki DTI Historical Archive",
                "Misfit Calibration References",
                "Other / Review queue",
            }:
                continue
            st.write(f"{category}: {len(grouped.get(category, []))}")

        st.caption(
            "Boundary: category guide only. No TSV modification, no likelihood evaluation, "
            "no posterior comparison, no Planck validation, no 7c execution, no graph rendering, "
            "and no physics-value update."
        )
# --- /DTI_PROFILE_CATEGORY_GUIDE_V1_SAFE_FIXINDENT ---

# --- DTI_PROFILE_CATEGORY_GUIDE_LABEL_POLISH_V1C_MINIMAL ---
# Minimal label-only clarification:
# - category guide is preview-only
# - registered/profile and Candidate/Reference selectors are active controls
# - no selector replacement
_DTI_PROFILE_CATEGORY_GUIDE_LABEL_POLISH_V1C_MINIMAL = True
# --- DTI_PROFILE_CATEGORY_GUIDE_SHOW_ALL_V1D ---
# Adds preview-only "Show all profiles / full TSV inventory".
# This does not replace the active profile loader.
_DTI_PROFILE_CATEGORY_GUIDE_SHOW_ALL_V1D = True
# --- /DTI_PROFILE_CATEGORY_GUIDE_SHOW_ALL_V1D ---

# --- DTI_SHOW_ALL_PROFILES_PREVIEW_V1E ---
# Makes "Show all profiles / full TSV inventory" preview the complete PRESETS inventory.
# This remains preview-only and does not replace the active loader.
_DTI_SHOW_ALL_PROFILES_PREVIEW_V1E = True

def _dti_profile_category_preview_models_v1e(selected_category, grouped_models, presets):
    """Return preview model IDs for the sidebar category browser.

    Boundary:
    - preview only
    - does not change the active selected_preset loader
    - does not mutate profile_presets_v606.tsv
    """
    if selected_category == "Show all profiles / full TSV inventory":
        return list(presets.keys())
    return list(grouped_models.get(selected_category, []))
# --- /DTI_SHOW_ALL_PROFILES_PREVIEW_V1E ---


# --- DTI_SHOW_ALL_PROFILES_TABLE_V1F ---
# Replaces JSON-like full inventory preview with a compact table and separate TSV/PRESETS counts.
_DTI_SHOW_ALL_PROFILES_TABLE_V1F = True
# --- /DTI_SHOW_ALL_PROFILES_TABLE_V1F ---


# DTI_PARSE_TARGET_MODEL_FOR_CORRELATED_BOUNDARY_V1B
# Minimal local parser for TARGET_MODEL-style text used by the proxy triage panel.
# Boundary: parser only; no CLASS run, no API request, no likelihood evaluation.
def _dti_parse_target_model_for_correlated_boundary_v1b(text):
    parsed = {}
    if not text:
        return parsed
    alias = {
        "H0": "H0",
        "h0": "H0",
        "H_0": "H0",
        "f_EDE": "f_EDE",
        "fede": "f_EDE",
        "fEDE": "f_EDE",
        "omega_cdm": "omega_cdm",
        "omega_c": "omega_cdm",
        "omch2": "omega_cdm",
        "omega_b": "omega_b",
        "ombh2": "omega_b",
        "sigma8": "sigma8",
        "S8": "S8",
        "s8": "S8",
        "ln10_10_As": "ln10_10_As",
        "n_s": "n_s",
        "ns": "n_s",
        "tau_reio": "tau_reio",
        "z_c": "z_c",
        "zc": "z_c",
    }
    for raw_line in str(text).replace("：", ":").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
        elif ":" in line:
            key, value = line.split(":", 1)
        else:
            continue
        key = key.strip().strip("*`- ").replace(" ", "_")
        value = value.strip().strip(",;")
        if not key:
            continue
        canonical = alias.get(key, alias.get(key.replace("-", "_"), key))
        try:
            parsed[canonical] = float(value)
        except Exception:
            continue
    return parsed
# /DTI_PARSE_TARGET_MODEL_FOR_CORRELATED_BOUNDARY_V1B

# --- DTI_CORRELATED_BOUNDARY_TRIAGE_V1 ---
# Lightweight geometric proxy for correlated-boundary triage.
# Boundary: proxy only; not likelihood evaluation, not posterior comparison,
# not Planck validation, not model validation, not physics-value update.

_DTI_CORRELATED_BOUNDARY_TRIAGE_V1 = True

def _dti_float_v1(value, default=None):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default

def _dti_correlated_boundary_score_v1(h0, s8, omega_cdm=None, f_ede=None):
    """
    Lightweight correlated-boundary proxy.

    This is an analytic triage surface, not a likelihood surface.
    It uses bounded geometric rules to refine GREEN / ORANGE / RED
    triage sensitivity without running CLASS, MCMC, or external APIs.
    """
    h0 = _dti_float_v1(h0, None)
    s8 = _dti_float_v1(s8, None)
    omega_cdm = _dti_float_v1(omega_cdm, None)
    f_ede = _dti_float_v1(f_ede, 0.0)

    if h0 is None or s8 is None:
        return {
            "status": "GRAY",
            "score": None,
            "reason": "insufficient H0 / S8 inputs",
            "boundary": "proxy only",
            "safe_interpretation": "No correlated-boundary proxy was evaluated because required fields are missing.",
            "not_claim": "not likelihood evaluation; not posterior comparison; not Planck validation",
        }

    # Baseline geometric proxy:
    # High H0 with high S8 is penalized more strongly than either variable alone.
    # These constants are deliberately conservative UI-triage constants, not fitted posterior values.
    h0_center = 67.4
    s8_center = 0.811
    h0_scale = 4.2
    s8_scale = 0.035
    rho = 0.58

    x = (h0 - h0_center) / h0_scale
    y = (s8 - s8_center) / s8_scale
    denom = max(1e-9, 1.0 - rho * rho)
    ellipse_score = (x * x - 2.0 * rho * x * y + y * y) / denom

    # Additional burden terms.
    ede_burden = max(0.0, f_ede - 0.03) / 0.04
    omega_burden = 0.0
    if omega_cdm is not None:
        omega_burden = max(0.0, omega_cdm - 0.125) / 0.012

    composite_score = float(ellipse_score + 0.35 * ede_burden * ede_burden + 0.20 * omega_burden * omega_burden)

    if composite_score < 2.30:
        status = "GREEN"
        reason = "inside conservative correlated proxy boundary"
        safe = "The input sits inside the lightweight correlated-boundary proxy."
    elif composite_score < 5.99:
        status = "ORANGE"
        reason = "near correlated proxy caution boundary"
        safe = "The input is near a correlated-boundary caution region and should be checked before stronger interpretation."
    else:
        status = "RED"
        reason = "outside correlated proxy caution boundary"
        safe = "The input is outside the lightweight correlated-boundary proxy and should not be promoted without stronger audited support."

    return {
        "status": status,
        "score": round(composite_score, 3),
        "ellipse_score": round(float(ellipse_score), 3),
        "ede_burden": round(float(ede_burden), 3),
        "omega_burden": round(float(omega_burden), 3),
        "reason": reason,
        "boundary": "correlated-boundary proxy only",
        "safe_interpretation": safe,
        "not_claim": "not likelihood evaluation; not posterior comparison; not Planck validation; not physical-discontinuity proof",
    }

def _dti_render_correlated_boundary_triage_v1():
    st.markdown("### Correlated-boundary triage proxy")
    _dti_panel_note_v1("Summary → compact table → raw audit view. Proxy-only; detailed limits are in Global claim limits / audit boundary.")
    st.caption(
        "Lightweight geometric audit proxy. No CLASS run, no Render API call, no likelihood evaluation, "
        "no posterior comparison, no Planck validation, and no physics-value update."
    )

    candidate_text = st.session_state.get("paper_text", "") or st.session_state.get("paper_text_widget", "")
    parsed = _dti_parse_target_model_for_correlated_boundary_v1b(candidate_text) if candidate_text else {}

    h0 = parsed.get("H0", st.session_state.get("H0", None))
    s8 = parsed.get("S8", st.session_state.get("S8", None))
    omega_cdm = parsed.get("omega_cdm", parsed.get("omega_c", st.session_state.get("omega_cdm", None)))
    f_ede = parsed.get("f_EDE", parsed.get("fede", st.session_state.get("f_EDE", 0.0)))

    result = _dti_correlated_boundary_score_v1(h0, s8, omega_cdm=omega_cdm, f_ede=f_ede)

    status = result.get("status", "GRAY")
    score = result.get("score")

    if status == "GREEN":
        st.success(f"Correlated-boundary proxy: GREEN / score={score}")
    elif status == "ORANGE":
        st.warning(f"Correlated-boundary proxy: ORANGE / score={score}")
    elif status == "RED":
        st.error(f"Correlated-boundary proxy: RED / score={score}")
    else:
        st.info("Correlated-boundary proxy: GRAY / insufficient inputs")

    rows = [
        {"field": "H0", "value": h0},
        {"field": "S8", "value": s8},
        {"field": "omega_cdm", "value": omega_cdm},
        {"field": "f_EDE", "value": f_ede},
        {"field": "status", "value": result.get("status")},
        {"field": "score", "value": result.get("score")},
        {"field": "ellipse_score", "value": result.get("ellipse_score")},
        {"field": "ede_burden", "value": result.get("ede_burden")},
        {"field": "omega_burden", "value": result.get("omega_burden")},
        {"field": "reason", "value": result.get("reason")},
    ]
    _dti_arrow_safe_df_v1(pd.DataFrame(rows), width="stretch", hide_index=True)

    with st.expander("Boundary and claim limits", expanded=False):
        st.markdown(
            """
This panel is a **triage proxy only**.

It is designed to improve audit sensitivity by using a correlated geometric boundary rather than a single fixed threshold.

It is **not**:

- a likelihood evaluation
- a posterior comparison
- a Planck validation
- a model validation
- a physical-discontinuity proof
- a physics-value update
- a manuscript conclusion
"""
        )
        st.caption(result.get("safe_interpretation", ""))
        st.caption(result.get("not_claim", ""))

# --- /DTI_CORRELATED_BOUNDARY_TRIAGE_V1 ---

# --- DTI_STATIC_DELTA_AUDIT_TABLE_V1 ---
# Static local TSV audit display for axiclass_fix1_delta.tsv.
# Boundary: table display only; not interpolation, not CLASS execution,
# not likelihood evaluation, not posterior comparison, not Planck validation.
_DTI_STATIC_DELTA_AUDIT_TABLE_V1 = True

def _dti_read_static_delta_table_v1():
    """Read local static AxiCLASS FIX1 delta TSV for audit display only."""
    try:
        delta_path = AXICLASS_DELTA
    except Exception:
        try:
            delta_path = DATA_DIR / "axiclass_fix1_delta.tsv"
        except Exception:
            delta_path = None

    if delta_path is None:
        return None, "AXICLASS_DELTA path is unavailable."

    try:
        if not delta_path.exists():
            return None, f"Static delta TSV not found: {delta_path}"
        df = pd.read_csv(delta_path, sep="\t")
        return df, ""
    except Exception as exc:
        return None, f"Could not read static delta TSV: {type(exc).__name__}"

def _dti_render_static_delta_audit_table_v1():
    st.markdown("### AxiCLASS FIX1 static delta audit table")
    _dti_panel_note_v1("Summary → compact table → raw audit view. Static TSV display only; detailed limits are centralized above.")
    st.caption(
        "Local static TSV checkpoint display only. No interpolation, no CLASS run, no Render API call, "
        "no likelihood evaluation, no posterior comparison, no Planck validation, and no physics-value update."
    )

    df, err = _dti_read_static_delta_table_v1()
    if df is None:
        st.info(f"Static delta audit table unavailable. {err}")
        return

    expected_cols = ["pair", "model_A", "model_B", "metric", "A", "B", "delta_A_minus_B", "pct_delta_vs_B", "direction"]
    available_cols = [c for c in expected_cols if c in df.columns]
    display_df = df[available_cols].copy() if available_cols else df.copy()

    row_count = int(len(display_df))
    metric_count = int(display_df["metric"].nunique()) if "metric" in display_df.columns else None
    pair_count = int(display_df["pair"].nunique()) if "pair" in display_df.columns else None

    st.info(
        f"Static delta audit table loaded: {row_count} rows"
        + (f", {metric_count} metrics" if metric_count is not None else "")
        + (f", {pair_count} comparison pairs" if pair_count is not None else "")
        + "."
    )

    if "direction" in display_df.columns:
        with st.expander("Direction summary — static TSV only", expanded=False):
            try:
                summary_df = (
                    display_df["direction"]
                    .fillna("unknown")
                    .astype(str)
                    .value_counts()
                    .rename_axis("direction")
                    .reset_index(name="count")
                )
                _dti_arrow_safe_df_v1(summary_df, width="stretch", hide_index=True)
            except Exception:
                st.caption("Direction summary unavailable.")

    with st.expander("Compact static delta table — audit display only", expanded=False):
        _dti_arrow_safe_df_v1(display_df, width="stretch", hide_index=True)

    
    st.caption("Compact reader-facing view: wide model names are shortened into columns; source TSV remains unchanged.")
    try:
        _dti_delta_compact_v1b = _dti_static_delta_table_compact_v1b(df)
        if not _dti_delta_compact_v1b.empty:
            with st.expander("Compact static delta table — reader view", expanded=True):
                _dti_arrow_safe_df_v1(_dti_delta_compact_v1b, width="stretch", hide_index=True)
    except Exception:
        st.caption("Compact static delta reader view unavailable; source TSV display remains bounded.")

    with st.expander("Boundary and safe interpretation", expanded=False):
        st.markdown(
            """
This panel displays the local `app/data/axiclass_fix1_delta.tsv` checkpoint table.

It is useful for:

- comparing fixed benchmark differences already present in the repository
- checking pair / metric / direction structure
- preserving static provenance for reader-facing audit

It is **not**:

- an interpolation engine
- a recomputation
- a CLASS run
- a Render API request
- a likelihood evaluation
- a posterior comparison
- a Planck validation
- a physics-value update
- a manuscript conclusion
"""
        )
        st.caption(
            "The previous read-only audit found this TSV is not ready for interpolation because it has no clear numeric interpolation axis. "
            "Therefore this panel intentionally uses it as a static delta audit table only."
        )

# --- DTI_STATIC_DELTA_TABLE_READABILITY_V1B ---
# Readability-only helpers for the static delta table.
# Boundary: no interpolation, no recomputation, no CLASS run, no API call.

_DTI_STATIC_DELTA_TABLE_READABILITY_V1B = True

def _dti_static_delta_table_compact_v1b(df):
    """Return compact static-delta table columns for reader-facing display."""
    try:
        if df is None or df.empty:
            return pd.DataFrame()
        display_cols = [
            c for c in [
                "pair",
                "metric",
                "model_A",
                "model_B",
                "A",
                "B",
                "delta_A_minus_B",
                "pct_delta_vs_B",
                "direction",
            ] if c in df.columns
        ]
        compact = df[display_cols].copy()
        rename = {
            "pair": "pair",
            "metric": "metric",
            "model_A": "A model",
            "model_B": "B model",
            "A": "A",
            "B": "B",
            "delta_A_minus_B": "Δ A−B",
            "pct_delta_vs_B": "%Δ vs B",
            "direction": "dir",
        }
        compact = compact.rename(columns=rename)
        for col in ["A", "B", "Δ A−B", "%Δ vs B"]:
            if col in compact.columns:
                compact[col] = pd.to_numeric(compact[col], errors="coerce").round(5)
        return compact
    except Exception:
        return df

# --- /DTI_STATIC_DELTA_TABLE_READABILITY_V1B ---

# --- /DTI_STATIC_DELTA_AUDIT_TABLE_V1 ---

# --- DTI_VANILLA_INPUT_RESULT_DISPLAY_POLISH_V1 ---
# Reader-facing display helpers for vanilla-profile API input/result.
# Boundary: UI display only; no CLASS execution, no Render API modification,
# no likelihood evaluation, no posterior comparison, no Planck validation.

_DTI_VANILLA_INPUT_RESULT_DISPLAY_POLISH_V1 = True

def _dti_vanilla_display_value_v1(value):
    if value is None:
        return "not returned by this lightweight endpoint"
    try:
        if pd.isna(value):
            return "not returned by this lightweight endpoint"
    except Exception:
        pass
    if isinstance(value, float):
        return round(value, 6)
    return value

def _dti_vanilla_payload_rows_v1(payload):
    rows = []
    if isinstance(payload, dict):
        for key in ["H0", "omega_cdm", "omega_b", "n_s", "ln10_10_As", "tau_reio", "sigma8", "S8", "f_EDE", "z_c"]:
            if key in payload:
                rows.append({"field": key, "value": _dti_vanilla_display_value_v1(payload.get(key))})
    return rows

def _dti_vanilla_result_rows_v1(result):
    rows = []
    if not isinstance(result, dict):
        return rows

    for key in ["ok", "status", "endpoint", "version"]:
        if key in result:
            rows.append({"field": key, "value": _dti_vanilla_display_value_v1(result.get(key))})

    inp = result.get("input", {})
    if isinstance(inp, dict):
        for key in ["H0", "omega_cdm", "omega_b", "n_s", "ln10_10_As", "tau_reio", "sigma8", "S8", "f_EDE", "z_c"]:
            if key in inp:
                rows.append({"field": f"input.{key}", "value": _dti_vanilla_display_value_v1(inp.get(key))})

    drv = result.get("derived", {})
    if isinstance(drv, dict):
        for key in ["h", "omega_m_proxy", "sigma8_reference", "S8_proxy_from_reference", "S8_proxy"]:
            if key in drv:
                rows.append({"field": f"derived.{key}", "value": _dti_vanilla_display_value_v1(drv.get(key))})

    return rows

def _dti_render_vanilla_probe_input_display_v1(payload):
    st.caption(
        "Payload preview for the configured vanilla-profile API endpoint. "
        "Shown as a compact table first; raw JSON is preserved below for audit."
    )
    rows = _dti_vanilla_payload_rows_v1(payload)
    if rows:
        _dti_arrow_safe_df_v1(pd.DataFrame(rows), width="stretch", hide_index=True)
    else:
        st.info("No vanilla-profile payload values are available yet.")
    with st.expander("Raw data — audit view", expanded=False):
        st.json(payload)

def _dti_render_vanilla_api_result_display_v1(result, http_status=None, cache_note=None):
    # st.markdown("### Vanilla-profile API check result")  # rendered by DTI_VANILLA_INPUT_RESULT_DISPLAY_POLISH_V1

    ok = bool(result.get("ok")) if isinstance(result, dict) else False
    status = result.get("status", "unknown") if isinstance(result, dict) else "unknown"
    endpoint = result.get("endpoint", "unknown") if isinstance(result, dict) else "unknown"

    if ok and str(status).lower() == "ok":
        st.success(f"Vanilla-profile API check: PASS / HTTP {http_status if http_status is not None else 'unknown'}")
    else:
        st.warning(f"Vanilla-profile API check: REVIEW / HTTP {http_status if http_status is not None else 'unknown'}")

    summary_rows = [
        {"field": "HTTP status", "value": http_status if http_status is not None else "unknown"},
        {"field": "API status", "value": status},
        {"field": "endpoint", "value": endpoint},
        {"field": "boundary", "value": "exploratory API check only; not likelihood, posterior, or Planck validation"},
    ]
    if cache_note:
        summary_rows.append({"field": "frontend cache", "value": cache_note})

    _dti_arrow_safe_df_v1(pd.DataFrame(summary_rows), width="stretch", hide_index=True)

    rows = _dti_vanilla_result_rows_v1(result)
    if rows:
        st.markdown("#### Input and derived summary")
        _dti_arrow_safe_df_v1(pd.DataFrame(rows), width="stretch", hide_index=True)

    with st.expander("Raw data — audit view", expanded=False):
        # DTI_VANILLA_RAW_RESULT_JSON_FIX_AFTER_7C_MISPATCH_V1D
        st.json(result)
        # /DTI_VANILLA_RAW_RESULT_JSON_FIX_AFTER_7C_MISPATCH_V1D

# DTI_VANILLA_RESULT_RAW_JSON_RECURSION_FIX_V1B
# Raw API response expander must render st.json(result), not call the result renderer recursively.
_DTI_VANILLA_RESULT_RAW_JSON_RECURSION_FIX_V1B = True
# /DTI_VANILLA_RESULT_RAW_JSON_RECURSION_FIX_V1B

# --- /DTI_VANILLA_INPUT_RESULT_DISPLAY_POLISH_V1 ---





# --- DTI_BGGEOM_RAW_RENDERER_EARLY_DEFINE_V6G ---
# --- DTI Moresco2016 BC03 cosmic chronometer visual overlay V1: begin ---
_DTI_MORESCO2016_BC03_COMPONENT_VISUAL_TABLE_V1 = (
    {
        "row_id": "M2016_BC03_ROW_001",
        "source_label": "Moresco2016_BOSS_DR9_CC",
        "model_basis": "BC03",
        "z": 0.3802,
        "H_km_s_Mpc": 83.0,
        "sigma_km_s_Mpc": 13.5,
        "uncertainty_semantics": "sigma_tot_BC03",
    },
    {
        "row_id": "M2016_BC03_ROW_002",
        "source_label": "Moresco2016_BOSS_DR9_CC",
        "model_basis": "BC03",
        "z": 0.4004,
        "H_km_s_Mpc": 77.0,
        "sigma_km_s_Mpc": 10.2,
        "uncertainty_semantics": "sigma_tot_BC03",
    },
    {
        "row_id": "M2016_BC03_ROW_003",
        "source_label": "Moresco2016_BOSS_DR9_CC",
        "model_basis": "BC03",
        "z": 0.4247,
        "H_km_s_Mpc": 87.1,
        "sigma_km_s_Mpc": 11.2,
        "uncertainty_semantics": "sigma_tot_BC03",
    },
    {
        "row_id": "M2016_BC03_ROW_004",
        "source_label": "Moresco2016_BOSS_DR9_CC",
        "model_basis": "BC03",
        "z": 0.4497,
        "H_km_s_Mpc": 92.8,
        "sigma_km_s_Mpc": 12.9,
        "uncertainty_semantics": "sigma_tot_BC03",
    },
    {
        "row_id": "M2016_BC03_ROW_005",
        "source_label": "Moresco2016_BOSS_DR9_CC",
        "model_basis": "BC03",
        "z": 0.4783,
        "H_km_s_Mpc": 80.9,
        "sigma_km_s_Mpc": 9.0,
        "uncertainty_semantics": "sigma_tot_BC03",
    },
)


def _dti_render_moresco2016_bc03_cc_visual_overlay_v1(_dti_moresco2016_caller_scope_v1=None):
    """Render a visual-only Moresco2016 BC03 cosmic-chronometer overlay panel."""
    rows = list(_DTI_MORESCO2016_BC03_COMPONENT_VISUAL_TABLE_V1)

    with st.expander(
        "Cosmic chronometer overlay — Moresco2016 BC03 component rows, visual-only",
        expanded=False,
    ):
        st.warning(
            "Audit-only visual overlay candidate. These are five BC03 component-row "
            "H(z) measurements from the direct Moresco2016 BOSS DR9 cosmic-chronometer "
            "source record. The table uses sigma_tot_BC03. Combined points, M11 "
            "alternatives, and LeafMelia duplicate/compiled rows are excluded. This panel "
            "is visual-only, not a likelihood evaluation, not a posterior comparison, "
            "not a fit, not an independent-count claim, and not a cosmological validation."
        )

        st.caption(
            "Source label: Moresco2016_BOSS_DR9_CC | model basis: BC03 | "
            "uncertainty: sigma_tot_BC03 | visual diagnostic only"
        )

        st.dataframe(rows, use_container_width=True)

        st.caption("DTI_MORESCO2016_STATIC_PNG_ASSET_CHART_V1")
        # DTI_MORESCO2016_LOCAL_DIAG_CHI2_LOCAL_ONLY_PATCH_V1_BEGIN
        # Local diagnostic-only residual auditor for Moresco2016 BC03 rows.
        # Boundary: not likelihood, not posterior, not fit, not validation, backend-disconnected.
        def _dti_moresco2016_validate_model_grid_v1(z_model, h_model):
            try:
                if z_model is None or h_model is None:
                    return False, "missing_model_grid"
                z_vals = list(z_model)
                h_vals = list(h_model)
                if len(z_vals) != len(h_vals):
                    return False, "grid_length_mismatch"
                if len(z_vals) < 2:
                    return False, "grid_too_short"
                for j in range(len(z_vals) - 1):
                    if not float(z_vals[j]) < float(z_vals[j + 1]):
                        return False, "grid_not_strictly_increasing"
                return True, "ok"
            except Exception as exc:
                return False, f"grid_validation_exception: {exc}"

        def _dti_moresco2016_linear_interp_v1(z_model, h_model, z_obs):
            z_vals = [float(v) for v in z_model]
            h_vals = [float(v) for v in h_model]
            z = float(z_obs)
            if z < z_vals[0] or z > z_vals[-1]:
                return None, "out_of_range"
            for j in range(len(z_vals) - 1):
                z0 = z_vals[j]
                z1 = z_vals[j + 1]
                if z0 <= z <= z1:
                    h0 = h_vals[j]
                    h1 = h_vals[j + 1]
                    if z1 == z0:
                        return None, "zero_width_grid_interval"
                    t = (z - z0) / (z1 - z0)
                    return h0 + t * (h1 - h0), "ok"
            return None, "interpolation_interval_not_found"

        def _dti_moresco2016_find_app_side_hz_grid_v1(local_scope):
            # DTI_MORESCO2016_LOCAL_DERIVED_EA_TO_HZ_BRIDGE_EXECUTE_V1_HELPER
            def _dti_as_float_array_v1(value):
                try:
                    arr = np.asarray(value, dtype=float).reshape(-1)
                except Exception:
                    return None
                if arr.size < 2:
                    return None
                if not np.all(np.isfinite(arr)):
                    return None
                return arr

            def _dti_normalize_grid_v1(z_values, h_values):
                z_arr = _dti_as_float_array_v1(z_values)
                h_arr = _dti_as_float_array_v1(h_values)
                if z_arr is None or h_arr is None:
                    return None, None
                if z_arr.shape != h_arr.shape:
                    return None, None
                if np.any(h_arr <= 0):
                    return None, None
                order = np.argsort(z_arr)
                z_arr = z_arr[order]
                h_arr = h_arr[order]
                if np.any(np.diff(z_arr) <= 0):
                    return None, None
                return z_arr, h_arr

            candidate_pairs = [
                ("z_model_grid", "h_model_grid"),
                ("z_model_grid", "H_model_grid"),
                ("z_grid", "H_grid"),
                ("z_grid", "h_grid"),
                ("z_values", "H_values"),
                ("z_bg", "H_bg"),
                ("z_arr", "H_arr"),
            ]

            for z_name, h_name in candidate_pairs:
                if z_name in local_scope and h_name in local_scope:
                    z_arr, h_arr = _dti_normalize_grid_v1(local_scope.get(z_name), local_scope.get(h_name))
                    if z_arr is not None and h_arr is not None:
                        return z_arr, h_arr, f"{z_name}/{h_name}"

            # Derived diagnostic-only bridge. This uses already-computed local background quantities only.
            # It is not a backend call, CLASS/AxiCLASS run, likelihood, posterior, fit, or validation.
            if all(k in local_scope for k in ("z_bg", "e_a", "H0")):
                try:
                    H0_value = float(local_scope.get("H0"))
                except Exception:
                    H0_value = float("nan")
                if np.isfinite(H0_value) and H0_value > 0:
                    z_arr = _dti_as_float_array_v1(local_scope.get("z_bg"))
                    e_arr = _dti_as_float_array_v1(local_scope.get("e_a"))
                    if z_arr is not None and e_arr is not None and z_arr.shape == e_arr.shape and np.all(e_arr > 0):
                        derived_diagnostic_Hz = H0_value * e_arr
                        z_arr, h_arr = _dti_normalize_grid_v1(z_arr, derived_diagnostic_Hz)
                        if z_arr is not None and h_arr is not None:
                            return z_arr, h_arr, "derived_local_Ea_to_Hz_bridge"

            return None, None, "not_found"

        def _dti_moresco2016_compute_local_diag_chi2_like_v1(z_model, h_model):
            rows = (
                {"row_id": "M2016_BC03_ROW_001", "z": 0.3802, "H_obs": 83.0, "sigma_eff": 13.5},
                {"row_id": "M2016_BC03_ROW_002", "z": 0.4004, "H_obs": 77.0, "sigma_eff": 10.2},
                {"row_id": "M2016_BC03_ROW_003", "z": 0.4247, "H_obs": 87.1, "sigma_eff": 11.2},
                {"row_id": "M2016_BC03_ROW_004", "z": 0.4497, "H_obs": 92.8, "sigma_eff": 12.9},
                {"row_id": "M2016_BC03_ROW_005", "z": 0.4783, "H_obs": 80.9, "sigma_eff": 9.0},
            )
            ok, reason = _dti_moresco2016_validate_model_grid_v1(z_model, h_model)
            if not ok:
                return {"status": "inactive", "reason": reason, "N_used": 0, "N_deferred": len(rows), "chi2_diag_like": None, "used_rows": [], "deferred_rows": [r["row_id"] for r in rows]}
            used_rows = []
            deferred_rows = []
            for row in rows:
                h_interp, interp_status = _dti_moresco2016_linear_interp_v1(z_model, h_model, row["z"])
                if h_interp is None:
                    deferred_rows.append({"row_id": row["row_id"], "reason": interp_status})
                    continue
                residual = float(row["H_obs"]) - float(h_interp)
                normalized = residual / float(row["sigma_eff"])
                contribution = normalized * normalized
                used_rows.append({
                    "row_id": row["row_id"],
                    "z": float(row["z"]),
                    "H_obs": float(row["H_obs"]),
                    "H_model_interp": float(h_interp),
                    "sigma_eff": float(row["sigma_eff"]),
                    "residual": float(residual),
                    "normalized_residual": float(normalized),
                    "chi2_like_contribution": float(contribution),
                })
            score = sum(r["chi2_like_contribution"] for r in used_rows) if used_rows else None
            return {
                "status": "active" if used_rows else "inactive_no_used_rows",
                "reason": "ok" if used_rows else "no_used_rows",
                "N_used": len(used_rows),
                "N_deferred": len(deferred_rows),
                "chi2_diag_like": score,
                "used_rows": used_rows,
                "deferred_rows": deferred_rows,
            }

        with st.expander("Dynamic residual auditor — diagnostic-only", expanded=False):
            st.caption("DTI_MORESCO2016_LOCAL_DIAG_CHI2_LOCAL_ONLY_PATCH_V1")
            st.markdown(
                "Dataset: Moresco2016 BC03 component rows only. "
                "Score: Moresco2016 BC03 diagonal chi2-like diagnostic score."
            )
            # DTI_MORESCO2016_LOCAL_HZ_GRID_SOURCE_ACTIVATION_EXECUTE_V1F_OVERLAY_SCOPE
            _dti_moresco2016_helper_scope_v1 = dict(locals())
            try:
                _dti_payload_v1 = st.session_state.get("dti_moresco2016_bg_proxy_grid_v1", None)
                if isinstance(_dti_payload_v1, dict):
                    _dti_moresco2016_helper_scope_v1.update({
                        "z_bg": _dti_payload_v1.get("z_bg"),
                        "e_a": _dti_payload_v1.get("e_a"),
                        "H0": _dti_payload_v1.get("H0"),
                    })
                    _dti_moresco2016_helper_scope_v1["dti_moresco2016_grid_source_hint_v1"] = "session_state_bg_proxy_Ea_to_Hz_bridge"
            except Exception:
                pass
            # DTI_MORESCO2016_CALLSITE_GUARDED_PARAM_SOURCE_PATCH_EXECUTE_V1B_ANCHOR_TOLERANT
            try:
                if "dti_moresco2016_bg_proxy_grid_v1" not in st.session_state:
                    # DTI_MORESCO2016_CALLER_SCOPE_BRIDGE_PATCH_V1
                    _dti_moresco2016_globals_v1 = (
                        _dti_moresco2016_caller_scope_v1
                        if isinstance(_dti_moresco2016_caller_scope_v1, dict)
                        else globals()
                    )
                    _dti_moresco2016_required_param_keys_v1 = ("h", "ob", "oc", "fe", "zc")
                    _dti_moresco2016_has_param_source_v1 = all(
                        _dti_key_v1 in _dti_moresco2016_globals_v1
                        for _dti_key_v1 in _dti_moresco2016_required_param_keys_v1
                    )
                    # DTI_MORESCO2016_TARGET_MODEL_PARAM_BRIDGE_PATCH_V1
                    if not _dti_moresco2016_has_param_source_v1:
                        _dti_moresco2016_target_model_v1 = _dti_moresco2016_globals_v1.get("target_model", None)
                        if isinstance(_dti_moresco2016_target_model_v1, dict):
                            try:
                                _dti_moresco2016_tm_h_v1 = _dti_moresco2016_target_model_v1.get(
                                    "h",
                                    _dti_moresco2016_target_model_v1.get("H0", np.nan) / 100.0,
                                )
                                _dti_moresco2016_tm_ob_v1 = _dti_moresco2016_target_model_v1.get("omega_b", np.nan)
                                _dti_moresco2016_tm_oc_v1 = _dti_moresco2016_target_model_v1.get("omega_cdm", np.nan)
                                _dti_moresco2016_tm_fe_v1 = _dti_moresco2016_target_model_v1.get("f_EDE", 0.0)
                                _dti_moresco2016_tm_zc_v1 = _dti_moresco2016_target_model_v1.get("z_c", 0.0)

                                _dti_moresco2016_tm_values_v1 = [
                                    float(_dti_moresco2016_tm_h_v1),
                                    float(_dti_moresco2016_tm_ob_v1),
                                    float(_dti_moresco2016_tm_oc_v1),
                                    float(_dti_moresco2016_tm_fe_v1),
                                    float(_dti_moresco2016_tm_zc_v1),
                                ]
                                if np.isfinite(_dti_moresco2016_tm_values_v1[0]) and np.isfinite(_dti_moresco2016_tm_values_v1[1]) and np.isfinite(_dti_moresco2016_tm_values_v1[2]):
                                    _dti_moresco2016_globals_v1 = dict(_dti_moresco2016_globals_v1)
                                    _dti_moresco2016_globals_v1.update({
                                        "h": _dti_moresco2016_tm_values_v1[0],
                                        "ob": _dti_moresco2016_tm_values_v1[1],
                                        "oc": _dti_moresco2016_tm_values_v1[2],
                                        "fe": _dti_moresco2016_tm_values_v1[3],
                                        "zc": _dti_moresco2016_tm_values_v1[4],
                                    })
                                    _dti_moresco2016_has_param_source_v1 = True
                                    st.session_state["dti_moresco2016_bg_proxy_grid_v1_guarded_call_status"] = "param_source_from_target_model_v1"
                                    st.session_state["dti_moresco2016_bg_proxy_param_source_v1"] = {
                                        "h": _dti_moresco2016_tm_values_v1[0],
                                        "ob": _dti_moresco2016_tm_values_v1[1],
                                        "oc": _dti_moresco2016_tm_values_v1[2],
                                        "fe": _dti_moresco2016_tm_values_v1[3],
                                        "zc": _dti_moresco2016_tm_values_v1[4],
                                        "source": "target_model_from_current_ui",
                                        "boundary": "diagnostic_only_not_likelihood_not_posterior_not_fit_not_validation",
                                    }
                            except Exception as _dti_moresco2016_tm_exc_v1:
                                st.session_state["dti_moresco2016_bg_proxy_grid_v1_guarded_call_status"] = (
                                    "target_model_param_source_failed:" + type(_dti_moresco2016_tm_exc_v1).__name__
                                )
                    if _dti_moresco2016_has_param_source_v1:
                        _dti_moresco2016_guarded_proxy_v1 = compute_background_proxy(
                            float(_dti_moresco2016_globals_v1["h"]),
                            float(_dti_moresco2016_globals_v1["ob"]),
                            float(_dti_moresco2016_globals_v1["oc"]),
                            float(_dti_moresco2016_globals_v1["fe"]),
                            float(_dti_moresco2016_globals_v1["zc"]),
                        )
                        st.session_state["dti_moresco2016_bg_proxy_grid_v1_guarded_call_count"] = int(
                            st.session_state.get("dti_moresco2016_bg_proxy_grid_v1_guarded_call_count", 0)
                        ) + 1
                        st.session_state["dti_moresco2016_bg_proxy_grid_v1_guarded_call_status"] = "attempted_from_moresco_overlay_v1b"
                        _dti_moresco2016_payload_after_guard_v1 = st.session_state.get("dti_moresco2016_bg_proxy_grid_v1", None)
                        if isinstance(_dti_moresco2016_payload_after_guard_v1, dict):
                            _dti_moresco2016_helper_scope_v1.update({
                                "z_bg": _dti_moresco2016_payload_after_guard_v1.get("z_bg"),
                                "e_a": _dti_moresco2016_payload_after_guard_v1.get("e_a"),
                                "H0": _dti_moresco2016_payload_after_guard_v1.get("H0"),
                                "H_model": _dti_moresco2016_payload_after_guard_v1.get("H_model"),
                                "dti_moresco2016_grid_source_hint_v1": "session_state_bg_proxy_Ea_to_Hz_bridge",
                            })
                    else:
                        st.session_state["dti_moresco2016_bg_proxy_grid_v1_guarded_call_status"] = "missing_global_param_source_v1b"
            except Exception as _dti_moresco2016_guarded_exc_v1:
                st.session_state["dti_moresco2016_bg_proxy_grid_v1_guarded_call_status"] = (
                    "guarded_call_failed_v1b:" + type(_dti_moresco2016_guarded_exc_v1).__name__
                )
            # DTI_MORESCO2016_EXPLICIT_HZ_GRID_EA_COMPAT_PATCH_V1
            # Compatibility adapter: the explicit diagnostic H(z) grid already has
            # z_bg, H0, and H_model. The existing helper path expects e_a, so derive
            # e_a = H_model / H0 locally. Diagnostic-only; not likelihood/posterior/fit/validation.
            try:
                _dti_moresco2016_payload_ea_v1 = st.session_state.get("dti_moresco2016_bg_proxy_grid_v1", None)
                if isinstance(_dti_moresco2016_payload_ea_v1, dict):
                    _dti_moresco2016_z_for_ea_v1 = _dti_moresco2016_payload_ea_v1.get("z_bg", None)
                    _dti_moresco2016_h_for_ea_v1 = _dti_moresco2016_payload_ea_v1.get("H_model", None)
                    _dti_moresco2016_h0_for_ea_v1 = _dti_moresco2016_payload_ea_v1.get("H0", None)
                    if (
                        "e_a" not in _dti_moresco2016_payload_ea_v1
                        and _dti_moresco2016_z_for_ea_v1 is not None
                        and _dti_moresco2016_h_for_ea_v1 is not None
                        and _dti_moresco2016_h0_for_ea_v1 is not None
                    ):
                        _dti_moresco2016_h0_float_v1 = float(_dti_moresco2016_h0_for_ea_v1)
                        if _dti_moresco2016_h0_float_v1 > 0:
                            _dti_moresco2016_h_arr_for_ea_v1 = np.asarray(_dti_moresco2016_h_for_ea_v1, dtype=float)
                            _dti_moresco2016_ea_arr_v1 = _dti_moresco2016_h_arr_for_ea_v1 / _dti_moresco2016_h0_float_v1
                            _dti_moresco2016_payload_ea_v1["e_a"] = _dti_moresco2016_ea_arr_v1.tolist()
                            _dti_moresco2016_payload_ea_v1["ea_compat_source"] = "H_model_over_H0"
                            _dti_moresco2016_payload_ea_v1["ea_compat_boundary"] = "diagnostic_only_not_likelihood_not_posterior_not_fit_not_validation"
                            st.session_state["dti_moresco2016_bg_proxy_grid_v1"] = _dti_moresco2016_payload_ea_v1
                            st.session_state["dti_moresco2016_bg_proxy_grid_v1_ea_compat_status"] = "created_from_H_model_over_H0_v1"
                            st.session_state["dti_moresco2016_bg_proxy_grid_v1_ea_compat_count"] = int(
                                st.session_state.get("dti_moresco2016_bg_proxy_grid_v1_ea_compat_count", 0)
                            ) + 1
                    if "e_a" in _dti_moresco2016_payload_ea_v1:
                        _dti_moresco2016_helper_scope_v1.update({
                            "z_bg": _dti_moresco2016_payload_ea_v1.get("z_bg"),
                            "e_a": _dti_moresco2016_payload_ea_v1.get("e_a"),
                            "H0": _dti_moresco2016_payload_ea_v1.get("H0"),
                            "H_model": _dti_moresco2016_payload_ea_v1.get("H_model"),
                            "dti_moresco2016_grid_source_hint_v1": "explicit_target_model_background_Hz_grid_diagnostic_only",
                        })
                else:
                    st.session_state["dti_moresco2016_bg_proxy_grid_v1_ea_compat_status"] = "payload_missing_or_not_dict"
            except Exception as _dti_moresco2016_ea_compat_exc_v1:
                st.session_state["dti_moresco2016_bg_proxy_grid_v1_ea_compat_status"] = (
                    "ea_compat_failed:" + type(_dti_moresco2016_ea_compat_exc_v1).__name__
                )
            _dti_z_model_v1, _dti_h_model_v1, _dti_grid_source_v1 = _dti_moresco2016_find_app_side_hz_grid_v1(_dti_moresco2016_helper_scope_v1)
            if (
                _dti_grid_source_v1 == "derived_local_Ea_to_Hz_bridge"
                and _dti_moresco2016_helper_scope_v1.get("dti_moresco2016_grid_source_hint_v1") == "session_state_bg_proxy_Ea_to_Hz_bridge"
            ):
                _dti_grid_source_v1 = "session_state_bg_proxy_Ea_to_Hz_bridge"

            # DTI_MORESCO2016_ACTIVATION_RUNTIME_DIAGNOSTIC_EXECUTE_V1_UI
            try:
                # DTI_MORESCO2016_PARAM_PAYLOAD_TO_EXPLICIT_HZ_GRID_PATCH_V1
                try:
                    if "dti_moresco2016_bg_proxy_grid_v1" not in st.session_state:
                        _dti_param_payload_v1 = st.session_state.get("dti_moresco2016_bg_proxy_param_source_v1", None)
                        if isinstance(_dti_param_payload_v1, dict):
                            _dti_h_v1 = float(_dti_param_payload_v1.get("h"))
                            _dti_ob_v1 = float(_dti_param_payload_v1.get("ob"))
                            _dti_oc_v1 = float(_dti_param_payload_v1.get("oc"))
                            _dti_fe_v1 = float(_dti_param_payload_v1.get("fe", 0.0))
                            _dti_zc_v1 = float(_dti_param_payload_v1.get("zc", 0.0))

                            _dti_z_grid_v1 = np.linspace(0.0, 2.5, 320)
                            _dti_H0_v1 = 100.0 * _dti_h_v1
                            _dti_omega_m_eff_v1 = max(_dti_ob_v1 + _dti_oc_v1, 1.0e-8)
                            _dti_omega_de_eff_v1 = max(1.0 - _dti_omega_m_eff_v1, 1.0e-8)

                            # Diagnostic-only background H(z) grid for visual residual audit.
                            # This is not a CLASS/AxiCLASS run, not a likelihood, not a posterior,
                            # not a fit, and not cosmological validation.
                            _dti_E_v1 = np.sqrt(
                                _dti_omega_m_eff_v1 * np.power(1.0 + _dti_z_grid_v1, 3.0)
                                + _dti_omega_de_eff_v1
                            )
                            _dti_H_model_v1 = _dti_H0_v1 * _dti_E_v1

                            if (
                                np.all(np.isfinite(_dti_z_grid_v1))
                                and np.all(np.isfinite(_dti_H_model_v1))
                                and np.all(_dti_H_model_v1 > 0)
                            ):
                                st.session_state["dti_moresco2016_bg_proxy_grid_v1"] = {
                                    "z_bg": _dti_z_grid_v1.tolist(),
                                    "H_model": _dti_H_model_v1.tolist(),
                                    "H0": float(_dti_H0_v1),
                                    "h": float(_dti_h_v1),
                                    "ob": float(_dti_ob_v1),
                                    "oc": float(_dti_oc_v1),
                                    "fe": float(_dti_fe_v1),
                                    "zc": float(_dti_zc_v1),
                                    "source": "explicit_target_model_background_Hz_grid_diagnostic_only",
                                    "boundary": "diagnostic_only_not_likelihood_not_posterior_not_fit_not_validation",
                                }
                                st.session_state["dti_moresco2016_bg_proxy_grid_v1_explicit_grid_status"] = "created_from_param_payload_v1"
                                st.session_state["dti_moresco2016_bg_proxy_grid_v1_explicit_grid_count"] = int(
                                    st.session_state.get("dti_moresco2016_bg_proxy_grid_v1_explicit_grid_count", 0)
                                ) + 1

                                _dti_moresco2016_payload_after_explicit_grid_v1 = st.session_state.get("dti_moresco2016_bg_proxy_grid_v1", None)
                                if isinstance(_dti_moresco2016_payload_after_explicit_grid_v1, dict):
                                    _dti_moresco2016_helper_scope_v1.update({
                                        "z_bg": _dti_moresco2016_payload_after_explicit_grid_v1.get("z_bg"),
                                        "H_model": _dti_moresco2016_payload_after_explicit_grid_v1.get("H_model"),
                                        "H0": _dti_moresco2016_payload_after_explicit_grid_v1.get("H0"),
                                        "dti_moresco2016_grid_source_hint_v1": "explicit_target_model_background_Hz_grid_diagnostic_only",
                                    })
                            else:
                                st.session_state["dti_moresco2016_bg_proxy_grid_v1_explicit_grid_status"] = "nonfinite_or_nonpositive_H_model"
                        else:
                            st.session_state["dti_moresco2016_bg_proxy_grid_v1_explicit_grid_status"] = "missing_param_payload"
                except Exception as _dti_explicit_grid_exc_v1:
                    st.session_state["dti_moresco2016_bg_proxy_grid_v1_explicit_grid_status"] = (
                        "explicit_grid_failed:" + type(_dti_explicit_grid_exc_v1).__name__
                    )
                # DTI_MORESCO2016_POST_EXPLICIT_GRID_EA_RERUN_HELPER_PATCH_V1B_TOLERANT
                # The explicit diagnostic H(z) grid is created above this point.
                # Derive e_a from H_model/H0 here, then rerun the existing helper before JSON capture.
                # Diagnostic-only; not likelihood/posterior/fit/validation.
                try:
                    _dti_payload_post_grid_v1b = st.session_state.get("dti_moresco2016_bg_proxy_grid_v1", None)
                    if isinstance(_dti_payload_post_grid_v1b, dict):
                        _dti_post_h_model_v1b = _dti_payload_post_grid_v1b.get("H_model", None)
                        _dti_post_h0_v1b = _dti_payload_post_grid_v1b.get("H0", None)
                        if (
                            "e_a" not in _dti_payload_post_grid_v1b
                            and _dti_post_h_model_v1b is not None
                            and _dti_post_h0_v1b is not None
                        ):
                            _dti_post_h0_float_v1b = float(_dti_post_h0_v1b)
                            if _dti_post_h0_float_v1b > 0:
                                _dti_post_h_arr_v1b = np.asarray(_dti_post_h_model_v1b, dtype=float)
                                _dti_post_ea_arr_v1b = _dti_post_h_arr_v1b / _dti_post_h0_float_v1b
                                _dti_payload_post_grid_v1b["e_a"] = _dti_post_ea_arr_v1b.tolist()
                                _dti_payload_post_grid_v1b["ea_compat_source"] = "post_explicit_grid_H_model_over_H0"
                                _dti_payload_post_grid_v1b["ea_compat_boundary"] = "diagnostic_only_not_likelihood_not_posterior_not_fit_not_validation"
                                st.session_state["dti_moresco2016_bg_proxy_grid_v1"] = _dti_payload_post_grid_v1b
                                st.session_state["dti_moresco2016_bg_proxy_grid_v1_post_explicit_ea_status"] = "created_from_H_model_over_H0_after_explicit_grid_v1b"
                                st.session_state["dti_moresco2016_bg_proxy_grid_v1_post_explicit_ea_count"] = int(
                                    st.session_state.get("dti_moresco2016_bg_proxy_grid_v1_post_explicit_ea_count", 0)
                                ) + 1
                
                        if "e_a" in _dti_payload_post_grid_v1b:
                            _dti_moresco2016_helper_scope_v1.update({
                                "z_bg": _dti_payload_post_grid_v1b.get("z_bg"),
                                "e_a": _dti_payload_post_grid_v1b.get("e_a"),
                                "H0": _dti_payload_post_grid_v1b.get("H0"),
                                "H_model": _dti_payload_post_grid_v1b.get("H_model"),
                                "dti_moresco2016_grid_source_hint_v1": "explicit_target_model_background_Hz_grid_diagnostic_only",
                            })
                            _dti_z_model_v1, _dti_h_model_v1, _dti_grid_source_v1 = _dti_moresco2016_find_app_side_hz_grid_v1(
                                _dti_moresco2016_helper_scope_v1
                            )
                            if _dti_grid_source_v1 == "derived_local_Ea_to_Hz_bridge":
                                _dti_grid_source_v1 = "explicit_target_model_background_Hz_grid_diagnostic_only"
                                st.session_state["dti_moresco2016_bg_proxy_grid_v1_helper_rerun_status"] = "model_grid_found_after_post_explicit_ea_v1b"
                            else:
                                st.session_state["dti_moresco2016_bg_proxy_grid_v1_helper_rerun_status"] = str(_dti_grid_source_v1)
                    else:
                        st.session_state["dti_moresco2016_bg_proxy_grid_v1_post_explicit_ea_status"] = "payload_missing_or_not_dict"
                except Exception as _dti_post_explicit_ea_exc_v1b:
                    st.session_state["dti_moresco2016_bg_proxy_grid_v1_post_explicit_ea_status"] = (
                        "post_explicit_ea_failed:" + type(_dti_post_explicit_ea_exc_v1b).__name__
                    )
                _dti_payload_diag_v1 = st.session_state.get("dti_moresco2016_bg_proxy_grid_v1", None)
                _dti_payload_is_dict_v1 = isinstance(_dti_payload_diag_v1, dict)
                _dti_payload_keys_v1 = sorted(list(_dti_payload_diag_v1.keys())) if _dti_payload_is_dict_v1 else []

                def _dti_runtime_diag_array_summary_v1(_dti_value_v1):
                    try:
                        _dti_arr_v1 = np.asarray(_dti_value_v1, dtype=float)
                        return {
                            "present": _dti_value_v1 is not None,
                            "len": int(_dti_arr_v1.size),
                            "finite": int(np.isfinite(_dti_arr_v1).sum()),
                            "positive": int((_dti_arr_v1 > 0).sum()),
                        }
                    except Exception as _dti_exc_v1:
                        return {
                            "present": _dti_value_v1 is not None,
                            "len": 0,
                            "finite": 0,
                            "positive": 0,
                            "error": str(type(_dti_exc_v1).__name__),
                        }

                _dti_runtime_diag_v1 = {
                    "session_key_exists": "dti_moresco2016_bg_proxy_grid_v1" in st.session_state,
                    "payload_type": type(_dti_payload_diag_v1).__name__,
                    "payload_keys": _dti_payload_keys_v1,
                    "store_count": st.session_state.get("dti_moresco2016_bg_proxy_grid_v1_store_count", None),
                    # DTI_MORESCO2016_ADD_GUARDED_STATUS_TO_RUNTIME_JSON_V1
                    "guarded_call_status": st.session_state.get("dti_moresco2016_bg_proxy_grid_v1_guarded_call_status", None),
                    "guarded_call_count": st.session_state.get("dti_moresco2016_bg_proxy_grid_v1_guarded_call_count", None),
                    "guarded_param_source": "caller_scope_or_globals_h_ob_oc_fe_zc",
                    "explicit_grid_status": st.session_state.get("dti_moresco2016_bg_proxy_grid_v1_explicit_grid_status", None),
                    "explicit_grid_count": st.session_state.get("dti_moresco2016_bg_proxy_grid_v1_explicit_grid_count", None),
                    "post_explicit_ea_status": st.session_state.get("dti_moresco2016_bg_proxy_grid_v1_post_explicit_ea_status", None),
                    "post_explicit_ea_count": st.session_state.get("dti_moresco2016_bg_proxy_grid_v1_post_explicit_ea_count", None),
                    "helper_rerun_status": st.session_state.get("dti_moresco2016_bg_proxy_grid_v1_helper_rerun_status", None),
                    "target_model_param_payload_exists": "dti_moresco2016_bg_proxy_param_source_v1" in st.session_state,
                    "target_model_param_payload_keys": sorted(list(st.session_state.get("dti_moresco2016_bg_proxy_param_source_v1", {}).keys())) if isinstance(st.session_state.get("dti_moresco2016_bg_proxy_param_source_v1", None), dict) else [],
                    "payload_has_z_bg": _dti_payload_is_dict_v1 and ("z_bg" in _dti_payload_diag_v1),
                    "payload_has_e_a": _dti_payload_is_dict_v1 and ("e_a" in _dti_payload_diag_v1),
                    "payload_has_H0": _dti_payload_is_dict_v1 and ("H0" in _dti_payload_diag_v1),
                    "payload_has_H_model": _dti_payload_is_dict_v1 and ("H_model" in _dti_payload_diag_v1),
                    "z_bg_summary": _dti_runtime_diag_array_summary_v1(_dti_payload_diag_v1.get("z_bg") if _dti_payload_is_dict_v1 else None),
                    "H_model_summary": _dti_runtime_diag_array_summary_v1(_dti_payload_diag_v1.get("H_model") if _dti_payload_is_dict_v1 else None),
                    "helper_scope_has_z_bg": "z_bg" in _dti_moresco2016_helper_scope_v1,
                    "helper_scope_has_e_a": "e_a" in _dti_moresco2016_helper_scope_v1,
                    "helper_scope_has_H0": "H0" in _dti_moresco2016_helper_scope_v1,
                    "helper_scope_source_hint": _dti_moresco2016_helper_scope_v1.get("dti_moresco2016_grid_source_hint_v1", None),
                    "grid_source_after_helper": _dti_grid_source_v1,
                    "model_grid_found": _dti_z_model_v1 is not None and _dti_h_model_v1 is not None,
                    "boundary": "diagnostic_only_not_likelihood_not_posterior_not_fit_not_validation",
                }
                st.caption("Runtime bridge diagnostic — diagnostic-only")
                st.json(_dti_runtime_diag_v1)
            except Exception as _dti_diag_exc_v1:
                st.caption("Runtime bridge diagnostic — diagnostic-only")
                st.warning(f"Runtime bridge diagnostic unavailable: {type(_dti_diag_exc_v1).__name__}")
            # DTI_MORESCO2016_LOCAL_DERIVED_EA_TO_HZ_BRIDGE_EXECUTE_V1_UI_WORDING
            if _dti_grid_source_v1 in ("derived_local_Ea_to_Hz_bridge", "session_state_bg_proxy_Ea_to_Hz_bridge"):
                st.caption("This local residual auditor uses a diagnostic-only H(z) bridge derived from already-computed local background quantities in this UI state. The bridge source may come from same-scope locals() or the session_state background-proxy bridge. It is not a likelihood evaluation, posterior comparison, fit result, or cosmological validation.")
            _dti_diag_v1 = _dti_moresco2016_compute_local_diag_chi2_like_v1(_dti_z_model_v1, _dti_h_model_v1)
            if _dti_diag_v1.get("status") == "active":
                st.metric("Moresco2016 BC03 diagonal χ²-like diagnostic score", f"{_dti_diag_v1['chi2_diag_like']:.3f}")
                st.caption(f"N_used={_dti_diag_v1['N_used']} / N_deferred={_dti_diag_v1['N_deferred']} / grid={_dti_grid_source_v1}")
                st.dataframe(_dti_diag_v1["used_rows"], use_container_width=True, hide_index=True)
            else:
                st.info(
                    "Local residual auditor inactive: app-side H(z) model grid was not found in this UI scope. "
                    "This is expected until a later gate wires an explicit local H(z) grid source."
                )
                st.caption(f"status={_dti_diag_v1.get('status')}; reason={_dti_diag_v1.get('reason')}; grid={_dti_grid_source_v1}")
            st.caption(
                "Boundary: not a likelihood evaluation; not a posterior comparison; not a fit; "
                "not an independent-count claim; not cosmological validation; "
                "backend-disconnected; CLASS/AxiCLASS not run; MCMC not run."
            )
        # DTI_MORESCO2016_LOCAL_DIAG_CHI2_LOCAL_ONLY_PATCH_V1_END
        from pathlib import Path as _DtiPath

        png_asset_path = _DtiPath(__file__).resolve().parent / "assets/moresco2016/moresco2016_bc03_component_rows_static_visual_v1.png"
        if png_asset_path.exists():
            st.image(str(png_asset_path), use_container_width=True)
        else:
            st.warning("Moresco2016 static PNG asset is missing; the source table remains available.")

        st.caption(
            "Excluded from this primary visual table: BC03 combined point, M11 combined "
            "point, M11 component rows, and LeafMelia duplicated/compiled rows."
        )

        st.caption(
            "Static PNG visual-only chart; not a likelihood evaluation, "
            "not a posterior comparison, not a fit, not an independent-count claim, "
            "and not a cosmological validation."
        )
# --- DTI Moresco2016 BC03 cosmic chronometer visual overlay V1: end ---

# Early safe raw renderer for Background Geometry.
# Reason: Streamlit may execute the Background Geometry raw audit call before
# the later V6E/V6F renderer block is reached. Keep this definition above the
# Background Geometry Anchor. Display-only; no CLASS, no API, no likelihood.
_DTI_BGGEOM_RAW_RENDERER_EARLY_DEFINE_V6G = True

def _dti_bggeom_json_safe_v6e(obj):
    import math as _math_v6g
    if obj is None or isinstance(obj, (str, bool, int)):
        return obj
    if isinstance(obj, float):
        if _math_v6g.isfinite(obj):
            return obj
        return None
    if isinstance(obj, dict):
        return {str(k): _dti_bggeom_json_safe_v6e(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_dti_bggeom_json_safe_v6e(v) for v in obj]
    try:
        if hasattr(obj, "item"):
            return _dti_bggeom_json_safe_v6e(obj.item())
    except Exception:
        pass
    return str(obj)

def _dti_bggeom_render_raw_data_v6e(obj):
    # DTI_BGGEOM_RAW_RENDERER_NO_WIDGET_KEY_V6J2
    import json as _json_v6j2
    try:
        safe = _dti_bggeom_json_safe_v6e(obj)
    except Exception:
        safe = str(obj)
    try:
        payload = _json_v6j2.dumps(safe, indent=2, sort_keys=True, ensure_ascii=False)
    except Exception:
        payload = str(safe)
    st.text(payload)
    # /DTI_BGGEOM_RAW_RENDERER_NO_WIDGET_KEY_V6J2
    # /DTI_BGGEOM_RAW_RENDERER_TEXTONLY_V6G_EARLY

# --- /DTI_BGGEOM_RAW_RENDERER_EARLY_DEFINE_V6G ---

# --- DTI_BACKGROUND_GEOMETRY_ANCHOR_V1 ---
# Local FLRW background-geometry calculator inspired by the public Ned Wright
# style of distance/time baseline checking. This is a lightweight background
# geometry anchor only: no CLASS run, no Render API call, no likelihood
# evaluation, no posterior comparison, no Planck validation, no physics-value
# update, and no manuscript update.

_DTI_BACKGROUND_GEOMETRY_ANCHOR_V1 = True

def _dti_bggeom_E_v1(z, omega_m, omega_vac):
    omega_k = 1.0 - float(omega_m) - float(omega_vac)
    zp1 = 1.0 + float(z)
    val = float(omega_m) * zp1**3 + omega_k * zp1**2 + float(omega_vac)
    if val <= 0:
        return None
    return val ** 0.5

def _dti_bggeom_integrate_simpson_v1(func, a, b, n=4096):
    a = float(a)
    b = float(b)
    n = int(n)
    if b <= a:
        return 0.0
    if n < 64:
        n = 64
    if n % 2:
        n += 1
    h = (b - a) / n
    total = func(a) + func(b)
    odd = 0.0
    even = 0.0
    for i in range(1, n):
        x = a + h * i
        fx = func(x)
        if fx is None:
            return None
        if i % 2:
            odd += fx
        else:
            even += fx
    return h * (total + 4.0 * odd + 2.0 * even) / 3.0

def _dti_bggeom_compute_v1(H0, omega_m, omega_vac, z):
    H0 = float(H0)
    omega_m = float(omega_m)
    omega_vac = float(omega_vac)
    z = float(z)
    c_km_s = 299792.458
    mpc_km = 3.0856775814913673e19
    sec_per_gyr = 31557600.0 * 1.0e9
    hubble_time_gyr = (mpc_km / H0) / sec_per_gyr
    omega_k = 1.0 - omega_m - omega_vac

    def inv_E(x):
        e = _dti_bggeom_E_v1(x, omega_m, omega_vac)
        return None if e is None else 1.0 / e

    # DTI_BACKGROUND_GEOMETRY_AGE_LOG_INTEGRAL_FIX_V1B
    # For age integrals, integrate over y = log(1+z), not over z directly.
    # Since dz / ((1+z) E(z)) = dy / E(exp(y)-1), this avoids numerical
    # over-weighting of the very wide high-redshift interval.
    def inv_age_integrand_y(y):
        zz = math.exp(float(y)) - 1.0
        e = _dti_bggeom_E_v1(zz, omega_m, omega_vac)
        return None if e is None else 1.0 / e

    zmax_age = 100000.0
    ymax_age = math.log1p(zmax_age)
    yz = math.log1p(z)
    age_now_int = _dti_bggeom_integrate_simpson_v1(inv_age_integrand_y, 0.0, ymax_age, n=12000)
    lookback_int = _dti_bggeom_integrate_simpson_v1(inv_age_integrand_y, 0.0, yz, n=4096)
    dc_int = _dti_bggeom_integrate_simpson_v1(inv_E, 0.0, z, n=4096)

    if age_now_int is None or lookback_int is None or dc_int is None:
        return {"status": "invalid", "reason": "E(z) became non-positive within the integration interval"}

    age_now_gyr = hubble_time_gyr * age_now_int
    lookback_gyr = hubble_time_gyr * lookback_int
    age_at_z_gyr = age_now_gyr - lookback_gyr

    dh_mpc = c_km_s / H0
    dc_mpc = dh_mpc * dc_int

    if abs(omega_k) < 1e-10:
        dm_mpc = dc_mpc
        curvature = "flat"
    elif omega_k > 0:
        sqrt_ok = omega_k ** 0.5
        dm_mpc = dh_mpc / sqrt_ok * math.sinh(sqrt_ok * dc_int)
        curvature = "open"
    else:
        sqrt_abs_ok = (-omega_k) ** 0.5
        dm_mpc = dh_mpc / sqrt_abs_ok * math.sin(sqrt_abs_ok * dc_int)
        curvature = "closed"

    da_mpc = dm_mpc / (1.0 + z)
    dl_mpc = dm_mpc * (1.0 + z)
    scale_kpc_per_arcsec = da_mpc * 1000.0 / 206265.0

    return {
        "status": "ok",
        "boundary": {
            "local_background_geometry_only": True,
            "class_run": False,
            "render_api_call": False,
            "likelihood_evaluation": False,
            "posterior_comparison": False,
            "planck_validation": False,
            "physics_value_update": False,
            "manuscript_update": False,
        },
        "input": {
            "H0": H0,
            "Omega_M": omega_m,
            "Omega_vac": omega_vac,
            "Omega_k": omega_k,
            "z": z,
            "curvature": curvature,
        },
        "time": {
            "hubble_time_Gyr": hubble_time_gyr,
            "age_now_Gyr": age_now_gyr,
            "age_at_z_Gyr": age_at_z_gyr,
            "light_travel_time_Gyr": lookback_gyr,
        },
        "distance": {
            "hubble_distance_Mpc": dh_mpc,
            "comoving_radial_distance_Mpc": dc_mpc,
            "transverse_comoving_distance_Mpc": dm_mpc,
            "angular_diameter_distance_Mpc": da_mpc,
            "luminosity_distance_Mpc": dl_mpc,
            "scale_kpc_per_arcsec": scale_kpc_per_arcsec,
        },
    }

def _dti_bggeom_rows_v1(result, group):
    rows = []
    if not isinstance(result, dict) or result.get("status") != "ok":
        return rows
    src = result.get(group, {})
    if not isinstance(src, dict):
        return rows
    for k, v in src.items():
        if isinstance(v, float):
            rows.append({"quantity": k, "value": round(v, 6)})
        else:
            rows.append({"quantity": k, "value": v})
    return rows

def _dti_render_background_geometry_anchor_v1():
    with st.expander("Background geometry anchor — local FLRW calculator", expanded=False):
        st.caption(
            "Summary → compact table → raw audit view. Local background-geometry baseline only; detailed limits are in Global claim limits / audit boundary."
        )

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            bg_H0 = st.number_input(
                "Geometry H0",
                min_value=40.0,
                max_value=100.0,
                value=69.6,
                step=0.1,
                format="%.3f",
                key="dti_bggeom_H0_v1",
            )
        with c2:
            bg_om = st.number_input(
                "Geometry Omega_M",
                min_value=0.01,
                max_value=1.50,
                value=0.286,
                step=0.001,
                format="%.4f",
                key="dti_bggeom_omega_m_v1",
            )
        with c3:
            bg_ov = st.number_input(
                "Geometry Omega_vac",
                min_value=0.0,
                max_value=1.50,
                value=0.714,
                step=0.001,
                format="%.4f",
                key="dti_bggeom_omega_vac_v1",
            )
        with c4:
            bg_z = st.number_input(
                "Geometry redshift z",
                min_value=0.0,
                max_value=1500.0,
                value=3.0,
                step=0.1,
                format="%.3f",
                key="dti_bggeom_z_v1",
            )

        result = _dti_bggeom_compute_v1(bg_H0, bg_om, bg_ov, bg_z)

        if result.get("status") != "ok":
            st.warning("Background geometry calculation returned invalid support for the selected parameters.")
            with st.expander("Raw data — audit view", expanded=False):
                _dti_bggeom_render_raw_data_v6e(result)
            return

        summary_rows = [
            {"field": "status", "value": result["status"]},
            {"field": "curvature", "value": result["input"]["curvature"]},
            {"field": "Omega_k", "value": round(result["input"]["Omega_k"], 8)},
            {"field": "boundary", "value": "local FLRW background geometry only; not CLASS, likelihood, posterior, or Planck validation"},
        ]
        st.markdown("#### Summary")
        _dti_arrow_safe_df_v1(pd.DataFrame(summary_rows), width="stretch", hide_index=True)

        st.markdown("#### Time baseline")
        _dti_arrow_safe_df_v1(pd.DataFrame(_dti_bggeom_rows_v1(result, "time")), width="stretch", hide_index=True)

        st.markdown("#### Distance baseline")
        _dti_arrow_safe_df_v1(pd.DataFrame(_dti_bggeom_rows_v1(result, "distance")), width="stretch", hide_index=True)

        
        # DTI_BACKGROUND_GEOMETRY_GRAPH_CALL_V1
        _dti_render_background_geometry_graph_v1(bg_H0, bg_om, bg_ov, bg_z)

        # DTI_BACKGROUND_GEOMETRY_JUMP_TOY_CALL_V1B
        _dti_render_background_geometry_jump_toy_v1b(bg_H0, bg_om, bg_ov, bg_z)
        # /DTI_BACKGROUND_GEOMETRY_JUMP_TOY_CALL_V1B


# --- DTI_BACKGROUND_GEOMETRY_JUMP_TOY_COMPARATOR_V1B ---
# Local toy comparator: continuous FLRW baseline vs a piecewise jump in E(z).
# Boundary: background-geometry diagnostic only. No CLASS, no Render API,
# no likelihood evaluation, no posterior comparison, no Planck/JWST validation.
_DTI_BACKGROUND_GEOMETRY_JUMP_TOY_COMPARATOR_V1B = True

def _dti_bggeom_E_jump_toy_v1b(z, omega_m, omega_vac, z_jump, jump_factor, delta_z=None):
    import math as _math_jump_width_v1

    base = _dti_bggeom_E_v1(z, omega_m, omega_vac)
    try:
        zf = float(z)
        zj = float(z_jump)
        jf = float(jump_factor)
        dz = None if delta_z is None else float(delta_z)
    except Exception:
        return None
    if base is None:
        return None
    if dz is None or dz <= 0:
        if zf > zj:
            return jf * float(base)
        return float(base)
    transition = 0.5 * (1.0 + _math_jump_width_v1.tanh((zf - zj) / dz))
    return float(base) * (1.0 + (jf - 1.0) * transition)

def _dti_bggeom_compute_jump_toy_v1b(H0, omega_m, omega_vac, z, z_jump, jump_factor, delta_z=0.010):
    import math as _math_jump_v1b

    try:
        H0 = float(H0)
        omega_m = float(omega_m)
        omega_vac = float(omega_vac)
        z = float(z)
        z_jump = float(z_jump)
        jump_factor = float(jump_factor)
        delta_z = float(delta_z)
    except Exception:
        return {"status": "invalid_input", "boundary": "jump toy background geometry only"}

    if H0 <= 0 or omega_m < 0 or omega_vac < 0 or z < 0 or z_jump < 0 or jump_factor <= 0 or delta_z <= 0:
        return {"status": "invalid_support", "boundary": "jump toy background geometry only"}

    c_km_s = 299792.458
    dh_mpc = c_km_s / H0
    hubble_time_gyr = 9.778131 / (H0 / 100.0)

    def E_jump(zz):
        return _dti_bggeom_E_jump_toy_v1b(zz, omega_m, omega_vac, z_jump, jump_factor, delta_z)

    def inv_E(zz):
        E = E_jump(zz)
        if E is None or E <= 0:
            return 0.0
        return 1.0 / E

    def inv_age_y(y):
        zz = _math_jump_v1b.exp(y) - 1.0
        E = E_jump(zz)
        if E is None or E <= 0:
            return 0.0
        return 1.0 / E

    y_max_age = _math_jump_v1b.log(1.0 + 100000.0)
    y_z = _math_jump_v1b.log(1.0 + z)

    age_now_int = _dti_bggeom_integrate_simpson_v1(inv_age_y, 0.0, y_max_age, n=12000)
    age_at_z_int = _dti_bggeom_integrate_simpson_v1(inv_age_y, y_z, y_max_age, n=12000)
    lookback_int = _dti_bggeom_integrate_simpson_v1(inv_age_y, 0.0, y_z, n=2400)
    dc_int = _dti_bggeom_integrate_simpson_v1(inv_E, 0.0, z, n=2400)

    if age_now_int is None or age_at_z_int is None or lookback_int is None or dc_int is None:
        return {"status": "integration_failed", "boundary": "jump toy background geometry only"}

    omega_k = 1.0 - omega_m - omega_vac
    dc_mpc = dh_mpc * dc_int
    dm_mpc = dc_mpc
    da_mpc = dm_mpc / (1.0 + z) if z >= 0 else None
    dl_mpc = dm_mpc * (1.0 + z)

    scale_kpc_per_arcsec = None
    if da_mpc is not None and da_mpc > 0:
        scale_kpc_per_arcsec = da_mpc * 1000.0 / 206265.0

    return {
        "status": "ok",
        "boundary": {
            "local_background_geometry_toy": True,
            "jump_model": "smoothed tanh transition in E(z) around z_jump",
            "class_run": False,
            "render_api_call": False,
            "likelihood_evaluation": False,
            "posterior_comparison": False,
            "planck_validation": False,
            "jwst_validation": False,
            "physics_value_update": False,
            "manuscript_update": False,
        },
        "input": {
            "H0": H0,
            "Omega_M": omega_m,
            "Omega_vac": omega_vac,
            "Omega_k": omega_k,
            "z": z,
            "z_jump": z_jump,
            "jump_factor_E_above_zjump": jump_factor,
            "transition_width_delta_z": delta_z,
        },
        "time": {
            "hubble_time_Gyr": hubble_time_gyr,
            "age_now_Gyr": hubble_time_gyr * age_now_int,
            "age_at_z_Gyr": hubble_time_gyr * age_at_z_int,
            "light_travel_time_Gyr": hubble_time_gyr * lookback_int,
        },
        "distance": {
            "hubble_distance_Mpc": dh_mpc,
            "comoving_radial_distance_Mpc": dc_mpc,
            "transverse_comoving_distance_Mpc": dm_mpc,
            "angular_diameter_distance_Mpc": da_mpc,
            "luminosity_distance_Mpc": dl_mpc,
            "scale_kpc_per_arcsec": scale_kpc_per_arcsec,
        },
    }

def _dti_bggeom_jump_delta_rows_v1b(vanilla, jump):
    rows = []
    pairs = [
        ("age_now_Gyr", "time", "age_now_Gyr"),
        ("age_at_z_Gyr", "time", "age_at_z_Gyr"),
        ("light_travel_time_Gyr", "time", "light_travel_time_Gyr"),
        ("comoving_radial_distance_Mpc", "distance", "comoving_radial_distance_Mpc"),
        ("angular_diameter_distance_Mpc", "distance", "angular_diameter_distance_Mpc"),
        ("luminosity_distance_Mpc", "distance", "luminosity_distance_Mpc"),
        ("scale_kpc_per_arcsec", "distance", "scale_kpc_per_arcsec"),
    ]

    if not isinstance(vanilla, dict) or not isinstance(jump, dict):
        return rows

    for label, group, key in pairs:
        v = vanilla.get(group, {}).get(key)
        j = jump.get(group, {}).get(key)
        try:
            vf = float(v)
            jf = float(j)
            delta = jf - vf
            pct = (delta / vf * 100.0) if vf != 0 else None
            rows.append({
                "quantity": label,
                "vanilla_FLRW": round(vf, 6),
                "jump_toy": round(jf, 6),
                "delta_jump_minus_vanilla": round(delta, 6),
                "delta_percent": None if pct is None else round(pct, 6),
            })
        except Exception:
            rows.append({
                "quantity": label,
                "vanilla_FLRW": v,
                "jump_toy": j,
                "delta_jump_minus_vanilla": None,
                "delta_percent": None,
            })
    return rows

def _dti_bggeom_jump_graph_rows_v1b(H0, omega_m, omega_vac, zmax, z_jump, jump_factor, delta_z):
    rows = []
    try:
        zmax = float(zmax)
    except Exception:
        zmax = 3.0
    if zmax < 0:
        zmax = 0.0

    n = 80
    grid = [0.0] if zmax == 0 else [round(zmax * (i / n) * (i / n), 6) for i in range(n + 1)]

    for zz in grid:
        vanilla = _dti_bggeom_compute_v1(H0, omega_m, omega_vac, zz)
        jump = _dti_bggeom_compute_jump_toy_v1b(H0, omega_m, omega_vac, zz, z_jump, jump_factor, delta_z)
        if vanilla.get("status") != "ok" or jump.get("status") != "ok":
            continue

        row = {"z": zz}
        for group, keys in {
            "time": ["age_at_z_Gyr", "light_travel_time_Gyr"],
            "distance": [
                "comoving_radial_distance_Mpc",
                "luminosity_distance_Mpc",
                "angular_diameter_distance_Mpc",
                "scale_kpc_per_arcsec",
            ],
        }.items():
            for key in keys:
                v = vanilla.get(group, {}).get(key)
                j = jump.get(group, {}).get(key)
                row[f"vanilla_{key}"] = v
                row[f"jump_{key}"] = j
                try:
                    row[f"delta_{key}"] = float(j) - float(v)
                except Exception:
                    row[f"delta_{key}"] = None
        rows.append(row)
    return rows

def _dti_render_background_geometry_jump_toy_v1b(H0, omega_m, omega_vac, z):
    # DTI_BACKGROUND_GEOMETRY_JUMP_TOY_RENDERER_V1B
    with st.expander("Jump toy comparator — piecewise background geometry", expanded=True):
        st.caption(
            "Summary → compact table → Raw data — audit view. Toy background-geometry comparator only; not CLASS, likelihood, posterior, Planck, or JWST validation."
        )

        if st.button("Load jump-toy demonstration values", key="dti_bggeom_load_jump_toy_demo_values_v1"):
            st.session_state["dti_bggeom_jump_z_v1b"] = 2.5
            st.session_state["dti_bggeom_jump_factor_v1b"] = 1.00001
            st.rerun()

        jc1, jc2 = st.columns(2)
        with jc1:
            z_jump = st.number_input(
                "Jump redshift z_jump",
                min_value=0.0,
                max_value=50.0,
                value=3.5,
                step=0.1,
                format="%.3f",
                key="dti_bggeom_jump_z_v1b",
            )
        with jc2:
            jump_factor = st.number_input(
                "Jump factor for E(z) above z_jump",
                min_value=0.1,
                max_value=10.0,
                value=1.05,
                step=0.00001,
                format="%.5f",
                key="dti_bggeom_jump_factor_v1b",
            )
        delta_z_width = st.slider(
            "Transition Width (delta_z)",
            min_value=0.001,
            max_value=0.500,
            value=0.010,
            step=0.001,
            key="dti_bggeom_delta_z_width_v1",
        )
        st.caption(
            "Transition-width control is a front-end toy-background diagnostic only. "
            "It does not run CLASS/AxiCLASS, compute a likelihood, compare posteriors, "
            "perform MCMC, or update manuscript-level values."
        )

        vanilla = _dti_bggeom_compute_v1(H0, omega_m, omega_vac, z)
        jump = _dti_bggeom_compute_jump_toy_v1b(H0, omega_m, omega_vac, z, z_jump, jump_factor, delta_z_width)

        summary_rows = [
            {"field": "mode", "value": "Vanilla FLRW vs piecewise jump toy geometry"},
            {"field": "jump_definition", "value": "E_jump(z) = E_vanilla(z) × [1 + (jump_factor - 1)/2 × (1 + tanh((z - z_jump)/delta_z))]"},
            {"field": "z_jump", "value": z_jump},
            {"field": "jump_factor", "value": jump_factor},
            {"field": "transition_width_delta_z", "value": delta_z_width},
            {"field": "boundary", "value": "local background-geometry toy only; not validation of DTI, Planck, JWST, likelihood, or posterior"},
        ]
        st.markdown("#### Summary")
        _dti_arrow_safe_df_v1(pd.DataFrame(summary_rows), width="stretch", hide_index=True)

        st.markdown("#### Compact table")
        delta_rows = _dti_bggeom_jump_delta_rows_v1b(vanilla, jump)
        if delta_rows:
            _dti_arrow_safe_df_v1(pd.DataFrame(delta_rows), width="stretch", hide_index=True)
        else:
            st.info("Jump comparator table is unavailable for the selected parameters.")

        graph_rows = _dti_bggeom_jump_graph_rows_v1b(H0, omega_m, omega_vac, z, z_jump, jump_factor, delta_z_width)
        if graph_rows:
            st.markdown("#### Jump toy curves")
            ttab, dtab, deltab = st.tabs(["Time baseline", "Distance baseline", "Delta"])

            with ttab:
                _dti_bggeom_svg_chart_v6i2(
                    graph_rows,
                    "z",
                    [
                        ("vanilla_age_at_z_Gyr", "vanilla age at z [Gyr]"),
                        ("jump_age_at_z_Gyr", "jump toy age at z [Gyr]"),
                        ("vanilla_light_travel_time_Gyr", "vanilla light-travel time [Gyr]"),
                        ("jump_light_travel_time_Gyr", "jump toy light-travel time [Gyr]"),
                    ],
                    "Time baseline: vanilla vs jump toy",
                )

            with dtab:
                _dti_bggeom_svg_chart_v6i2(
                    graph_rows,
                    "z",
                    [
                        ("vanilla_comoving_radial_distance_Mpc", "vanilla comoving [Mpc]"),
                        ("jump_comoving_radial_distance_Mpc", "jump toy comoving [Mpc]"),
                        ("vanilla_luminosity_distance_Mpc", "vanilla luminosity [Mpc]"),
                        ("jump_luminosity_distance_Mpc", "jump toy luminosity [Mpc]"),
                    ],
                    "Distance baseline: vanilla vs jump toy",
                )

            with deltab:
                _dti_bggeom_svg_chart_v6i2(
                    graph_rows,
                    "z",
                    [
                        ("delta_age_at_z_Gyr", "delta age at z [Gyr]"),
                        ("delta_comoving_radial_distance_Mpc", "delta comoving [Mpc]"),
                        ("delta_luminosity_distance_Mpc", "delta luminosity [Mpc]"),
                    ],
                    "Delta: jump toy minus vanilla",
                )

        with st.expander("Raw data — audit view", expanded=False):
            _dti_bggeom_render_raw_data_v6e({
                "vanilla": vanilla,
                "jump_toy": jump,
                "delta_rows": delta_rows,
                "graph_rows": graph_rows,
                "boundary": {
                    "local_background_geometry_toy": True,
                    "class_run": False,
                    "render_api_call": False,
                    "likelihood_evaluation": False,
                    "posterior_comparison": False,
                    "planck_validation": False,
                    "jwst_validation": False,
                    "physics_value_update": False,
                    "manuscript_update": False,
                },
            })

# --- /DTI_BACKGROUND_GEOMETRY_JUMP_TOY_COMPARATOR_V1B ---
        # /DTI_BACKGROUND_GEOMETRY_GRAPH_CALL_V1


# --- /DTI_BACKGROUND_GEOMETRY_ANCHOR_V1 ---




# --- DTI_BGGEOM_SAFE_RAW_JSON_RENDERER_V6E ---
# Streamlit Cloud can fail when st.json receives nested numeric objects that
# are internally routed through PyArrow. Keep raw audit visibility but render
# through sanitized json.dumps + st.code.
_DTI_BGGEOM_SAFE_RAW_JSON_RENDERER_V6E = True

def _dti_bggeom_json_safe_v6e(obj):
    import math as _math_v6e
    if obj is None or isinstance(obj, (str, bool, int)):
        return obj
    if isinstance(obj, float):
        if _math_v6e.isfinite(obj):
            return obj
        return None
    if isinstance(obj, dict):
        return {str(k): _dti_bggeom_json_safe_v6e(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_dti_bggeom_json_safe_v6e(v) for v in obj]
    try:
        if hasattr(obj, "item"):
            return _dti_bggeom_json_safe_v6e(obj.item())
    except Exception:
        pass
    return str(obj)

def _dti_bggeom_render_raw_data_v6e(obj):
    # DTI_BGGEOM_RAW_RENDERER_NO_WIDGET_KEY_V6J2
    import json as _json_v6j2
    try:
        safe = _dti_bggeom_json_safe_v6e(obj)
    except Exception:
        safe = str(obj)
    try:
        payload = _json_v6j2.dumps(safe, indent=2, sort_keys=True, ensure_ascii=False)
    except Exception:
        payload = str(safe)
    st.text(payload)
    # /DTI_BGGEOM_RAW_RENDERER_NO_WIDGET_KEY_V6J2
    # /DTI_BGGEOM_RAW_RENDERER_TEXTONLY_V6F_DIRECT

# --- /DTI_BGGEOM_SAFE_RAW_JSON_RENDERER_V6E ---


# --- DTI_BACKGROUND_GEOMETRY_SVG_CHART_V6I2 ---
# Local SVG renderer for Background Geometry only.
# Reason: st.line_chart may be globally silenced elsewhere in the app.
_DTI_BACKGROUND_GEOMETRY_SVG_CHART_V6I2 = True

def _dti_bggeom_svg_chart_v6i2(rows, x_key, series_specs, title):
    import math as _math_v6i2
    import html as _html_v6i2

    if not isinstance(rows, list):
        st.info("Graph data is unavailable.")
        return

    clean = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        try:
            x = float(row.get(x_key))
        except Exception:
            continue

        vals = {}
        ok_any = False
        for key, label in series_specs:
            val = row.get(key)
            if val is None:
                vals[key] = None
                continue
            try:
                f = float(val)
            except Exception:
                vals[key] = None
                continue
            if _math_v6i2.isfinite(f):
                vals[key] = f
                ok_any = True
            else:
                vals[key] = None

        if ok_any:
            vals["x"] = x
            clean.append(vals)

    if len(clean) < 2:
        st.info("Not enough numeric graph rows for this panel.")
        return

    xs = [r["x"] for r in clean]
    ys = []
    for key, label in series_specs:
        ys.extend([r[key] for r in clean if r.get(key) is not None])

    if not xs or not ys:
        st.info("No numeric graph values for this panel.")
        return

    xmin = min(xs)
    xmax = max(xs)
    ymin = min(ys)
    ymax = max(ys)

    if xmax == xmin:
        xmax = xmin + 1.0
    if ymax == ymin:
        ymax = ymin + 1.0

    width = 760
    height = 320
    left = 56
    right = 18
    top = 28
    bottom = 42
    plot_w = width - left - right
    plot_h = height - top - bottom

    def sx(x):
        return left + (float(x) - xmin) / (xmax - xmin) * plot_w

    def sy(y):
        return top + (1.0 - (float(y) - ymin) / (ymax - ymin)) * plot_h

    palette = ["#7dd3fc", "#fda4af", "#86efac", "#facc15", "#c4b5fd"]

    polylines = []
    legend_items = []

    for idx, spec in enumerate(series_specs):
        key, label = spec
        pts = []
        for r in clean:
            y = r.get(key)
            if y is None:
                continue
            pts.append(f"{sx(r['x']):.2f},{sy(y):.2f}")

        if len(pts) < 2:
            continue

        color = palette[idx % len(palette)]
        safe_label = _html_v6i2.escape(str(label))
        polyline = (
            '<polyline points="' + " ".join(pts) + '" '
            'fill="none" stroke="' + color + '" '
            'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />'
        )
        polylines.append(polyline)

        legend_items.append(
            '<span style="display:inline-flex;align-items:center;margin-right:14px;">'
            '<span style="display:inline-block;width:18px;height:3px;background:' + color + ';margin-right:6px;"></span>'
            + safe_label +
            '</span>'
        )

    if not polylines:
        st.info("No drawable numeric graph series for this panel.")
        return

    safe_title = _html_v6i2.escape(str(title))
    legend_html = "".join(legend_items)

    svg_parts = []
    svg_parts.append('<div style="border:1px solid rgba(255,255,255,0.18);border-radius:8px;padding:12px;margin:8px 0 14px 0;">')
    svg_parts.append('<div style="font-weight:650;margin-bottom:4px;">' + safe_title + '</div>')
    svg_parts.append('<div style="font-size:12px;opacity:0.78;margin-bottom:8px;">x-axis: redshift z. Local FLRW background geometry only.</div>')
    svg_parts.append(f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" role="img" aria-label="{safe_title}">')
    svg_parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="rgba(255,255,255,0.02)" />')
    svg_parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="rgba(255,255,255,0.35)" stroke-width="1"/>')
    svg_parts.append(f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="rgba(255,255,255,0.35)" stroke-width="1"/>')
    svg_parts.append(f'<text x="{left}" y="{height-12}" fill="rgba(255,255,255,0.70)" font-size="11">z={xmin:.3g}</text>')
    svg_parts.append(f'<text x="{width-right-58}" y="{height-12}" fill="rgba(255,255,255,0.70)" font-size="11">z={xmax:.3g}</text>')
    svg_parts.append(f'<text x="8" y="{top+4}" fill="rgba(255,255,255,0.70)" font-size="11">{ymax:.4g}</text>')
    svg_parts.append(f'<text x="8" y="{height-bottom}" fill="rgba(255,255,255,0.70)" font-size="11">{ymin:.4g}</text>')
    svg_parts.extend(polylines)
    svg_parts.append('</svg>')
    svg_parts.append('<div style="font-size:12px;margin-top:4px;">' + legend_html + '</div>')
    svg_parts.append('</div>')

    st.markdown("\n".join(svg_parts), unsafe_allow_html=True)

# --- /DTI_BACKGROUND_GEOMETRY_SVG_CHART_V6I2 ---

# --- DTI_BACKGROUND_GEOMETRY_GRAPH_V1 ---
# Lightweight FLRW-only graph for the Background Geometry Anchor.
# Boundary: local background geometry only. No CLASS execution, no Render API,
# no likelihood evaluation, no posterior comparison, no Planck validation.

_DTI_BACKGROUND_GEOMETRY_GRAPH_V1 = True

def _dti_bggeom_graph_grid_v1(H0, omega_m, omega_vac, zmax):
    # DTI_BACKGROUND_GEOMETRY_GRAPH_GRID_FLATTEN_V6D
    # Flatten nested _dti_bggeom_compute_v1 output into chart-ready rows.
    try:
        zmax = float(zmax)
        if zmax <= 0:
            zmax = 0.1
        n = 81
        rows = []
        for i in range(n):
            t = i / float(n - 1)
            z = zmax * (t ** 2)
            result = _dti_bggeom_compute_v1(H0, omega_m, omega_vac, z)
            if not isinstance(result, dict) or result.get("status") != "ok":
                rows.append({
                    "z": round(z, 6),
                    "age_at_z_Gyr": None,
                    "light_travel_time_Gyr": None,
                    "comoving_radial_distance_Mpc": None,
                    "luminosity_distance_Mpc": None,
                    "angular_diameter_distance_Mpc": None,
                    "scale_kpc_per_arcsec": None,
                })
                continue

            time_part = result.get("time", {}) if isinstance(result.get("time", {}), dict) else {}
            dist_part = result.get("distance", {}) if isinstance(result.get("distance", {}), dict) else {}

            rows.append({
                "z": round(z, 6),
                "age_at_z_Gyr": time_part.get("age_at_z_Gyr"),
                "light_travel_time_Gyr": time_part.get("light_travel_time_Gyr"),
                "comoving_radial_distance_Mpc": dist_part.get("comoving_radial_distance_Mpc"),
                "luminosity_distance_Mpc": dist_part.get("luminosity_distance_Mpc"),
                "angular_diameter_distance_Mpc": dist_part.get("angular_diameter_distance_Mpc"),
                "scale_kpc_per_arcsec": dist_part.get("scale_kpc_per_arcsec"),
            })
        return rows
    except Exception:
        return []

def _dti_render_background_geometry_graph_v1(H0, omega_m, omega_vac, zmax):
    # DTI_BACKGROUND_GEOMETRY_GRAPH_RENDERER_SVG_V6I2
    _dti_panel_note_v1("Summary → compact table → Raw data — audit view. FLRW background geometry only; SVG renderer avoids the globally silenced st.line_chart path.")

    try:
        rows = _dti_bggeom_graph_grid_v1(H0, omega_m, omega_vac, zmax)
    except Exception as exc:
        st.info(f"Background geometry graph data could not be prepared: {exc}")
        rows = []

    if not rows:
        st.info("Background geometry graph rows are unavailable.")
        return

    st.markdown("#### Background geometry curves")

    tab_time, tab_distance, tab_scale = st.tabs(["Time baseline", "Distance baseline", "Angular scale"])

    with tab_time:
        _dti_bggeom_svg_chart_v6i2(
            rows,
            "z",
            [
                ("age_at_z_Gyr", "age at z [Gyr]"),
                ("light_travel_time_Gyr", "light-travel time [Gyr]"),
            ],
            "Time baseline",
        )

    with tab_distance:
        _dti_bggeom_svg_chart_v6i2(
            rows,
            "z",
            [
                ("comoving_radial_distance_Mpc", "comoving radial distance [Mpc]"),
                ("luminosity_distance_Mpc", "luminosity distance [Mpc]"),
                ("angular_diameter_distance_Mpc", "angular-diameter distance [Mpc]"),
            ],
            "Distance baseline",
        )

    with tab_scale:
        _dti_bggeom_svg_chart_v6i2(
            rows,
            "z",
            [
                ("scale_kpc_per_arcsec", "scale [kpc/arcsec]"),
            ],
            "Angular scale",
        )

    with st.expander("Raw data — audit view", expanded=False):
        _dti_bggeom_render_raw_data_v6e(rows)


# DTI_BACKGROUND_GEOMETRY_GRAPH_DROPNA_FIX_V6
# Graph tables drop None rows per panel before st.line_chart.
# Boundary: Background Geometry FLRW-only graph rendering; no CLASS, no API, no likelihood/posterior/Planck validation.
_DTI_BACKGROUND_GEOMETRY_GRAPH_DROPNA_FIX_V6 = True
# /DTI_BACKGROUND_GEOMETRY_GRAPH_DROPNA_FIX_V6


# DTI_BACKGROUND_GEOMETRY_GRAPH_DROPNA_FIX_V6B
# Graph tables drop None rows per panel before st.line_chart.
# Boundary: Background Geometry FLRW-only graph rendering; no CLASS, no API, no likelihood/posterior/Planck validation.
_DTI_BACKGROUND_GEOMETRY_GRAPH_DROPNA_FIX_V6B = True
# /DTI_BACKGROUND_GEOMETRY_GRAPH_DROPNA_FIX_V6B

# --- /DTI_BACKGROUND_GEOMETRY_GRAPH_V1 ---


# --- DTI_UI_CONSOLIDATION_V1 ---
# Display-only consolidation layer.
# Purpose: reduce repeated boundary text while keeping audit safeguards visible.
# Boundary: no CLASS execution, no Render API modification, no 7c execution,
# no likelihood evaluation, no posterior comparison, no Planck validation,
# no physics-value update, no graph rendering, and no manuscript update.

_DTI_UI_CONSOLIDATION_V1 = True

def _dti_render_global_claim_limits_audit_boundary_v1():
    st.markdown("### Global claim limits / audit boundary")
    st.caption(
        "Applies to all panels unless a panel explicitly states otherwise. "
        "Panel-local notes are intentionally short; detailed limits are centralized here."
    )
    with st.expander("Global claim limits / audit boundary", expanded=False):
        rows = [
            {"scope": "CLASS / solver", "limit": "No CLASS execution is performed by display-only panels."},
            {"scope": "Render API", "limit": "No Render API modification and no Streamlit Secret modification."},
            {"scope": "7c", "limit": "7c remains gated; display polish is not 7c execution or 7c logic modification."},
            {"scope": "Statistics", "limit": "No likelihood evaluation and no posterior comparison."},
            {"scope": "Validation", "limit": "No Planck validation and no model validation claim."},
            {"scope": "Physics values", "limit": "No physics-value update."},
            {"scope": "Graphs", "limit": "No graph rendering is reopened."},
            {"scope": "Manuscript", "limit": "No manuscript update or manuscript conclusion."},
            {"scope": "Raw data", "limit": "Raw payloads remain available under Raw data — audit view expanders."},
        ]
        _dti_arrow_safe_df_v1(pd.DataFrame(rows), width="stretch", hide_index=True)

def _dti_panel_note_v1(text):
    st.caption(text)

# --- /DTI_UI_CONSOLIDATION_V1 ---

# --- DTI_UI_CONSOLIDATION_V2B_SAFE_CALL_WRAP ---
# Display-only consolidation. Legacy/detail-heavy duplicate panels are folded by
# wrapping their existing render calls, not by reindenting function bodies.
# Boundary: no solver execution, no API modification, no data mutation.

_DTI_UI_CONSOLIDATION_V2B_SAFE_CALL_WRAP = True

def _dti_legacy_detail_expander_v2b(title):
    return st.expander(title, expanded=False)

# --- /DTI_UI_CONSOLIDATION_V2B_SAFE_CALL_WRAP ---


# --- DTI_7C_EXAMINER_PAYLOAD_DISPLAY_POLISH_V1 ---
# Reader-facing display helper for 7c continuity/discontinuity examiner payloads.
# Boundary: UI display only. No CLASS execution, no Render API modification,
# no 7c execution, no likelihood evaluation, no posterior comparison,
# no Planck validation, no physics-value update, and no graph rendering.

_DTI_7C_EXAMINER_PAYLOAD_DISPLAY_POLISH_V1 = True

def _dti_7c_display_value_v1(value):
    if value is None:
        return "not provided"
    try:
        if pd.isna(value):
            return "not provided"
    except Exception:
        pass
    if isinstance(value, float):
        return round(value, 6)
    return value

def _dti_7c_dict_rows_v1(obj, prefix=""):
    rows = []
    if not isinstance(obj, dict):
        return rows
    for key, value in obj.items():
        label = f"{prefix}{key}" if prefix else str(key)
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                rows.append({
                    "field": f"{label}.{sub_key}",
                    "value": _dti_7c_display_value_v1(sub_value),
                })
        else:
            rows.append({
                "field": label,
                "value": _dti_7c_display_value_v1(value),
            })
    return rows

def _dti_render_7c_examiner_payload_display_v1(payload):
    st.caption(
        "7c examiner payload preview. Compact audit tables are shown first; raw JSON is preserved below. "
        "This is local exploratory triage input only, not a physical-discontinuity proof."
    )

    if not isinstance(payload, dict):
        st.info("7c examiner payload is not available yet.")
        with st.expander("Raw data — audit view", expanded=False):
            st.json(payload)
        return

    boundary = payload.get("boundary", {})
    sweep = payload.get("sweep", {})
    base_payload = payload.get("base_payload", {})

    boundary_rows = []
    if isinstance(boundary, dict):
        for key in [
            "local_only",
            "experimental",
            "non_canonical",
            "likelihood_evaluation",
            "posterior_comparison",
            "planck_validation",
            "physical_discontinuity_proof",
        ]:
            if key in boundary:
                boundary_rows.append({"field": key, "value": _dti_7c_display_value_v1(boundary.get(key))})

    sweep_rows = []
    if isinstance(sweep, dict):
        for key in ["parameter", "start", "end", "grid_points", "repeat_count", "relative_jump_threshold"]:
            if key in sweep:
                sweep_rows.append({"field": key, "value": _dti_7c_display_value_v1(sweep.get(key))})

    input_rows = []
    if isinstance(base_payload, dict):
        for key in ["H0", "omega_cdm", "omega_b", "n_s", "ln10_10_As", "tau_reio", "sigma8", "S8", "f_EDE", "z_c"]:
            if key in base_payload:
                input_rows.append({"field": key, "value": _dti_7c_display_value_v1(base_payload.get(key))})

    summary_rows = [
        {"field": "panel", "value": "7c continuity/discontinuity examiner"},
        {"field": "display mode", "value": "compact payload preview"},
        {"field": "interpretation", "value": "exploratory local triage input only"},
        {"field": "claim boundary", "value": "not likelihood, posterior, Planck validation, or physical-discontinuity proof"},
    ]
    _dti_arrow_safe_df_v1(pd.DataFrame(summary_rows), width="stretch", hide_index=True)

    if sweep_rows:
        st.markdown("#### Sweep summary")
        _dti_arrow_safe_df_v1(pd.DataFrame(sweep_rows), width="stretch", hide_index=True)

    if input_rows:
        st.markdown("#### Base payload summary")
        _dti_arrow_safe_df_v1(pd.DataFrame(input_rows), width="stretch", hide_index=True)

    if boundary_rows:
        st.markdown("#### Boundary flags")
        _dti_arrow_safe_df_v1(pd.DataFrame(boundary_rows), width="stretch", hide_index=True)

    with st.expander("Raw data — audit view", expanded=False):
        st.json(payload)


# --- DTI_7C_EXAMINER_VERDICT_RECORD_DISPLAY_V1 ---
# Reader-facing display helper for 7c examiner verdict records.
# Boundary: display-only. No CLASS execution, no Render API modification,
# no 7c logic modification, no likelihood evaluation, no posterior comparison,
# no Planck validation, no physics-value update, and no graph rendering.

_DTI_7C_EXAMINER_VERDICT_RECORD_DISPLAY_V1 = True

def _dti_7c_verdict_display_value_v1(value):
    if value is None:
        return "not provided"
    try:
        if pd.isna(value):
            return "not provided"
    except Exception:
        pass
    if isinstance(value, float):
        return round(value, 6)
    return value

def _dti_7c_dict_rows_v1(prefix, data):
    rows = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list, tuple)):
                continue
            rows.append({"field": f"{prefix}.{key}" if prefix else str(key), "value": _dti_7c_verdict_display_value_v1(value)})
    return rows

def _dti_render_7c_examiner_verdict_record_v1(record):
    st.markdown("##### Examiner verdict record")
    _dti_panel_note_v1("Summary → compact tables → raw audit view. Display-only; detailed limits are in Global claim limits / audit boundary.")

    if not isinstance(record, dict):
        st.warning("7c examiner verdict record is not available in table form.")
        with st.expander("Raw data — audit view", expanded=False):
            st.json(record)
        return

    status = record.get("status", "unknown")
    verdict = record.get("overall_bounded_verdict", "unknown")
    examiner = record.get("examiner", "7c examiner")
    if str(status).lower() == "ok":
        st.success(f"7c examiner verdict: {verdict}")
    else:
        st.warning(f"7c examiner verdict requires review: {verdict}")

    summary_rows = [
        {"field": "status", "value": _dti_7c_verdict_display_value_v1(status)},
        {"field": "examiner", "value": _dti_7c_verdict_display_value_v1(examiner)},
        {"field": "overall_bounded_verdict", "value": _dti_7c_verdict_display_value_v1(verdict)},
        {"field": "boundary", "value": "local numerical examiner only; not likelihood, posterior, Planck validation, or physical-discontinuity proof"},
    ]
    _dti_arrow_safe_df_v1(pd.DataFrame(summary_rows), width="stretch", hide_index=True)

    base_rows = _dti_7c_dict_rows_v1("", record.get("base_payload", {}))
    if base_rows:
        st.markdown("###### Base payload summary")
        _dti_arrow_safe_df_v1(pd.DataFrame(base_rows), width="stretch", hide_index=True)

    sweep_rows = _dti_7c_dict_rows_v1("", record.get("sweep", {}))
    if sweep_rows:
        st.markdown("###### Sweep summary")
        _dti_arrow_safe_df_v1(pd.DataFrame(sweep_rows), width="stretch", hide_index=True)

    result_rows = _dti_7c_dict_rows_v1("", record.get("result", {}))
    if result_rows:
        st.markdown("###### Result summary")
        _dti_arrow_safe_df_v1(pd.DataFrame(result_rows), width="stretch", hide_index=True)

    boundary_rows = _dti_7c_dict_rows_v1("", record.get("boundary", {}))
    if boundary_rows:
        st.markdown("###### Boundary flags")
        _dti_arrow_safe_df_v1(pd.DataFrame(boundary_rows), width="stretch", hide_index=True)

    warning = record.get("interpretation_warning")
    if warning:
        st.caption(str(warning))

    with st.expander("Raw data — audit view", expanded=False):
        st.json(record)

# --- /DTI_7C_EXAMINER_VERDICT_RECORD_DISPLAY_V1 ---

# --- /DTI_7C_EXAMINER_PAYLOAD_DISPLAY_POLISH_V1 ---






# --- /DTI_PROFILE_CATEGORY_GUIDE_LABEL_POLISH_V1C_MINIMAL ---


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
    # DTI_MORESCO2016_LOCAL_HZ_GRID_SOURCE_ACTIVATION_EXECUTE_V1F_BG_PAYLOAD
    try:
        _dti_moresco2016_z_bg_v1 = np.asarray(z_bg, dtype=float)
        _dti_moresco2016_e_a_v1 = np.asarray(e_a, dtype=float)
        _dti_moresco2016_h0_v1 = float(H0)
        _dti_moresco2016_h_model_v1 = _dti_moresco2016_h0_v1 * _dti_moresco2016_e_a_v1
        if (
            _dti_moresco2016_z_bg_v1.shape == _dti_moresco2016_h_model_v1.shape
            and _dti_moresco2016_z_bg_v1.size >= 2
            and np.all(np.isfinite(_dti_moresco2016_z_bg_v1))
            and np.all(np.isfinite(_dti_moresco2016_e_a_v1))
            and np.all(np.isfinite(_dti_moresco2016_h_model_v1))
            and np.isfinite(_dti_moresco2016_h0_v1)
            and _dti_moresco2016_h0_v1 > 0
            and np.all(_dti_moresco2016_e_a_v1 > 0)
            and np.all(_dti_moresco2016_h_model_v1 > 0)
        ):
            # DTI_MORESCO2016_ACTIVATION_RUNTIME_DIAGNOSTIC_EXECUTE_V1_PAYLOAD_COUNTER
            st.session_state["dti_moresco2016_bg_proxy_grid_v1_store_count"] = int(
                st.session_state.get("dti_moresco2016_bg_proxy_grid_v1_store_count", 0)
            ) + 1
            st.session_state["dti_moresco2016_bg_proxy_grid_v1"] = {
                "z_bg": _dti_moresco2016_z_bg_v1,
                "e_a": _dti_moresco2016_e_a_v1,
                "H0": _dti_moresco2016_h0_v1,
                "H_model": _dti_moresco2016_h_model_v1,
                "source": "session_state_bg_proxy_Ea_to_Hz_bridge",
                "boundary": "diagnostic_only_not_likelihood_not_posterior_not_fit_not_validation",
            }
    except Exception:
        pass
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


# === DTI CMB / Likelihood Capability Matrix V1 ===
# Front-end capability audit only.
# This block does not compute CMB spectra, does not compute Planck likelihoods,
# does not compare posteriors, does not call external APIs, and does not modify backend state.

def _dti_find_nested_key_v1(payload, candidates):
    """Return (found, value, matched_path) for dot-path candidates in nested dict payload."""
    if not isinstance(payload, dict):
        return False, None, ""

    for path in candidates:
        cur = payload
        ok = True
        for part in str(path).split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break
        if ok:
            return True, cur, path

    return False, None, ""


def _dti_value_is_array_like_v1(value):
    """Conservative array-like check without importing numpy or pandas."""
    if isinstance(value, (list, tuple)):
        return len(value) > 0
    return False


def _dti_cmb_likelihood_capability_matrix_v1(payload):
    """Build capability rows from the current API payload.

    This is intentionally conservative. Missing CMB/Planck fields are readiness NO.
    Existing scalar CLASS-like derived values are allowed as scalar diagnostics only.
    """
    if not isinstance(payload, dict):
        payload = {}

    boundary = payload.get("boundary", {})
    derived = payload.get("derived", {})
    if not isinstance(boundary, dict):
        boundary = {}
    if not isinstance(derived, dict):
        derived = {}

    boundary_note = str(boundary.get("note", ""))
    note_lower = boundary_note.lower()

    scalar_candidates = [
        "derived.age_Gyr_CLASS",
        "derived.rs_drag_Mpc_CLASS",
        "derived.sigma8_CLASS",
        "derived.S8_CLASS",
        "age_Gyr_CLASS",
        "rs_drag_Mpc_CLASS",
        "sigma8_CLASS",
        "S8_CLASS",
    ]

    ell_candidates = [
        "derived.ell",
        "ell",
        "cmb.ell",
        "cls.ell",
    ]

    tt_candidates = [
        "derived.cl_tt",
        "cl_tt",
        "cmb.cl_tt",
        "cls.tt",
        "cls.cl_tt",
    ]

    te_candidates = [
        "derived.cl_te",
        "cl_te",
        "cmb.cl_te",
        "cls.te",
        "cls.cl_te",
    ]

    ee_candidates = [
        "derived.cl_ee",
        "cl_ee",
        "cmb.cl_ee",
        "cls.ee",
        "cls.cl_ee",
    ]

    pp_candidates = [
        "derived.cl_pp",
        "derived.cl_phiphi",
        "cl_pp",
        "cl_phiphi",
        "cmb.cl_pp",
        "cmb.cl_phiphi",
        "cls.pp",
        "cls.cl_pp",
        "cls.phiphi",
    ]

    planck_candidates = [
        "chi2_planck_highl",
        "chi2_planck_lowl",
        "chi2_planck_lensing",
        "chi2.planck_highl",
        "chi2.planck_lowl",
        "chi2.planck_lensing",
        "likelihood.planck",
        "likelihood.planck_highl",
        "likelihood.planck_lowl",
        "likelihood.planck_lensing",
        "derived.chi2_planck_highl",
        "derived.chi2_planck_lowl",
        "derived.chi2_planck_lensing",
    ]

    posterior_candidates = [
        "posterior",
        "logposterior",
        "minuslogpost",
        "derived.posterior",
        "derived.logposterior",
        "derived.minuslogpost",
    ]

    scalar_found = False
    scalar_paths = []
    for p in scalar_candidates:
        found, value, matched = _dti_find_nested_key_v1(payload, [p])
        if found:
            scalar_found = True
            scalar_paths.append(matched)

    ell_found, ell_value, ell_path = _dti_find_nested_key_v1(payload, ell_candidates)
    tt_found, tt_value, tt_path = _dti_find_nested_key_v1(payload, tt_candidates)
    te_found, te_value, te_path = _dti_find_nested_key_v1(payload, te_candidates)
    ee_found, ee_value, ee_path = _dti_find_nested_key_v1(payload, ee_candidates)
    pp_found, pp_value, pp_path = _dti_find_nested_key_v1(payload, pp_candidates)

    planck_found, planck_value, planck_path = _dti_find_nested_key_v1(payload, planck_candidates)
    posterior_found, posterior_value, posterior_path = _dti_find_nested_key_v1(payload, posterior_candidates)

    interface_only = False
    if "interface compatibility" in note_lower:
        interface_only = True
    if "not used as axiclass ede microphysics" in note_lower:
        interface_only = True
    if "minimal backend" in note_lower and "f_ede" in note_lower and "z_c" in note_lower:
        interface_only = True

    rows = []

    def add_row(capability, readiness, evidence, boundary):
        rows.append({
            "capability": capability,
            "readiness": readiness,
            "evidence": evidence,
            "boundary": boundary,
        })

    add_row(
        "Scalar derived values",
        "YES" if scalar_found else "NO",
        ", ".join(scalar_paths) if scalar_paths else "No representative scalar derived keys found",
        "Scalar diagnostics only; not CMB spectra and not likelihood."
    )

    add_row(
        "CMB ell array",
        "YES" if (ell_found and _dti_value_is_array_like_v1(ell_value)) else "NO",
        ell_path if ell_found else "Missing keys: derived.ell, ell, cmb.ell, cls.ell",
        "Required before real CMB graph can be rendered."
    )

    add_row(
        "CMB TT spectrum",
        "YES" if (tt_found and _dti_value_is_array_like_v1(tt_value)) else "NO",
        tt_path if tt_found else "Missing keys: derived.cl_tt, cl_tt, cmb.cl_tt, cls.tt",
        "Do not fake TT curve in front-end."
    )

    add_row(
        "CMB TE spectrum",
        "YES" if (te_found and _dti_value_is_array_like_v1(te_value)) else "NO",
        te_path if te_found else "Missing keys: derived.cl_te, cl_te, cmb.cl_te, cls.te",
        "Do not fake TE curve in front-end."
    )

    add_row(
        "CMB EE spectrum",
        "YES" if (ee_found and _dti_value_is_array_like_v1(ee_value)) else "NO",
        ee_path if ee_found else "Missing keys: derived.cl_ee, cl_ee, cmb.cl_ee, cls.ee",
        "Do not fake EE curve in front-end."
    )

    add_row(
        "CMB lensing / phi-phi",
        "YES" if (pp_found and _dti_value_is_array_like_v1(pp_value)) else "NO",
        pp_path if pp_found else "Missing keys: derived.cl_pp, derived.cl_phiphi, cl_pp, cl_phiphi, cmb.cl_pp, cls.pp",
        "Do not fake lensing curve in front-end."
    )

    add_row(
        "Planck likelihood components",
        "YES" if planck_found else "NO",
        planck_path if planck_found else "Missing Planck chi2 / likelihood fields",
        "CLASS spectra alone are not Planck likelihood evaluation."
    )

    add_row(
        "Posterior comparison",
        "YES" if posterior_found else "NO",
        posterior_path if posterior_found else "Missing posterior / logposterior / minuslogpost fields",
        "This app panel must not compare posteriors."
    )

    add_row(
        "AxiCLASS/EDE microphysics",
        "NO" if interface_only else "UNKNOWN",
        boundary_note if boundary_note else "No backend boundary note available",
        "Current backend note indicates f_EDE/z_c are interface-only when stated."
    )

    add_row(
        "Backend extension required",
        "YES",
        "CMB arrays and Planck likelihood fields are absent unless backend adds them.",
        "Required before real CMB Cl graph or Planck chi2 matrix."
    )

    add_row(
        "Current response can support scalar diagnostics only",
        "YES" if scalar_found and not (ell_found or tt_found or te_found or ee_found or pp_found or planck_found) else "CHECK",
        "Derived scalar values present; CMB/Planck arrays not confirmed.",
        "Safe front-end output is capability audit, not scientific graph/matrix."
    )

    summary = {
        "api_status": payload.get("status", "NO_PAYLOAD" if not payload else "UNKNOWN"),
        "engine": payload.get("engine", "UNKNOWN"),
        "runtime_sec": payload.get("runtime_sec", "UNKNOWN"),
        "boundary_note": boundary_note if boundary_note else "No boundary note available",
        "cmb_graph_readiness": "NO" if not (ell_found and tt_found) else "CHECK",
        "planck_likelihood_readiness": "NO" if not planck_found else "CHECK",
        "backend_extension_required": "YES",
        "scalar_only_api_response": "YES" if scalar_found and not (ell_found or tt_found or te_found or ee_found or pp_found or planck_found) else "CHECK",
    }

    return summary, rows


def _dti_render_cmb_likelihood_capability_matrix_v1(payload=None):
    """Render display-only CMB / Likelihood capability audit panel."""
    st.markdown("### CMB / Likelihood capability matrix — API readiness audit")

    if payload is None:
        payload = {}

    if not isinstance(payload, dict) or not payload:
        st.info("No API payload available in this session. Showing required fields and readiness boundaries.")
        payload = {}

    summary, rows = _dti_cmb_likelihood_capability_matrix_v1(payload)

    st.markdown("#### Summary")
    st.text(
        "API status: {api_status}\n"
        "engine: {engine}\n"
        "runtime_sec: {runtime_sec}\n"
        "CMB graph readiness = {cmb_graph_readiness}\n"
        "Planck likelihood readiness = {planck_likelihood_readiness}\n"
        "backend extension required = {backend_extension_required}\n"
        "scalar-only API response = {scalar_only_api_response}\n"
        "boundary note: {boundary_note}".format(**summary)
    )

    st.markdown("#### Capability matrix")
    try:
        st.table(rows)
    except Exception:
        lines = []
        for row in rows:
            lines.append(
                f"{row.get('capability', '')}\t"
                f"readiness={row.get('readiness', '')}\t"
                f"evidence={row.get('evidence', '')}\t"
                f"boundary={row.get('boundary', '')}"
            )
        st.text("\n".join(lines))

    st.warning(
        "This panel is a capability audit only. "
        "It does not compute CMB spectra. "
        "It does not compute Planck likelihoods. "
        "It does not compare posteriors. "
        "It does not validate Planck or JWST. "
        "It does not update physics values. "
        "Backend extension is required before real CMB Cl graph or Planck χ² matrix can be shown."
    )

    st.markdown("#### Raw data — audit view")
    st.caption("Large arrays are summarized here to keep the UI readable. The graph renderer still uses the full real API arrays.")
    _dti_render_summarized_raw_api_payload_v1(payload)

    # === DTI REAL API CMB SVG GRAPH V1 render call ===
    with st.expander("CMB spectra graph — real API arrays only", expanded=False):
        _dti_render_real_api_cmb_svg_graph_v1(payload)
    # === END DTI REAL API CMB SVG GRAPH V1 render call ===


def _dti_render_cmb_likelihood_capability_matrix_v1_no_payload():
    """Safe fallback renderer when no live API payload object is in local scope."""
    _dti_render_cmb_likelihood_capability_matrix_v1({})
# === END DTI CMB / Likelihood Capability Matrix V1 ===



# === DTI RAW API ARRAY SUMMARY V1 ===
# Display-only JSON summarizer for large API arrays.
# Does not alter payload used by graph renderers.
# Does not create fake arrays, does not call APIs, and does not evaluate likelihoods.

def _dti_summarize_large_api_arrays_v1(obj, max_preview=3):
    try:
        if isinstance(obj, dict):
            out = {}
            for k, v in obj.items():
                if isinstance(v, list) and len(v) > 20:
                    first = v[:max_preview]
                    last = v[-max_preview:] if len(v) >= max_preview else v
                    out[k] = {
                        "__array_summary__": True,
                        "length": len(v),
                        "first": first,
                        "last": last,
                        "note": "Full array hidden in raw audit view only. Graph renderer still uses the real payload arrays.",
                    }
                else:
                    out[k] = _dti_summarize_large_api_arrays_v1(v, max_preview=max_preview)
            return out
        if isinstance(obj, list):
            if len(obj) > 20:
                first = obj[:max_preview]
                last = obj[-max_preview:] if len(obj) >= max_preview else obj
                return {
                    "__array_summary__": True,
                    "length": len(obj),
                    "first": first,
                    "last": last,
                    "note": "Full array hidden in raw audit view only.",
                }
            return [_dti_summarize_large_api_arrays_v1(v, max_preview=max_preview) for v in obj]
        return obj
    except Exception:
        return obj


def _dti_render_summarized_raw_api_payload_v1(payload):
    try:
        import json
        summarized = _dti_summarize_large_api_arrays_v1(payload)
        st.text(json.dumps(summarized, indent=2, ensure_ascii=False, sort_keys=True))
    except Exception:
        st.text(str(payload))
# === END DTI RAW API ARRAY SUMMARY V1 ===


# === DTI REAL API CMB SVG GRAPH V1 ===
# Front-end renderer only. Uses real arrays returned by the external API.
# No fake arrays, no API calls, no CLASS execution, no Planck likelihood,
# no posterior comparison, and no physics-value update.

def _dti_real_cmb_array_v1(payload, key):
    try:
        if not isinstance(payload, dict):
            return []
        derived = payload.get("derived", {})
        if not isinstance(derived, dict):
            return []
        value = derived.get(key, [])
        if not isinstance(value, (list, tuple)):
            return []
        out = []
        for x in value:
            try:
                out.append(float(x))
            except Exception:
                out.append(None)
        return out
    except Exception:
        return []


def _dti_real_cmb_arrays_ready_v1(payload):
    ell = _dti_real_cmb_array_v1(payload, "ell")
    dl_tt = _dti_real_cmb_array_v1(payload, "dl_tt")
    cl_tt = _dti_real_cmb_array_v1(payload, "cl_tt")

    if len(ell) < 3:
        return False

    if len(dl_tt) >= 3:
        return True

    if len(cl_tt) >= 3:
        return True

    return False


def _dti_svg_polyline_from_xy_v1(xs, ys, width=760, height=320, pad=44):
    pts = []
    clean = []

    for x, y in zip(xs, ys):
        if x is None or y is None:
            continue
        try:
            xf = float(x)
            yf = float(y)
        except Exception:
            continue
        if xf <= 0:
            continue
        clean.append((xf, yf))

    if len(clean) < 3:
        return "", None

    # Drop ell < 2 for visual stability.
    clean = [(x, y) for x, y in clean if x >= 2]
    if len(clean) < 3:
        return "", None

    x_vals = [p[0] for p in clean]
    y_vals = [p[1] for p in clean]

    x_min = min(x_vals)
    x_max = max(x_vals)
    y_min = min(y_vals)
    y_max = max(y_vals)

    if x_max <= x_min:
        return "", None

    if y_max == y_min:
        y_max = y_min + 1.0

    # Use linear x-axis. This is intentionally simple and auditable.
    def sx(x):
        return pad + (float(x) - x_min) / (x_max - x_min) * (width - 2 * pad)

    def sy(y):
        return height - pad - (float(y) - y_min) / (y_max - y_min) * (height - 2 * pad)

    for x, y in clean:
        pts.append(f"{sx(x):.2f},{sy(y):.2f}")

    meta = {
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max,
        "n": len(clean),
    }

    return " ".join(pts), meta


def _dti_render_one_cmb_svg_curve_v1(label, ell, y, y_label):
    points, meta = _dti_svg_polyline_from_xy_v1(ell, y)
    if not points or not meta:
        st.info(f"{label}: no valid real array available for plotting.")
        return

    width = 760
    height = 320
    pad = 44

    svg = f"""
<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">
  <rect x="0" y="0" width="{width}" height="{height}" fill="#0f172a" stroke="#334155"/>
  <line x1="{pad}" y1="{height-pad}" x2="{width-pad}" y2="{height-pad}" stroke="#64748b" stroke-width="1"/>
  <line x1="{pad}" y1="{pad}" x2="{pad}" y2="{height-pad}" stroke="#64748b" stroke-width="1"/>
  <text x="{width/2}" y="24" text-anchor="middle" font-size="16" fill="#e5e7eb">{label}</text>
  <text x="{width/2}" y="{height-10}" text-anchor="middle" font-size="12" fill="#cbd5e1">ell</text>
  <text x="15" y="{height/2}" text-anchor="middle" font-size="12" fill="#cbd5e1" transform="rotate(-90 15 {height/2})">{y_label}</text>
  <text x="{pad}" y="{height-pad+18}" text-anchor="middle" font-size="10" fill="#cbd5e1">{meta['x_min']:.0f}</text>
  <text x="{width-pad}" y="{height-pad+18}" text-anchor="middle" font-size="10" fill="#cbd5e1">{meta['x_max']:.0f}</text>
  <text x="{pad-8}" y="{height-pad}" text-anchor="end" font-size="10" fill="#cbd5e1">{meta['y_min']:.3g}</text>
  <text x="{pad-8}" y="{pad+4}" text-anchor="end" font-size="10" fill="#cbd5e1">{meta['y_max']:.3g}</text>
  <polyline fill="none" stroke="#f8fafc" stroke-width="1.8" points="{points}"/>
</svg>
"""
    st.markdown(svg, unsafe_allow_html=True)
    st.caption(
        f"Source: external API derived arrays only. n={meta['n']}; "
        f"ell range: {meta['x_min']:.0f} to {meta['x_max']:.0f}. "
        "This is not a Planck likelihood evaluation."
    )


def _dti_render_real_api_cmb_svg_graph_v1(payload=None):
    st.markdown("### CMB spectra graph — real API arrays only")

    if payload is None or not isinstance(payload, dict):
        st.info("No API payload available. CMB graph is not rendered.")
        return

    derived = payload.get("derived", {})
    boundary = payload.get("boundary", {})

    if not isinstance(derived, dict):
        st.info("No derived payload available. CMB graph is not rendered.")
        return

    ell = _dti_real_cmb_array_v1(payload, "ell")
    dl_tt = _dti_real_cmb_array_v1(payload, "dl_tt")
    dl_te = _dti_real_cmb_array_v1(payload, "dl_te")
    dl_ee = _dti_real_cmb_array_v1(payload, "dl_ee")
    cl_tt = _dti_real_cmb_array_v1(payload, "cl_tt")
    cl_te = _dti_real_cmb_array_v1(payload, "cl_te")
    cl_ee = _dti_real_cmb_array_v1(payload, "cl_ee")
    cl_pp = _dti_real_cmb_array_v1(payload, "cl_pp")

    if not _dti_real_cmb_arrays_ready_v1(payload):
        st.warning(
            "CMB graph readiness = NO. Real API arrays ell and TT spectrum are not present in this payload. "
            "No fallback or fake curve is drawn."
        )
        return

    st.success("CMB graph readiness = YES. Rendering only real arrays returned by the external API.")

    source = derived.get("cmb_array_source", "unknown")
    status = derived.get("cmb_array_export_status", "unknown")
    lmax = derived.get("cmb_array_lmax_requested", "unknown")

    st.text(
        "API CMB array status: {status}\n"
        "array source: {source}\n"
        "lmax requested: {lmax}\n"
        "ell length: {ell_len}\n"
        "Planck likelihood readiness: NO".format(
            status=status,
            source=source,
            lmax=lmax,
            ell_len=len(ell),
        )
    )

    st.warning(
        "Boundary: this graph displays CLASS/PyCLASS spectra arrays returned by the API. "
        "It does not compute Planck chi2, does not evaluate likelihoods, does not compare posteriors, "
        "does not validate Planck or JWST, and does not activate AxiCLASS/EDE microphysics."
    )

    with st.expander("CMB array availability audit", expanded=False):
        rows = [
            {"array": "ell", "present": bool(ell), "length": len(ell)},
            {"array": "dl_tt", "present": bool(dl_tt), "length": len(dl_tt)},
            {"array": "dl_te", "present": bool(dl_te), "length": len(dl_te)},
            {"array": "dl_ee", "present": bool(dl_ee), "length": len(dl_ee)},
            {"array": "cl_tt", "present": bool(cl_tt), "length": len(cl_tt)},
            {"array": "cl_te", "present": bool(cl_te), "length": len(cl_te)},
            {"array": "cl_ee", "present": bool(cl_ee), "length": len(cl_ee)},
            {"array": "cl_pp", "present": bool(cl_pp), "length": len(cl_pp)},
        ]
        try:
            st.table(rows)
        except Exception:
            st.text("\\n".join([str(r) for r in rows]))

    tab1, tab2, tab3, tab4 = st.tabs(["TT", "TE", "EE", "Lensing"])

    with tab1:
        if dl_tt:
            _dti_render_one_cmb_svg_curve_v1("TT spectrum: D_l^TT from API", ell, dl_tt, "D_l^TT")
        elif cl_tt:
            _dti_render_one_cmb_svg_curve_v1("TT spectrum: C_l^TT from API", ell, cl_tt, "C_l^TT")
        else:
            st.info("TT array not available.")

    with tab2:
        if dl_te:
            _dti_render_one_cmb_svg_curve_v1("TE spectrum: D_l^TE from API", ell, dl_te, "D_l^TE")
        elif cl_te:
            _dti_render_one_cmb_svg_curve_v1("TE spectrum: C_l^TE from API", ell, cl_te, "C_l^TE")
        else:
            st.info("TE array not available.")

    with tab3:
        if dl_ee:
            _dti_render_one_cmb_svg_curve_v1("EE spectrum: D_l^EE from API", ell, dl_ee, "D_l^EE")
        elif cl_ee:
            _dti_render_one_cmb_svg_curve_v1("EE spectrum: C_l^EE from API", ell, cl_ee, "C_l^EE")
        else:
            st.info("EE array not available.")

    with tab4:
        if cl_pp:
            _dti_render_one_cmb_svg_curve_v1("Lensing spectrum: raw cl_pp from API", ell, cl_pp, "cl_pp")
        else:
            st.info("Lensing array cl_pp not available.")
# === END DTI REAL API CMB SVG GRAPH V1 ===



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
    # DTI_CATEGORIZED_ACTIVE_PROFILE_LOADER_CALL_V2B
    selected_preset = _dti_render_categorized_active_profile_loader_v2b(
        preset_names,
        current_default="FUJIKI_DTI_Candidate_v6" if "FUJIKI_DTI_Candidate_v6" in preset_names else (preset_names[0] if preset_names else None),
    )
    # DTI_CURRENT_SELECTED_SAFE_FALLBACK_V2C
    if 'current_selected' not in globals() and 'current_selected' not in locals():
        current_selected = selected_preset if selected_preset in preset_names else None
        if current_selected is None and "FUJIKI_DTI_Candidate_v6" in preset_names:
            current_selected = "FUJIKI_DTI_Candidate_v6"
        if current_selected is None and preset_names:
            current_selected = preset_names[0]
    # /DTI_CURRENT_SELECTED_SAFE_FALLBACK_V2C
    with st.sidebar.expander("Fallback: legacy registered profile loader", expanded=False):
        st.caption("Fallback only. Normal use should use Profile category → ACTIVE loader above.")
        _dti_fallback_selected_preset_v2b = st.selectbox(
            "Load registered profile — ACTIVE loader",
            preset_names,
            index=preset_names.index(current_selected) if ('current_selected' in locals() and current_selected in preset_names) else 0,
            key="selected_preset_selector_v606",
        )
        if _dti_fallback_selected_preset_v2b and _dti_fallback_selected_preset_v2b != selected_preset:
            st.caption("Fallback selection is visible for compatibility; categorized ACTIVE loader remains primary.")

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

    # --- DTI_REAL_APP_MANUAL_DOCS_LINKS_V1 BEGIN ---
    with st.expander("DTI Real App manuals / documentation", expanded=False):
        st.markdown(
            "- [Full parameter manual](https://github.com/fujikix1102/dti-real-app-v606/blob/main/docs/DTI_REAL_APP_FULL_PARAMETER_MANUAL_V1.md)  \\n"
            "- [Item-by-item manual](https://github.com/fujikix1102/dti-real-app-v606/blob/main/docs/DTI_REAL_APP_ITEM_BY_ITEM_MANUAL_V1.md)  \\n\\n"
            "These manuals are documentation-only references. They do not run CLASS/AxiCLASS, "
            "do not evaluate likelihoods, do not perform MCMC/posterior inference, and do not "
            "modify any manuscript-level claim."
        )
    # --- DTI_REAL_APP_MANUAL_DOCS_LINKS_V1 END ---

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

_dti_arrow_safe_df_v1(df_blocks, width="stretch", hide_index=True)

st.subheader("TARGET_MODEL vs LCDM comparison")
if delta_df.empty:
    st.warning("TARGET_MODEL and LCDM comparison values are incomplete.")
else:
    _dti_arrow_safe_df_v1(delta_df, width="stretch", hide_index=True)

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
    _dti_arrow_safe_df_v1(search_df, width="stretch", hide_index=True)

st.subheader("Current input model safety/readout cards")
# DTI_READOUT_CARD_DETAIL_GUIDE_CALL_V1B
_dti_render_readout_card_detail_guide_v1b()
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

# DTI_VISITOR_QUICK_GUIDE_CALL_V1
_dti_render_visitor_quick_guide_v1()

# DTI_GLOBAL_CLAIM_LIMITS_AUDIT_BOUNDARY_CALL_V1
_dti_render_global_claim_limits_audit_boundary_v1()
# /DTI_GLOBAL_CLAIM_LIMITS_AUDIT_BOUNDARY_CALL_V1


# DTI_BACKGROUND_GEOMETRY_ANCHOR_CALL_V1
_dti_render_background_geometry_anchor_v1()
# /DTI_BACKGROUND_GEOMETRY_ANCHOR_CALL_V1



# DTI_CANDIDATE_TEXT_SAFE_FALLBACK_V1B
# Safe text source for correlated-boundary proxy; no CLASS run and no API request.
candidate_text = st.session_state.get("paper_text_widget", "")
if not candidate_text:
    candidate_text = st.session_state.get("paper_text", "")
if not candidate_text:
    _dti_candidate_profile_name_v1b = st.session_state.get("selected_preset", "")
    candidate_text = PRESETS.get(_dti_candidate_profile_name_v1b, {}).get("text", "")
if not candidate_text and "FUJIKI_DTI_Candidate_v6" in PRESETS:
    candidate_text = PRESETS.get("FUJIKI_DTI_Candidate_v6", {}).get("text", "")
# /DTI_CANDIDATE_TEXT_SAFE_FALLBACK_V1B

# DTI_CORRELATED_BOUNDARY_TRIAGE_CALL_V1
_dti_render_correlated_boundary_triage_v1()
# /DTI_CORRELATED_BOUNDARY_TRIAGE_CALL_V1


# DTI_STATIC_DELTA_AUDIT_TABLE_CALL_V1
_dti_render_static_delta_audit_table_v1()
# /DTI_STATIC_DELTA_AUDIT_TABLE_CALL_V1

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
        _dti_arrow_safe_df_v1(axi_results, width="stretch", hide_index=True)

    with tabs[4]:
        if axi_delta.empty:
            st.warning("AxiCLASS FIX1 delta TSV was not found.")
        else:
            _dti_arrow_safe_df_v1(axi_delta, width="stretch", hide_index=True)

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
            _dti_arrow_safe_df_v1(st.session_state["dti_public_api_warmup_rows_7a7b_v2"], width="stretch")

    # DTI_POSITIVE_ANSWER_NAVIGATOR_CALL_V2
    _dti_render_positive_answer_navigator_v2()

    # DTI_RESEARCH_MOTIVATION_LAYER_CALL_V1
    _dti_render_research_motivation_layer_v1()

    # DTI_RESEARCH_OPPORTUNITY_ENGINE_CALL_V1D
    _dti_render_research_opportunity_engine_v1d()

    # DTI_DISCOVERY_SCORE_PANEL_CALL_V1E
    _dti_render_discovery_score_panel_v1e()

    # DTI_PARAMETER_QUALITY_MATRIX_CALL_V1H
    _dti_render_parameter_quality_matrix_v1h()

    # DTI_PROBE_RESULT_VALUE_MATRIX_CALL_V2
    _dti_render_probe_result_value_matrix_v2()

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
            _dti_arrow_safe_df_v1(pd.DataFrame(derived_rows), hide_index=True, width="stretch")

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
            _dti_arrow_safe_df_v1(pd.DataFrame(selected_rows), hide_index=True, width="stretch")

    boundary = result.get("boundary", {})
    if isinstance(boundary, dict) and boundary:
        boundary_rows = [{"flag": k, "value": v} for k, v in boundary.items() if k != "note"]
        if boundary_rows:
            st.markdown("##### Boundary flags")
            _dti_arrow_safe_df_v1(pd.DataFrame(boundary_rows), hide_index=True, width="stretch")

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
_dti_arrow_safe_df_v1(_compat_rows_8b, width="stretch", hide_index=True)

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
    "The compact table below is the payload sent to the configured vanilla-profile API endpoint. Raw JSON is folded below for audit."
)

_dti_render_vanilla_probe_input_display_v1(live_payload)

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
                # DTI_VANILLA_RESULT_RENDERER_CALL_V1B
                _dti_render_vanilla_api_result_display_v1(
                    data,
                    http_status=cached_result_7b.get('status_code') if isinstance(cached_result_7b, dict) else None,
                    cache_note=str(cached_result_7b.get('cache', '')) if isinstance(cached_result_7b, dict) and cached_result_7b.get('cache') is not None else None,
                )
                # /DTI_VANILLA_RESULT_RENDERER_CALL_V1B

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


# --- DTI_SECTION8_TOP_RESTRICTED_NOTICE_ONCE_V3 ---
# Consolidate repeated Section 8 restricted boundary notices.
# UI cleanup only: does not enable graph rendering, 7c, likelihood, posterior,
# Planck validation, physics-value updates, or manuscript updates.
_DTI_SECTION8_TOP_RESTRICTED_NOTICE_ONCE_V3 = True

def _dti_section8_top_restricted_notice_once_v3():
    key = "dti_section8_top_restricted_notice_once_v3"
    try:
        already = bool(st.session_state.get(key, False))
    except Exception:
        already = False
    if already:
        return
    try:
        st.session_state[key] = True
    except Exception:
        pass
    st.info(
        "Section 8 boundary: candidate-payload and boundary confirmation only. "
        "No graph, no 8011 realtime probe, no heuristic distance ranking, no S8 stress review, "
        "no likelihood evaluation, no posterior comparison, no Planck validation, and no physics-value update."
    )
# --- /DTI_SECTION8_TOP_RESTRICTED_NOTICE_ONCE_V3 ---

# --- DTI_SECTION8_NOTICE_PRUNE_HELPER_V1 ---
# Consolidated Section 8 notice. UI cleanup only.
# Does not enable graph rendering, likelihood evaluation, posterior comparison,
# Planck validation, physics-value updates, or manuscript updates.
_DTI_SECTION8_NOTICE_PRUNE_HELPER_V1 = True

def _dti_section8_boundary_notice_once_v1():
    key = "dti_section8_boundary_notice_once_v1"
    try:
        already = bool(st.session_state.get(key, False))
    except Exception:
        already = False
    if already:
        return
    try:
        st.session_state[key] = True
    except Exception:
        pass
    st.info(
        "Section 8 boundary: candidate-payload and boundary confirmation only. "
        "Graphs remain disabled unless compatible source-of-record diagnostic data are present. "
        "This section does not perform likelihood evaluation, posterior comparison, Planck validation, "
        "physics-value updates, or manuscript updates."
    )

def _dti_section8_no_source_data_notice_v1():
    key = "dti_section8_no_source_data_notice_v1"
    try:
        already = bool(st.session_state.get(key, False))
    except Exception:
        already = False
    if already:
        return
    try:
        st.session_state[key] = True
    except Exception:
        pass
    st.info(
        "No source-of-record Section 8 diagnostic table is available in session memory. "
        "Graphs remain disabled until compatible audited data are loaded."
    )
# --- /DTI_SECTION8_NOTICE_PRUNE_HELPER_V1 ---

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
    # DTI_SECTION8_NOTICE_PRUNE_ROUTE_V1
    try:
        _label_text = "" if label is None else str(label)
    except Exception:
        _label_text = ""
    if "Section 8" in _label_text or "reference-distance" in _label_text or "S8" in _label_text:
        _dti_section8_boundary_notice_once_v1()
        return
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
            _DTI_DISABLED_GRAPH_CALL(_dti_graph_ui_v607_altair_line_with_band(df, "sweep_value", "sigma8").properties(height=260), width="stretch", key="dti_graph_ui_dom_stable_chart_01")
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
            _dti_arrow_safe_df_v1(df.head(30), width="stretch")
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
            _dti_arrow_safe_df_v1(work.head(30), width="stretch")
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
        _DTI_DISABLED_GRAPH_CALL(chart, width="stretch", key="dti_graph_ui_dom_stable_chart_02")
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
            _DTI_DISABLED_GRAPH_CALL(chart, width="stretch", key="dti_graph_ui_dom_stable_chart_03")
            st.caption(
                f"Source table: `{distance_name}`. Smaller values indicate closer proximity in the registered "
                "parameter-profile space. This is heuristic triage only."
            )
        else:
            _dti_section8_no_source_data_notice_v1()
            _dti_graph_ui_v607_fallback_notice("Section 8 distance fallback")
            distance_frame = _dti_graph_ui_v607_fallback_distance_frame()
            dist_chart = alt.Chart(distance_frame).mark_bar().encode(
                x=alt.X("distance:Q", title="heuristic reference distance"),
                y=alt.Y("profile:N", sort="-x", title="profile"),
                tooltip=list(distance_frame.columns),
            )
            _DTI_DISABLED_GRAPH_CALL(dist_chart.properties(height=220), width="stretch", key="dti_graph_ui_dom_stable_chart_04")
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
                    _DTI_DISABLED_GRAPH_CALL((band_chart + base).properties(height=280), width="stretch", key="dti_graph_ui_dom_stable_chart_05")
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
            _DTI_DISABLED_GRAPH_CALL(chart_s8.properties(height=280), width="stretch", key="dti_graph_ui_dom_stable_chart_06")

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
                _DTI_DISABLED_GRAPH_CALL((hband + vline + chart).properties(height=300), width="stretch", key="dti_graph_ui_dom_stable_chart_07")
                st.caption(
                    "This scatter visualizes a heuristic early-scale / late-clustering trade-off. "
                    "The reference line and band are visual guides only, not a formal exclusion rule regions."
                )
            else:
                st.info("rs_drag/S8 table found, but no numeric rows are available.")
        else:
            _dti_section8_no_source_data_notice_v1()


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

# DTI_7C_EXAMINER_PAYLOAD_PREVIEW_OBJECT_V1D
_dti_7c_examiner_payload_preview_v1d = {
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
# DTI_7C_EXAMINER_PAYLOAD_DISPLAY_CALL_V1D
_dti_render_7c_examiner_payload_display_v1(_dti_7c_examiner_payload_preview_v1d)
# /DTI_7C_EXAMINER_PAYLOAD_DISPLAY_CALL_V1D

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
            _dti_arrow_safe_df_v1(result_rows_7c, width="stretch", hide_index=True)

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
            _dti_arrow_safe_df_v1(score_rows_7c, width="stretch", hide_index=True)

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
            # DTI_7C_EXAMINER_VERDICT_RECORD_DISPLAY_CALL_V1
            _dti_render_7c_examiner_verdict_record_v1(examiner_record_7c)
            # /DTI_7C_EXAMINER_VERDICT_RECORD_DISPLAY_CALL_V1

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
    _dti_section8_boundary_notice_once_v1()
    _dti_boundary_readonly_caption_v1()
    # DTI_SECTION8_REMOVE_INEFFECTIVE_BOUNDARY_TABS_INDENT_SAFE_V2
    _dti_boundary_readonly_caption_v1()
    _tab_s8_v3 = _dti_noop_context_v1()
    _tab_trade_v3 = _dti_noop_context_v1()
    with _tab_s8_v3:
        _DTI_DISABLED_GRAPH_CALL(
            _dti_graph_ui_v607_altair_line_with_band(_fallback_v3, "sweep_value", "S8").properties(height=280), width="stretch",
        )
    with _tab_trade_v3:
        _DTI_DISABLED_GRAPH_CALL(
            _dti_graph_ui_v607_altair_scatter(_fallback_v3, "rs_drag", "S8").properties(height=280), width="stretch",
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
    _dti_arrow_safe_df_v1(fit_df, width="stretch")

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
_dti_arrow_safe_df_v1(pd.DataFrame([external_api_payload]), hide_index=True, width="stretch")

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
            _dti_arrow_safe_df_v1(pd.DataFrame(derived_rows), hide_index=True, width="stretch")

    with st.expander("Raw external API response", expanded=False):
        st.caption("Large arrays are summarized here to keep the UI readable. The CMB graph still uses the full real API arrays.")
        _dti_render_summarized_raw_api_payload_v1(external_api_result)

    # === DTI EXTERNAL RESULT DIRECT CMB GRAPH V1 ===
    with st.expander("CMB spectra graph — real API arrays only", expanded=True):
        _dti_render_real_api_cmb_svg_graph_v1(external_api_result)
    # === END DTI EXTERNAL RESULT DIRECT CMB GRAPH V1 ===


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


# === DTI CMB / Likelihood Capability Matrix V1 standalone fallback ===
# This fallback does not execute by itself unless called from an existing UI flow.
# To render without a payload, call:
# _dti_render_cmb_likelihood_capability_matrix_v1_no_payload()
# === END DTI CMB / Likelihood Capability Matrix V1 standalone fallback ===


# === DTI_FRONTEND_TRANSLATOR_INTEGRATION_LOCAL_PATCH_V1 ===
# Frontend-only translator integration panel.
# This panel calls the public backend translator endpoint only when the user presses the button.
# It does not modify backend code, does not run CLASS/AxiCLASS, does not generate CMB spectra,
# does not evaluate Planck likelihoods, and does not compare posteriors.

def _dti_render_jump_translator_boundary_badges_v1(response_obj):
    boundary = response_obj.get("boundary", {}) if isinstance(response_obj, dict) else {}
    impl = response_obj.get("implementation_status", {}) if isinstance(response_obj, dict) else {}

    st.markdown("##### Boundary confirmation")

    rows = [
        ("No CLASS run", boundary.get("class_run") is False),
        ("No AxiCLASS run", boundary.get("axiclass_run") is False),
        ("No CMB spectra generation", boundary.get("cmb_spectra_generated") is False),
        ("No Planck chi2", boundary.get("planck_chi2") is False),
        ("No likelihood evaluation", boundary.get("likelihood_evaluation") is False),
        ("No posterior comparison", boundary.get("posterior_comparison") is False),
        ("Jump model active: false", impl.get("jump_model_active") is False),
        ("Jump background active: false", impl.get("jump_background_active") is False),
        ("Jump perturbations active: false", impl.get("jump_perturbations_active") is False),
    ]

    for label, ok in rows:
        if ok:
            st.success(label)
        else:
            st.warning(f"{label} — not confirmed in response")


def _dti_call_jump_translator_v1(payload, timeout_sec=30):
    import requests as _dti_requests_v1

    endpoint = "https://dti-class-api.onrender.com/class/translate-jump-params"
    response = _dti_requests_v1.post(endpoint, json=payload, timeout=timeout_sec)
    try:
        data = response.json()
    except Exception:
        data = {
            "accepted": False,
            "errors": ["response_json_parse_failed"],
            "raw_text": response.text,
        }

    return {
        "endpoint": endpoint,
        "http_code": response.status_code,
        "ok": response.ok,
        "data": data,
    }


def _dti_render_jump_translator_panel_v1():
    st.markdown("---")
    with st.expander("Jump parameter translator — backend boundary check", expanded=False):
        st.markdown(
            "Translator-only panel. This sends jump parameters to the backend translator endpoint "
            "and displays normalized values plus explicit boundary fields. It does not run CLASS, "
            "does not run AxiCLASS, does not generate CMB spectra, does not evaluate Planck chi2, "
            "does not evaluate likelihood, and does not compare posteriors."
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            h0 = st.number_input("H0", min_value=1.0, max_value=150.0, value=72.6, step=0.1, key="dti_jump_tr_h0_v1")
            omega_b = st.number_input("omega_b", min_value=0.0001, max_value=0.2, value=0.02237, step=0.00001, format="%.5f", key="dti_jump_tr_omega_b_v1")
            omega_cdm = st.number_input("omega_cdm", min_value=0.0001, max_value=1.0, value=0.1200, step=0.0001, format="%.4f", key="dti_jump_tr_omega_cdm_v1")
        with c2:
            ln10_10_as = st.number_input("ln10_10_As", min_value=0.1, max_value=10.0, value=3.044, step=0.001, format="%.3f", key="dti_jump_tr_ln10as_v1")
            n_s = st.number_input("n_s", min_value=0.1, max_value=2.0, value=0.965, step=0.001, format="%.3f", key="dti_jump_tr_ns_v1")
            tau_reio = st.number_input("tau_reio", min_value=0.0, max_value=1.0, value=0.054, step=0.001, format="%.3f", key="dti_jump_tr_tau_v1")
        with c3:
            a_j = st.number_input("A_J", min_value=-1.0, max_value=1.0, value=-0.00022, step=0.00001, format="%.5f", key="dti_jump_tr_aj_v1")
            z_j = st.number_input("z_J", min_value=0.0001, max_value=5000.0, value=1100.0, step=1.0, key="dti_jump_tr_zj_v1")
            delta_z = st.number_input("Delta_z", min_value=0.0001, max_value=2000.0, value=30.0, step=1.0, key="dti_jump_tr_dz_v1")

        regime = st.selectbox(
            "jump_regime_label",
            ["low_z_geometry", "recombination_scale", "early_time_ede_like"],
            index=1,
            key="dti_jump_tr_regime_v1",
        )

        payload = {
            "backend_mode": "jump_parameter_translation_only",
            "H0": float(h0),
            "omega_b": float(omega_b),
            "omega_cdm": float(omega_cdm),
            "ln10_10_As": float(ln10_10_as),
            "n_s": float(n_s),
            "tau_reio": float(tau_reio),
            "jump_model_enabled": True,
            "jump_target": "E_z",
            "transition_form": "smoothed_tanh_step",
            "A_J": float(a_j),
            "z_J": float(z_j),
            "Delta_z": float(delta_z),
            "jump_regime_label": str(regime),
            "request_claim_level": "translation_only",
        }

        st.caption("Fixed request fields: backend_mode=jump_parameter_translation_only, jump_target=E_z, transition_form=smoothed_tanh_step, request_claim_level=translation_only.")

        with st.expander("Request payload preview", expanded=False):
            st.json(payload)

        if st.button("Run translator boundary check", key="dti_jump_translator_run_v1"):
            with st.spinner("Calling backend translator endpoint..."):
                try:
                    result = _dti_call_jump_translator_v1(payload)
                except Exception as exc:
                    st.error(f"Translator request failed: {exc!r}")
                    return

            st.write(f"HTTP status: {result.get('http_code')}")
            data = result.get("data", {})

            if result.get("ok") and isinstance(data, dict) and data.get("accepted") is True:
                st.success("Translator response accepted. Boundary-only response received.")
            else:
                st.warning("Translator response was not accepted or returned a non-OK HTTP status.")

            if isinstance(data, dict):
                warnings = data.get("warnings", [])
                errors = data.get("errors", [])
                if errors:
                    st.error("Errors")
                    st.json(errors)
                if warnings:
                    st.warning("Warnings")
                    st.json(warnings)

                st.markdown("##### Normalized values")
                st.json(data.get("normalized", {}))

                st.markdown("##### Formula")
                st.json(data.get("formula", {}))

                st.markdown("##### Implementation status")
                st.json(data.get("implementation_status", {}))

                _dti_render_jump_translator_boundary_badges_v1(data)

                with st.expander("Full translator response", expanded=False):
                    st.json(data)
            else:
                st.json(result)


_dti_render_jump_translator_panel_v1()

# === END DTI_FRONTEND_TRANSLATOR_INTEGRATION_LOCAL_PATCH_V1 ===

# DTI_REAL_APP_UI_BOUNDED_STATUS_PANEL_PATCH_V1_BEGIN
# Bounded DTI capability status panel.
# Boundary: diagnostic capability/status only. No CLASS run, no CMB generation,
# no likelihood, no Planck chi2, no posterior comparison, no physical validation,
# and no perturbation-closure claim.

def _dti_bounded_status_badge(value):
    """Return a conservative display badge for bounded DTI status values."""
    text = str(value) if value is not None else "UNKNOWN"
    return text


def _render_dti_bounded_capability_status_panel(backend_base_url=None):
    """
    Render audited DTI backend capability status.

    This panel is diagnostic/status-only. It does not run CLASS, generate spectra,
    evaluate likelihoods, compute Planck chi2, perform posterior comparison,
    validate physical CMB output, or claim perturbation closure.
    """
    import streamlit as st

    st.markdown("### DTI backend capability status")
    st.caption(
        "Bounded diagnostic capability status only. "
        "No physical CMB validation, likelihood, Planck chi2, posterior comparison, "
        "or perturbation-closure claim."
    )

    default_url = "https://dti-class-api.onrender.com"
    base_url = backend_base_url or default_url

    status_payload = None
    error_text = None

    try:
        import requests
        r = requests.get(base_url.rstrip("/") + "/dti/capability-status", timeout=8)
        if r.status_code == 200:
            status_payload = r.json()
        else:
            error_text = f"Capability endpoint returned HTTP {r.status_code}"
    except Exception as exc:
        error_text = f"Capability endpoint unavailable: {exc}"

    if status_payload is None:
        st.warning("DTI capability endpoint is not available in this session.")
        if error_text:
            st.caption(error_text)
        st.info(
            "Boundary retained: this panel does not run CLASS, generate spectra, "
            "evaluate likelihoods, or claim physical validation."
        )
        return

    fields = status_payload.get("status_fields", {})
    boundaries = status_payload.get("boundaries", {})
    provenance = status_payload.get("provenance", {})

    rows = [
        ("Compile gate", fields.get("compile_gate", "UNKNOWN"), "no physics claim"),
        ("Short-root smoke", fields.get("short_root_smoke", "UNKNOWN"), "no physics claim"),
        ("perturbations_derivs reached", fields.get("derivs_entry_reached", "UNKNOWN"), "diagnostic path only"),
        ("Guard zone reached", fields.get("guard_zone_reached", "UNKNOWN"), "diagnostic path only"),
        ("V1C hook reached", fields.get("v1c_hook_reached", "UNKNOWN"), "diagnostic path only"),
        ("Numeric hygiene", fields.get("numeric_hygiene", "UNKNOWN"), "log hygiene only"),
        ("Diagnostic response", fields.get("probe_response", "UNKNOWN"), "not non-inertness proof"),
        ("Non-inertness", fields.get("non_inertness_status", "UNKNOWN"), "not established"),
        ("Physical validation", fields.get("physical_validation", "NOT_OPENED"), "not run"),
        ("Likelihood", fields.get("likelihood_status", "NOT_OPENED"), "not run"),
        ("Planck chi2", fields.get("planck_chi2_status", "NOT_OPENED"), "not run"),
        ("Posterior comparison", fields.get("posterior_comparison", "NOT_OPENED"), "not run"),
        ("Closure claim", fields.get("closure_claim", "NO"), "none"),
        ("Public claim level", fields.get("public_claim_level", "BOUNDED_DIAGNOSTIC_ONLY"), "bounded diagnostic only"),
    ]

    st.table(
        [
            {"item": name, "status": _dti_bounded_status_badge(value), "boundary": boundary}
            for name, value, boundary in rows
        ]
    )

    with st.expander("DTI capability provenance and no-claim boundary", expanded=False):
        st.json(
            {
                "classification": status_payload.get("classification"),
                "schema_name": status_payload.get("schema_name"),
                "provenance": provenance,
                "boundaries": boundaries,
                "no_claims": {
                    "class_run_from_panel": False,
                    "cmb_generation": False,
                    "physical_validation": False,
                    "likelihood": False,
                    "planck_chi2": False,
                    "posterior_comparison": False,
                    "perturbation_closure_claim": False,
                    "hubble_tension_solution_claim": False,
                },
            }
        )

# DTI_REAL_APP_UI_BOUNDED_STATUS_PANEL_PATCH_V1_END

# DTI_REAL_APP_UI_BOUNDED_STATUS_PANEL_RENDER_V1_BEGIN
try:
    _render_dti_bounded_capability_status_panel()
except Exception as _dti_status_panel_exc:
    import streamlit as st
    st.warning("DTI capability status panel could not be rendered.")
    st.caption(str(_dti_status_panel_exc))
# DTI_REAL_APP_UI_BOUNDED_STATUS_PANEL_RENDER_V1_END

# --- PAPER/APJ STATUS PANEL: project-status boundary readout only ---
with st.expander("Paper / APJ conversion status", expanded=False):
    st.markdown(
        """
        **Current APJ-oriented text artifact**

        A non-promoted APJ-oriented clone has completed title, abstract, and introduction compression.

        - artifact type: project-status manuscript clone
        - page count: 76
        - PDF SHA256: `d8f31844e3b061da5f71bf8bb2c12f769338d27469635bb63fca53c503b8fd02`
        - status: human-accepted for app-facing status display
        - promotion status: not promoted
        - submission status: no submission-ready claim

        **Boundary**

        This panel is a status and boundary-readout panel only.

        It is not a likelihood result, posterior comparison, Planck chi-square evaluation,
        CMB validation, perturbation-sector validation, or Hubble-tension solution.

        **Correct reading**

        This records manuscript-conversion progress only. It does not add new cosmological evidence.
        """
    )
# --- END PAPER/APJ STATUS PANEL ---


# === DTI EMBEDDED POSTERIOR VIEWER PUBLIC SECTION: START ===
# Added by DTI_PUBLIC_APP_INTEGRATION_PUBLIC_UPDATE_IMPL_CLONE_V1.
# Read-only frozen artifact display. No live sampling, no likelihood evaluation,
# no backend inference, and no physics-validation claim.

from pathlib import Path as _DTIPath
import json as _dti_json

def _dti_embedded_posterior_viewer_public_section():
    """Display pending state only; no sample/synthetic/proxy posterior is shown."""
    st.subheader("Observed-data posterior")
    st.warning(
        "Status: pending. No sample, synthetic, smoke, or proxy posterior is displayed."
    )
    st.markdown(
        """
    This public panel is intentionally disabled until the posterior is connected to a real-data likelihood path.
    
    Required before posterior display:
    - CLASS output path
    - real likelihood connection
    - at least one observed-data likelihood source such as CMB, BAO, SN, or H(z)
    - reproducible offline chain freeze
    - manifest/hash/audit package
    - explicit boundary review
    
    Current boundary:
    - no sample posterior displayed
    - no synthetic posterior displayed
    - no smoke posterior displayed
    - no proxy posterior displayed
    - no live MCMC in Streamlit
    - no real likelihood evaluation in the public app
    - no Planck likelihood in the public app
    - no physics validation claim
    - no cosmological inference claim
    - no manuscript value update
    """
    )
    with st.expander("Boundary / audit status", expanded=True):
        st.markdown(
            """
    **Displayed posterior:** none.  
    **Reason:** the previous embedded viewer used a proxy/smoke/synthetic path, not observed-data likelihood inference.  
    **Next valid route:** real data / real likelihood / CLASS output / CMB or BAO or SN or H(z) connected posterior.
    """
        )
    return


# --- DTI embedded posterior viewer: SDSS DR16cosmo offline BAO chain V1 ---
def _dti_render_embedded_bao_sdss_dr16cosmo_posterior_v1():
    """Render an audit-only embedded posterior package.

    Boundary:
    - offline BAO chain only
    - no live MCMC
    - no Planck likelihood
    - no CLASS execution
    - no physics validation claim
    """
    import json
    from pathlib import Path

    import pandas as pd
    import streamlit as st

    base = Path(__file__).resolve().parent / "data" / "embedded_bao_sdss_dr16cosmo_v1"
    payload_path = base / "data" / "posterior_payload.json"
    summary_path = base / "data" / "chain_summary.tsv"
    diagnostics_path = base / "data" / "diagnostics.tsv"
    bestfit_path = base / "data" / "map_or_bestfit.tsv"
    source_identity_path = base / "meta" / "source_identity.tsv"
    claim_boundary_path = base / "notes" / "CLAIM_BOUNDARY.md"

    def _dti_redact_local_paths_for_public_ui_v1(df):
        """Redact local absolute paths before displaying provenance tables in the UI."""
        try:
            redacted = df.copy()
            for col in redacted.columns:
                if redacted[col].dtype == object:
                    redacted[col] = redacted[col].astype(str).str.replace(
                        r"/Users/[^\s\t\n]+",
                        "[LOCAL_PATH_REDACTED]",
                        regex=True,
                    )
                    redacted[col] = redacted[col].str.replace(
                        r"/private/var/[^\s\t\n]+",
                        "[LOCAL_PATH_REDACTED]",
                        regex=True,
                    )
            return redacted
        except Exception:
            return df

    with st.expander("Embedded posterior viewer — offline BAO chain, audit-only", expanded=True):
        st.success(
            "REAL-DATA BAO VIEWER ACTIVE: this section uses frozen SDSS DR16cosmo BAO offline-chain outputs only. "
            "Smoke / synthetic figures are not used for this graph viewer."
        )
        st.warning(
            "Audit-only embedded package. Not a live MCMC run, not a Planck likelihood, "
            "not a physics validation, and not a manuscript claim."
        )

        required = [
            payload_path,
            summary_path,
            diagnostics_path,
            bestfit_path,
            source_identity_path,
            claim_boundary_path,
        ]
        missing = [str(p) for p in required if not p.exists()]
        if missing:
            st.info("Embedded posterior package is not loaded here; frozen BAO graph/table sections remain audit-only where available.")
            # DTI_HIDE_ABSOLUTE_PATH_DUMP_V1
            st.caption("Local package path details hidden for UI safety.")
            return

        try:
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
        except Exception as exc:
            st.error(f"Could not read posterior payload JSON: {exc}")
            return

        st.caption("Boundary: offline BAO chain only; public display does not imply physics validation.")
        st.json(payload)

        with st.expander("Raw embedded tables — provenance / audit readback", expanded=False):
            st.subheader("Chain summary")
            _dti_arrow_safe_df_v1(pd.read_csv(summary_path, sep="\t"), width="stretch")

            st.subheader("G02 diagnostics — TSV")
            _dti_arrow_safe_df_v1(pd.read_csv(diagnostics_path, sep="\t"), width="stretch")

            st.subheader("MAP / best-fit table")
            _dti_arrow_safe_df_v1(pd.read_csv(bestfit_path, sep="\t"), width="stretch")

            st.subheader("Source identity")
            st.caption("Local absolute paths are redacted in the public UI. Full provenance remains in the frozen local artifact.")
            source_identity_df = pd.read_csv(source_identity_path, sep="\t")
            source_identity_df = _dti_redact_local_paths_for_public_ui_v1(source_identity_df)
            for _dti_col in source_identity_df.columns:
                source_identity_df[_dti_col] = source_identity_df[_dti_col].astype(str).str.replace(
                    r"/Users/[^\s\t\n]+",
                    "[LOCAL_PATH_REDACTED]",
                    regex=True,
                )
                source_identity_df[_dti_col] = source_identity_df[_dti_col].astype(str).str.replace(
                    r"/private/var/[^\s\t\n]+",
                    "[LOCAL_PATH_REDACTED]",
                    regex=True,
                )
            _dti_arrow_safe_df_v1(source_identity_df, width="stretch")

        with st.expander("Claim boundary", expanded=False):
            st.markdown(claim_boundary_path.read_text(encoding="utf-8"))

        # --- DTI real-data graph viewer: frozen BAO chain audit-only V1 ---
        try:
            st.markdown("#### Embedded graph viewer — frozen offline BAO chain, audit-only")
            st.warning(
                "This graph viewer renders frozen real-data-derived offline BAO chain outputs "
                "from the embedded package. It is not a toy model, not a sample model, "
                "not synthetic data, not live MCMC, not CLASS execution, not a Planck likelihood, "
                "not physics validation, and not a manuscript claim."
            )

            graph_root = base
            graph_chain_summary = graph_root / "data" / "chain_summary.tsv"
            graph_diagnostics = graph_root / "data" / "diagnostics.tsv"
            graph_bestfit = graph_root / "data" / "map_or_bestfit.tsv"

            # FORCE_REAL_DATA_TSV_CHART_BOARD_V1
            # FORCE_NUMERIC_TSV_CHART_RENDER_FIX7
            st.markdown("### Real-data TSV chart board — G01/G02/G03")
            st.caption(
                "These charts are rendered directly from frozen SDSS DR16cosmo BAO embedded TSV files. "
                "No smoke figures, no generated samples, no synthetic fallback, and no live inference are used."
            )

            def _dti_numeric_chart_frame_v1(df, label_col_candidates):
                """Return a numeric-only chart frame, coercing TSV string values to numbers."""
                chart_df = df.copy()

                label_col = None
                for cand in label_col_candidates:
                    if cand in chart_df.columns:
                        label_col = cand
                        break

                numeric = chart_df.drop(columns=[label_col], errors="ignore").copy()
                for col in numeric.columns:
                    numeric[col] = pd.to_numeric(numeric[col], errors="coerce")

                numeric = numeric.dropna(axis=1, how="all")

                if label_col is not None:
                    numeric.index = chart_df[label_col].astype(str)

                return numeric

            def _dti_html_bar_chart_from_numeric_frame_v1(numeric_df, title):
                """FORCE_HTML_TSV_BAR_RENDER_FIX8: deterministic UI bars from frozen TSV numeric values."""
                try:
                    work = numeric_df.copy()
                    if work.empty or len(work.columns) == 0:
                        return "<div><b>No numeric values available for chart.</b></div>"

                    html = []
                    html.append('<div style="border:1px solid #3a3f4b; border-radius:8px; padding:12px; margin:8px 0 16px 0;">')
                    html.append(f'<div style="font-weight:700; margin-bottom:10px;">{title}</div>')
                    html.append('<div style="font-size:12px; opacity:0.8; margin-bottom:10px;">Bars are rendered directly from frozen embedded TSV numeric values. No generated samples.</div>')

                    flat = []
                    for idx, row in work.iterrows():
                        for col in work.columns:
                            val = row[col]
                            if pd.notna(val):
                                try:
                                    fval = float(val)
                                    flat.append((str(idx), str(col), fval))
                                except Exception:
                                    pass

                    if not flat:
                        html.append('<div>No finite numeric values available after coercion.</div>')
                        html.append('</div>')
                        return "\n".join(html)

                    max_abs = max(abs(v) for _, _, v in flat)
                    if max_abs == 0:
                        max_abs = 1.0

                    for idx, col, val in flat:
                        width = max(2.0, min(100.0, abs(val) / max_abs * 100.0))
                        label = f"{idx} / {col}"
                        html.append('<div style="margin:7px 0;">')
                        html.append(f'<div style="font-size:12px; margin-bottom:2px;">{label}: <code>{val:.6g}</code></div>')
                        html.append(
                            '<div style="height:13px; background:#242833; border-radius:6px; overflow:hidden;">'
                            f'<div style="height:13px; width:{width:.2f}%; background:#7aa2f7;"></div>'
                            '</div>'
                        )
                        html.append('</div>')

                    html.append('</div>')
                    return "\n".join(html)
                except Exception as exc:
                    return f"<div><b>HTML TSV chart failed closed:</b> {exc}</div>"

            try:
                board_chain_df = pd.read_csv(graph_chain_summary, sep="\t")
                board_diag_df = pd.read_csv(graph_diagnostics, sep="\t")
                board_bestfit_df = pd.read_csv(graph_bestfit, sep="\t")

                board_tabs = st.tabs([
                    "G01 chart — chain summary TSV",
                    "G02 chart — diagnostics TSV",
                    "G03 chart — MAP/best-fit TSV",
                ])

                with board_tabs[0]:
                    st.markdown("**TSV-derived chart — G01 chain summary**")
                    board_chart_df = _dti_numeric_chart_frame_v1(
                        board_chain_df,
                        ["parameter", "param", "name", "key"],
                    )
                    if not board_chart_df.empty and len(board_chart_df.columns) >= 1:
                        st.markdown(
                            _dti_html_bar_chart_from_numeric_frame_v1(board_chart_df, "G01 chain summary TSV bars"),
                            unsafe_allow_html=True,
                        )
                    else:
                        st.error("G01 chart could not render because no numeric TSV columns were available after coercion.")
                    with st.expander("Source TSV table — G01", expanded=False):
                        _dti_arrow_safe_df_v1(board_chain_df, width="stretch")

                with board_tabs[1]:
                    st.markdown("**TSV-derived chart — G02 diagnostics**")
                    board_chart_df = _dti_numeric_chart_frame_v1(
                        board_diag_df,
                        ["chain", "chain_seed", "key"],
                    )
                    if not board_chart_df.empty and len(board_chart_df.columns) >= 1:
                        st.markdown(
                            _dti_html_bar_chart_from_numeric_frame_v1(board_chart_df, "G02 diagnostics TSV bars"),
                            unsafe_allow_html=True,
                        )
                    else:
                        st.error("G02 chart could not render because no numeric TSV columns were available after coercion.")
                    with st.expander("Source TSV table — G02", expanded=False):
                        _dti_arrow_safe_df_v1(board_diag_df, width="stretch")

                with board_tabs[2]:
                    st.markdown("**TSV-derived chart — G03 MAP / best-fit**")
                    board_chart_df = _dti_numeric_chart_frame_v1(
                        board_bestfit_df,
                        ["chain", "step", "key"],
                    )
                    if not board_chart_df.empty and len(board_chart_df.columns) >= 1:
                        st.markdown(
                            _dti_html_bar_chart_from_numeric_frame_v1(board_chart_df, "G03 MAP / best-fit TSV bars"),
                            unsafe_allow_html=True,
                        )
                    else:
                        st.error("G03 chart could not render because no numeric TSV columns were available after coercion.")
                    with st.expander("Source TSV table — G03", expanded=False):
                        _dti_arrow_safe_df_v1(board_bestfit_df, width="stretch")

            except Exception as board_exc:
                st.error(f"Real-data TSV chart board failed closed: {board_exc}")

            graph_tabs = st.tabs([
                "G01 source table",
                "G02 source table",
                "G03 source table",
                "Boundary / forbidden plots",
            ])

            with graph_tabs[0]:
                if not graph_chain_summary.exists():
                    st.error("Missing frozen embedded file: chain_summary.tsv")
                else:
                    graph_chain_df = pd.read_csv(graph_chain_summary, sep="\t")
                    st.caption("G01 — source readback from frozen chain_summary.tsv.")
                    _dti_arrow_safe_df_v1(graph_chain_df, width="stretch")

            with graph_tabs[1]:
                if not graph_diagnostics.exists():
                    st.error("Missing frozen embedded file: diagnostics.tsv")
                else:
                    graph_diag_df = pd.read_csv(graph_diagnostics, sep="\t")
                    st.caption("G02 — source readback from frozen diagnostics.tsv.")
                    _dti_arrow_safe_df_v1(graph_diag_df, width="stretch")

            with graph_tabs[2]:
                if not graph_bestfit.exists():
                    st.error("Missing frozen embedded file: map_or_bestfit.tsv")
                else:
                    graph_bestfit_df = pd.read_csv(graph_bestfit, sep="\t")
                    st.caption("G03 — source readback from frozen map_or_bestfit.tsv.")
                    _dti_arrow_safe_df_v1(graph_bestfit_df, width="stretch")

            with graph_tabs[3]:
                st.markdown(
                    """
                    **Allowed graphs in this patch**

                    - G01: `chain_summary.tsv` chart/table
                    - G02: `diagnostics.tsv` chart/table
                    - G03: `map_or_bestfit.tsv` chart/table

                    **Explicitly not rendered**

                    - G04: alpha_DM / alpha_DH scatter
                    - G05: chi2 trace
                    - G06: alpha_DM histogram
                    - G07: alpha_DH histogram

                    These are not rendered because the current `posterior_payload.json`
                    does not contain real frozen sample arrays. No generated, toy,
                    sample, synthetic, random, demo, illustrative, or fallback data are used.
                    """
                )
        except Exception as exc:
            st.error(f"Frozen real-data graph viewer failed closed: {exc}")
        # --- /DTI real-data graph viewer: frozen BAO chain audit-only V1 ---


try:
    _dti_render_embedded_bao_sdss_dr16cosmo_posterior_v1()

    # --- DTI Route A manual-sanity static diagnostic panel V1 BEGIN ---
    with st.expander("Route A manual-sanity diagnostic — frozen independent lane", expanded=False):
        st.caption(
            "Frozen diagnostic values only. Not a full eBOSS LRG likelihood, "
            "not a full BAO likelihood, not a posterior comparison, and not a Planck validation claim."
        )
    
        st.warning(
            "Boundary: diagnostic-only static display. No backend call, no CLASS/AxiCLASS run, "
            "no likelihood, no MCMC, no posterior claim, no manuscript update."
        )
    
        st.markdown("### Frozen diagnostic comparison")
        st.table([
            {
                "lane": "Route B frozen reference",
                "chi2": "0.2887322581504387",
                "scope": "TOPLEFT_2X2_DM_DH_ONLY / NOT_FULL_EBOSS_LRG_LIKELIHOOD",
                "status": "FROZEN_REFERENCE_ACTIVE",
            },
            {
                "lane": "Route A derived-from-Route-B template",
                "chi2": "0.2887322581504387",
                "scope": "MINIMAL_CHI2_DIAGNOSTIC_ONLY",
                "status": "FROZEN_REVIEW_PASS",
            },
            {
                "lane": "Route A manual-sanity independent lane",
                "chi2": "0.848405000840325",
                "scope": "MANUAL_SANITY_GEOMETRY_RATIO_DIAGNOSTIC_ONLY",
                "status": "FROZEN_REVIEW_PASS",
            },
        ])
    
        st.markdown("### Manual-sanity algebraic decomposition")
        st.json({
            "source": {
                "handoff": "_DTI_ROUTE_A_ROUTE_B_DIAGNOSTIC_HANDOFF_V1B_WITH_MANUAL_SANITY_LANE_20260609_150156",
                "mount_request": "_DTI_APP_ROUTE_A_MANUAL_SANITY_MOUNT_REQUEST_V1B_20260609_150643",
                "payload_json_sha256": "045a01b4c1c57a2d4e1eb6f10dbd97220745848308ad449b9e8c0a0d86c94ed5",
                "app_py_pre_patch_sha256": "7e08d5056dae8b3351f7deddb60dccd5b402c3e0c5dd1e54c821d72f53a744dc",
            },
            "manual_sanity": {
                "model_vector": [17.45, 19.55],
                "observation_vector": [17.65, 19.77],
                "delta_model_minus_observation": [-0.1999999999999993, -0.21999999999999886],
                "inverse_covariance": [[11.6279311211, 1.75457174953], [1.75457174953, 4.72903805863]],
                "terms": {
                    "DM_DM": 0.4651172448439967,
                    "cross_total": 0.15440231395863865,
                    "DH_DH": 0.22888544203768962,
                    "term_sum_chi2": 0.848405000840325,
                },
                "manual_minus_route_b": 0.5596727426898863,
            },
            "boundaries": {
                "full_eboss_lrg_likelihood": False,
                "full_bao_likelihood": False,
                "likelihood": False,
                "mcmc": False,
                "posterior_claim": False,
                "planck_validation": False,
                "physical_validation": False,
                "backend_call": False,
                "class_or_axiclass_run": False,
                "manuscript_update": False,
            },
        })
    
        st.caption(
            "Source-locked static panel. The values are displayed as frozen diagnostics; "
            "the app does not recompute chi2 in this panel."
        )
    # --- DTI Route A manual-sanity static diagnostic panel V1 END ---
except Exception as _dti_embed_exc:
    try:
        import streamlit as st
        st.error(f"Embedded posterior viewer failed safely: {_dti_embed_exc}")
    except Exception:
        pass



# --- /DTI embedded posterior viewer: SDSS DR16cosmo offline BAO chain V1 ---
# --- DTI Route A/B boundary matrix static UI V1 BEGIN ---
with st.expander("Route A/B Boundary Matrix — diagnostic available, full inference unavailable", expanded=False):
    st.warning(
        "Boundary: diagnostic lanes are available, but full BAO/eBOSS likelihood, "
        "MCMC, posterior inference, Planck validation, and manuscript-level claim promotion "
        "remain unavailable in this public app."
    )
    st.markdown("### Diagnostic availability matrix")
    _dti_route_ab_boundary_rows_v1 = [
        {
            "lane": "Route B frozen reference",
            "available": "YES",
            "what_it_is": "Top-left 2x2 DM/DH diagnostic",
            "what_it_is_not": "Not full eBOSS LRG likelihood",
            "frozen_value_or_source": "chi2 = 0.2887322581504387",
        },
        {
            "lane": "Route A derived template",
            "available": "YES",
            "what_it_is": "Minimal diagnostic derived from frozen Route B values",
            "what_it_is_not": "Not independent full likelihood",
            "frozen_value_or_source": "chi2 = 0.2887322581504387",
        },
        {
            "lane": "Route A manual-sanity independent lane",
            "available": "YES",
            "what_it_is": "Independent geometry-ratio diagnostic lane",
            "what_it_is_not": "Not posterior, not MCMC, not Planck validation",
            "frozen_value_or_source": "chi2 = 0.848405000840325",
        },
        {
            "lane": "Full BAO/eBOSS likelihood",
            "available": "NO",
            "what_it_is": "Not implemented in this public app",
            "what_it_is_not": "Current diagnostic lanes are not full likelihood inference",
            "frozen_value_or_source": "Unavailable here",
        },
        {
            "lane": "MCMC / posterior / Planck validation",
            "available": "NO",
            "what_it_is": "Out of scope for this public diagnostic viewer",
            "what_it_is_not": "No inference claim and no validation claim",
            "frozen_value_or_source": "Unavailable here",
        },
    ]
    st.table(_dti_route_ab_boundary_rows_v1)
    st.caption(
        "Status badge: Diagnostic available / full inference unavailable. "
        "Route B, Route A template, and Route A manual-sanity are frozen diagnostic lanes only. "
        "They do not constitute a full BAO/eBOSS likelihood, MCMC posterior, Planck validation, "
        "or manuscript-level claim promotion."
    )
    with st.expander("Route A/B boundary provenance", expanded=False):
        st.json(
            {
                "route_b_frozen_reference_chi2": 0.2887322581504387,
                "route_a_derived_template_chi2": 0.2887322581504387,
                "route_a_manual_sanity_independent_lane_chi2": 0.848405000840325,
                "manual_minus_route_b": 0.5596727426898863,
                "route_b_scope": "TOPLEFT_2X2_DM_DH_ONLY / NOT_FULL_EBOSS_LRG_LIKELIHOOD",
                "route_a_scope": "MINIMAL_CHI2_DIAGNOSTIC_ONLY",
                "manual_sanity_scope": "MANUAL_SANITY_GEOMETRY_RATIO_DIAGNOSTIC_ONLY",
                "full_bao_eboss_likelihood": False,
                "mcmc": False,
                "posterior_inference": False,
                "planck_validation": False,
                "manuscript_claim_promotion": False,
                "source_dossier": "_DTI_ROUTE_A_ROUTE_B_DIAGNOSTIC_LANE_CONVERGENCE_DOSSIER_V1_20260609_155139",
                "source_app_hits_review": "_DTI_APP_ROUTE_AB_BOUNDARY_APP_HITS_REVIEW_V1_20260609_163516",
            }
        )
# --- DTI Route A/B boundary matrix static UI V1 END ---



# ---------------------------------------------------------------------
# DTI_INLINE_SAFE_V5_BLOCK_BEGIN
# Local-only embedded payload viewer. Audit display only.
# Boundaries: no MCMC, no CLASS, no likelihood, no posterior claim,
# no Planck/CMB validation, no physics validation, no public app update.
try:
    from pathlib import Path as _DTI_Path
    import runpy as _DTI_runpy
    import streamlit as _DTI_st

    _DTI_st.markdown("---")
    with _DTI_st.expander(
        "11. Embedded payload viewer — SAFE V5 frozen offline MCMC audit",
        expanded=False,
    ):
        _DTI_st.warning(
            "Audit-only embedded payload viewer. "
            "No new MCMC. No CLASS. No likelihood. No posterior claim. "
            "No Planck/CMB validation. No physics validation. No public app update."
        )
        _DTI_VIEWER = (
            _DTI_Path(__file__).resolve().parent
            / "embedded_payload_viewer_inline"
            / "local_embedded_payload_viewer_safe_v5.py"
        )
        if _DTI_VIEWER.exists():
            _DTI_runpy.run_path(str(_DTI_VIEWER), run_name="__main__")
        else:
            _DTI_st.error("SAFE V5 embedded viewer file is missing.")
except Exception as _dti_inline_safe_v5_exc:
    try:
        import streamlit as _DTI_st
        _DTI_st.error(f"SAFE V5 embedded viewer failed safely: {_dti_inline_safe_v5_exc}")
    except Exception:
        pass
# DTI_INLINE_SAFE_V5_BLOCK_END




# DTI_LIKELIHOOD_DEFINITION_BINDER_V1_BEGIN
def _dti_render_likelihood_definition_binder_v1():
    """Audit-only likelihood definition binder. No likelihood/MCMC/CLASS execution."""
    import streamlit as st
    import pandas as pd
    from pathlib import Path

    base = Path(__file__).resolve().parent / "data" / "likelihood_definition_binder_v1"
    definition_path = base / "LIKELIHOOD_DEFINITION_TEXT_V1.md"
    matrix_path = base / "READINESS_MATRIX_V1.tsv"
    audit_req_path = base / "STATIC_AUDIT_REQUIREMENTS.tsv"

    st.markdown("## Panel 8: Likelihood Definition Binder — audit-only")
    st.warning(
        "Audit-definition panel only. This panel does not evaluate likelihoods, "
        "run CLASS, run MCMC, mount a Planck likelihood backend, compare posterior weights, "
        "or support a physics-validation claim."
    )

    if definition_path.exists():
        st.markdown(definition_path.read_text(encoding="utf-8", errors="replace"))
    else:
        st.error("LIKELIHOOD_DEFINITION_TEXT_V1.md is missing.")

    st.markdown("### Execution readiness matrix")
    if matrix_path.exists():
        try:
            df = pd.read_csv(matrix_path, sep="\t").fillna("").astype(str)
            _dti_arrow_safe_df_v1(df, width="stretch")
        except Exception as e:
            st.error(f"Could not render readiness matrix: {e}")
    else:
        st.error("READINESS_MATRIX_V1.tsv is missing.")

    st.markdown("### Static audit requirements")
    if audit_req_path.exists():
        try:
            df2 = pd.read_csv(audit_req_path, sep="\t").fillna("").astype(str)
            _dti_arrow_safe_df_v1(df2, width="stretch")
        except Exception as e:
            st.error(f"Could not render static audit requirements: {e}")
    else:
        st.error("STATIC_AUDIT_REQUIREMENTS.tsv is missing.")

    st.info(
        "Current status: identity-locked and viewer-ready, not likelihood-validated. "
        "Before any posterior, Planck/CMB, DESI-fit, physics, or manuscript claim, "
        "a separate validation gate is required."
    )
# DTI_LIKELIHOOD_DEFINITION_BINDER_V1_END



# DTI_CLAIM_BOUNDARY_RED_SHIELD_VIEWER_V1_BEGIN
def _dti_claim_boundary_red_shield_viewer_v1():
    from pathlib import Path
    import streamlit as st
    import pandas as pd

    st.markdown("---")
    st.error("🛑 Panel 7: Claim Boundary Red Shield — audit guardrail")
    st.caption("This panel is a claim-boundary guardrail. It is not a new computation and it does not change the frozen payloads.")

    vows = [
        ("No new live MCMC execution inside this public app", "PASS"),
        ("No CLASS execution inside this public app", "PASS"),
        ("No live likelihood evaluation inside this public app", "PASS"),
        ("No Planck CMB validation claim", "PASS"),
        ("No posterior-validation claim beyond frozen audited packages", "PASS"),
        ("No physics-validation claim", "PASS"),
        ("No Hubble-tension-solution claim", "PASS"),
        ("No manuscript update claim", "PASS"),
        ("No raw-chain or large-original payload exposure", "PASS"),
    ]

    df = pd.DataFrame(vows, columns=["boundary_vow", "status"])
    _dti_arrow_safe_df_v1(df, width="stretch")

    base = Path(__file__).resolve().parent
    boundary_path = base / "data" / "embedded_bao_sdss_dr16cosmo_v1" / "notes" / "CLAIM_BOUNDARY.md"

    if boundary_path.exists():
        st.success("Frozen claim-boundary file found.")
        with st.expander("Frozen CLAIM_BOUNDARY.md readback", expanded=False):
            st.markdown(boundary_path.read_text(encoding="utf-8", errors="replace"))
    else:
        st.error("Frozen claim-boundary file is missing.")

    st.warning(
        "Current status: source-lock and public visual freeze are complete, "
        "but this does not constitute full physical proof, Planck validation, "
        "or final cosmological solution."
    )

try:
    _dti_claim_boundary_red_shield_viewer_v1()
except Exception as exc:
    import streamlit as st
    st.error(f"Claim Boundary Red Shield failed to render: {exc}")
# DTI_CLAIM_BOUNDARY_RED_SHIELD_VIEWER_V1_END

# DTI_PANEL8_LIKELIHOOD_BINDER_CALL_V1
_dti_render_likelihood_definition_binder_v1()

# --- DTI citation/contact block V1 BEGIN ---
st.divider()
# --- DTI Moresco2016 BC03 cosmic chronometer visual overlay V1: visible call ---
_dti_render_moresco2016_bc03_cc_visual_overlay_v1(locals())
# --- /DTI Moresco2016 BC03 cosmic chronometer visual overlay V1: visible call ---

with st.expander("About / Citation / Provenance", expanded=False):
    st.markdown(
        """
**Author**  
Junichi Fujiki / FUJIKIX

**Contact**  
jun@fujikix.com

**Project**  
MAXOMEGA / DTI diagnostic viewer

**Related archival records, not live-compute dependencies**

1. **Extended Evidence Ledger and Provenance Framework for Fixed-H0 Cosmology Branch Audits**  
   106-Page Comprehensive Freeze Candidate  
   DOI: `10.5281/zenodo.20603277`

2. **Audit-First Evidence for Reproducible Branch Structure in Fixed-H0 Cosmology Fits**  
   Core Manuscript / Review Target  
   DOI: `10.5281/zenodo.20603167`

**Boundary**  
This public app is a diagnostic and provenance viewer. It does not perform live likelihood evaluation, MCMC sampling, Planck validation, posterior inference, or manuscript-level claim promotion.
        """
    )
# --- DTI citation/contact block V1 END ---

# --- DTI_NEXT_CC_HZ_DIAGNOSTIC_PANEL_V1_BEGIN ---
# Source-locked additional CC/H(z) diagnostic-only lane.
# This top-level block is intentionally guarded and does not call backend/API/CLASS/AxiCLASS/MCMC/likelihood.
try:
    with st.expander("Additional CC/H(z) diagnostic lane — source-locked, diagnostic-only", expanded=False):
        st.caption("Diagnostic-only CC/H(z) score. This is not a likelihood evaluation, not a posterior comparison, not a fit, and not cosmological validation.")

        _dti_next_cc_hz_rows_v1 = [
    {"row_id": 'ZHANG2014_CC_ROW_001', "z": 0.07, "H_obs": 69, "sigma_H": 19.6, "source_label": 'Zhang2014_CC'},
    {"row_id": 'ZHANG2014_CC_ROW_002', "z": 0.12, "H_obs": 68.6, "sigma_H": 26.2, "source_label": 'Zhang2014_CC'},
    {"row_id": 'ZHANG2014_CC_ROW_003', "z": 0.2, "H_obs": 72.9, "sigma_H": 29.6, "source_label": 'Zhang2014_CC'},
    {"row_id": 'ZHANG2014_CC_ROW_004', "z": 0.28, "H_obs": 88.8, "sigma_H": 36.6, "source_label": 'Zhang2014_CC'},
    {"row_id": 'ZHANG2014_CC_ROW_005', "z": 1.363, "H_obs": 160, "sigma_H": 33.6, "source_label": 'Zhang2014_CC'},
    {"row_id": 'ZHANG2014_CC_ROW_006', "z": 1.965, "H_obs": 186.5, "sigma_H": 50.4, "source_label": 'Zhang2014_CC'},
    {"row_id": 'SIMON2005_CC_ROW_001', "z": 0.09, "H_obs": 69, "sigma_H": 12, "source_label": 'Simon2005_CC'},
    {"row_id": 'SIMON2005_CC_ROW_002', "z": 0.17, "H_obs": 83, "sigma_H": 8, "source_label": 'Simon2005_CC'},
    {"row_id": 'SIMON2005_CC_ROW_003', "z": 0.27, "H_obs": 77, "sigma_H": 14, "source_label": 'Simon2005_CC'},
    {"row_id": 'SIMON2005_CC_ROW_004', "z": 0.4, "H_obs": 95, "sigma_H": 17, "source_label": 'Simon2005_CC'},
    {"row_id": 'SIMON2005_CC_ROW_005', "z": 0.9, "H_obs": 117, "sigma_H": 23, "source_label": 'Simon2005_CC'},
    {"row_id": 'SIMON2005_CC_ROW_006', "z": 1.3, "H_obs": 168, "sigma_H": 17, "source_label": 'Simon2005_CC'},
    {"row_id": 'SIMON2005_CC_ROW_007', "z": 1.43, "H_obs": 177, "sigma_H": 18, "source_label": 'Simon2005_CC'},
    {"row_id": 'SIMON2005_CC_ROW_008', "z": 1.53, "H_obs": 140, "sigma_H": 14, "source_label": 'Simon2005_CC'},
    {"row_id": 'SIMON2005_CC_ROW_009', "z": 1.75, "H_obs": 202, "sigma_H": 40, "source_label": 'Simon2005_CC'},
]
        _dti_next_cc_hz_excluded_summary_v1 = {'Moresco2016_BC03': 5, 'Moresco2016_combined': 1, 'Moresco2016_M11': 1, 'LeafMelia_compiled': 1}

        _dti_next_cc_hz_payload_v1 = None
        for _dti_next_cc_hz_key_v1 in (
            "explicit_target_model_background_Hz_grid_diagnostic_only",
            "dti_explicit_target_model_background_Hz_grid_diagnostic_only",
            "target_model_background_Hz_grid_diagnostic_only",
        ):
            if _dti_next_cc_hz_key_v1 in st.session_state:
                _dti_next_cc_hz_payload_v1 = st.session_state.get(_dti_next_cc_hz_key_v1)
                break

        _dti_next_cc_hz_status_v1 = "model_grid_unavailable"
        _dti_next_cc_hz_score_v1 = None
        _dti_next_cc_hz_used_v1 = []
        _dti_next_cc_hz_deferred_v1 = []

        if isinstance(_dti_next_cc_hz_payload_v1, dict):
            _dti_next_cc_hz_z_grid_v1 = _dti_next_cc_hz_payload_v1.get("z_bg")
            _dti_next_cc_hz_H_grid_v1 = _dti_next_cc_hz_payload_v1.get("H_model")

            if _dti_next_cc_hz_z_grid_v1 is not None and _dti_next_cc_hz_H_grid_v1 is not None:
                try:
                    import numpy as _dti_next_cc_hz_np_v1

                    _dti_next_cc_hz_z_arr_v1 = _dti_next_cc_hz_np_v1.asarray(_dti_next_cc_hz_z_grid_v1, dtype=float)
                    _dti_next_cc_hz_H_arr_v1 = _dti_next_cc_hz_np_v1.asarray(_dti_next_cc_hz_H_grid_v1, dtype=float)

                    _dti_next_cc_hz_grid_ok_v1 = (
                        _dti_next_cc_hz_z_arr_v1.ndim == 1
                        and _dti_next_cc_hz_H_arr_v1.ndim == 1
                        and len(_dti_next_cc_hz_z_arr_v1) == len(_dti_next_cc_hz_H_arr_v1)
                        and len(_dti_next_cc_hz_z_arr_v1) >= 2
                        and bool(_dti_next_cc_hz_np_v1.all(_dti_next_cc_hz_np_v1.isfinite(_dti_next_cc_hz_z_arr_v1)))
                        and bool(_dti_next_cc_hz_np_v1.all(_dti_next_cc_hz_np_v1.isfinite(_dti_next_cc_hz_H_arr_v1)))
                    )

                    if _dti_next_cc_hz_grid_ok_v1:
                        _dti_next_cc_hz_order_v1 = _dti_next_cc_hz_np_v1.argsort(_dti_next_cc_hz_z_arr_v1)
                        _dti_next_cc_hz_z_arr_v1 = _dti_next_cc_hz_z_arr_v1[_dti_next_cc_hz_order_v1]
                        _dti_next_cc_hz_H_arr_v1 = _dti_next_cc_hz_H_arr_v1[_dti_next_cc_hz_order_v1]

                        _dti_next_cc_hz_terms_v1 = []
                        for _dti_next_cc_hz_row_v1 in _dti_next_cc_hz_rows_v1:
                            _z_v1 = float(_dti_next_cc_hz_row_v1["z"])
                            _obs_v1 = float(_dti_next_cc_hz_row_v1["H_obs"])
                            _sig_v1 = float(_dti_next_cc_hz_row_v1["sigma_H"])

                            if _sig_v1 <= 0 or _z_v1 < float(_dti_next_cc_hz_z_arr_v1[0]) or _z_v1 > float(_dti_next_cc_hz_z_arr_v1[-1]):
                                _dti_next_cc_hz_deferred_v1.append(_dti_next_cc_hz_row_v1["row_id"])
                                continue

                            _model_v1 = float(_dti_next_cc_hz_np_v1.interp(_z_v1, _dti_next_cc_hz_z_arr_v1, _dti_next_cc_hz_H_arr_v1))
                            _term_v1 = ((_model_v1 - _obs_v1) / _sig_v1) ** 2
                            _dti_next_cc_hz_terms_v1.append(_term_v1)
                            _dti_next_cc_hz_used_v1.append(_dti_next_cc_hz_row_v1["row_id"])

                        if _dti_next_cc_hz_terms_v1:
                            _dti_next_cc_hz_score_v1 = float(sum(_dti_next_cc_hz_terms_v1))
                            _dti_next_cc_hz_status_v1 = "computed_from_runtime_Hz_grid_diagnostic_only"
                        else:
                            _dti_next_cc_hz_status_v1 = "no_locked_rows_inside_runtime_grid"

                except Exception as _dti_next_cc_hz_exc_v1:
                    _dti_next_cc_hz_status_v1 = f"guarded_unavailable: {type(_dti_next_cc_hz_exc_v1).__name__}"

        _dti_next_cc_hz_col1_v1, _dti_next_cc_hz_col2_v1, _dti_next_cc_hz_col3_v1 = st.columns(3)
        _dti_next_cc_hz_col1_v1.metric("N locked included", len(_dti_next_cc_hz_rows_v1))
        _dti_next_cc_hz_col2_v1.metric("N used", len(_dti_next_cc_hz_used_v1))
        _dti_next_cc_hz_col3_v1.metric("N excluded/deferred", 8 + len(_dti_next_cc_hz_deferred_v1))

        if _dti_next_cc_hz_score_v1 is None:
            st.info("Additional CC/H(z) diagnostic score unavailable: runtime H(z) model grid is not available or no locked rows fall inside the grid.")
        else:
            st.metric("Additional CC/H(z) chi2-like diagnostic score", f"{_dti_next_cc_hz_score_v1:.6g}")

        st.write("Status:", _dti_next_cc_hz_status_v1)
        st.write("Included source families: Zhang2014_CC; Simon2005_CC")
        st.write("Excluded/deferred source families:", _dti_next_cc_hz_excluded_summary_v1)

        with st.expander("Locked included CC/H(z) rows", expanded=False):
            st.dataframe(_dti_next_cc_hz_rows_v1, use_container_width=True)

        st.caption("Moresco2016 BC03 rows are not reused as new independent evidence. Backend disconnected; CLASS/AxiCLASS not run; MCMC not run.")
except Exception as _dti_next_cc_hz_panel_exc_v1:
    st.warning(f"Additional CC/H(z) diagnostic panel unavailable: {type(_dti_next_cc_hz_panel_exc_v1).__name__}")
# --- DTI_NEXT_CC_HZ_DIAGNOSTIC_PANEL_V1_END ---


# DTI_PROVENANCE_LEDGER_UI_V1_BEGIN
# Read-only provenance/freeze ledger panel.
try:
    with st.expander("Provenance / freeze ledger — source-locked, diagnostic-only", expanded=False):
        st.caption(
            "Read-only provenance ledger. This panel is diagnostic/provenance-only; "
            "it is not a likelihood evaluation, not a posterior comparison, not a fit, "
            "not validation, and not manuscript-level claim promotion."
        )

        st.markdown("**Current public source identity**")
        st.code(
            "commit = d6d2697f7a8191c60c689df09edf8eec31aebf83\n"
            "origin/main = d6d2697f7a8191c60c689df09edf8eec31aebf83\n"
            "app.py SHA256 = f8c0f6c1475fcf562f4d397243d466bd02400d25c7ed690ad456784a712f16e8\n"
            "app.py lines = 12625",
            language="text",
        )

        st.markdown("**Closed diagnostic lane**")
        st.code(
            "closed_lane = CC_HZ_ADDITIONAL_DIAGNOSTIC_LANE\n"
            "closed_lane_status = PUBLIC_VISUAL_PASS_FREEZE_V1_PASS\n"
            "safe_stop_point = YES\n"
            "freeze_zip_sha256 = 07a7156714281e80d018af07103677c936b12339b464295282af6d0d688302c1",
            language="text",
        )

        st.markdown("**Boundary**")
        st.write(
            "This public app remains a diagnostic and provenance viewer only. "
            "No live likelihood evaluation, posterior comparison, fit, validation, "
            "CLASS/AxiCLASS runtime result, MCMC result, Planck validation, DESI-fit validation, "
            "or manuscript-level claim promotion is performed here."
        )

        st.markdown("**No-reopen rule**")
        st.write(
            "Moresco2016 and the current CC/H(z) lane are closed unless a new, separate "
            "input-definition lock gate is created. Closed lanes are not reused as new "
            "independent evidence."
        )
except Exception as _dti_provenance_ledger_ui_v1_err:
    st.caption(f"Provenance ledger panel unavailable: {_dti_provenance_ledger_ui_v1_err}")
# DTI_PROVENANCE_LEDGER_UI_V1_END
