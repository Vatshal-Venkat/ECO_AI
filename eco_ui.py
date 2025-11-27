# eco_ui.py — Royal Premium Dashboard Edition (Optimized & Patched)

import streamlit as st
import requests
import json
import altair as alt
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

from eco_insights_utils import (
    get_impact_counts_from_api,
    compute_weighted_risk,
    render_multi_ring_svg,
    render_progress_gauge,
    bar_chart_counts,
    donut_chart,
    THEME
)

API_BASE = "http://127.0.0.1:8000"


# --------------------------------------
# Load external CSS
# --------------------------------------
with open("eco_ui.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --------------------------------------
# Page Config
# --------------------------------------
st.set_page_config(
    page_title="ECO AI Assistant",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------
# Header
# --------------------------------------
st.markdown("""
<div class="header-title">ECO AI Assistant</div>
<div class="header-sub">Royal Premium ECO Intelligence Dashboard</div>
<br>
""", unsafe_allow_html=True)


# --------------------------------------
# KPI Row
# --------------------------------------
c1, c2, c3, c4 = st.columns(4)
kpi_data = [
    ("Total ECOs Processed", "128"),
    ("High Impact Items", "42"),
    ("Pending Updates", "17"),
    ("Total Attachments", "63"),
]

for col, (title, value) in zip([c1, c2, c3, c4], kpi_data):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)


# --------------------------------------
# Tabs
# --------------------------------------
tabs = st.tabs([
    "Summary",
    "Impact",
    "Teamcenter",
    "Attachments",
    "Insights",
    "ECO List"
])


# --------------------------------------
# TAB 1 — Summary
# --------------------------------------
with tabs[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("ECO Summarizer")

    eco_id = st.text_input("Enter ECO ID", "1001", key="summary_eco_id")

    if st.button("Generate Summary", key="summary_btn"):
        r = requests.get(f"{API_BASE}/eco/{eco_id}/summarize")
        try:
            d = r.json()
            st.success("Summary Generated Successfully")
            st.write(d.get("summary", "No summary returned"))
        except:
            st.error("Invalid response from server.")

    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------
# TAB 2 — Impact
# --------------------------------------
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Impact Analysis")

    eco_id2 = st.text_input("ECO ID for Impact", "1001", key="impact_eco_id")

    if st.button("Run Impact Analysis", key="impact_btn"):
        r = requests.get(f"{API_BASE}/eco/{eco_id2}/impact")
        try:
            d = r.json()
            st.success("Impact Analysis Retrieved")
            st.write(d.get("impact_analysis", "No analysis returned"))
        except:
            st.error("Invalid response from server.")

    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------
# TAB 3 — Teamcenter Operations
# --------------------------------------
with tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Teamcenter Operations")

    left, right = st.columns([1.3, 1])

    with left:
        tc_action = st.radio(
            "Select Action",
            ["Create ECO", "Get ECO Details", "Update ECO Status", "Add Impacted Item", "Remove Impacted Item"],
            key="tc_action"
        )

        # -------------------- CREATE ECO --------------------
        if tc_action == "Create ECO":
            st.subheader("Create New ECO")

            tc_title = st.text_input("ECO Title", key="tc_title")
            tc_desc = st.text_area("ECO Description", key="tc_desc")

            if st.button("Create ECO", key="tc_create_btn"):
                payload = {
                    "clientId": "UI_ECO_CREATE",
                    "className": "ChangeNoticeRevision",
                    "properties": {
                        "object_name": tc_title,
                        "object_desc": tc_desc
                    }
                }

                r = requests.post(f"{API_BASE}/tc/eco/create", json=payload)
                try:
                    out = r.json()
                    st.session_state["log"] = out
                    eco_uid = out.get("eco_uid")
                    st.success(f"ECO Created Successfully: {eco_uid}")
                    st.json(out)
                except:
                    st.error("Error processing response")
                    st.code(r.text)

        # -------------------- GET DETAILS --------------------
        elif tc_action == "Get ECO Details":
            uid = st.text_input("ECO UID", key="tc_get_uid")

            if st.button("Fetch Details", key="fetch_tc_details"):
                r = requests.get(f"{API_BASE}/tc/eco/{uid}")
                st.session_state["log"] = r.json()

        # -------------------- UPDATE STATUS --------------------
        elif tc_action == "Update ECO Status":
            uid = st.text_input("ECO UID", key="tc_update_uid")
            act = st.selectbox("Action", ["Promote", "Demote"], key="tc_update_action")

            if st.button("Update Status", key="update_status_btn"):
                r = requests.post(f"{API_BASE}/tc/eco/{uid}/status", params={"action": act})
                st.session_state["log"] = r.json()

        # -------------------- ADD ITEM --------------------
        elif tc_action == "Add Impacted Item":
            uid = st.text_input("ECO UID", key="tc_add_uid")
            item = st.text_input("Item UID", key="tc_add_item_uid")

            if st.button("Add Item", key="tc_add_item_btn"):
                r = requests.post(f"{API_BASE}/tc/eco/{uid}/add_item/{item}")
                st.session_state["log"] = r.json()

        # -------------------- REMOVE ITEM --------------------
        elif tc_action == "Remove Impacted Item":
            uid = st.text_input("ECO UID", key="tc_remove_uid")
            item = st.text_input("Item UID", key="tc_remove_item_uid")

            if st.button("Remove Item", key="tc_remove_item_btn"):
                r = requests.post(f"{API_BASE}/tc/eco/{uid}/remove_item/{item}")
                st.session_state["log"] = r.json()

    # RIGHT COLUMN LOG VIEW
    with right:
        st.subheader("Live Response / Logs")

        log = st.session_state.get("log")

        if isinstance(log, dict):
            st.json(log)
        else:
            st.info("No actions yet.")

    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------
# TAB 4 — Attachments
# --------------------------------------
with tabs[3]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Attach Files")

    eco_uid = st.text_input("ECO UID", key="attach_eco_uid")
    file = st.file_uploader("Upload File", key="attach_file")

    if st.button("Upload", key="attach_btn"):
        if eco_uid and file:
            st.success("Uploaded successfully (mock).")
        else:
            st.error("ECO UID + File required.")

    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------
# TAB 5 — Insights
# --------------------------------------
with tabs[4]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Insights & Analytics")
    st.markdown('<br/>', unsafe_allow_html=True)

    eco_uid_insight = st.text_input("ECO UID for insights", key="insights_uid")

    counts = get_impact_counts_from_api(eco_uid_insight or None)

    df_counts = pd.DataFrame([
        {"impact": "High", "count": counts.get("High", 0) if isinstance(counts, dict) else 0},
        {"impact": "Medium", "count": counts.get("Medium", 0)},
        {"impact": "Low", "count": counts.get("Low", 0)},
    ])

    overall_score = compute_weighted_risk(counts)

    left_col, right_col = st.columns([1, 1.3])

    with left_col:
        st.markdown("### Impact Rings")
        components.html(render_multi_ring_svg(counts), height=380)

        st.markdown("### Overall Risk")
        components.html(render_progress_gauge(overall_score), height=230)

    with right_col:
        st.markdown("### Distribution & Breakdown")
        st.altair_chart(bar_chart_counts(df_counts), use_container_width=True)
        st.altair_chart(donut_chart(df_counts), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------
# TAB 6 — ECO LIST
# --------------------------------------
with tabs[5]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📘 ECO Database")

    search_query = st.text_input("Search ECO by ID", key="search_eco")

    try:
        ecos = requests.get(f"{API_BASE}/tc/eco/all").json()
    except:
        ecos = []

    if not isinstance(ecos, list):
        st.error("Invalid backend response")
        st.stop()

    # filter
    if search_query.strip():
        ecos = [e for e in ecos if isinstance(e, dict) and search_query.lower() in e.get("eco_uid", "").lower()]

    st.success(f"{len(ecos)} ECO(s) found")

    for eco in ecos:
        status = eco.get("status", "Created")

        color = (
            "#10B981" if "Promoted" in status else
            "#F59E0B" if "Demoted" in status else
            "#3B82F6"
        )

        with st.expander(f"🔧 {eco.get('eco_uid')} — {eco.get('title')}"):
            st.markdown(
                f"<span style='background:{color};padding:4px 10px;border-radius:8px;"
                f"color:white;font-weight:700;font-size:12px;'>{status}</span>",
                unsafe_allow_html=True
            )

            st.write(f"**Revision:** {eco.get('revision')}")
            st.write(f"**Creator:** {eco.get('creator')}")
            st.write(f"**Created At:** {eco.get('created_at')}")
            st.write(f"**Updated At:** {eco.get('updated_at')}")
            st.write(f"**Description:** {eco.get('description')}")

            items = eco.get("impacted_items", [])
            if items:
                st.markdown("### Impacted Items")
                st.table(items)
            else:
                st.info("No impacted items.")

    st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------
# Footer
# --------------------------------------
st.markdown("""
<br>
<center><span style="color:#666; font-size:12px;">
ECO AI Assistant — ECO Dashboard © 2025
</span></center>
""", unsafe_allow_html=True)
