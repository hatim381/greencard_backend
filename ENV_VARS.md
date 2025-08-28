# Variables d'environnement pour Render

## Configuration JWT
```
JWT_SECRET_KEY=ton-secret-jwt-super-securise
```

## Configuration Stripe
```
STRIPE_SECRET_KEY=sk_test_51S17BwCNTaKCn2KIsRZBGHktBZYjYOSLfLVKqEqNc2FIE2L8T4KKVW7ej5N4GqOJ0ufPW5YZ9QXCcK5dW
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