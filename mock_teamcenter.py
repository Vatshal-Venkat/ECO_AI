def get_mock_eco(change_id: str):
    return {
        "change_id": change_id,
        "title": "Modify bracket thickness",
        "description": "Increase thickness from 3mm to 4mm for durability.",
        "datasets": ["CAD", "Drawing"],
        "bom": [
            {"item": "A1001", "impact": "High"},
            {"item": "A1002", "impact": "Low"}
        ]
    }
def create_eco(payload):
    global ECO_COUNTER

    # Generate ID: ECO-YYYY-XXXX
    from datetime import datetime
    year = datetime.now().year
    eco_id = f"ECO-{year}-{ECO_COUNTER:04d}"
    ECO_COUNTER += 1

    # Return simulated Teamcenter response
    return {
        "status": "success",
        "eco_uid": eco_id,
        "properties_received": payload
    }
