import sqlite3

db_path = "db/greencart.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

def column_exists(table, column):
    cur.execute(f"PRAGMA table_info({table});")
    return any(row[1] == column for row in cur.fetchall())

if not column_exists("users", "loyalty_points"):
    try:
        cur.execute("ALTER TABLE users ADD COLUMN loyalty_points INTEGER DEFAULT 0;")
        print("Colonne loyalty_points ajoutée à users.")
    except Exception as e:
        print("Erreur colonne loyalty_points :", e)
else:
    print("Colonne loyalty_points déjà existante.")

conn.commit()
print("\nSchéma de la table 'users' :")
for row in cur.execute("PRAGMA table_info(users);"):
    print(row)
conn.close()
print("Migration terminée.")
