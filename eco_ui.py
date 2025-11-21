import streamlit as st
import requests
import re

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="ECO AI Assistant", layout="wide")
st.title("🔧 ECO AI Assistant – Teamcenter PoC UI")

# ============================================================
#  STRUCTURED IMPACT ANALYSIS RENDERER (NO NEW CONTENT ADDED)
# ============================================================

def render_structured_impact(md_text: str):
    """
    Converts the raw impact_analysis Markdown text into a more
    structured, readable Streamlit format.
    100% backend content — NO additions or rewrites.
    """

    # Split by Markdown headings or item labels
    sections = re.split(r"(###.*|####.*|\*\*Item:.*)", md_text)

    formatted = "# 📘 Impact Analysis\n\n---\n"

    i = 0
    while i < len(sections):
        part = sections[i].strip()

        # Detect headings dynamically
        if (
            part.startswith("###")
            or part.startswith("####")
            or part.startswith("**Item:")
        ):
            # Next chunk = section content
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

{content}

</details>

---
"""
            i += 2
        else:
            formatted += part + "\n\n"
            i += 1

    formatted += "\n---\n*End of analysis.*"
    return formatted


# ============================================================
#  SIDEBAR MENU
# ============================================================

st.sidebar.header("ECO Operations")
mode = st.sidebar.selectbox(
    "Choose an action",
    [
        "Summarize ECO (Mock)",
        "Impact Analysis (Mock)",
        "Create ECO (TC)",
        "Get ECO (TC)",
        "Update Status (TC)",
        "Add Impacted Item (TC)",
        "Remove Impacted Item (TC)",
        "Attach File (TC)"
    ]
)


# ============================================================
#  MOCK SUMMARY
# ============================================================

if mode == "Summarize ECO (Mock)":
    eco_id = st.text_input("Enter ECO ID", "1001")
    if st.button("Summarize"):
        r = requests.get(f"{API_BASE}/eco/{eco_id}/summarize")
        st.json(r.json())


# ============================================================
#  MOCK IMPACT ANALYSIS (NOW STRUCTURED & CLEAN)
# ============================================================

if mode == "Impact Analysis (Mock)":
    eco_id = st.text_input("Enter ECO ID", "1001")
    if st.button("Analyze Impact"):
        r = requests.get(f"{API_BASE}/eco/{eco_id}/impact")
        data = r.json()
        raw_md = data.get("impact_analysis", "")
        st.markdown(render_structured_impact(raw_md), unsafe_allow_html=True)


# ============================================================
#  CREATE ECO (TEAMCENTER)
# ============================================================

if mode == "Create ECO (TC)":
    object_name = st.text_input("ECO Title")
    object_desc = st.text_area("ECO Description")

    if st.button("Create ECO"):
        payload = {
            "clientId": "UI_ECO_CREATE",
            "className": "ChangeNoticeRevision",
            "properties": {
                "object_name": object_name,
                "object_desc": object_desc
            }
        }
        r = requests.post(f"{API_BASE}/tc/eco/create", json=payload)
        st.json(r.json())


# ============================================================
#  GET ECO DETAILS
# ============================================================

if mode == "Get ECO (TC)":
    uid = st.text_input("Enter ECO UID")
    if st.button("Fetch Details"):
        r = requests.get(f"{API_BASE}/tc/eco/{uid}")
        st.json(r.json())


# ============================================================
#  UPDATE ECO STATUS
# ============================================================

if mode == "Update Status (TC)":
    uid = st.text_input("Enter ECO UID")
    action = st.selectbox("Action", ["Promote", "Demote"])

    if st.button("Update Status"):
        r = requests.post(f"{API_BASE}/tc/eco/{uid}/status", params={"action": action})
        st.json(r.json())


# ============================================================
#  ADD IMPACTED ITEM
# ============================================================

if mode == "Add Impacted Item (TC)":
    eco_uid = st.text_input("ECO UID")
    item_uid = st.text_input("Item UID")

    if st.button("Add Item"):
        r = requests.post(f"{API_BASE}/tc/eco/{eco_uid}/add_item/{item_uid}")
        st.json(r.json())


# ============================================================
#  REMOVE IMPACTED ITEM
# ============================================================

if mode == "Remove Impacted Item (TC)":
    eco_uid = st.text_input("ECO UID")
    item_uid = st.text_input("Item UID")

    if st.button("Remove Item"):
        r = requests.post(f"{API_BASE}/tc/eco/{eco_uid}/remove_item/{item_uid}")
        st.json(r.json())


# ============================================================
#  ATTACH FILE TO ECO
# ============================================================

if mode == "Attach File (TC)":
    eco_uid = st.text_input("ECO UID")
    file = st.file_uploader("Upload File", type=["pdf", "jpg", "png", "txt"])

    if st.button("Attach") and file:
        files = {"file": (file.name, file.getvalue())}
        r = requests.post(f"{API_BASE}/tc/eco/{eco_uid}/attach", files=files)
        st.json(r.json())
