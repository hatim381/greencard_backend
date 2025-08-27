#!/bin/bash

echo "🚀 Démarrage GreenCart (version simple)..."

# Variables d'environnement
export RENDER=true
export PATH="/usr/local/bin:$PATH"

# Chemins
DB_PATH="/opt/render/project/src/db/greencart.db"

# Créer le dossier de la base de données
mkdir -p /opt/render/project/src/db

echo "🔧 Initialisation de la base de données..."
python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Base de données initialisée')
"

# Démarrer l'application Flask
echo "🌐 Démarrage de l'application Flask..."
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
