from flask import Blueprint, jsonify
from models import Product
import random

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/recommendations', methods=['GET'])
def recommend_products():
    products = Product.query.all()
    if len(products) <= 3:
        selected = products
    else:
        selected = random.sample(products, 3)
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'co2_reduction': p.co2_reduction,
        'dlc': p.dlc.isoformat()
    } for p in selected])
