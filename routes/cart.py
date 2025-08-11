# === cart.py ===
from flask import Blueprint, request, jsonify
from models import db, Cart, Product
from flask_jwt_extended import jwt_required, get_jwt_identity

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "product_id": item.product.id,
            "name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity
        } for item in cart_items
    ])

@cart_bp.route('/', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Produit introuvable"}), 404

    existing_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(new_item)

    db.session.commit()
    return jsonify({"message": "Produit ajouté au panier"}), 201

@cart_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(product_id):
    user_id = get_jwt_identity()
    item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Produit supprimé du panier"})
    else:
        return jsonify({"error": "Produit non trouvé dans le panier"}), 404
