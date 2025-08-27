#!/bin/bash

echo "🚀 Démarrage ultra-simple..."

# Aller dans le bon répertoire  
cd /opt/render/project/src

# ACTIVER L'ENVIRONNEMENT VIRTUEL
echo "🔧 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Test basique
echo "📍 Répertoire actuel: $(pwd)"
echo " Version Python: $(python3 --version)"
echo "📦 Pip location: $(which pip)"

# Test des modules après activation
echo "🔍 Test modules après activation..."
python3 -c "
import flask
print('✅ Flask version:', flask.__version__)
import gunicorn
print('✅ Gunicorn disponible')
"

# Démarrer Flask directement
echo "🌐 Démarrage Flask basique..."
python3 -c "
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello from Render!', 'status': 'success'}

@app.route('/health')  
def health():
    return {'status': 'ok', 'service': 'greencard-backend'}

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print(f'🚀 Démarrage sur le port {port}')
    app.run(host='0.0.0.0', port=port)
"
