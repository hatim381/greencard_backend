import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import db

def add_withdrawal_request_table():
    """
    Ajoute la table withdrawal_requests à la base de données si elle n'existe pas déjà.
    """
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    if 'withdrawal_requests' not in inspector.get_table_names():
        db.create_all()
        print("Table withdrawal_requests créée.")
    else:
        print("Table withdrawal_requests existe déjà.")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        add_withdrawal_request_table()
