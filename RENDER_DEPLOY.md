# 🚀 GreenCart Backend - Déploiement Render + Litestream

## Configuration Render (100% gratuit)

### 1. Variables d'environnement à ajouter sur Render :

```bash
# Token GitHub pour les sauvegardes (obligatoire)
GITHUB_TOKEN=ghp_votre_token_github_ici

# JWT Secret (générer une clé sécurisée)
JWT_SECRET_KEY=votre-super-secret-jwt-key-ici

# Variable pour identifier l'environnement Render
RENDER=true
```

### 2. Commandes de déploiement Render :

```bash
# Build Command:
./build.sh

# Start Command:
./start.sh
```

### 3. Comment créer un token GitHub :

1. Va sur https://github.com/settings/tokens
2. Clique **"Generate new token (classic)"**
3. Nom : `Render Database Backup`
4. Permissions : Coche **`repo`** (accès complet aux repos privés)
5. Copie le token et colle-le dans `GITHUB_TOKEN` sur Render

## 🔄 Comment ça fonctionne

1. **Démarrage** : Restaure la DB depuis les sauvegardes GitHub
2. **Fonctionnement** : Litestream sauvegarde en continu dans `/litestream-backups/`
3. **Sauvegarde** : Toutes les 10 minutes, push automatique vers ton repo GitHub
4. **Redémarrage** : Restauration automatique depuis GitHub

## 📁 Structure après déploiement

```
greencard_backend/
├── litestream-backups/     # Ajouté automatiquement
│   ├── generations/        # Sauvegardes Litestream
│   └── snapshots/
├── app.py                  # Ton code
├── models.py
├── routes/
└── ...
```

## 💰 Coûts

- **Render** : 0€ (plan gratuit)
- **GitHub** : 0€ (repos privés gratuits)
- **Litestream** : 0€ (open source)
- **TOTAL** : **0€** ✅

## 🧪 Test en local

```bash
# Démarrer normalement (sans Litestream)
python app.py

# Ou tester avec la config Render
export RENDER=true
./start.sh
```

## 🚨 Important

- ⚠️ Garde ton `GITHUB_TOKEN` secret !
- ✅ Les sauvegardes sont automatiques
- 🔄 En cas de problème, Render redémarre et restaure tout
