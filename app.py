from flask import Flask, send_from_directory
from flask_cors import CORS
from models import db
import os

# === Création de l'application ===
app = Flask(__name__)

# === Autoriser les appels du frontend Vercel ===
CORS(app, resources={
    r"/api/*": {"origins": "https://greencard-fronted.vercel.app"},
    r"/uploads/*": {"origins": "https://greencard-fronted.vercel.app"}
}, supports_credentials=True)

# === Configuration ===
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'db', 'greencart.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# === Initialisation de la base de données ===
db.init_app(app)

# === Création des tables si elles n'existent pas ===
with app.app_context():
    if not os.path.exists("db"):
        os.makedirs("db")
    db.create_all()

# === Route de test ===
@app.route('/')
def index():
    return {'message': 'Bienvenue sur l’API GreenCart 🎉'}

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# === En-têtes CORS forcés (utile pour Render) ===
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://greencard-fronted.vercel.app'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

# === Import des routes ===
from routes.auth import auth_bp
from routes.products import products_bp
from routes.orders import orders_bp
from routes.ai import ai_bp
from routes.testimonials import testimonials_bp
from routes.newsletter import newsletter_bp
from routes.cart import cart_bp
from routes.blog import blog_bp

# === Enregistrement des blueprints ===
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(ai_bp, url_prefix='/api/ai')
app.register_blueprint(testimonials_bp, url_prefix='/api/testimonials')
app.register_blueprint(newsletter_bp, url_prefix='/api/newsletter')
app.register_blueprint(cart_bp, url_prefix='/api/cart')
app.register_blueprint(blog_bp, url_prefix='/api/blog')

# === Lancement local ===
if __name__ == '__main__':
    app.run(debug=True, port=5000)
