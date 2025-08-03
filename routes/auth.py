from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash  # <-- Ajouté

auth_bp = Blueprint('auth', __name__)

# Inscription
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role')  # 'consumer' ou 'producer'

    if not all([email, password, name, role]):
        return jsonify({'error': 'Champs requis manquants'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Utilisateur déjà existant'}), 409

    hashed_pw = generate_password_hash(password)
    user = User(email=email, password=hashed_pw, name=name, role=role)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'Inscription réussie',
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role
        }
    }), 201

# Connexion
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Identifiants invalides'}), 401

    return jsonify({
        'message': 'Connexion réussie',
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role
        }
    }), 200

@auth_bp.route('/users', methods=['GET'])
def list_users():
    from models import User
    users = User.query.all()
    return jsonify([
        {
            'id': u.id,
            'email': u.email,
            'name': u.name,
            'role': u.role,
            'wallet_balance': u.wallet_balance  # Ajout du solde
        }
        for u in users
    ])

@auth_bp.route('/consumers', methods=['GET'])
def get_consumers():
    consumers = User.query.filter_by(role='consumer').all()
    return jsonify([{
        'id': u.id,
        'email': u.email,
        'name': u.name,
        'registered_at': u.registered_at.isoformat()
    } for u in consumers]), 200

@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    # Ajoute ce champ si tu veux permettre l'adresse par défaut
    if hasattr(user, 'default_address'):
        user.default_address = data.get('default_address', getattr(user, 'default_address', None))
    db.session.commit()
    return jsonify({"message": "Profil mis à jour"}), 200

@auth_bp.route('/users/<int:user_id>/password', methods=['PUT'])
def update_user_password(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    new_password = data.get('password')
    if not new_password or len(new_password) < 6:
        return jsonify({"error": "Mot de passe trop court"}), 400
    user.password = generate_password_hash(new_password)  # <-- Correction ici
    db.session.commit()
    return jsonify({"message": "Mot de passe mis à jour"}), 200
