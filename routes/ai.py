from flask import Blueprint, jsonify
from models import Product
from datetime import datetime
import ai_tools

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/recommendations', methods=['GET'])
def recommend_products():
    mois = datetime.now().month
    # Récupère toutes les catégories présentes dans la base
    categories = [c[0] for c in Product.query.with_entities(Product.category).distinct().all() if c[0]]
    # Priorité d'affichage
    priority = ['Fruits', 'Légumes']
    # Trie les catégories : Fruits, Légumes d'abord, puis le reste
    categories_sorted = priority + [c for c in categories if c not in priority]
    recommendations = []
    for cat in categories_sorted:
        # Cherche le meilleur produit du mois pour la catégorie
        best_name = ai_tools.meilleur_produit(cat, mois)
        product = None
        if best_name:
            product = Product.query.filter_by(name=best_name, category=cat).order_by(Product.dlc.desc()).first()
        # Si aucun produit trouvé, prend n'importe quel produit de la catégorie
        if not product:
            product = Product.query.filter_by(category=cat).order_by(Product.dlc.desc()).first()
        if product:
            recommendations.append({
                'id': product.id,
                'name': product.name,
                'category': product.category,
                'co2_reduction': product.co2_reduction,
                'dlc': product.dlc.isoformat() if product.dlc else None
            })
    return jsonify(recommendations)
