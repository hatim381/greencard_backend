import sqlite3
import os

db_dir = os.path.join("backend", "db")
db_path = os.path.join(db_dir, "greencart.db")

# Crée le dossier db si besoin (ne crée pas la base si elle n'existe pas déjà)
if not os.path.exists(db_dir):
    print(f"Le dossier '{db_dir}' n'existe pas. Chemin attendu : {db_path}")
    exit(1)
if not os.path.exists(db_path):
    print(f"La base '{db_path}' n'existe pas.")
    exit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("Schéma de la table 'orders' :")
for row in cur.execute("PRAGMA table_info(orders);"):
    print(row)

conn.close()