from __future__ import annotations

import streamlit as st

CSS = """
<style>
.main .block-container { padding-top: 1.4rem; }
.hero {
  border: 1px solid rgba(148, 163, 184, 0.25);
  border-radius: 18px;
  padding: 30px;
  background:
    linear-gradient(135deg, rgba(34,197,94,.13), rgba(59,130,246,.08)),
    radial-gradient(circle at 88% 18%, rgba(244,114,182,.18), transparent 32%);
  margin-bottom: 1.3rem;
}
.hero h1 { font-size: 2.3rem; line-height: 1.08; margin-bottom: .8rem; }
.hero p { color: #cbd5e1; font-size: 1.02rem; max-width: 980px; }
.tag-row { display: flex; flex-wrap: wrap; gap: .45rem; margin-top: 1rem; }
.tag-row span {
  border: 1px solid rgba(34,197,94,.28);
  color: #bbf7d0;
  border-radius: 999px;
  padding: .28rem .68rem;
  font-size: .78rem;
  font-weight: 700;
  background: rgba(34,197,94,.08);
}
.metric-card {
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 12px;
  padding: 1rem;
  background: rgba(15, 23, 42, .56);
  min-height: 145px;
}
.metric-card span {
  color: #93c5fd;
  text-transform: uppercase;
  font-size: .72rem;
  letter-spacing: .08em;
  font-weight: 800;
}
.metric-card strong { display: block; color: #f8fafc; font-size: 1.35rem; margin: .25rem 0; }
.metric-card p { color: #cbd5e1; font-size: .86rem; margin: 0; }
.script-box {
  border-left: 4px solid #22c55e;
  background: rgba(34,197,94,.08);
  padding: 1rem 1.1rem;
  border-radius: 10px;
  color: #e2e8f0;
  line-height: 1.7;
}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def metric_card(label: str, value: str, help_text: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
          <span>{label}</span>
          <strong>{value}</strong>
          <p>{help_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
