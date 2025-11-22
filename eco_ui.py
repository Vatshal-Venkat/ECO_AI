# eco_ui.py (Enhanced Enterprise UI)
import streamlit as st
import requests
import re
import json
import altair as alt
from typing import List, Dict
from datetime import datetime

API_BASE = "http://127.0.0.1:8000"

# ---------------- Page config ----------------
st.set_page_config(
    page_title="ECO AI Assistant",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="auto"
)

# ---------------- Custom CSS ----------------
_CUSTOM_CSS = """
<style>
/* Page background & card styling */
[data-testid="stAppViewContainer"] {
  background: linear-gradient(180deg, #f7f9fc 0%, #ffffff 100%);
}
.card {
  border-radius: 12px;
  background: #ffffff;
  padding: 18px;
  box-shadow: 0 6px 18px rgba(15,23,42,0.06);
  margin-bottom: 16px;
}
.header {
  display: flex;
  align-items: center;
  gap: 12px;
}
.app-title {
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
}
.subtitle {
  color: #475569;
  margin-top: -6px;
  font-size: 13px;
}

/* small badges */
.badge {
  display:inline-block;
  padding:6px 10px;
  border-radius:999px;
  font-size:12px;
  font-weight:700;
  color: #fff;
}
.badge-high { background:#ef4444; }
.badge-medium { background:#f59e0b; }
.badge-low { background:#10b981; }

/* small utility */
.kv { color:#475569; font-weight:600; }
.small { font-size:13px; color:#6b7280; }

/* hover effect for cards */
.card:hover { transform: translateY(-3px); transition: .18s ease; }

/* details tag styling when unsafe_allow_html true */
details summary { cursor: pointer; font-weight:700; padding:6px 0; }
</style>
"""
st.markdown(_CUSTOM_CSS, unsafe_allow_html=True)

# ---------------- Header ----------------
col_a, col_b = st.columns([0.9, 0.1])
with col_a:
    st.markdown("""
    <div class="header">
      <div style="font-size:28px">🔧 <span class="app-title">ECO AI Assistant</span></div>
      <div style="margin-left:8px" class="subtitle">Teamcenter PoC — Enhanced Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
with col_b:
    if st.button("Refresh UI", use_container_width=True):
        st.experimental_rerun()

st.markdown("---")

# ---------------- Utilities ----------------
def safe_json(response):
    """Return response.json() if possible; otherwise return dict with raw_response."""
    try:
        return response.json()
    except Exception:
        return {"raw_response": response.text}

def pretty_print_json(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False)

def badge_html(level: str) -> str:
    lvl = (level or "").strip().lower()
    if "high" in lvl:
        cls = "badge-high"
        text = "HIGH"
    elif "medium" in lvl:
        cls = "badge-medium"
        text = "MEDIUM"
    else:
        cls = "badge-low"
        text = "LOW"
    return f'<span class="badge {cls}">{text}</span>'

def parse_impacted_items_from_eco_details(details: Dict) -> List[Dict]:
    """
    Try to extract impacted items list from ECO GET response.
    Normalized to a list of {item, impact}.
    """
    if not details:
        return []
    # common key names used in our mock: impacted_items (list of dicts)
    items = details.get("impacted_items") or details.get("impactedItems") or details.get("impacted_items_list")
    if not items:
        # sometimes it's a list of strings
        return []
    normalized = []
    for it in items:
        if isinstance(it, dict):
            # expected keys: item, impact
            item_id = it.get("item") or it.get("uid") or it.get("id") or it.get("name")
            impact = it.get("impact") or it.get("risk") or it.get("level") or "Low"
            normalized.append({"item": item_id, "impact": impact})
        else:
            normalized.append({"item": str(it), "impact": "Low"})
    return normalized

# ---------------- Tabs / Navigation ----------------
tabs = st.tabs([
    "📄 Summary",
    "📘 Impact",
    "🧩 Teamcenter",
    "📎 Attachments",
    "📊 Insights"
])

# ------------------- TAB 1: Summary -------------------
with tabs[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📄 ECO Summarizer (Mock)")
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        summary_eco_id = st.text_input("Enter ECO ID", "1001", key="sum_eco_id")
    with c2:
        if st.button("Generate Summary", key="summarize_btn"):
            r = requests.get(f"{API_BASE}/eco/{summary_eco_id}/summarize")
            d = safe_json(r)
            if "summary" in d:
                st.success("Summary generated")
                st.markdown(f"**Summary for ECO `{summary_eco_id}`**")
                st.write(d["summary"])
            else:
                st.error("No summary returned. See raw response below.")
                st.code(d.get("raw_response", str(d)))
    with c3:
        st.write("")  # placeholder
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- TAB 2: Impact -------------------
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📘 Impact Analysis (Mock)")
    imp_col1, imp_col2 = st.columns([2,1])
    with imp_col1:
        impact_eco_id = st.text_input("ECO ID for Impact Analysis", "1001", key="impact_eco_id")
    with imp_col2:
        if st.button("Analyze Impact", key="analyze_imp"):
            r = requests.get(f"{API_BASE}/eco/{impact_eco_id}/impact")
            d = safe_json(r)
            md_text = d.get("impact_analysis") or d.get("impact") or d.get("analysis") or d.get("raw_response","")
            if md_text:
                st.success("Impact analysis retrieved")
                st.markdown(render_structured_impact(md_text), unsafe_allow_html=True)
            else:
                st.warning("No impact text returned.")
                st.code(pretty_print_json(d))
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- TAB 3: Teamcenter Actions -------------------
with tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧩 Teamcenter ECO Operations")

    # Split into two columns: left for inputs, right for results/logs
    left, right = st.columns([1.2, 1])

    with left:
        tc_action = st.radio("Select action", [
            "Create ECO",
            "Get ECO Details",
            "Update ECO Status",
            "Add Impacted Item",
            "Remove Impacted Item"
        ], horizontal=False)

        # dynamic form fields
        if tc_action == "Create ECO":
            tc_title = st.text_input("ECO Title", key="tc_create_title")
            tc_desc = st.text_area("ECO Description", key="tc_create_desc")
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
                out = safe_json(r)
                st.session_state["last_tc_response"] = out
                st.success("Create ECO request sent")

        elif tc_action == "Get ECO Details":
            tc_uid = st.text_input("ECO UID", key="tc_get_uid")
            if st.button("Fetch Details", key="tc_get_btn"):
                r = requests.get(f"{API_BASE}/tc/eco/{tc_uid}")
                out = safe_json(r)
                st.session_state["last_tc_response"] = out
                if "raw_response" in out:
                    st.error("Teamcenter returned non-JSON; see raw text below")
                else:
                    st.success("ECO details fetched")

        elif tc_action == "Update ECO Status":
            tc_uid2 = st.text_input("ECO UID", key="tc_update_uid")
            tc_act = st.selectbox("Action", ["Promote", "Demote"], key="tc_update_action")
            if st.button("Update Status", key="tc_update_btn"):
                r = requests.post(f"{API_BASE}/tc/eco/{tc_uid2}/status", params={"action": tc_act})
                out = safe_json(r)
                st.session_state["last_tc_response"] = out
                st.success("Status update request sent")

        elif tc_action == "Add Impacted Item":
            eco_uid_add = st.text_input("ECO UID", key="tc_add_uid")
            item_uid_add = st.text_input("Item UID", key="tc_add_item")
            if st.button("Add Item", key="tc_add_btn"):
                r = requests.post(f"{API_BASE}/tc/eco/{eco_uid_add}/add_item/{item_uid_add}")
                out = safe_json(r)
                st.session_state["last_tc_response"] = out
                st.success("Add item request sent")

        elif tc_action == "Remove Impacted Item":
            eco_uid_rem = st.text_input("ECO UID", key="tc_rem_uid")
            item_uid_rem = st.text_input("Item UID", key="tc_rem_item")
            if st.button("Remove Item", key="tc_rem_btn"):
                r = requests.post(f"{API_BASE}/tc/eco/{eco_uid_rem}/remove_item/{item_uid_rem}")
                out = safe_json(r)
                st.session_state["last_tc_response"] = out
                st.success("Remove item request sent")

    with right:
        st.markdown("**Live Response / Log**")
        last = st.session_state.get("last_tc_response")
        if last:
            # pretty JSON if possible
            if isinstance(last, dict) and "raw_response" not in last:
                st.json(last)
            else:
                st.code(last.get("raw_response", str(last)))
        else:
            st.info("No Teamcenter action executed yet. Perform an action to see results here.")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- TAB 4: Attachments -------------------
with tabs[3]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📎 Attach Files to ECO")

    attach_uid = st.text_input("ECO UID for attachment", key="attach_uid")
    uploaded_file = st.file_uploader("Select file to upload", type=["pdf", "jpg", "png", "txt", "docx"])

    if uploaded_file:
        st.markdown(f"**Selected file:** {uploaded_file.name} — <span class='small'>{uploaded_file.type}</span>", unsafe_allow_html=True)
        size_kb = len(uploaded_file.getvalue()) / 1024
        st.markdown(f"<span class='small'>Size: {size_kb:.1f} KB</span>", unsafe_allow_html=True)

    if st.button("Upload & Attach", key="upload_btn"):
        if not attach_uid or not uploaded_file:
            st.error("Please provide ECO UID and select a file before uploading.")
        else:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            r = requests.post(f"{API_BASE}/tc/eco/{attach_uid}/attach", files=files)
            out = safe_json(r)
            if "raw_response" in out:
                st.error("Attach failed — server returned non-JSON response.")
                st.code(out.get("raw_response"))
            else:
                st.success("File attached (mock).")
                st.json(out)

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- TAB 5: Insights (Charts) -------------------
with tabs[4]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Insights & Visuals")

    insight_uid = st.text_input("ECO UID for insights", "1001", key="insight_uid")
    if st.button("Refresh Insights", key="insight_refresh"):
        r = requests.get(f"{API_BASE}/tc/eco/{insight_uid}")
        eco_details = safe_json(r)

        # Attempt to parse impacted items
        impacted = parse_impacted_items_from_eco_details(eco_details)
        if not impacted:
            st.warning("No impacted items found in ECO details.")
            st.code(pretty_print_json(eco_details))
        else:
            # Build dataframe-like list
            items = []
            for it in impacted:
                items.append({"item": it["item"], "impact": it["impact"]})

            # Build chart counts
            counts = {}
            for it in items:
                level = (it["impact"] or "Low").strip().title()
                counts[level] = counts.get(level, 0) + 1

            df = [{"impact": k, "count": v} for k, v in counts.items()]
            chart_data = alt.Data(values=df)

            chart = alt.Chart(chart_data).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="count", type="quantitative"),
                color=alt.Color(field="impact", type="nominal", sort=list(counts.keys())),
                tooltip=["impact", "count"]
            ).properties(width=360, height=360)

            st.markdown("### Impact Distribution")
            st.altair_chart(chart, use_container_width=False)

            # Table of items
            st.markdown("### Impacted Items")
            st.table(items)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown("""
---
*Built for demo & PoC. Switch to real Teamcenter by changing the backend toggle in `main.py`.*
""")
