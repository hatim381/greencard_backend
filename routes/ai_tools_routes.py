from flask import Blueprint, request, jsonify
 # plus besoin de flask_jwt_extended
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

@ai_tools_bp.route('/api/ai/meilleur_produit', methods=['GET'])
def meilleur_produit_route():
    categorie = request.args.get("categorie")
    mois = int(request.args.get("mois"))
    produit = meilleur_produit(categorie, mois)
    return jsonify({"meilleur_produit": produit})
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ai_tools import predict_good_sale, meilleur_produit

ai_tools_bp = Blueprint('ai_tools', __name__)

# Exemple de contrôle de rôle (à adapter selon ton système d'auth)
def is_admin_or_producer(user):
    return user.get("role") in ["admin", "producer"]

@ai_tools_bp.route('/api/ai/predict_good_sale', methods=['POST'])
def predict_good_sale_route():
    data = request.json
    try:
        prediction = predict_good_sale(data)
        return jsonify({"good_sale": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@ai_tools_bp.route('/api/ai/meilleur_produit', methods=['GET'])
def meilleur_produit_route():
    categorie = request.args.get("categorie")
    mois = int(request.args.get("mois"))
    produit = meilleur_produit(categorie, mois)
    return jsonify({"meilleur_produit": produit})
