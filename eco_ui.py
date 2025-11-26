# eco_ui.py — Royal Premium Dashboard Edition (Updated With Themed Insights Chart + Floating Tabs)

import streamlit as st
import requests
import json
import altair as alt
import pandas as pd
from typing import List, Dict
from datetime import datetime
import streamlit.components.v1 as components
from eco_insights_utils import (
    get_impact_counts_from_api,
    compute_weighted_risk,
    render_multi_ring_svg,
    render_progress_gauge,     # ← THIS ONE WAS MISSING
    bar_chart_counts,
    donut_chart,
    THEME
)



API_BASE = "http://127.0.0.1:8000"


# ------------------------------------------------------
#                  PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="ECO AI Assistant",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------------------------------
#            ROYAL PREMIUM DARK THEME CSS
# ------------------------------------------------------
st.markdown("""
<style>

    /* Global background */
    .stApp {
        background: linear-gradient(180deg, #0a0c12 0%, #05070a 100%) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0d1017 !important;
        border-right: 1px solid rgba(212,175,55,0.18) !important;
        padding-top: 20px;
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span {
        color: #D4AF37 !important;
        font-size: 15px !important;
    }
    [data-testid="stSidebar"] .css-1d391kg:hover {
        color: #f6d46e !important;
        text-shadow: 0px 0px 6px rgba(212,175,55,0.6);
    }

    /* Main Header */
    .header-title {
        font-size: 40px;
        font-weight: 900;
        color: #D4AF37;
        text-shadow: 0px 0px 12px rgba(212,175,55,0.45);
        animation: fadein 1.2s ease-out;
        letter-spacing: 1px;
    }
    .header-sub {
        margin-top: -10px;
        font-size: 15px;
        color: #8C93A1;
    }

    /* KPI Cards */
    .kpi-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(212,175,55,0.25);
        backdrop-filter: blur(8px);
        border-radius: 14px;
        padding: 22px;
        transition: 0.25s ease;
    }
    .kpi-card:hover {
        border-color: rgba(212,175,55,0.60);
        transform: translateY(-4px);
        box-shadow: 0px 0px 12px rgba(212,175,55,0.35);
    }
    .kpi-title {
        font-size: 13px;
        color: #D4AF37;
        font-weight: 700;
    }
    .kpi-value {
        font-size: 30px;
        font-weight: 800;
        color: #FFFFFF;
        margin-top: -6px;
    }

    /* Card Container */
    .card {
        background: rgba(255,255,255,0.04);
        border-radius: 16px;
        padding: 25px;
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(6px);
        transition: 0.28s ease;
        margin-bottom: 22px;
    }
    .card:hover {
        border: 1px solid rgba(212,175,55,0.45);
        box-shadow: 0px 0px 20px rgba(212,175,55,0.20);
        transform: translateY(-5px);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #D4AF37 0%, #b8922c 100%);
        border-radius: 12px;
        padding: 10px 20px;
        border: none;
        font-size: 15px;
        font-weight: 700;
        transition: 0.25s;
        color: #000 !important;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #f4d98c 0%, #d0a747 100%);
        transform: translateY(-3px);
        box-shadow: 0px 0px 12px rgba(212,175,55,0.40);
    }

    /* File Upload */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(255,255,255,0.03);
        border: 2px dashed #D4AF37;
        border-radius: 14px;
    }

    /* Floating Glass Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 18px !important;
        padding: 8px !important;
        margin-bottom: 18px !important;
        border-bottom: none !important;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(12px);
        padding: 10px 20px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.08);
        color: #dcdcdc !important;
        font-size: 15px !important;
        transition: all 0.25s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #D4AF37 !important;
        border-color: rgba(212,175,55,0.45);
        transform: translateY(-3px);
        box-shadow: 0px 0px 8px rgba(212,175,55,0.25);
    }

    .stTabs [aria-selected="true"] {
        color: #D4AF37 !important;
        background: rgba(212,175,55,0.08) !important;
        border: 1px solid rgba(212,175,55,0.45) !important;
        box-shadow: 0px 0px 16px rgba(212,175,55,0.35);
        font-weight: 800 !important;
        transform: translateY(-3px);
    }

</style>
""", unsafe_allow_html=True)



# ------------------------------------------------------
#                      HEADER
# ------------------------------------------------------
st.markdown("""
<div class="header-title">
    ECO AI Assistant
</div>
<div class="header-sub">
    Royal Premium ECO Intelligence Dashboard
</div>
<br>
""", unsafe_allow_html=True)



# ------------------------------------------------------
#                      KPI ROW
# ------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown('<div class="kpi-title">Total ECOs Processed</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-value">128</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown('<div class="kpi-title">High Impact Items</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-value">42</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown('<div class="kpi-title">Pending Updates</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-value">17</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown('<div class="kpi-title">Total Attachments</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-value">63</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)



# ------------------------------------------------------
#                      TABS
# ------------------------------------------------------
tabs = st.tabs(["Summary", "Impact", "Teamcenter", "Attachments", "Insights"])



# ========================== TAB 1 ==========================
with tabs[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("ECO Summarizer")

    eco_id = st.text_input("Enter ECO ID", "1001")

    if st.button("Generate Summary"):
        r = requests.get(f"{API_BASE}/eco/{eco_id}/summarize")
        try:
            d = r.json()
            st.success("Summary Generated Successfully")
            st.write(d.get("summary", "No summary returned"))
        except:
            st.error("Invalid response from server.")

    st.markdown('</div>', unsafe_allow_html=True)



# ========================== TAB 2 ==========================
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Impact Analysis")

    eco_id2 = st.text_input("ECO ID for Impact", "1001")

    if st.button("Run Impact Analysis"):
        r = requests.get(f"{API_BASE}/eco/{eco_id2}/impact")
        try:
            d = r.json()
            st.success("Impact Analysis Retrieved")
            st.write(d.get("impact_analysis", "No analysis returned"))
        except:
            st.error("Invalid response from server.")

    st.markdown('</div>', unsafe_allow_html=True)



# ========================== TAB 3 ==========================
with tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Teamcenter Operations")

    left, right = st.columns([1.3, 1])

    with left:
        tc_action = st.radio("Select Action", [
            "Create ECO",
            "Get ECO Details",
            "Update ECO Status",
            "Add Impacted Item",
            "Remove Impacted Item"
        ])

        # -------------------- CREATE ECO (Premium UI) --------------------
        if tc_action == "Create ECO":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Create New ECO")

            tc_title = st.text_input("ECO Title", placeholder="Enter ECO title…")
            tc_desc = st.text_area("ECO Description", placeholder="Describe the engineering change…")

            if st.button("Create ECO", key="create_eco_btn"):
                if not tc_title.strip():
                    st.error("ECO Title cannot be empty.")
                else:
                    payload = {
                        "clientId": "UI_ECO_CREATE",
                        "className": "ChangeNoticeRevision",
                        "properties": {
                            "object_name": tc_title,
                            "object_desc": tc_desc
                        }
                    }

                    with st.spinner("Creating ECO…"):
                        response = requests.post(f"{API_BASE}/tc/eco/create", json=payload)

                    try:
                        out = response.json()
                        st.session_state["log"] = out
        
                        eco_uid = out.get("eco_uid") or out.get("uid") or out.get("id")

                        st.success(f"🎉 ECO Created Successfully! UID: {eco_uid}")
                        st.json(out)

                    except Exception:
                        st.error("❌ Server returned unexpected response:")
                        st.code(response.text)

            st.markdown('</div>', unsafe_allow_html=True)


        elif tc_action == "Get ECO Details":
            uid = st.text_input("ECO UID")
            if st.button("Fetch"):
                r = requests.get(f"{API_BASE}/tc/eco/{uid}")
                st.session_state["log"] = r.json()

        elif tc_action == "Update ECO Status":
            uid = st.text_input("ECO UID")
            act = st.selectbox("Action", ["Promote", "Demote"])
            if st.button("Update"):
                r = requests.post(f"{API_BASE}/tc/eco/{uid}/status", params={"action": act})
                st.session_state["log"] = r.json()

        elif tc_action == "Add Impacted Item":
            uid = st.text_input("ECO UID")
            item = st.text_input("Item UID")
            if st.button("Add"):
                r = requests.post(f"{API_BASE}/tc/eco/{uid}/add_item/{item}")
                st.session_state["log"] = r.json()

        elif tc_action == "Remove Impacted Item":
            uid = st.text_input("ECO UID")
            item = st.text_input("Item UID")
            if st.button("Remove"):
                r = requests.post(f"{API_BASE}/tc/eco/{uid}/remove_item/{item}")
                st.session_state["log"] = r.json()

    with right:
        st.markdown("### Live Response / Logs")
        if "log" in st.session_state:
            st.json(st.session_state["log"])
        else:
            st.info("No actions yet.")

    st.markdown('</div>', unsafe_allow_html=True)



# ========================== TAB 4 ==========================
with tabs[3]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Attach Files")

    eco_uid = st.text_input("ECO UID")
    file = st.file_uploader("Upload File")

    if st.button("Upload"):
        if eco_uid and file:
            st.success("Uploaded successfully (mock).")
        else:
            st.error("ECO UID and file required.")

    st.markdown('</div>', unsafe_allow_html=True)



# ========================== TAB 5 ==========================
with tabs[4]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Insights & Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-muted">Impact distribution and executive risk gauges</div>', unsafe_allow_html=True)
    st.markdown('<br/>', unsafe_allow_html=True)

    # ---------------- FETCH COUNTS ----------------
    eco_uid = st.text_input("ECO UID for insights (leave empty for sample)", value="")
    counts = get_impact_counts_from_api(eco_uid if eco_uid.strip() else None)

    df_counts = pd.DataFrame([
        {"impact": "High", "count": counts.get("High", 0)},
        {"impact": "Medium", "count": counts.get("Medium", 0)},
        {"impact": "Low", "count": counts.get("Low", 0)}
    ])

    # ---------------- WEIGHTED RISK SCORE ----------------
    overall_score = compute_weighted_risk(counts)

    # ---------------- LAYOUT: LEFT (SVGs) + RIGHT (Altair charts) ----------------
    left_col, right_col = st.columns([1, 1.3])

    # ---------------- LEFT: MULTI-RING GAUGE + PROGRESS GAUGE ----------------
    with left_col:
        st.markdown("### Impact Rings")
        svg_multi = render_multi_ring_svg(counts, size=360, stroke_widths=(20, 18, 16))
        components.html(svg_multi, height=380)

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("### Overall Risk")
        svg_prog = render_progress_gauge(overall_score, size=220)
        components.html(svg_prog, height=230)

    # ---------------- RIGHT: BAR + DONUT ----------------
    with right_col:
        st.markdown("### Distribution & Breakdown")
        c1, c2 = st.columns([1, 0.9])

        with c1:
            bar = bar_chart_counts(df_counts)
            st.altair_chart(bar, use_container_width=True)

        with c2:
            donut = donut_chart(df_counts)
            st.altair_chart(donut, use_container_width=True)

        # ---------------- LEGEND ----------------
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("<div style='display:flex; gap:12px; align-items:center;'>", unsafe_allow_html=True)

        for k, col in [("High", THEME["gold"]), ("Medium", THEME["gold_deep"]), ("Low", THEME["muted"])]:
            st.markdown(
                f"""
                <div style='display:flex; gap:8px; align-items:center;'>
                    <div style='width:12px;height:12px;border-radius:4px;
                                background:{col};box-shadow:0 0 8px {col};'></div>
                    <div style='color:{THEME['text']}; font-weight:700'>{k}</div>
                    <div style='color:{THEME['muted']}; margin-left:6px'>{counts.get(k,0)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)



# ------------------------------------------------------
#                       FOOTER
# ------------------------------------------------------
st.markdown("""
<br>
<center>
<span style="color:#666; font-size:12px;">
ECO AI Assistant — Royal Premium Dashboard © 2025
</span>
</center>
""", unsafe_allow_html=True)
