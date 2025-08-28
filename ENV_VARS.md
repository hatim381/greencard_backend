# Variables d'environnement pour Render

## Configuration JWT
```
JWT_SECRET_KEY=ton-secret-jwt-super-securise
```

## Configuration Stripe
```
STRIPE_SECRET_KEY=sk_test_51S17BwCNTaKCn2KI[...reste_de_la_cle]
```

## GitHub pour Litestream (optionnel si tu veux garder le backup)
```
GITHUB_TOKEN=ton-token-github
GITHUB_REPO=ton-username/greencard-db-backup
```

## Notes
- Les clés Stripe sont en mode TEST (sk_test_... et pk_test_...)
- Pour passer en production, remplace par tes vraies clés Stripe
- Le JWT_SECRET_KEY doit être unique et sécurisé en production
- Remplace [...]reste_de_la_cle par la vraie clé dans Render (pas dans le code !)