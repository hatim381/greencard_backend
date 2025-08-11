
from flask import Blueprint, request, jsonify
from models import db, User, WithdrawalRequest
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

# Liste des demandes de virement (admin)
@auth_bp.route('/withdrawals', methods=['GET'])
def list_withdrawal_requests():
    withdrawals = WithdrawalRequest.query.order_by(WithdrawalRequest.requested_at.desc()).all()
    result = []
    for w in withdrawals:
        user = User.query.get(w.user_id)
        result.append({
            'id': w.id,
            'user_id': w.user_id,
            'producer_name': user.name if user else '',
            'producer_email': user.email if user else '',
            'amount': w.amount,
            'iban': w.iban,
            'bic': w.bic,
            'rib': w.rib,
            'status': w.status,
            'requested_at': w.requested_at.isoformat() if w.requested_at else ''
        })
    return jsonify(result)

# Suppression (validation) d'une demande de virement (admin)
@auth_bp.route('/withdrawals/<int:withdrawal_id>', methods=['DELETE'])
def delete_withdrawal_request(withdrawal_id):
    withdrawal = WithdrawalRequest.query.get_or_404(withdrawal_id)
    db.session.delete(withdrawal)
    db.session.commit()
    return jsonify({'message': 'Demande de virement supprimée'}), 200

# Demande de virement (producteur)
@auth_bp.route('/withdrawals', methods=['POST'])
def create_withdrawal_request():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')
    iban = data.get('iban')
    bic = data.get('bic')
    rib = data.get('rib')
    if not all([user_id, amount, iban]):
        return jsonify({'error': 'Champs requis manquants'}), 400
    # Vérifie le solde du producteur
    user = User.query.get(user_id)
    if not user or user.role != 'producer':
        return jsonify({'error': 'Utilisateur non trouvé ou non producteur'}), 404
    try:
        amount = float(amount)
    except Exception:
        return jsonify({'error': 'Montant invalide'}), 400
    if user.wallet_balance is None:
        user.wallet_balance = 0.0
    if amount > user.wallet_balance:
        return jsonify({'error': 'Solde insuffisant'}), 400
    # Décrémente le portefeuille
    user.wallet_balance -= amount
    withdrawal = WithdrawalRequest(
        user_id=user_id,
        amount=amount,
        iban=iban,
        bic=bic,
        rib=rib
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

    # Générer le token JWT
    token = create_access_token(identity={
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'role': user.role
    })

    return jsonify({
        'message': 'Connexion réussie',
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'default_address': user.default_address
        },
        'token': token
    }), 200

@auth_bp.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([
        {
            'id': u.id,
            'email': u.email,
            'name': u.name,
            'role': u.role,
            'wallet_balance': u.wallet_balance,
            'default_address': u.default_address
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
