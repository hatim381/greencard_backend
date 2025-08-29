"""
Test de la contrainte PayPal
"""
import sqlite3
import os

def test_paypal_constraint():
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'greencart.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Test de la contrainte PayPal...")
        
        # Essayer d'insérer un enregistrement avec PayPal
        try:
            cursor.execute('''
            INSERT INTO orders (consumer_id, payment, address) 
            VALUES (1, 'paypal', 'Test Address')
            ''')
            conn.commit()
            print("✅ Insertion PayPal réussie !")
            
            # Supprimer l'enregistrement test
            cursor.execute("DELETE FROM orders WHERE payment = 'paypal' AND address = 'Test Address'")
            conn.commit()
            print("✅ Test PayPal terminé avec succès !")
            
        except sqlite3.IntegrityError as e:
            print(f"❌ Contrainte PayPal échouée: {e}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    test_paypal_constraint()
