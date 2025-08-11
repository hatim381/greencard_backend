import sqlite3
from datetime import datetime

db_path = "db/greencart.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Vérifie si un owner existe déjà
cur.execute("SELECT id FROM users WHERE role = 'owner'")
if cur.fetchone():
    print("Un utilisateur owner existe déjà.")
else:
    cur.execute("""
        INSERT INTO users (email, password, name, role, wallet_balance, registered_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "admin@greencart.fr",
        "admin",  
        "Propriétaire",
        "owner",
        0.0,
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    print("Utilisateur owner ajouté.")

conn.close()
