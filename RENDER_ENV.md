# Variables d'environnement pour Render

## Configuration JWT
```
JWT_SECRET_KEY=votre-secret-jwt-securise
```

## Configuration Stripe
```
STRIPE_SECRET_KEY=sk_test_votre_cle_stripe_de_test
```

## GitHub pour Litestream (optionnel)
```
GITHUB_TOKEN=votre-token-github
GITHUB_REPO=username/repo-backup
```

## Notes importantes
- Remplacez toutes les valeurs par vos vraies clés dans Render
- Les clés Stripe en mode TEST commencent par sk_test_
- Ne jamais commiter les vraies clés dans le code source
- Utilisez les variables d'environnement de Render
