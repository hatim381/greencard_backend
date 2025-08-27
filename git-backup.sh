#!/bin/bash

# Sauvegarde automatique vers GitHub
# set -e # Désactivé pour éviter les plantages

DB_PATH="/opt/render/project/src/db/greencart.db"
GITHUB_TOKEN="${GITHUB_TOKEN}"

echo "🔄 Sauvegarde Git - $(date)"

# Vérifier que le token existe
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️ GITHUB_TOKEN non défini, saut de la sauvegarde"
    exit 0
fi

# Aller dans le dossier du projet
cd /opt/render/project/src

# Configurer Git si pas déjà fait
git config --global user.name "GreenCart Auto-Backup"
git config --global user.email "backup@greencart.app"

# Configurer le remote GitHub si pas déjà fait
if ! git remote get-url origin >/dev/null 2>&1; then
    echo "🔗 Configuration du remote GitHub..."
    git remote add origin https://${GITHUB_TOKEN}@github.com/YubaC/greencart-db-backup.git || true
fi

# Sauvegarder la base de données principale
if [ -f "$DB_PATH" ]; then
    echo "📋 Sauvegarde de la base de données principale..."
    
    # Ajouter la base de données principale
    echo "📁 Ajout de greencart.db..."
    git add db/greencart.db || true
    
    # Vérifier s'il y a des changements
    if ! git diff --staged --quiet 2>/dev/null; then
        echo "💾 Commit des sauvegardes..."
        git commit -m "Auto backup DB $(date -u +%Y-%m-%d_%H:%M:%S_UTC)" || true
        
        echo "🚀 Push vers GitHub..."
        git push origin main || echo "⚠️ Erreur push (probablement normal en premier démarrage)"
    else
        echo "✅ Aucun changement à sauvegarder"
    fi
else
    echo "❌ Base de données non trouvée : $DB_PATH"
fi
