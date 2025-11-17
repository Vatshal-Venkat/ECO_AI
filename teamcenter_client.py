import os
import requests
from requests.auth import HTTPBasicAuth

# ---------------------------------------------------------
# Load Teamcenter Credentials from .env
# ---------------------------------------------------------
TC_URL = os.getenv("TC_URL")              # Example: http://your-tc-server:8080
TC_USERNAME = os.getenv("TC_USERNAME")    # TC user
TC_PASSWORD = os.getenv("TC_PASSWORD")    # TC password

if not TC_URL:
    raise ValueError("❌ TC_URL is missing in .env")
if not TC_USERNAME or not TC_PASSWORD:
    raise ValueError("❌ Teamcenter username/password missing in .env")

AUTH = HTTPBasicAuth(TC_USERNAME, TC_PASSWORD)



# ---------------------------------------------------------
# 1️⃣ CREATE ECO
# ---------------------------------------------------------
def create_eco(data: dict):
    """
    Create an ECO (Change Notice Revision) using StructureManagement/Create
    """
    url = f"{TC_URL}/tc/api/StructureManagement/Create"
    response = requests.post(url, auth=AUTH, json={"input": [data]})
    return response.json()



# ---------------------------------------------------------
# 2️⃣ READ ECO DETAILS
# ---------------------------------------------------------
def get_eco_details(uid: str):
    """
    Fetch properties of ECO using DataManagement/getProperties
    """
    url = f"{TC_URL}/tc/api/Core-2006-03-DataManagement/getProperties"
    payload = {"objects": [{"uid": uid}]}
    response = requests.post(url, auth=AUTH, json=payload)
    return response.json()



# ---------------------------------------------------------
# 3️⃣ UPDATE ECO STATUS (Promote/Demote)
# ---------------------------------------------------------
def update_eco_status(uid: str, action: str):
    """
    Perform a lifecycle action (Promote, Demote, etc.)
    """
    url = f"{TC_URL}/tc/api/Core-2007-01-Lifecycle/performAction"
    payload = {
        "objects": [{"uid": uid}],
        "action": action
    }
    response = requests.post(url, auth=AUTH, json=payload)
    return response.json()



# ---------------------------------------------------------
# 4️⃣ ADD IMPACTED / AFFECTED ITEM
# ---------------------------------------------------------
def add_impacted_item(eco_uid: str, item_uid: str):
    """
    Adds an item to ECO affected/impacted list
    """
    url = f"{TC_URL}/tc/api/Core-2007-01-RelationManagement/createRelations"
    payload = {
        "input": [{
            "relationType": "CMHasImpactedItem",
            "primaryObject": {"uid": eco_uid},
            "secondaryObject": {"uid": item_uid}
        }]
    }

    response = requests.post(url, auth=AUTH, json=payload)
    return response.json()



# ---------------------------------------------------------
# 5️⃣ REMOVE IMPACTED / AFFECTED ITEM
# ---------------------------------------------------------
def remove_impacted_item(eco_uid: str, item_uid: str):
    """
    Removes an affected/impacted item from ECO
    """
    url = f"{TC_URL}/tc/api/Core-2007-01-RelationManagement/deleteRelations"
    payload = {
        "input": [{
            "relationType": "CMHasImpactedItem",
            "primaryObject": {"uid": eco_uid},
            "secondaryObject": {"uid": item_uid}
        }]
    }

    response = requests.post(url, auth=AUTH, json=payload)
    return response.json()



# ---------------------------------------------------------
# 6️⃣ ATTACH FILE TO ECO
# ---------------------------------------------------------
def attach_file(eco_uid: str, file_path: str):
    """
    Upload a file to Teamcenter AND attach to ECO
    """
    # Step 1: Upload file
    upload_url = f"{TC_URL}/tc/api/Core-2006-03-FileManagement/upload"
    files = {"file": open(file_path, "rb")}
    data = {"container_uid": eco_uid}

    upload_res = requests.post(upload_url, auth=AUTH, files=files, data=data).json()

    try:
        file_uid = upload_res["objects"][0]["uid"]
    except Exception:
        return {"error": "Upload failed", "response": upload_res}

    # Step 2: Create relation to ECO
    relation_url = f"{TC_URL}/tc/api/Core-2007-01-RelationManagement/createRelations"
    payload = {
        "input": [{
            "relationType": "IMAN_specification",
            "primaryObject": {"uid": eco_uid},
            "secondaryObject": {"uid": file_uid}
        }]
    }

    relation_res = requests.post(relation_url, auth=AUTH, json=payload).json()

    return {
        "upload": upload_res,
        "relation": relation_res
    }
