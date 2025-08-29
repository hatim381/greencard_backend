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
        payment_method_types = data.get('payment_method_types')
        preferred_payment_method = data.get('preferred_payment_method')
        
        if not amount:
            return jsonify({'error': 'Montant requis'}), 400
            
        # Configuration pour PaymentIntent
        payment_intent_config = {
            'amount': int(amount),
            'currency': currency,
            'metadata': {
                'integration_check': 'accept_a_payment',
                'platform': 'greencart'
            }
        }
        
        # Si PayPal est demandé spécifiquement
        if payment_method_types and 'paypal' in payment_method_types:
            payment_intent_config['payment_method_types'] = ['paypal']
            payment_intent_config['metadata']['preferred_method'] = 'paypal'
        else:
            # Utiliser automatic_payment_methods pour tous les autres cas
            payment_intent_config['automatic_payment_methods'] = {
                'enabled': True,
            }
        
        # Créer un PaymentIntent Stripe
        intent = stripe.PaymentIntent.create(**payment_intent_config)
        
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
