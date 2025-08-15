#!/usr/bin/env python3
"""Test simple pour vérifier l'envoi d'email"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email():
    try:
        print("🧪 Test d'envoi d'email...")
        
        # Configuration (même que dans newsletter.py)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "greencart.newsletter@gmail.com"
        sender_password = "vftw hxux wgiv ymhy"
        
        # Email de test
        test_recipient = input("Entrez votre email pour le test: ")
        
        # Message simple
        message = MIMEMultipart()
        message["Subject"] = "🧪 Test GreenCart Newsletter"
        message["From"] = sender_email
        message["To"] = test_recipient
        
        body = "Ceci est un test d'envoi d'email depuis GreenCart ! 🌱"
        message.attach(MIMEText(body, "plain"))
        
        print("📤 Tentative de connexion à Gmail...")
        
        # Envoi
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            print("🔐 Activation TLS...")
            server.starttls()
            
            print("🔑 Connexion avec les identifiants...")
            server.login(sender_email, sender_password)
            
            print("📧 Envoi de l'email...")
            server.sendmail(sender_email, test_recipient, message.as_string())
            
        print("✅ Email envoyé avec succès !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    test_email()
