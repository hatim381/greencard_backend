from werkzeug.security import generate_password_hash
import sqlite3

db_path = "db/greencart.db"
email = "elisa@green.fr"
new_password = "AZERTY"
new_hash = generate_password_hash(new_password, method="scrypt")

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("UPDATE users SET password = ? WHERE email = ?", (new_hash, email))
conn.commit()
print(f"Mot de passe de {email} mis à jour.")
conn.close()
print(f"Mot de passe de {email} mis à jour.")
conn.close()
