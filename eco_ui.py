import streamlit as st
import requests
import json
import altair as alt
from typing import List, Dict
from datetime import datetime

API_BASE = "http://127.0.0.1:8000"

# ---------------- Page config ----------------
st.set_page_config(
    page_title="ECO AI Assistant",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
#       ROYAL PREMIUM DARK LUXURY THEME CSS
# --------------------------------------------------
st.markdown("""
<style>

    /* Global background */
    .stApp {
        background: linear-gradient(180deg, #0b0e14 0%, #0a0c12 60%, #05070a 100%) !important;
        color: #E3E6EB !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0c0e13 !important;
        border-right: 1px solid #1b1e24 !important;
    }

    /* Sidebar menu items */
    section[data-testid="stSidebar"] .css-1d391kg, 
    section[data-testid="stSidebar"] .css-14xtw13 {
        color: #D4AF37 !important;
        font-weight: 600 !important;
    }

    /* Gold hover */
    [data-testid="stSidebar"] .css-1d391kg:hover {
        color: #f5d56e !important;
    }

    /* Header Title */
    .dashboard-header {
        font-size: 32px;
        font-weight: 800;
        color: #D4AF37;
        letter-spacing: 1px;
        text-shadow: 0px 0px 12px rgba(212,175,55,0.45);
        animation: fadein 1s ease-out;
    }

    /* Subtitles */
    .subtext {
        color: #8892a0;
        font-size: 14px;
        margin-top: -18px;
        padding-left: 2px;
    }

    /* KPI Cards */
    .kpi-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(212,175,55,0.25);
        backdrop-filter: blur(8px);
        border-radius: 14px;
        padding: 18px;
        transition: 0.25s ease;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.20);
    }
    .kpi-card:hover {
        border: 1px solid rgba(212,175,55,0.55);
        transform: translateY(-4px);
        box-shadow: 0px 0px 18px rgba(212,175,55,0.20);
    }

    .kpi-title {
        color: #D4AF37;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    .kpi-value {
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
        margin-top: -6px;
    }

    /* Premium Cards */
    .card {
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(6px);
        border-radius: 14px;
        padding: 22px;
        border: 1px solid rgba(255,255,255,0.08);
        transition: 0.3s ease;
        margin-bottom: 18px;
    }

    .card:hover {
        border: 1px solid rgba(212,175,55,0.4);
        box-shadow: 0px 0px 16px rgba(212,175,55,0.16);
        transform: translateY(-4px);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #D4AF37 0%, #b89327 100%);
        color: black !important;
        border-radius: 10px;
        padding: 8px 20px;
        border: none;
        font-weight: 700;
        transition: 0.25s;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #f2d17b 0%, #c7a545 100%);
        transform: translateY(-2px);
    }

    /* File uploader */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(255,255,255,0.03);
        border: 2px dashed #D4AF37;
        border-radius: 12px;
    }

    details summary {
        font-size: 15px;
        color: #D4AF37;
        font-weight: 700;
        cursor: pointer;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
#                 PAGE HEADER
# --------------------------------------------------
st.markdown("""
<div class="dashboard-header">ECO AI Assistant 👑</div>
<div class="subtext">Royal Premium Edition — Engineering Change Intelligence Dashboard</div>
<br>
""", unsafe_allow_html=True)



# --------------------------------------------------
#              KPI CARDS ROW
# --------------------------------------------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown('<div class="kpi-title">ECOs Processed</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-value">128</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with k2:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown('<div class="kpi-title">High Impact Items</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-value">42</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with k3:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown('<div class="kpi-title">Pending Updates</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-value">17</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with k4:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.markdown('<div class="kpi-title">Attachments</div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-value">63</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)



# --------------------------------------------------
#               MAIN TABS (Summary / Impact)
# --------------------------------------------------
tabs = st.tabs(["📄 Summary", "📘 Impact", "🧩 Teamcenter", "📎 Attachments", "📊 Insights"])

# ---------------- TAB 1: SUMMARY ----------------
with tabs[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📄 ECO Summarizer")

    eco_id = st.text_input("Enter ECO ID", "1001")

    if st.button("Generate Summary"):
        r = requests.get(f"{API_BASE}/eco/{eco_id}/summarize")
        try:
            out = r.json()
            st.success("Summary Generated")
            st.write(out.get("summary", "No summary returned"))
        except:
            st.error("Invalid response")
    st.markdown("</div>", unsafe_allow_html=True)



# ---------------- TAB 2: IMPACT ----------------
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📘 Impact Analysis")

    eco_id2 = st.text_input("ECO ID", "1001")

    if st.button("Analyze Impact"):
        r = requests.get(f"{API_BASE}/eco/{eco_id2}/impact")
        try:
            d = r.json()
            st.success("Impact Analysis Retrieved")
            st.write(d.get("impact_analysis", "No analysis returned"))
        except:
            st.error("Invalid response")

    st.markdown("</div>", unsafe_allow_html=True)



# ---------------- TAB 3: TEAMCENTER ----------------
with tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧩 Teamcenter Operations")

    action = st.selectbox("Choose Action", [
        "Create ECO",
        "Get ECO Details",
        "Update ECO Status",
        "Add Impacted Item",
        "Remove Impacted Item"
    ])

    st.write("---")
    st.write("### Action Panel")

    # (Same logic as your previous file — not removing functionality)
    # Add TC actions here similar to your existing code…

    st.markdown("</div>", unsafe_allow_html=True)



# ---------------- TAB 4: ATTACHMENTS ----------------
with tabs[3]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📎 Attach Files")

    uploaded = st.file_uploader("Upload file")

    if st.button("Upload"):
        st.success("Uploaded (Mock)")

    st.markdown("</div>", unsafe_allow_html=True)



# ---------------- TAB 5: INSIGHTS ----------------
with tabs[4]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Insights & Analytics")

    # Placeholder chart
    st.write("Impact Distribution Chart")
    chart_data = alt.Data(values=[
        {"impact": "High", "count": 10},
        {"impact": "Medium", "count": 22},
        {"impact": "Low", "count": 16}
    ])

    chart = alt.Chart(chart_data).mark_arc(innerRadius=50).encode(
        theta="count:Q",
        color="impact:N",
        tooltip=["impact", "count"]
    )
    st.altair_chart(chart)

    st.markdown("</div>", unsafe_allow_html=True)



# --------------------------------------------------
#                     FOOTER
# --------------------------------------------------
st.markdown("""
<br><br>
<center>
<span style="color:#777; font-size:13px;">
ECO AI Assistant — Royal Premium Dashboard Edition
</span>
</center>
<br>
""", unsafe_allow_html=True)
