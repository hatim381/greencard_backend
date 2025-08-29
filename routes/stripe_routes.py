from flask import Blueprint, request, jsonify
import stripe
import os

stripe_bp = Blueprint('stripe', __name__)

# Configuration Stripe - utilise les variables d'environnement
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@stripe_bp.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.get_json()
        amount = data.get('amount')  # en centimes (ex: 1550 pour 15.50€)
        currency = data.get('currency', 'eur')
        
        if not amount:
            return jsonify({'error': 'Montant requis'}), 400
            
        # Créer un PaymentIntent Stripe avec toutes les méthodes automatiques
        intent = stripe.PaymentIntent.create(
            amount=int(amount),
            currency=currency,
            automatic_payment_methods={
                'enabled': True,
            },
            metadata={
                'integration_check': 'accept_a_payment',
                'platform': 'greencart'
            }
        )
        
        return jsonify({
            'client_secret': intent.client_secret,
            'payment_intent_id': intent.id
        }), 200
        
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stripe_bp.route('/confirm-payment', methods=['POST'])
def confirm_payment():
    try:
        data = request.get_json()
        payment_intent_id = data.get('payment_intent_id')
        
        if not payment_intent_id:
            return jsonify({'error': 'payment_intent_id requis'}), 400
            
        # Récupérer le PaymentIntent pour vérifier son statut
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if intent.status == 'succeeded':
            return jsonify({
                'status': 'success',
                'payment_intent': {
                    'id': intent.id,
                    'amount': intent.amount,
                    'currency': intent.currency,
                    'status': intent.status
                }
            }), 200
        else:
            return jsonify({
                'status': 'failed',
                'message': f'Paiement en statut: {intent.status}'
            }), 400
            
    except stripe.error.StripeError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
