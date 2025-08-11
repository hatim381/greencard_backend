from flask import Blueprint, request, jsonify
from models import db, Testimonial

testimonials_bp = Blueprint('testimonials', __name__)

@testimonials_bp.route('/', methods=['POST'])
def add_testimonial():
    data = request.get_json()
    t = Testimonial(
        user_id=data.get('user_id'),
        message=data.get('message'),
        rating=data.get('rating')
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({'message': 'Avis enregistré'}), 201

@testimonials_bp.route('/', methods=['GET'])
def list_testimonials():
    items = Testimonial.query.all()
    return jsonify([{
        'id': t.id,
        'message': t.message,
        'rating': t.rating,
        'user_id': t.user_id
    } for t in items]), 200
