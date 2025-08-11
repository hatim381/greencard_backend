import sqlite3
import os

db_dir = os.path.join("backend", "db")
db_path = os.path.join(db_dir, "greencart.db")

if not os.path.exists(db_path):
    print(f"La base '{db_path}' n'existe pas.")
    exit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("Liste des commandes (orders) :")
for row in cur.execute("SELECT * FROM orders;"):
    print(row)

conn.close()
