import sqlite3

db_path = "db/greencart.db"
email = "admin@greencart.fr"
new_hash = "scrypt:32768:8:1$vVFYRRdMoYMXqcia$b92f3212cdeb879fb1bab783c4a64c3c27d0db3a5c280b399f02c61cb4f8e28969bb99d40736d6fb56d4b31f8a0f3461c9676c88d94f235abc1896384587e89c"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("UPDATE users SET password = ? WHERE email = ?", (new_hash, email))
conn.commit()

print("Mot de passe du propriétaire mis à jour.")
conn.close()
