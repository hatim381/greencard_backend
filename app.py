from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from models import db
import os
from flask_jwt_extended import JWTManager

# === Création de l'application ===
app = Flask(__name__)

# === CORS pour autoriser le front Vercel + dev local ===
ALLOWED_ORIGINS = [
    "https://greencard-fronted.vercel.app",  # prod vercel (attention: 'fronted' sans le 'n')
    "http://localhost:3000",                 # dev create-react-app
    "http://localhost:5173"                  # dev Vite
]

# On autorise les routes API + uploads. Pas de credentials (cookies) côté front.
CORS(app, resources={
    r"/api/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "max_age": 3600
    },
    r"/uploads/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "max_age": 3600
    }
})

# === Configuration BDD ===
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    # Correction du schéma pour SQLAlchemy (Render)
    database_url = database_url.replace("postgres://", "postgresql://", 1)

if not database_url:
    # Fallback local (dev) si DATABASE_URL n'est pas défini
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_url = f"sqlite:///{os.path.join(basedir, 'db', 'greencart.db')}"

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# === JWT ===
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
jwt = JWTManager(app)

# === Dossier uploads ===
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# === Initialisation DB ===
db.init_app(app)
with app.app_context():
    # Crée le dossier DB en local si besoin
    os.makedirs(os.path.join(os.path.dirname(__file__), "db"), exist_ok=True)
    db.create_all()

# === Healthchecks ===
@app.get("/health")
def health_root():
    return jsonify(status="ok", service="greencard-backend"), 200

@app.get("/api/health")
def health_api():
    return jsonify(status="ok", service="greencard-backend"), 200

# === Accueil API ===
@app.get("/")
def index():
    return {'message': 'Bienvenue sur l’API GreenCart 🎉'}

# === Fichiers uploads ===
@app.get("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# === Import & enregistrement des blueprints ===
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
    # En prod (Render) tu utilises gunicorn; ce run() est pour le dev local
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
