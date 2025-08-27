#!/bin/bash

# Sauvegarde automatique vers GitHub
# set -e # Désactivé pour éviter les plantages

BACKUP_DIR="/opt/render/project/src/litestream-backups"
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
git config --global user.name "Litestream Auto-Backup"
git config --global user.email "backup@greencart.app"

# Ajouter les sauvegardes au repo existant
if [ -d "$BACKUP_DIR" ] && [ "$(ls -A $BACKUP_DIR 2>/dev/null)" ]; then
    echo "📁 Ajout des sauvegardes..."
    git add litestream-backups/ || true
    
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
    echo "📂 Dossier de sauvegarde vide"
fi
