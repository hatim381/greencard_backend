#!/bin/bash

echo "🚀 Démarrage ultra-simple..."

# Aller dans le bon répertoire  
cd /opt/render/project/src

# Test basique
echo "📍 Répertoire actuel: $(pwd)"
echo "📁 Contenu:"
ls -la

# Test Python
echo "🐍 Version Python: $(python3 --version)"

# Test des modules de base
echo "🔍 Test modules..."
python3 -c "print('Python fonctionne')"

# Démarrer Flask directement sans gunicorn d'abord
echo "🌐 Démarrage Flask basique..."
python3 -c "
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello from Render!'}

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"
