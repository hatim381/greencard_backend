"""
Script pour ajouter PayPal aux moyens de paiement autorisés
"""
import sqlite3
import os

def update_payment_constraint():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'greencart.db')
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Modification de la contrainte payment pour inclure PayPal...")
        
        # 1. Créer une nouvelle table temporaire avec la contrainte mise à jour
        cursor.execute('''
        CREATE TABLE orders_temp (
            id INTEGER PRIMARY KEY,
            consumer_id INTEGER NOT NULL,
            ordered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_price FLOAT,
            total_co2_saved FLOAT,
            address VARCHAR(255),
            payment VARCHAR(50) CHECK (payment IN ('cb', 'especes', 'paypal')),
            email VARCHAR(255),
            phone VARCHAR(50),
            instructions TEXT,
            payment_intent_id VARCHAR(255),
            FOREIGN KEY (consumer_id) REFERENCES users (id)
        )
        ''')
        
        # 2. Copier toutes les données existantes
        cursor.execute('''
        INSERT INTO orders_temp 
        SELECT * FROM orders
        ''')
        
        # 3. Supprimer l'ancienne table
        cursor.execute('DROP TABLE orders')
        
        # 4. Renommer la nouvelle table
        cursor.execute('ALTER TABLE orders_temp RENAME TO orders')
        
        # Valider les changements
        conn.commit()
        print("✅ Contrainte payment mise à jour avec succès ! PayPal est maintenant autorisé.")
        
        # Vérifier que la contrainte fonctionne
        cursor.execute("INSERT INTO orders (consumer_id, payment) VALUES (1, 'paypal')")
        cursor.execute("DELETE FROM orders WHERE payment = 'paypal' AND consumer_id = 1")
        conn.commit()
        print("✅ Test PayPal réussi !")
        
    except sqlite3.Error as e:
        print(f"❌ Erreur SQLite: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    update_payment_constraint()
