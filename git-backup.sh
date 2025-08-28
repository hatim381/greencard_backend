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
    git remote add origin https://${GITHUB_TOKEN}@github.com/hatim381/greencard_backend.git || true
else
    # Mettre à jour l'URL si elle existe déjà
    git remote set-url origin https://${GITHUB_TOKEN}@github.com/hatim381/greencard_backend.git || true
fi

# S'assurer qu'on est sur la branche main
echo "🔀 Basculement sur main..."
git checkout main 2>/dev/null || git checkout -b main || true

# Vérifier s'il y a des changements dans la DB et uploads avant de pull
echo "📋 Vérification des changements DB et uploads..."
CHANGES_DETECTED=false

# Vérifier la DB
if [ -f "$DB_PATH" ]; then
    git add db/greencart.db || true
    if ! git diff --staged --quiet db/greencart.db 2>/dev/null; then
        CHANGES_DETECTED=true
    fi
fi

# Vérifier le dossier uploads
if [ -d "/opt/render/project/src/uploads" ]; then
    git add uploads/ || true
    if ! git diff --staged --quiet uploads/ 2>/dev/null; then
        CHANGES_DETECTED=true
    fi
fi

# S'il y a des changements, les stash temporairement
if [ "$CHANGES_DETECTED" = true ]; then
    echo "💾 Mise de côté temporaire des changements (DB + uploads)..."
    git stash push -m "Temp backup before pull $(date -u +%Y-%m-%d_%H:%M:%S_UTC)" || true
fi

# Pull des derniers changements
echo "📥 Pull des derniers changements..."
git pull origin main || echo "⚠️ Premier pull, normal"

# Sauvegarder la base de données et uploads
echo "📋 Sauvegarde de la base de données et uploads..."

# Récupérer les changements stashés s'il y en a
if git stash list | grep -q "Temp backup before pull"; then
    echo "🔄 Récupération des changements (DB + uploads)..."
    git stash pop || true
fi

# Toujours ajouter la DB et uploads après le pop (pour être sûr)
echo "📁 Ajout final de greencart.db et uploads/..."
if [ -f "$DB_PATH" ]; then
    git add db/greencart.db || true
fi
if [ -d "/opt/render/project/src/uploads" ]; then
    git add uploads/ || true
fi

# Vérifier s'il y a des changements à commit
if ! git diff --staged --quiet 2>/dev/null; then
    echo "💾 Commit des sauvegardes (DB + uploads)..."
    git commit -m "Auto backup DB + uploads $(date -u +%Y-%m-%d_%H:%M:%S_UTC)" || true
    
    echo "🚀 Push vers GitHub..."
    git push origin main || echo "⚠️ Erreur push"
else
    echo "✅ Aucun changement à sauvegarder"
fi
