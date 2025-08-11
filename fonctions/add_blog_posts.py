from models import db, BlogPost
from app import app
from datetime import datetime, timedelta
import random

# Génère 100 recettes fictives pour 2025
base_date = datetime(2025, 1, 1)
posts = []

# Listes de choix
categories = ['légumes', 'fruits', 'pain', 'viande', 'laitage']
restes    = ['carottes', 'pommes', 'pain', 'poulet', 'fromage']
astuces   = [
    'Ajoutez des herbes fraîches',
    'Faites gratiner au four',
    'Servez avec une salade',
    "Accompagnez d'une sauce maison",
    'Congelez pour plus tard'
]

for i in range(100):
    day = base_date + timedelta(days=i)

    # On tire au sort chaque partie avant l'f-string
    cat   = random.choice(categories)
    reste = random.choice(restes)
    tip   = random.choice(astuces)

    posts.append({
        "title":   f"Recette anti-gaspi #{i+1} : Astuce {cat}",
        "content": (
            f"Voici la recette anti-gaspillage numéro {i+1} pour l'année 2025. "
            f"Utilisez vos restes de {reste} pour préparer un délicieux plat. "
            f"Astuce : {tip}."
        ),
        "author": "GreenCart",
        "date":   day.strftime("%Y-%m-%d")  # Correction : conversion explicite en string
    })

with app.app_context():
    for post in posts:
        if not BlogPost.query.filter_by(title=post["title"]).first():
            db.session.add(BlogPost(**post))
    db.session.commit()
    print(f"{len(posts)} posts (100) ajoutés à la table blog_posts.")
