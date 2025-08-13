from flask import Blueprint, request, jsonify
from models import db, NewsletterSubscriber
from flask_jwt_extended import jwt_required
from utils.security import role_required
from utils.validators import is_valid_email

newsletter_bp = Blueprint('newsletter', __name__)

@newsletter_bp.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.get_json().get('email')
    if not email or not is_valid_email(email):
        return jsonify({'error': 'Email invalide'}), 400
    if NewsletterSubscriber.query.filter_by(email=email).first():
        return jsonify({'error': 'Déjà inscrit'}), 409
    db.session.add(NewsletterSubscriber(email=email))
    db.session.commit()
    return jsonify({'message': 'Inscription réussie'}), 201

@newsletter_bp.route('/list', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_subscribers():
    subs = NewsletterSubscriber.query.all()
    def mask(email):
        name, domain = email.split('@')
        return name[0] + "***@" + domain
    return jsonify([mask(s.email) for s in subs])
