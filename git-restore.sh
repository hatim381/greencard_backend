#!/bin/bash

# Restauration depuis GitHub
# set -e # Désactivé pour éviter les plantages

BACKUP_DIR="/opt/render/project/src/litestream-backups"
GITHUB_TOKEN="${GITHUB_TOKEN}"

echo "📥 Restauration Git - $(date)"

# Vérifier que le token existe
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️ GITHUB_TOKEN non défini, saut de la restauration"
    mkdir -p "$BACKUP_DIR"
    exit 0
fi

# Aller dans le dossier du projet
cd /opt/render/project/src

# Configurer Git
git config --global user.name "Litestream Auto-Backup"
git config --global user.email "backup@greencart.app"

# Pull des dernières sauvegardes
echo "🔄 Pull depuis GitHub..."
git pull origin main || echo "⚠️ Erreur pull (normal si premier démarrage)"

if [ -d "$BACKUP_DIR" ] && [ "$(ls -A $BACKUP_DIR 2>/dev/null)" ]; then
    echo "✅ Sauvegardes restaurées depuis GitHub"
    ls -la "$BACKUP_DIR"
else
    echo "📂 Aucune sauvegarde trouvée (normal pour le premier démarrage)"
    mkdir -p "$BACKUP_DIR"
fi
