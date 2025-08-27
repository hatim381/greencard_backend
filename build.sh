#!/bin/bash

echo "🔨 Build GreenCart Backend..."

# Installer les dépendances Python
pip install -r requirements.txt

# Rendre les scripts exécutables
chmod +x install_litestream.sh
chmod +x git-backup.sh
chmod +x git-restore.sh
chmod +x start.sh
chmod +x start-simple.sh
chmod +x start-ultra-simple.sh

echo "✅ Build terminé !"
