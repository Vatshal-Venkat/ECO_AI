# main.py — Clean, Corrected, Unified Backend

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from gemini_client import ask_gemini
from mock_teamcenter import seed_mock_eco_1001
from teamcenter_client import create_eco, get_eco_details





# --- NEW Mock Teamcenter (your DB version) ---
from mock_teamcenter import (
    create_eco,
    get_eco_details,
    update_eco_status,
    add_impacted_item,
    remove_impacted_item,
    list_all_ecos
)

# -------------------------------------------------------------
# Safety Wrapper – ensures backend never returns raw strings
# -------------------------------------------------------------
def safe(result):
    # Allow dicts and lists to pass through untouched
    if isinstance(result, (dict, list)):
        return result

    # None → empty list fallback
    if result is None:
        return []

    # Anything else becomes an error
    return {"error": str(result)}


app = FastAPI()

# -------------------------------------------------------------
# CORS for Frontend
# -------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# ROOT TEST
# -------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Teamcenter ECO PoC backend running", "mock_mode": True}

# ==================================================================
# SUMMARY (Gemini)
# ==================================================================
@app.get("/eco/{eco_id}/summarize")
def summarize_eco(eco_id: str):
    """
    Uses Gemini to generate summary.
    Does NOT use old get_mock_eco() anymore.
    """
    eco = get_eco_details(eco_id)
    if "error" in eco:
        return eco

    prompt = f"""
    Summarize this ECO clearly:

    Title: {eco.get('title')}
    Description: {eco.get('description')}
    Revision: {eco.get('revision')}
    Status: {eco.get('status')}
    """

    summary = ask_gemini(prompt)
    return {"eco_id": eco_id, "summary": summary}

# ==================================================================
# IMPACT (Gemini)
# ==================================================================
@app.get("/eco/{eco_id}/impact")
def impact_eco(eco_id: str):
    eco = get_eco_details(eco_id)
    if "error" in eco:
        return eco

    bom = eco.get("impacted_items", [])

    prompt = f"""
    Perform engineering impact analysis based on this impacted item list:
    {bom}
    """

    impact = ask_gemini(prompt)
    return {"eco_id": eco_id, "impact_analysis": impact}

# ==================================================================
# TEAMCENTER MOCK ENDPOINTS (your DB-based mock)
# ==================================================================

# CREATE ECO
@app.post("/tc/eco/create")
def route_create_eco(body: dict):
    return safe(create_eco(body))

# GET ECO DETAILS
@app.get("/tc/eco/{eco_uid}")
def route_get_eco(eco_uid: str):
    return safe(get_eco_details(eco_uid))

# UPDATE STATUS
@app.post("/tc/eco/{eco_uid}/status")
def route_update_status(eco_uid: str, action: str):
    return safe(update_eco_status(eco_uid, action))

# ADD ITEM
@app.post("/tc/eco/{eco_uid}/add_item/{item_uid}")
def route_add_item(eco_uid: str, item_uid: str):
    return safe(add_impacted_item(eco_uid, item_uid))

# REMOVE ITEM
@app.post("/tc/eco/{eco_uid}/remove_item/{item_uid}")
def route_remove_item(eco_uid: str, item_uid: str):
    return safe(remove_impacted_item(eco_uid, item_uid))

# GET ALL ECOs (for database tab)
@app.get("/tc/eco/all")
def route_get_all_ecos():
    return safe(list_all_ecos())


@app.post("/tc/eco/seed_1001")
async def seed_1001():
    return seed_mock_eco_1001()


@app.post("/eco/create")
async def create_eco_api(data: dict):
    return create_eco(
        change_id=data["change_id"],
        title=data["title"],
        description=data["description"],
        datasets=data["datasets"],
        bom_list=data["bom"]
    )


@app.get("/eco/{change_id}")
async def get_details(change_id: str):
    details = get_eco_details(change_id)
    if details:
        return details
    return {"error": "ECO not found"}


# ==================================================================
# ATTACH FILE (Mock Mode Only)
# ==================================================================
@app.post("/tc/eco/{eco_uid}/attach")
async def route_attach_file(eco_uid: str, file: UploadFile = File(...)):
    """
    Fake file attachment. Saves file metadata inside mock DB.
    """
    content = await file.read()
    size = len(content)

    return {
        "status": "success",
        "eco_uid": eco_uid,
        "filename": file.filename,
        "size_bytes": size
    }
