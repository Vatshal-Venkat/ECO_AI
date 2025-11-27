from db import get_db

db = get_db()

db.execute("""
CREATE TABLE IF NOT EXISTS eco_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    change_id TEXT UNIQUE,
    title TEXT,
    description TEXT,
    datasets TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
""")

db.execute("""
CREATE TABLE IF NOT EXISTS eco_bom (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    change_id TEXT,
    item TEXT,
    impact TEXT,
    FOREIGN KEY(change_id) REFERENCES eco_master(change_id)
);
""")

db.commit()
db.close()
