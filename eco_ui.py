import streamlit as st
import requests
import re

API_BASE = "http://127.0.0.1:8000"

# Page config
st.set_page_config(
    page_title="ECO AI Assistant",
    page_icon="🔧",
    layout="wide"
)

# Header
st.markdown("""
# 🔧 ECO AI Assistant – Teamcenter PoC  
A clean, modern dashboard for ECO Summaries, Impact Analysis & Teamcenter operations.
""")

# ============================================================================
#  UTILITY FUNCTIONS
# ============================================================================

def safe_json(response):
    """Safely decode JSON or return raw text (prevents crashes)."""
    try:
        return response.json()
    except:
        return {"raw_response": response.text}


def render_structured_impact(md_text: str):
    """Convert raw Markdown from backend into structured collapsible sections."""
    sections = re.split(r"(###.*|####.*|\*\*Item:.*)", md_text)
    formatted = "## 📘 Impact Analysis\n\n---\n"

    i = 0
    while i < len(sections):
        part = sections[i].strip()

        if (
            part.startswith("###") or
            part.startswith("####") or
            part.startswith("**Item:")
        ):
            content = sections[i + 1].strip() if i + 1 < len(sections) else ""
            title = (
                part.replace("###", "")
                .replace("####", "")
                .replace("**", "")
                .strip()
            )

            formatted += f"""
<details>
  <summary><strong>{title}</strong></summary>
  <div style='padding-left: 15px;'>
  {content}
  </div>
</details>

---
"""
            i += 2
        else:
            formatted += part + "\n\n"
            i += 1

    formatted += "\n---\n*End of analysis.*"
    return formatted


# ============================================================================
#  MAIN UI – TABS
# ============================================================================

tabs = st.tabs([
    "📄 ECO Summary (Mock)",
    "📘 Impact Analysis (Mock)",
    "🧩 Teamcenter ECO Actions",
    "📎 Attachments"
])

# ============================================================================
#  TAB 1 — SUMMARY
# ============================================================================

with tabs[0]:
    st.subheader("📄 ECO Summary Generator (Mock Data)")

    col1, col2 = st.columns([2, 1])
    with col1:
        eco_id = st.text_input("Enter ECO ID", "1001")

    if st.button("Generate Summary", use_container_width=True):
        r = requests.get(f"{API_BASE}/eco/{eco_id}/summarize")
        data = safe_json(r)

        st.success("ECO Summary Generated")
        st.markdown(f"### 📝 Summary for ECO `{eco_id}`")
        st.write(data.get("summary", "No summary returned"))


# ============================================================================
#  TAB 2 — IMPACT ANALYSIS
# ============================================================================

with tabs[1]:
    st.subheader("📘 ECO Impact Analysis (Mock)")

    eco_id = st.text_input("Enter ECO ID for Impact Analysis", "1001")

    if st.button("Analyze Impact", use_container_width=True):
        r = requests.get(f"{API_BASE}/eco/{eco_id}/impact")
        data = safe_json(r)
        md_text = data.get("impact_analysis", "")

        st.success("Impact Analysis Complete")
        st.markdown(render_structured_impact(md_text), unsafe_allow_html=True)


# ============================================================================
#  TAB 3 — TEAMCENTER ACTIONS
# ============================================================================

with tabs[2]:
    st.subheader("🧩 Teamcenter ECO Operations")

    action = st.selectbox("Choose Action", [
        "Create ECO",
        "Get ECO Details",
        "Update ECO Status",
        "Add Impacted Item",
        "Remove Impacted Item"
    ])

    st.markdown("---")

    # Create ECO
    if action == "Create ECO":
        name = st.text_input("ECO Title")
        desc = st.text_area("ECO Description")

        if st.button("Create ECO", use_container_width=True):
            payload = {
                "clientId": "UI_ECO_CREATE",
                "className": "ChangeNoticeRevision",
                "properties": {
                    "object_name": name,
                    "object_desc": desc
                }
            }
            r = requests.post(f"{API_BASE}/tc/eco/create", json=payload)
            st.json(safe_json(r))

    # Get ECO Details
    if action == "Get ECO Details":
        uid = st.text_input("ECO UID")
        if st.button("Fetch Details", use_container_width=True):
            r = requests.get(f"{API_BASE}/tc/eco/{uid}")
            st.json(safe_json(r))

    # Update ECO Status
    if action == "Update ECO Status":
        uid = st.text_input("ECO UID")
        status_act = st.selectbox("Select Action", ["Promote", "Demote"])

        if st.button("Update Status", use_container_width=True):
            r = requests.post(
                f"{API_BASE}/tc/eco/{uid}/status",
                params={"action": status_act}
            )
            st.json(safe_json(r))

    # Add Impacted Item
    if action == "Add Impacted Item":
        eco_uid = st.text_input("ECO UID")
        item_uid = st.text_input("Item UID")

        if st.button("Add Item", use_container_width=True):
            r = requests.post(
                f"{API_BASE}/tc/eco/{eco_uid}/add_item/{item_uid}"
            )
            st.json(safe_json(r))

    # Remove Impacted Item
    if action == "Remove Impacted Item":
        eco_uid = st.text_input("ECO UID")
        item_uid = st.text_input("Item UID")

        if st.button("Remove Item", use_container_width=True):
            r = requests.post(
                f"{API_BASE}/tc/eco/{eco_uid}/remove_item/{item_uid}"
            )
            st.json(safe_json(r))


# ============================================================================
#  TAB 4 — FILE ATTACHMENTS
# ============================================================================

with tabs[3]:
    st.subheader("📎 Attach Files to ECO")

    eco_uid = st.text_input("ECO UID for attachment")
    file = st.file_uploader("Upload ECO File", type=["pdf", "jpg", "png", "txt"])

    if st.button("Upload File", use_container_width=True) and file:
        files = {"file": (file.name, file.getvalue())}
        r = requests.post(f"{API_BASE}/tc/eco/{eco_uid}/attach", files=files)

        st.success("File attached successfully!")
        st.json(safe_json(r))
