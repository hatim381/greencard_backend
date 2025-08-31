from flask import Blueprint, request, jsonify
from ai_tools import predict_good_sale, meilleur_produit

ai_tools_bp = Blueprint('ai_tools', __name__)

@ai_tools_bp.route('/api/ai/predict_good_sale', methods=['POST'])
def predict_good_sale_route():
    data = request.json
    try:
        # On ne garde que produit, categorie, mois
        filtered = {
            "produit": data.get("produit"),
            "categorie": data.get("categorie"),
            "mois": int(data.get("mois"))
        }
        prediction = predict_good_sale(filtered)
        return jsonify({"good_sale": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@ai_tools_bp.route('/api/ai/best_product', methods=['POST'])
def best_product_route():
    data = request.json
    try:
        categorie = data.get("categorie")
        mois = int(data.get("mois"))
        produit = meilleur_produit(categorie, mois)
        return jsonify({"best_product": produit})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
