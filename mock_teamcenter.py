# mock_teamcenter.py — Full Mock Teamcenter with Database, Timestamps, Revisions

from datetime import datetime


ECO_COUNTER = 1
MOCK_DB = {}  # stores all ECOs



def next_revision(current: str | None):
    if not current:
        return "A"
    return chr(ord(current) + 1)  # A → B → C → ...



def create_eco(payload: dict):
    global ECO_COUNTER

    # Generate ECO ID
    year = datetime.now().year
    eco_uid = f"ECO-{year}-{ECO_COUNTER:04d}"
    ECO_COUNTER += 1

    title = payload.get("properties", {}).get("object_name", "Untitled ECO")
    desc = payload.get("properties", {}).get("object_desc", "")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # New ECO record
    eco_record = {
        "eco_uid": eco_uid,
        "title": title,
        "description": desc,
        "revision": "A",
        "creator": "Vatshal@celerinnTech", 
        "created_at": timestamp,
        "updated_at": timestamp,
        "status": "Created",
        "impacted_items": [],
        "datasets": [],
    }

    MOCK_DB[eco_uid] = eco_record

    return {
        "status": "success",
        "eco_uid": eco_uid,
        "record": eco_record
    }



def get_eco_details(eco_uid: str):
    eco = MOCK_DB.get(eco_uid)
    if not eco:
        return {"error": "ECO not found", "eco_uid": eco_uid}
    return eco



def update_eco_status(eco_uid: str, action: str):
    eco = MOCK_DB.get(eco_uid)
    if not eco:
        return {"error": "ECO not found", "eco_uid": eco_uid}

    old_status = eco["status"]

    if action.lower() == "promote":
        eco["revision"] = next_revision(eco["revision"])
        eco["status"] = f"Promoted to Rev {eco['revision']}"
    elif action.lower() == "demote":
        eco["status"] = f"Demoted (no revision change)"
    else:
        eco["status"] = "Unknown Action"

    eco["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "status": "success",
        "old_status": old_status,
        "new_status": eco["status"],
        "eco_uid": eco_uid,
    }



def add_impacted_item(eco_uid: str, item_uid: str):
    eco = MOCK_DB.get(eco_uid)
    if not eco:
        return {"error": "ECO not found", "eco_uid": eco_uid}

    eco["impacted_items"].append({
        "item": item_uid,
        "impact": "Medium"  # default impact for mock
    })

    eco["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "status": "success",
        "eco_uid": eco_uid,
        "added_item": item_uid
    }



def remove_impacted_item(eco_uid: str, item_uid: str):
    eco = MOCK_DB.get(eco_uid)
    if not eco:
        return {"error": "ECO not found", "eco_uid": eco_uid}

    eco["impacted_items"] = [
        it for it in eco["impacted_items"] if it["item"] != item_uid
    ]

    eco["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "status": "success",
        "eco_uid": eco_uid,
        "removed_item": item_uid
    }



def list_all_ecos():
    """Return all ECOs for listing page."""
    return list(MOCK_DB.values())




def seed_mock_eco_1001():
    """Insert predefined ECO 1001 into the mock DB."""
    eco_uid = "ECO-1001"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    eco_record = {
        "eco_uid": eco_uid,
        "title": "Modify bracket thickness",
        "description": "Increase thickness from 3mm to 4mm for durability.",
        "revision": "A",
        "creator": "vatshal@company.com",
        "created_at": timestamp,
        "updated_at": timestamp,
        "status": "Created",

        # Old BOM converted into new structure
        "impacted_items": [
            {"item": "A1001", "impact": "High"},
            {"item": "A1002", "impact": "Low"}
        ],

        # Old dataset values
        "datasets": ["CAD", "Drawing"],
    }

    MOCK_DB[eco_uid] = eco_record
    return eco_record
