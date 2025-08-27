#!/bin/bash

echo "📦 Installation de Litestream v0.3.13..."

# Créer le dossier bin local si nécessaire
mkdir -p /opt/render/project/bin

# Télécharger Litestream pour Linux
curl -L https://github.com/benbjohnson/litestream/releases/download/v0.3.13/litestream-v0.3.13-linux-amd64-static.tar.gz -o /tmp/litestream.tar.gz

# Extraire et installer dans le dossier du projet
tar -xzf /tmp/litestream.tar.gz -C /tmp
mv /tmp/litestream /opt/render/project/bin/
chmod +x /opt/render/project/bin/litestream

# Ajouter au PATH
export PATH="/opt/render/project/bin:$PATH"

# Vérifier l'installation
echo "✅ Litestream installé :"
/opt/render/project/bin/litestream version