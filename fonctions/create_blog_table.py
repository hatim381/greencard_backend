from models import db, BlogPost
from app import app

with app.app_context():
    db.create_all()
    print("Table blog_posts créée (si elle n'existait pas déjà).")
