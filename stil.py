"""Arayüz stili."""
import streamlit as st

CSS = """
<style>
:root { --ink:#1d2b3d; --muted:#5b6b7e; --line:#dfe5ec; --navy:#1b3554; --blue:#315f96; }
.stApp { background:#f4f6f8; color:var(--ink); font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
.block-container { padding-top:1rem; max-width:1250px; }
h1,h2,h3 { color:#17263c; letter-spacing:-.025em; }
:focus-visible { outline:3px solid #3d78b5 !important; outline-offset:2px; }
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button { width:100%; border-radius:10px; font-weight:700; }
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] { background:var(--blue); border:0; color:#fff; }
.top-brand { display:flex; align-items:center; gap:.8rem; padding:.35rem 0 .6rem; }
.top-brand-name { font-weight:800; font-size:1.2rem; color:#172b46; }
.top-brand-sub { color:var(--muted); font-size:.78rem; }
.notice-bar { display:flex; align-items:center; gap:.55rem; padding:.6rem .85rem; margin:.4rem 0 .8rem; border:1px solid #dbe5ef; border-radius:11px; background:#fff; color:#4d5f75; font-size:.82rem; }
.notice-dot { width:8px; height:8px; flex-shrink:0; border-radius:50%; background:#3d78b5; }
.hero { padding:2rem 2rem; border-radius:16px; background:var(--navy); color:#fff; margin:.3rem 0 1.2rem; }
.hero h1 { color:#fff !important; margin:0 0 .5rem; font-size:clamp(1.8rem,4vw,2.5rem); }
.hero p { color:#e4efff; margin:0; max-width:720px; font-size:1.02rem; }
.eyebrow { text-transform:uppercase; letter-spacing:.14em; font-size:.72rem; font-weight:700; color:#bde9f3; margin-bottom:.6rem; }
.eyebrow-dark { color:#2d5f9a; font-size:.72rem; font-weight:800; letter-spacing:.14em; }
.page-heading h1 { margin:.1rem 0 .3rem; font-size:clamp(1.7rem,3vw,2.2rem); }
.page-heading p { margin:0; color:var(--muted); max-width:760px; }
.soft-card { background:#fff; border:1px solid var(--line); border-radius:16px; padding:1.1rem 1.2rem; height:100%; }
.soft-card h3 { margin:.1rem 0 .4rem; font-size:1.1rem; }
.soft-card p { color:var(--muted); margin:0; }
.emergency { border:1px solid #f0c9c4; background:#fff5f3; color:#7a2a20; border-radius:12px; padding:.7rem .9rem; font-size:.9rem; }
.emergency b { color:#a1281b; }
.record-banner { display:flex; align-items:center; justify-content:space-between; gap:1rem; padding:.8rem 1rem; margin-bottom:1rem; border:1px solid #e4eaf2; border-radius:14px; background:#f8fbff; }
.record-kicker { color:var(--muted); font-size:.68rem; font-weight:800; letter-spacing:.12em; }
.record-id { color:#17263c; font-size:1.2rem; font-weight:800; }
.pills { display:flex; gap:.4rem; flex-wrap:wrap; justify-content:flex-end; }
.pill { display:inline-block; border-radius:999px; padding:.3rem .7rem; font-size:.76rem; font-weight:800; white-space:nowrap; }
.status-waiting { color:#8a5700; background:#fff3d6; }
.status-active { color:#1d4ed8; background:#e4edff; }
.status-followup { color:#9a3412; background:#ffeadf; }
.status-done { color:#166534; background:#dcfce7; }
.prio-none { color:#475569; background:#eef2f6; }
.prio-low { color:#1d4ed8; background:#e4edff; }
.prio-mid { color:#8a5700; background:#fff3d6; }
.prio-high { color:#9a3412; background:#ffeadf; }
.prio-urgent { color:#fff; background:#b42318; }
.access-panel { padding:1.1rem; border:1px solid #dbe5f1; border-radius:14px; background:#fff; }
@media (max-width:700px) { .hero { padding:1.4rem 1.1rem; } }
[data-testid="stSidebar"] { background:#12263f; border-right:1px solid #0d1c30; }
[data-testid="stSidebar"] * { color:#dbe6f3; }
.nav-title { font-size:.66rem; font-weight:800; letter-spacing:.16em; color:#8fa6c2 !important; margin:1.1rem 0 .3rem; }
[data-testid="stSidebar"] .stButton > button { justify-content:flex-start; background:transparent; border:0; box-shadow:none; color:#dbe6f3; font-weight:600; padding:.45rem .7rem; border-radius:8px; margin-bottom:2px; }
[data-testid="stSidebar"] .stButton > button:hover { background:rgba(255,255,255,.09); }
[data-testid="stSidebar"] .stButton > button[kind="primary"] { background:#315f96; color:#fff; box-shadow:inset 3px 0 0 #8fc1ff; }
.topbar { display:flex; justify-content:space-between; align-items:center; padding:.2rem 0 .7rem; border-bottom:1px solid var(--line); margin-bottom:.8rem; }
.crumb { color:#5b6b7e; font-size:.88rem; }
.crumb span { margin:0 .35rem; color:#a8b4c2; }
.crumb b { color:#17263c; }
.daily-summary { background:linear-gradient(135deg, #eff7ff, #ffffff); border:1px solid #dfeaf9; border-radius:18px; padding:1rem 1.1rem; margin:0 0 1rem; }
.daily-summary h3 { margin:0 0 .75rem; }
.summary-grid { display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:0.8rem; }
.summary-grid div { background:#fff; border:1px solid #e3edf8; border-radius:12px; padding:.8rem .9rem; }
.summary-grid span { display:block; font-size:.72rem; color:var(--muted); margin-bottom:.35rem; }
.summary-grid strong { font-size:1.6rem; color:#17263c; }
@media (max-width:640px) {
  .summary-grid { grid-template-columns:1fr; }
  .block-container { padding:.6rem .8rem 3rem; }
  .hero { padding:1.2rem 1rem; }
  .record-banner { flex-direction:column; align-items:flex-start; }
  .pills { justify-content:flex-start; }
  .topbar { flex-direction:column; align-items:flex-start; gap:.4rem; }
}
.durum-not { color:var(--muted); font-size:.92rem; margin:.2rem 0 1rem; }
"""


def uygula() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
