import sqlite3

db_path = "db/greencart.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

def column_exists(table, column):
    cur.execute(f"PRAGMA table_info({table});")
    return any(row[1] == column for row in cur.fetchall())

if not column_exists("order_items", "status"):
    try:
        cur.execute("ALTER TABLE order_items ADD COLUMN status VARCHAR(20) DEFAULT 'en attente';")
        print("Colonne status ajoutée à order_items.")
    except Exception as e:
        print("Erreur colonne status :", e)
else:
    print("Colonne status déjà existante.")

conn.commit()
print("\nSchéma de la table 'order_items' :")
for row in cur.execute("PRAGMA table_info(order_items);"):
    print(row)
conn.close()
print("Migration terminée.")
