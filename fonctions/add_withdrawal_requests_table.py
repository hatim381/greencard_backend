import sqlite3

def add_withdrawal_requests_table(db_path='db/greencart.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Vérifie si la table existe déjà
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='withdrawal_requests';
    """)
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("""
            CREATE TABLE withdrawal_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                iban TEXT NOT NULL,
                bic TEXT,
                rib TEXT,
                status TEXT DEFAULT 'en attente',
                requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Table 'withdrawal_requests' ajoutée avec succès.")
    else:
        print("La table 'withdrawal_requests' existe déjà.")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_withdrawal_requests_table()
