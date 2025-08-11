import sqlite3

db_path = "db/greencart.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("Liste des consommateurs (email, mot de passe) :")
for row in cur.execute("SELECT email, password FROM users WHERE role = 'consumer'"):
    print(f"Email: {row[0]} | Password: {row[1]}")

conn.close()
