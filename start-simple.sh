#!/bin/bash

echo "🚀 Démarrage GreenCart (version simple)..."

# Variables d'environnement
export RENDER=true

# Créer le dossier DB basique
mkdir -p /opt/render/project/src/db

# Aller dans le bon répertoire
cd /opt/render/project/src

# Vérifier que Flask est installé
echo "� Vérification des modules Python..."
python3 -c "import flask; print('✅ Flask trouvé:', flask.__version__)" || echo "❌ Flask non trouvé"
python3 -c "import gunicorn; print('✅ Gunicorn trouvé')" || echo "❌ Gunicorn non trouvé"

# Initialiser la base de données 
echo "🔧 Initialisation de la base de données..."
python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Base de données initialisée')
" || echo "⚠️ Erreur initialisation DB"

# Démarrer l'application Flask avec le chemin complet
echo "🌐 Démarrage de l'application Flask..."
python3 -m gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
