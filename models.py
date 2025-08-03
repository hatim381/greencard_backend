from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# =============================
# UTILISATEURS
# =============================
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'consumer' ou 'producer'
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    wallet_balance = db.Column(db.Float, default=0.0)  # Solde du portefeuille producteur
    loyalty_points = db.Column(db.Integer, default=0)  # Points de fidélité

    # Relation avec les produits et commandes
    products = db.relationship('Product', backref='producer', lazy=True)
    orders = db.relationship('Order', backref='consumer', lazy=True)
    testimonials = db.relationship('Testimonial', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.email} - {self.role}>'

# =============================
# PRODUITS
# =============================
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))
    status = db.Column(db.String(20))  # 'invendu', 'surplus'
    dlc = db.Column(db.Date, nullable=False)
    co2_reduction = db.Column(db.Integer)  # % de CO2 économisé
    distance_km = db.Column(db.Integer)  # distance entre producteur et client
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    producer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Product {self.name} ({self.status})>'

# =============================
# COMMANDES
# =============================
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    consumer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ordered_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float)
    total_co2_saved = db.Column(db.Float)
    address = db.Column(db.String(255))  # Adresse de livraison
    payment = db.Column(db.String(50))   # Moyen de paiement

    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order #{self.id} by user {self.consumer_id}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="en attente")  # Nouveau champ

    product = db.relationship('Product')

# =============================
# TÉMOIGNAGES CLIENTS
# =============================
class Testimonial(db.Model):
    __tablename__ = 'testimonials'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # ex : 1 à 5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Testimonial by user {self.user_id}>'

# =============================
# NEWSLETTER
# =============================
class NewsletterSubscriber(db.Model):
    __tablename__ = 'newsletter_subscribers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<NewsletterSubscriber {self.email}>'

# =============================
# PANIER UTILISATEUR
# =============================
class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    product = db.relationship('Product')

    def __repr__(self):
        return f'<Cart user={self.user_id} product={self.product_id} qty={self.quantity}>'

# =============================
# ARTICLES DE BLOG
# =============================
class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    author = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<BlogPost {self.title}>'
