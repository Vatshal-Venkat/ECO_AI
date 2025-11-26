# eco_ui.py — Royal Premium Dashboard Edition (Final With Floating Glass Tabs + Chart Fix)

import streamlit as st
import requests
import json
import altair as alt
import pandas as pd
from typing import List, Dict
from datetime import datetime

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


    /* FILE UPLOADER */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(255,255,255,0.03);
        border: 2px dashed #D4AF37;
        border-radius: 14px;
    }


    /* -------------------------------------------------- */
    /*         FLOATING GLASS TABS (Royal Premium)        */
    /* -------------------------------------------------- */

    .stTabs [data-baseweb="tab-list"] {
        gap: 18px !important;
        padding: 8px !important;
        margin-bottom: 18px !important;
        justify-content: flex-start !important;
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
        font-weight: 500 !important;
        transition: all 0.25s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #D4AF37 !important;
        border-color: rgba(212,175,55,0.45);
        box-shadow: 0px 0px 8px rgba(212,175,55,0.25);
        transform: translateY(-3px);
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
    Teamcenter ECO Intelligence Dashboard 
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

        if tc_action == "Create ECO":
            title = st.text_input("ECO Title")
            desc = st.text_area("ECO Description")
            if st.button("Create"):
                r = requests.post(
                    f"{API_BASE}/tc/eco/create",
                    json={
                        "clientId": "UI_ECO_CREATE",
                        "className": "ChangeNoticeRevision",
                        "properties": {"object_name": title, "object_desc": desc}
                    }
                )
                st.session_state["log"] = r.json()

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
    st.subheader("Insights & Analytics")

    df = pd.DataFrame([
        {"impact": "High", "count": 12},
        {"impact": "Medium", "count": 21},
        {"impact": "Low", "count": 8}
    ])

    chart = (
        alt.Chart(df)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta("count:Q"),
            color=alt.Color("impact:N"),
            tooltip=["impact", "count"]
        )
        .properties(width=360, height=360)
    )

    st.altair_chart(chart, use_container_width=False)

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
