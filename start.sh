#!/bin/bash

echo "🚀 Démarrage GreenCart avec Litestream + GitHub..."

# Aller dans le bon répertoire
cd /opt/render/project/src

# ACTIVER L'ENVIRONNEMENT VIRTUEL  
echo "🔧 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Variables d'environnement
export RENDER=true
export PATH="/opt/render/project/bin:/usr/local/bin:$PATH"

# Chemins
DB_PATH="/opt/render/project/src/db/greencart.db"
CONFIG_PATH="/opt/render/project/src/litestream.yml"

# Créer les dossiers nécessaires
mkdir -p /opt/render/project/src/db
mkdir -p /opt/render/project/src/litestream-backups

# Créer la DB si elle n'existe pas
if [ ! -f "$DB_PATH" ]; then
    echo "🔧 Initialisation de la base de données..."
    python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Base de données initialisée')
"
fi

# Démarrer l'application Flask
echo "🌐 Démarrage de l'application Flask..."
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
