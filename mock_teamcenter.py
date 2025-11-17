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
