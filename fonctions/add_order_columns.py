#!/usr/bin/env python3
"""
Script pour ajouter les nouvelles colonnes à la table orders
"""

import sqlite3
import sys
import os

def add_order_columns():
    db_path = "db/greencart.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée : {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupérer la structure actuelle de la table orders
        cursor.execute("PRAGMA table_info(orders);")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Colonnes actuelles dans orders: {columns}")
        
        # Ajouter les nouvelles colonnes si elles n'existent pas
        new_columns = [
            ("email", "VARCHAR(255)"),
            ("phone", "VARCHAR(50)"),
            ("instructions", "TEXT"),
            ("payment_intent_id", "VARCHAR(255)")
        ]
        
        for col_name, col_type in new_columns:
            if col_name not in columns:
                sql = f"ALTER TABLE orders ADD COLUMN {col_name} {col_type};"
                cursor.execute(sql)
                print(f"✅ Colonne '{col_name}' ajoutée à la table orders")
            else:
                print(f"ℹ️  Colonne '{col_name}' existe déjà")
        
        conn.commit()
        
        # Vérifier le résultat
        cursor.execute("PRAGMA table_info(orders);")
        columns_after = [row[1] for row in cursor.fetchall()]
        print(f"Colonnes après modification: {columns_after}")
        
        conn.close()
        print("✅ Mise à jour de la table orders terminée avec succès !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour : {e}")
        if conn:
            conn.close()
        return False

if __name__ == "__main__":
    add_order_columns()
