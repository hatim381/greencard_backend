#!/bin/bash

echo "🚀 Démarrage GreenCart (version simple)..."

# Variables d'environnement
export RENDER=true

# Créer le dossier DB basique
mkdir -p /opt/render/project/src/db

# Initialiser la base de données sans Litestream d'abord
echo "🔧 Initialisation de la base de données..."
python3 -c "
import os
import sys
sys.path.append('/opt/render/project/src')
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Base de données initialisée')
" || echo "⚠️ Erreur initialisation DB"

# Démarrer l'application Flask directement
echo "🌐 Démarrage de l'application Flask..."
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
