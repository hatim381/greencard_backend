import sqlite3

db_path = "db/greencart.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Vérifie si la colonne existe déjà avant de l'ajouter
def column_exists(table, column):
    cur.execute(f"PRAGMA table_info({table});")
    return any(row[1] == column for row in cur.fetchall())

if not column_exists("orders", "address"):
    try:
        cur.execute("ALTER TABLE orders ADD COLUMN address VARCHAR(255);")
        print("Colonne address ajoutée.")
    except Exception as e:
        print("Erreur colonne address :", e)
else:
    print("Colonne address déjà existante.")

if not column_exists("orders", "payment"):
    try:
        cur.execute("ALTER TABLE orders ADD COLUMN payment VARCHAR(50);")
        print("Colonne payment ajoutée.")
    except Exception as e:
        print("Erreur colonne payment :", e)
else:
    print("Colonne payment déjà existante.")

conn.commit()

# Affiche le schéma de la table orders pour vérification
print("\nSchéma de la table 'orders' :")
for row in cur.execute("PRAGMA table_info(orders);"):
    print(row)

conn.close()
print("Migration terminée.")
