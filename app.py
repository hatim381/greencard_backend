from flask import Flask, send_from_directory
from flask_cors import CORS
from models import db
import os
from flask_jwt_extended import JWTManager

# === Création de l'application ===
app = Flask(__name__)
# === CORS pour autoriser le front Vercel ===
ALLOWED_ORIGINS = [
    "https://greencard-fronted.vercel.app",
    "https://greencard-frontend.vercel.app",
    "http://localhost:3000"  # gardé pour le développement local
]

CORS(app, resources={
    r"/api/*": {"origins": ALLOWED_ORIGINS},
    r"/uploads/*": {"origins": ALLOWED_ORIGINS}
})


# === Configuration BDD ===
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    # Correction du schéma pour SQLAlchemy
    database_url = database_url.replace("postgres://", "postgresql://", 1)

if not database_url:
    # fallback local (dev) si DATABASE_URL n'est pas défini
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_url = f"sqlite:///{os.path.join(basedir, 'db', 'greencart.db')}"

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')  # Ajout pour JWT
# Correction pour JWT: ajout du token location et du header name
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')


# === Initialisation JWT ===
jwt = JWTManager(app)

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

# === Import des routes ===
from routes.auth import auth_bp
from routes.products import products_bp
from routes.orders import orders_bp
from routes.ai import ai_bp
from routes.testimonials import testimonials_bp
from routes.newsletter import newsletter_bp
from routes.cart import cart_bp
from routes.blog import blog_bp
from routes.ai_tools_routes import ai_tools_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(ai_bp, url_prefix='/api/ai')
app.register_blueprint(testimonials_bp, url_prefix='/api/testimonials')
app.register_blueprint(newsletter_bp, url_prefix='/api/newsletter')
app.register_blueprint(cart_bp, url_prefix='/api/cart')
app.register_blueprint(blog_bp, url_prefix='/api/blog')
app.register_blueprint(ai_tools_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
