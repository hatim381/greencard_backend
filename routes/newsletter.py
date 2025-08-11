from flask import Blueprint, request, jsonify
from models import db, NewsletterSubscriber

newsletter_bp = Blueprint('newsletter', __name__)

@newsletter_bp.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.get_json().get('email')
    if not email:
        return jsonify({'error': 'Email requis'}), 400
    if NewsletterSubscriber.query.filter_by(email=email).first():
        return jsonify({'error': 'Déjà inscrit'}), 409
    db.session.add(NewsletterSubscriber(email=email))
    db.session.commit()
    return jsonify({'message': 'Inscription réussie'}), 201

@newsletter_bp.route('/list', methods=['GET'])
def list_subscribers():
    from models import NewsletterSubscriber
    subs = NewsletterSubscriber.query.all()
    return jsonify([s.email for s in subs])
