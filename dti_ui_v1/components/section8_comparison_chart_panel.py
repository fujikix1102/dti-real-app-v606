import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

def render_section8_comparison_chart(source_path: str):
    st.subheader("Section 8: Primary Comparison Graph")

    p = Path(source_path)
    if not p.exists():
        st.error(f"Source data not found: {source_path}")
        return

    try:
        df = pd.read_csv(p, sep="\t")

        # グラフ描画のための明示的な型キャスト（数値演算エラー防止）
        df['delta_value'] = pd.to_numeric(df['delta_value'], errors='coerce').fillna(0.0)
        df['x_label'] = df['x_label'].astype(str)

        # Altairによる安全な静的グラフ生成
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('x_label:N', title='Parameter / Metric (x_label)', sort='-y'),
            y=alt.Y('delta_value:Q', title='Delta Value'),
            color=alt.Color('source_id:N', legend=alt.Legend(title="Source ID")),
            tooltip=['source_id', 'x_label', 'baseline_value', 'candidate_value', 'delta_value']
        ).properties(
            height=400
        ).interactive()

        st.altair_chart(chart, use_container_width=True)

        with st.expander("Raw Diagnostic Data (Schema Hardened)", expanded=False):
            # [ROUTE A HARDENING] プレビューテーブルのPyArrowクラッシュを防止
            safe_df = df.astype(str)
            st.dataframe(safe_df, hide_index=True, use_container_width=True)

        st.caption(
            "Diagnostic comparison view only. "
            "No likelihood, posterior, MCMC, or physical inference execution."
        )

    except Exception as exc:
        st.error("Failed to render Section 8 chart: " + str(exc))
