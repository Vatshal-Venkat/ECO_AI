from teamcenter_client import create_eco

create_eco(
    "1001",
    "Modify bracket thickness",
    "Increase thickness from 3mm to 4mm for durability.",
    ["CAD", "Drawing"],
    [
        {"item": "A1001", "impact": "High"},
        {"item": "A1002", "impact": "Low"}
    ]
)
