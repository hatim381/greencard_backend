from flask import Blueprint, request, jsonify, current_app
from models import db, Product, User
from datetime import datetime
import os
from werkzeug.utils import secure_filename

products_bp = Blueprint('products', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Obtenir tous les produits
@products_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'quantity': p.quantity,
        'category': p.category,
        'status': p.status,
        'dlc': p.dlc.isoformat() if p.dlc else None,
        'co2_reduction': p.co2_reduction,
        'distance_km': p.distance_km,
        'producer': p.producer.name,
        'producer_id': p.producer_id,
        'image_url': p.image_url
    } for p in products]), 200

# Ajouter un produit
@products_bp.route('/', methods=['POST'])
def add_product():
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        data = request.form
        file = request.files.get('image')
    else:
        data = request.get_json()
        file = None

    required = ['name', 'price', 'quantity', 'producer_id', 'dlc']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Champ obligatoire manquant: {field}'}), 400
    try:
        try:
            dlc = datetime.strptime(data.get('dlc'), '%Y-%m-%d')
        except Exception:
            return jsonify({'error': 'Format de date DLC invalide. Utilisez AAAA-MM-JJ.'}), 400

        image_url = None
        if file and allowed_file(file.filename):
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            image_url = f"/uploads/{filename}"
        elif data.get('image_url'):
            image_url = data.get('image_url')

        product = Product(
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            quantity=data.get('quantity'),
            category=data.get('category'),
            status=data.get('status'),
            dlc=dlc,
            co2_reduction=data.get('co2_reduction'),
            distance_km=data.get('distance_km'),
            producer_id=data.get('producer_id'),
            image_url=image_url
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Produit ajouté avec succès'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        data = request.form
        file = request.files.get('image')
    else:
        data = request.get_json()
        file = None

    product = Product.query.get_or_404(product_id)
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.quantity = data.get('quantity', product.quantity)
    product.category = data.get('category', product.category)
    product.dlc = datetime.strptime(data.get('dlc'), '%Y-%m-%d') if data.get('dlc') else product.dlc

    if file and allowed_file(file.filename):
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        product.image_url = f"/uploads/{filename}"
    elif data.get('image_url'):
        product.image_url = data.get('image_url')

    db.session.commit()
    return jsonify({'message': 'Produit modifié avec succès'}), 200
