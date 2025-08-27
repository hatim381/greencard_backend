#!/bin/bash

# Restauration depuis GitHub
# set -e # Désactivé pour éviter les plantages

DB_PATH="/opt/render/project/src/db/greencart.db"
GITHUB_TOKEN="${GITHUB_TOKEN}"

echo "📥 Restauration Git - $(date)"

# Vérifier que le token existe
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️ GITHUB_TOKEN non défini, saut de la restauration"
    mkdir -p "/opt/render/project/src/db"
    exit 0
fi

# Aller dans le dossier du projet
cd /opt/render/project/src

# Configurer Git
git config --global user.name "GreenCart Auto-Backup"
git config --global user.email "backup@greencart.app"

# Pull des dernières sauvegardes
echo "🔄 Pull depuis GitHub..."
git pull origin main || echo "⚠️ Erreur pull (normal si premier démarrage)"

# Vérifier si la base de données existe maintenant
if [ -f "$DB_PATH" ]; then
    echo "✅ Base de données restaurée depuis GitHub"
    ls -la db/
else
    echo "📂 Aucune sauvegarde DB trouvée (normal pour le premier démarrage)"
    mkdir -p "/opt/render/project/src/db"
fi
