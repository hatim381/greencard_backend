import sqlite3

def add_default_address_column(db_path='db/greencart.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Vérifie si la colonne existe déjà
    cursor.execute("PRAGMA table_info(users);")
    columns = [col[1] for col in cursor.fetchall()]
    if 'default_address' not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN default_address VARCHAR(255);")
        print("Colonne 'default_address' ajoutée avec succès.")
    else:
        print("La colonne 'default_address' existe déjà.")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_default_address_column()
