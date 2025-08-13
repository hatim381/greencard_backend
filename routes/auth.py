
from flask import Blueprint, request, jsonify
from models import db, User, WithdrawalRequest
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, set_access_cookies
)
from utils.security import role_required, encrypt_data
from utils.validators import is_valid_email, is_valid_iban, is_valid_bic

auth_bp = Blueprint('auth', __name__)

# Liste des demandes de virement (admin)
@auth_bp.route('/withdrawals', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_withdrawal_requests():
    withdrawals = WithdrawalRequest.query.order_by(WithdrawalRequest.requested_at.desc()).all()
    result = []
    for w in withdrawals:
        user = User.query.get(w.user_id)
        result.append({
            'id': w.id,
            'producer_name': user.name if user else '',
            'amount': w.amount,
            'status': w.status,
            'requested_at': w.requested_at.isoformat() if w.requested_at else ''
        })
    return jsonify(result)

# Suppression (validation) d'une demande de virement (admin)
@auth_bp.route('/withdrawals/<int:withdrawal_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_withdrawal_request(withdrawal_id):
    withdrawal = WithdrawalRequest.query.get_or_404(withdrawal_id)
    db.session.delete(withdrawal)
    db.session.commit()
    return jsonify({'message': 'Demande de virement supprimée'}), 200

# Demande de virement (producteur)
@auth_bp.route('/withdrawals', methods=['POST'])
@jwt_required()
@role_required('producer')
def create_withdrawal_request():
    data = request.get_json() or {}
    amount = data.get('amount')
    iban = data.get('iban')
    bic = data.get('bic')
    rib = data.get('rib')
    if not all([amount, iban]):
        return jsonify({'error': 'Champs requis manquants'}), 400
    if not is_valid_iban(iban) or (bic and not is_valid_bic(bic)):
        return jsonify({'error': 'IBAN/BIC invalide'}), 400
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except Exception:
        return jsonify({'error': 'Montant invalide'}), 400
    identity = get_jwt_identity()
    user_id = identity['id'] if isinstance(identity, dict) else identity
    user = User.query.get(user_id)
    if user.wallet_balance is None:
        user.wallet_balance = 0.0
    if amount > user.wallet_balance:
        return jsonify({'error': 'Solde insuffisant'}), 400
    # Décrémente le portefeuille
    user.wallet_balance -= amount
    withdrawal = WithdrawalRequest(
        user_id=user_id,
        amount=amount,
        iban=encrypt_data(iban),
        bic=encrypt_data(bic) if bic else None,
        rib=encrypt_data(rib) if rib else None
    )
    db.session.add(withdrawal)
    db.session.commit()
    return jsonify({'message': 'Demande de virement envoyée', 'withdrawal_id': withdrawal.id, 'new_wallet_balance': user.wallet_balance}), 201

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
    if not is_valid_email(email):
        return jsonify({'error': 'Email invalide'}), 400
    if role not in ['consumer', 'producer', 'admin']:
        return jsonify({'error': 'Rôle invalide'}), 400

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

    # Générer le token JWT et le placer dans un cookie sécurisé
    token = create_access_token(identity={
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'role': user.role
    })
    response = jsonify({
        'message': 'Connexion réussie',
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'default_address': user.default_address
        }
    })
    set_access_cookies(response, token)
    return response, 200

@auth_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_users():
    users = User.query.all()
    return jsonify([
        {
            'id': u.id,
            'name': u.name,
            'role': u.role
        }
        for u in users
    ])

@auth_bp.route('/consumers', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_consumers():
    consumers = User.query.filter_by(role='consumer').all()
    return jsonify([{
        'id': u.id,
        'name': u.name,
        'registered_at': u.registered_at.isoformat()
    } for u in consumers]), 200

@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_profile(user_id):
    identity = get_jwt_identity()
    if identity['id'] != user_id and identity.get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    if hasattr(user, 'default_address'):
        user.default_address = data.get('default_address', getattr(user, 'default_address', None))
    db.session.commit()
    return jsonify({"message": "Profil mis à jour"}), 200

@auth_bp.route('/users/<int:user_id>/password', methods=['PUT'])
@jwt_required()
def update_user_password(user_id):
    identity = get_jwt_identity()
    if identity['id'] != user_id and identity.get('role') != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    new_password = data.get('password')
    if not new_password or len(new_password) < 6:
        return jsonify({"error": "Mot de passe trop court"}), 400
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "Mot de passe mis à jour"}), 200
