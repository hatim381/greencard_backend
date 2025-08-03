import sqlite3

db_path = "db/greencart.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

def column_exists(table, column):
    cur.execute(f"PRAGMA table_info({table});")
    return any(row[1] == column for row in cur.fetchall())

if not column_exists("users", "wallet_balance"):
    try:
        cur.execute("ALTER TABLE users ADD COLUMN wallet_balance FLOAT DEFAULT 0.0;")
        print("Colonne wallet_balance ajoutée à users.")
    except Exception as e:
        print("Erreur colonne wallet_balance :", e)
else:
    print("Colonne wallet_balance déjà existante.")

conn.commit()
print("\nSchéma de la table 'users' :")
for row in cur.execute("PRAGMA table_info(users);"):
    print(row)
conn.close()
print("Migration terminée.")
