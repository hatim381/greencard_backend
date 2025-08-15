from flask import Blueprint, request, jsonify
from models import db, NewsletterSubscriber
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

newsletter_bp = Blueprint('newsletter', __name__)

def send_welcome_email(email):
    """Envoie un email de bienvenue"""
    try:
        # Configuration email (MODIFIEZ ICI vos informations)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "greencart.newsletter@gmail.com"  # ← REMPLACEZ par votre email Gmail
        sender_password = "vftw hxux wgiv ymhy"  # ← REMPLACEZ par votre mot de passe d'application
        
        # Création du message
        message = MIMEMultipart("alternative")
        message["Subject"] = "🌱 Bienvenue dans la communauté GreenCart !"
        message["From"] = f"GreenCart <{sender_email}>"
        message["To"] = email
        
        # Contenu HTML de l'email
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f8fffe; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; }}
                .header {{ background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%); padding: 30px; text-align: center; }}
                .header h1 {{ color: white; margin: 0; font-size: 28px; font-weight: 700; }}
                .content {{ padding: 40px 30px; }}
                .content h2 {{ color: #22C55E; font-size: 24px; margin-bottom: 20px; }}
                .content p {{ color: #374151; line-height: 1.6; font-size: 16px; margin-bottom: 15px; }}
                .highlight {{ background-color: #DCFCE7; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                .footer {{ background-color: #1F2937; color: #D1D5DB; padding: 20px; text-align: center; font-size: 14px; }}
                .button {{ background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; display: inline-block; font-weight: 600; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌱 GreenCart</h1>
                    <p style="color: #E0F2FE; margin: 10px 0 0 0; font-size: 18px;">Bienvenue dans notre communauté !</p>
                </div>
                
                <div class="content">
                    <h2>Merci de votre inscription ! 🎉</h2>
                    
                    <p>Bonjour et bienvenue chez <strong>GreenCart</strong> !</p>
                    
                    <p>Nous sommes ravis que vous rejoigniez notre communauté de consommateurs soucieux de l'environnement. En vous abonnant à notre newsletter, vous faites un pas de plus vers une alimentation plus durable et responsable.</p>
                    
                    <div class="highlight">
                        <h3 style="color: #22C55E; margin-top: 0;">🌍 Ce que vous allez recevoir :</h3>
                        <ul style="margin: 15px 0;">
                            <li>🍅 <strong>Produits locaux exclusifs</strong> de nos producteurs partenaires</li>
                            <li>💡 <strong>Conseils anti-gaspillage</strong> pour réduire votre impact environnemental</li>
                            <li>🎁 <strong>Offres spéciales</strong> et promotions réservées aux abonnés</li>
                            <li>📚 <strong>Recettes créatives</strong> pour utiliser vos produits frais</li>
                        </ul>
                    </div>
                    
                    <p>Notre mission est simple : connecter les consommateurs avec des producteurs locaux pour une alimentation plus fraîche, plus saine et plus respectueuse de l'environnement.</p>
                    
                    <center>
                        <a href="https://greencard-frontend.vercel.app/products" class="button">
                            🛒 Découvrir nos produits
                        </a>
                    </center>
                    
                    <p><strong>Ensemble, construisons un avenir plus vert ! 🌱</strong></p>
                    
                    <p>L'équipe GreenCart</p>
                </div>
                
                <div class="footer">
                    <p>📧 Vous recevez cet email car vous vous êtes inscrit(e) à notre newsletter.</p>
                    <p>GreenCart - Pour une alimentation durable et anti-gaspillage</p>
                    <p style="font-size: 12px; margin-top: 15px;">
                        © 2024 GreenCart. Tous droits réservés.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Ajout du contenu HTML
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Envoi de l'email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
            
        return True
        
    except Exception as e:
        print(f"Erreur envoi email: {e}")
        return False

@newsletter_bp.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.get_json().get('email')
    if not email:
        return jsonify({'error': 'Email requis'}), 400
    if NewsletterSubscriber.query.filter_by(email=email).first():
        return jsonify({'error': 'Déjà inscrit'}), 409
    
    # Ajout en base de données
    db.session.add(NewsletterSubscriber(email=email))
    db.session.commit()
    
    # Envoi de l'email de bienvenue
    email_sent = send_welcome_email(email)
    
    if email_sent:
        return jsonify({'message': 'Inscription réussie et email de bienvenue envoyé'}), 201
    else:
        return jsonify({'message': 'Inscription réussie (email non envoyé)'}), 201

@newsletter_bp.route('/list', methods=['GET'])
def list_subscribers():
    from models import NewsletterSubscriber
    subs = NewsletterSubscriber.query.all()
    return jsonify([s.email for s in subs])
