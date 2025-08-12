# Cloner le projet:
## Cloner le back:
git clone git@github.com:hatim381/greencard_backend.git

## Cloner le front:
git@github.com:hatim381/greencard_fronted.git

git branch -v pour vérifier la branche courante
Dans votre cas si la branche différente de main, faire un git checkout main


# Récupération des modifications de la branche
git pull --rebase

### Si conflit:
 Faire git stash pour mettre de côté les modifications faites
 Ensuite git pull
 Et finalement git stash apply pour réappliquer les modifications

# Cas actuel:
Eviter de faire les modifications des 2 côtés pour éviter les conflits

# Publication des modifications:

Faire un git add des chemins de fichiers à push
Si tous les fichiers doivent être rajoutés, faire un git add .

git commit -m "Message" pour décrire la modification réalisée.
Attention: Mettre le message entre guillements

git push pour publier les modifications



git reset --hard HEAD~2  (Remonter de comit en ne prenant pas en compte les modifiaction)

git push -f