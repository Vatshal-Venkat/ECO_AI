# main.py (updated)
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File
from gemini_client import ask_gemini
from mock_teamcenter import get_mock_eco

# We'll conditionally import or define Teamcenter client functions
# based on the USE_MOCK toggle below.
# If USE_MOCK = False, ensure teamcenter_client.py exists and provides the real functions.
# If USE_MOCK = True, the mock functions below will be used.
USE_MOCK = True

if not USE_MOCK:
    from teamcenter_client import (
        create_eco,
        get_eco_details,
        update_eco_status,
        add_impacted_item,
        remove_impacted_item,
        attach_file
    )
else:
    # -------------------------
    # Mock Teamcenter client functions (used only when USE_MOCK = True)
    # -------------------------
    def create_eco(payload):
        """Mock create_eco"""
        return {
            "status": "success",
            "eco_uid": "MOCK_ECO_1001",
            "message": "Mock ECO created successfully.",
            "payload_received": payload
        }

    def get_eco_details(uid):
        """Mock get_eco_details"""
        return {
            "status": "success",
            "eco_uid": uid,
            "object_name": "Mock ECO Title",
            "object_desc": "This ECO is returned from MOCK Teamcenter.",
            "status_info": "In Review",
            "impacted_items": [
                {"item": "A1001", "impact": "High"},
                {"item": "A1002", "impact": "Low"}
            ],
        }

    def update_eco_status(uid, action):
        """Mock update_eco_status"""
        return {
            "status": "success",
            "eco_uid": uid,
            "action": action,
            "new_state": "Promoted" if action == "Promote" else "Demoted"
        }

    def add_impacted_item(eco_uid, item_uid):
        """Mock add_impacted_item"""
        return {
            "status": "success",
            "eco_uid": eco_uid,
            "added_item": item_uid
        }

    def remove_impacted_item(eco_uid, item_uid):
        """Mock remove_impacted_item"""
        return {
            "status": "success",
            "eco_uid": eco_uid,
            "removed_item": item_uid
        }

    def attach_file(eco_uid, file_path_or_bytes):
        """
        Mock attach_file.
        The real client might accept a path or binary content; our mock just returns metadata.
        """
        # If a path string was provided, attempt to measure file size; otherwise if bytes, use len
        try:
            if isinstance(file_path_or_bytes, str):
                import os
                size = os.path.getsize(file_path_or_bytes) if os.path.exists(file_path_or_bytes) else 0
                name = file_path_or_bytes.split("/")[-1].split("\\")[-1]
            else:
                # assume bytes-like
                size = len(file_path_or_bytes)
                name = "uploaded_mock_file"
        except Exception:
            size = 0
            name = "unknown"
        return {
            "status": "success",
            "eco_uid": eco_uid,
            "attached_file": name,
            "file_size_bytes": size
        }

app = FastAPI()


# ---------------------------------------------------------
# ROOT TEST ENDPOINT
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Teamcenter ECO PoC running", "use_mock": USE_MOCK}


# =====================================================================
#  MOCK ECO ENDPOINTS (Your existing functionality using Gemini)
# =====================================================================

@app.get("/eco/{change_id}/summarize")
def summarize_eco(change_id: str):
    """
    Mock-based ECO summary using Gemini
    """
    eco = get_mock_eco(change_id)

    prompt = f"""
    Summarize this ECO clearly:
    Title: {eco['title']}
    Description: {eco['description']}
    """

    summary = ask_gemini(prompt)
    return {"eco_id": change_id, "summary": summary}


@app.get("/eco/{change_id}/impact")
def impact_eco(change_id: str):
    """
    Mock-based ECO impact analysis using Gemini
    """
    eco = get_mock_eco(change_id)

    prompt = f"""
    Perform impact analysis based on this BOM:
    {eco['bom']}
    """

    impact = ask_gemini(prompt)
    return {"eco_id": change_id, "impact_analysis": impact}


# =====================================================================
#  TEAMCENTER ENDPOINTS (Mocked or Real per USE_MOCK)
# =====================================================================

# ---------------------------------------------------------
# CREATE ECO
# ---------------------------------------------------------
@app.post("/tc/eco/create")
def route_create_eco(body: dict):
    """
    Create an ECO in Teamcenter (mock or real based on USE_MOCK)
    """
    return create_eco(body)


# ---------------------------------------------------------
# READ ECO DETAILS
# ---------------------------------------------------------
@app.get("/tc/eco/{uid}")
def route_get_eco(uid: str):
    """
    Fetch ECO details from Teamcenter (mock or real)
    """
    return get_eco_details(uid)


# ---------------------------------------------------------
# UPDATE ECO STATUS (Promote/Demote)
# ---------------------------------------------------------
@app.post("/tc/eco/{uid}/status")
def route_update_status(uid: str, action: str):
    """
    Update ECO lifecycle status
    action = Promote or Demote
    """
    return update_eco_status(uid, action)


# ---------------------------------------------------------
# ADD IMPACTED ITEM
# ---------------------------------------------------------
@app.post("/tc/eco/{eco_uid}/add_item/{item_uid}")
def route_add_item(eco_uid: str, item_uid: str):
    """
    Add affected/impacted item
    """
    return add_impacted_item(eco_uid, item_uid)


# ---------------------------------------------------------
# REMOVE IMPACTED ITEM
# ---------------------------------------------------------
@app.post("/tc/eco/{eco_uid}/remove_item/{item_uid}")
def route_remove_item(eco_uid: str, item_uid: str):
    """
    Remove affected/impacted item
    """
    return remove_impacted_item(eco_uid, item_uid)


# ---------------------------------------------------------
# ATTACH FILE TO ECO
# ---------------------------------------------------------
@app.post("/tc/eco/{eco_uid}/attach")
async def route_attach_file(eco_uid: str, file: UploadFile = File(...)):
    """
    Upload and attach file to ECO.
    In mock mode we save a temporary file and pass path/bytes to the mock attach_file.
    In real mode, teamcenter client should handle the UploadFile accordingly.
    """
    # Read uploaded file content
    content = await file.read()

    # If using mock, pass bytes so mock records size; if real, write to temp path and pass path (depends on real client)
    if USE_MOCK:
        return attach_file(eco_uid, content)
    else:
        # For real client, save temporarily and pass path (this mirrors previous behavior)
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(content)
        return attach_file(eco_uid, temp_path)
