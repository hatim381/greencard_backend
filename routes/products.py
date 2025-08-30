from flask import Blueprint, request, jsonify
from models import db, Product, User
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename

products_bp = Blueprint('products', __name__)

# Dossier d'upload : <backend_root>/uploads
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def serialize_product(p: Product) -> dict:
    if p is None:
        return None
    return {
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
        'producer': getattr(p.producer, 'name', None),
        'producer_id': p.producer_id,
        'image_url': p.image_url,
        'created_at': p.created_at.isoformat() if p.created_at else None,
    }

# ===========================
# GET / - Liste des produits
# ===========================
@products_bp.route('/', methods=['GET'])
@products_bp.route('', methods=['GET'])  # Accepter sans slash
def get_products():
    products = Product.query.all()
    # Filtrer les objets None et sérialiser
    serialized_products = [serialize_product(p) for p in products if p is not None]
    # Filtrer les résultats None de la sérialisation
    serialized_products = [p for p in serialized_products if p is not None]
    return jsonify(serialized_products), 200

# ===========================
# POST / - Ajouter un produit
# ===========================
@products_bp.route('/', methods=['POST'])
def add_product():
    # Accepte JSON ou multipart/form-data
    is_multipart = bool(request.content_type and request.content_type.startswith('multipart/form-data'))
    data = request.form if is_multipart else (request.get_json(silent=True) or {})
    file = request.files.get('image') if is_multipart else None

    # Champs obligatoires
    required = ['name', 'price', 'quantity', 'producer_id', 'dlc']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'Champ obligatoire manquant: {field}'}), 400

    # Conversions et validations
    try:
        name = data.get('name').strip()
        price = float(data.get('price'))
        quantity = int(data.get('quantity'))
        producer_id = int(data.get('producer_id'))
        dlc_str = data.get('dlc')
        try:
            dlc = datetime.strptime(dlc_str, '%Y-%m-%d').date()
        except Exception:
            return jsonify({'error': "Format de date DLC invalide. Utilisez AAAA-MM-JJ."}), 400

        # Optionnels
        description = data.get('description')
        category = data.get('category')
        status = data.get('status')
        co2_reduction = int(data['co2_reduction']) if data.get('co2_reduction') not in (None, '', 'null') else None
        distance_km = int(data['distance_km']) if data.get('distance_km') not in (None, '', 'null') else None

        # Vérifier que le producer existe (facultatif mais sain)
        if not User.query.get(producer_id):
            return jsonify({'error': "Producer introuvable."}), 400

        # Image
        image_url = None
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(filepath)
            image_url = f"/uploads/{unique_name}"
        elif data.get('image_url'):
            # Permet d'utiliser une URL distante si fournie
            image_url = data.get('image_url')

        product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category=category,
            status=status,
            dlc=dlc,
            co2_reduction=co2_reduction,
            distance_km=distance_km,
            producer_id=producer_id,
            image_url=image_url
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Produit ajouté avec succès', 'product': serialize_product(product)}), 201

    except ValueError as ve:
        return jsonify({'error': f'Valeur invalide: {str(ve)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ===========================
# PUT /<id> - Modifier produit
# ===========================
@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    is_multipart = bool(request.content_type and request.content_type.startswith('multipart/form-data'))
    data = request.form if is_multipart else (request.get_json(silent=True) or {})
    file = request.files.get('image') if is_multipart else None

    product = Product.query.get_or_404(product_id)

    try:
        # Champs texte
        if data.get('name') is not None:
            product.name = data.get('name').strip()
        if data.get('description') is not None:
            product.description = data.get('description')
        if data.get('category') is not None:
            product.category = data.get('category')
        if data.get('status') is not None:
            product.status = data.get('status')

        # Numériques
        if data.get('price') not in (None, ''):
            product.price = float(data.get('price'))
        if data.get('quantity') not in (None, ''):
            product.quantity = int(data.get('quantity'))
        if data.get('producer_id') not in (None, ''):
            new_producer_id = int(data.get('producer_id'))
            if not User.query.get(new_producer_id):
                return jsonify({'error': "Producer introuvable."}), 400
            product.producer_id = new_producer_id
        if data.get('co2_reduction') not in (None, '', 'null'):
            product.co2_reduction = int(data.get('co2_reduction'))
        if data.get('distance_km') not in (None, '', 'null'):
            product.distance_km = int(data.get('distance_km'))

        # Date
        if data.get('dlc'):
            try:
                product.dlc = datetime.strptime(data.get('dlc'), '%Y-%m-%d').date()
            except Exception:
                return jsonify({'error': "Format de date DLC invalide. Utilisez AAAA-MM-JJ."}), 400

        # Image
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(filepath)
            product.image_url = f"/uploads/{unique_name}"
        elif data.get('image_url'):
            # Permet de remplacer par une URL externe si fournie
            product.image_url = data.get('image_url')

        db.session.commit()
        return jsonify({'message': 'Produit modifié avec succès', 'product': serialize_product(product)}), 200

    except ValueError as ve:
        return jsonify({'error': f'Valeur invalide: {str(ve)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ===========================
# DELETE /<id> - Supprimer produit
# ===========================
@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        
        # Optionnel : supprimer le fichier image du disque
        if product.image_url and product.image_url.startswith('/uploads/'):
            try:
                image_path = os.path.join(UPLOAD_FOLDER, os.path.basename(product.image_url))
                if os.path.exists(image_path):
                    os.remove(image_path)
            except Exception:
                pass  # On continue même si la suppression de l'image échoue
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Produit supprimé avec succès'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
