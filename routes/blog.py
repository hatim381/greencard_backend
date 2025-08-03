from flask import Blueprint, jsonify, request
from models import db, BlogPost
from datetime import datetime

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/', methods=['GET'])
def get_blog_posts():
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()
    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "date": p.date.isoformat(),
            "author": p.author
        } for p in posts
    ])

@blog_bp.route('/', methods=['POST'])
def add_blog_post():
    data = request.get_json()
    post = BlogPost(
        title=data.get('title'),
        content=data.get('content'),
        date=datetime.utcnow(),
        author=data.get('author')
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "Post ajouté"}), 201
