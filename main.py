from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File
from gemini_client import ask_gemini
from mock_teamcenter import get_mock_eco

# Import REAL Teamcenter client functions
from teamcenter_client import (
    create_eco,
    get_eco_details,
    update_eco_status,
    add_impacted_item,
    remove_impacted_item,
    attach_file
)

app = FastAPI()


# ---------------------------------------------------------
# ROOT TEST ENDPOINT
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Teamcenter ECO PoC running"}



# =====================================================================
#  MOCK ECO ENDPOINTS (YOUR EXISTING FUNCTIONALITY)
# =====================================================================

@app.get("/eco/{change_id}/summarize")
def summarize_eco(change_id: str):
    """
    Your existing mock-based ECO summary using Gemini
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
    Your existing mock-based ECO impact analysis using Gemini
    """
    eco = get_mock_eco(change_id)

    prompt = f"""
    Perform impact analysis based on this BOM:
    {eco['bom']}
    """

    impact = ask_gemini(prompt)
    return {"eco_id": change_id, "impact_analysis": impact}



# =====================================================================
#  REAL TEAMCENTER ENDPOINTS (NEW)
# =====================================================================

# ---------------------------------------------------------
# CREATE ECO
# ---------------------------------------------------------
@app.post("/tc/eco/create")
def route_create_eco(body: dict):
    """
    Create an ECO in Teamcenter
    """
    return create_eco(body)



# ---------------------------------------------------------
# READ ECO DETAILS
# ---------------------------------------------------------
@app.get("/tc/eco/{uid}")
def route_get_eco(uid: str):
    """
    Fetch ECO details from Teamcenter
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
    Upload and attach file to ECO
    """
    temp_path = f"/tmp/{file.filename}"

    # Save uploaded file temporarily
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    return attach_file(eco_uid, temp_path)
