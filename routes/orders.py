from flask import Blueprint, request, jsonify
from models import db, Order, OrderItem, Product, User
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

orders_bp = Blueprint('orders', __name__)

# Créer une commande
@orders_bp.route('/', methods=['POST'])
def create_order():
    print("DEBUG - Données reçues :", request.get_json())  # Ajoute cette ligne
    try:
        data = request.get_json()
        print("DEBUG - Données reçues pour la commande :", data)  # Ajoute ce log

        consumer_id = data.get('consumer_id')
        items = data.get('items')  # liste : [{product_id, quantity}, ...]
        address = data.get('address')
        payment = data.get('payment')

        if not consumer_id or not items:
            return jsonify({'error': 'Requête invalide'}), 400
        if not address or not payment:
            return jsonify({'error': 'Adresse et paiement requis'}), 400

        # Simulation du paiement CB
        if payment == "cb":
            # Ici tu pourrais intégrer Stripe ou autre, ou simuler
            # Pour la démo, on simule un paiement toujours accepté
            pass  # Si tu veux simuler un échec, tu peux lever une exception ici

        total_price = 0
        total_co2 = 0
        order = Order(
            consumer_id=consumer_id,
            ordered_at=datetime.utcnow(),
            address=address,
            payment=payment
        )
        db.session.add(order)
        db.session.flush()

        for item in items:
            product = Product.query.get(item['product_id'])
            if not product or product.quantity < item['quantity']:
                return jsonify({'error': f"Produit {item['product_id']} indisponible ou quantité insuffisante"}), 400

            product.quantity -= item['quantity']
            total_price += product.price * item['quantity']
            # Sécurise le calcul du CO2
            co2 = product.co2_reduction if product.co2_reduction is not None else 0
            total_co2 += co2 * item['quantity']

            db.session.add(OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item['quantity'],
                unit_price=product.price
            ))

            # NE PAS créditer les portefeuilles ici !

        order.total_price = total_price
        order.total_co2_saved = total_co2
        db.session.commit()
        # Ajout des points de fidélité
        try:
            user = User.query.get(consumer_id)
            if user:
                points = int(order.total_price or 0)
                user.loyalty_points = (user.loyalty_points or 0) + points
                db.session.commit()
        except Exception as e:
            print("Erreur fidélité :", e)
        return jsonify({'message': 'Commande créée'}), 201
    except Exception as e:
        print("Erreur lors de la création de la commande :", e)  # Affiche l'erreur dans le terminal
        import traceback; traceback.print_exc()  # Affiche la stacktrace complète
        return jsonify({'error': str(e)}), 500

# Liste des commandes par user
@orders_bp.route('/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    print("API /api/orders/ appelé avec user_id =", user_id)
    orders = Order.query.filter_by(consumer_id=user_id).all()
    # Toujours retourner une liste, même vide
    return jsonify([{
        'id': o.id,
        'date': o.ordered_at.isoformat(),
        'total_price': o.total_price,
        'total_co2_saved': o.total_co2_saved
    } for o in orders]), 200

@orders_bp.route('/', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    return jsonify([
        {
            'id': o.id,
            'consumer_id': o.consumer_id,
            'ordered_at': o.ordered_at.isoformat() if o.ordered_at else None,
            'total_price': o.total_price,
            'total_co2_saved': o.total_co2_saved,
            'address': o.address,
            'payment': o.payment
        }
        for o in orders
    ]), 200

@orders_bp.route('/orderitem/<int:item_id>/status', methods=['PUT'])
def update_orderitem_status(item_id):
    data = request.get_json()
    status = data.get('status')
    item = OrderItem.query.get_or_404(item_id)
    old_status = item.status
    item.status = status

    # Créditer le portefeuille seulement si on passe à "traitée" et que ce n'était pas déjà le cas
    if status == "traitée" and old_status != "traitée":
        product = Product.query.get(item.product_id)
        commission_rate = 0.10
        montant_commission = item.unit_price * item.quantity * commission_rate
        montant_producteur = item.unit_price * item.quantity * (1 - commission_rate)
        producer = product.producer
        producer.wallet_balance = (producer.wallet_balance or 0) + montant_producteur
        db.session.add(producer)
        # Créditer le owner
        owner = db.session.query(User).filter_by(role='owner').first()
        if owner:
            owner.wallet_balance = (owner.wallet_balance or 0) + montant_commission
            db.session.add(owner)

    db.session.commit()
    return jsonify({'message': 'Statut mis à jour'}), 200

@orders_bp.route('/producer/<int:producer_id>', methods=['GET'])
def get_orders_for_producer(producer_id):
    # Récupère toutes les commandes contenant au moins un produit du producteur
    order_items = OrderItem.query.join(Product).filter(Product.producer_id == producer_id).all()
    orders_dict = {}
    for item in order_items:
        o = item.order
        if o.id not in orders_dict:
            orders_dict[o.id] = {
                'order_id': o.id,
                'ordered_at': o.ordered_at.isoformat() if o.ordered_at else None,
                'total_price': 0,
                'products': [],
                'consumer_id': o.consumer_id,
                'address': o.address  # Ajout de l'adresse de livraison
            }
        orders_dict[o.id]['products'].append({
            'orderitem_id': item.id,  # Pour l'action sur le statut
            'product_id': item.product_id,
            'name': item.product.name,
            'quantity': item.quantity,
            'unit_price': item.unit_price,
            'status': item.status
        })
        orders_dict[o.id]['total_price'] += item.unit_price * item.quantity
    return jsonify(list(orders_dict.values())), 200

# La route create_order est déjà correcte, rien à changer ici si le modèle Order est à jour.
