#!/bin/bash

echo "🚀 Démarrage GreenCart avec persistance GitHub..."

# Aller dans le bon répertoire
cd /opt/render/project/src

# ACTIVER L'ENVIRONNEMENT VIRTUEL  
echo "🔧 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Variables d'environnement
export RENDER=true

# Chemins
DB_PATH="/opt/render/project/src/db/greencart.db"

# Créer le dossier DB
mkdir -p /opt/render/project/src/db

# Restaurer depuis GitHub si la DB n'existe pas
if [ ! -f "$DB_PATH" ]; then
    echo "📥 Tentative de restauration depuis GitHub..."
    
    # Restaurer les sauvegardes depuis GitHub (avec la nouvelle version)
    chmod +x /opt/render/project/src/git-restore.sh
    /opt/render/project/src/git-restore.sh || echo "⚠️ Pas de sauvegarde GitHub trouvée"
fi

# Créer la DB si elle n'existe toujours pas
if [ ! -f "$DB_PATH" ]; then
    echo "🔧 Initialisation de la base de données..."
    python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Base de données initialisée')
"
fi

# Sauvegarde immédiate (pas besoin de copie)
echo "💾 Sauvegarde initiale..."
# La DB sera sauvegardée directement par git-backup.sh

# Démarrer les sauvegardes Git périodiques (toutes les 20 minutes)
echo "⏰ Démarrage des sauvegardes Git..."
chmod +x /opt/render/project/src/git-backup.sh
(while true; do
    sleep 1200  # 20 minutes
    echo "🔄 Sauvegarde automatique $(date)"
    /opt/render/project/src/git-backup.sh || echo "⚠️ Erreur sauvegarde Git"
done) &
BACKUP_PID=$!

# Fonction de nettoyage
cleanup() {
    echo "🛑 Arrêt des services..."
    echo "💾 Sauvegarde finale..."
    /opt/render/project/src/git-backup.sh || echo "⚠️ Erreur sauvegarde finale"
    kill $BACKUP_PID 2>/dev/null || true
    wait $BACKUP_PID 2>/dev/null || true
    exit 0
}

# Capturer les signaux d'arrêt
trap cleanup SIGINT SIGTERM

# Démarrer l'application Flask
echo "🌐 Démarrage de l'application Flask..."
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
