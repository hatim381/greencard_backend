import sqlite3

# Nouvelles astuces pour remplacer le contenu
astuces = [
    "Conservez vos légumes dans un torchon humide pour prolonger leur fraîcheur.",
    "Utilisez les fanes de carottes pour faire un pesto maison.",
    "Transformez le pain rassis en croûtons ou en chapelure.",
    "Congelez les fruits trop mûrs pour les utiliser dans des smoothies.",
    "Réutilisez l’eau de cuisson des légumes pour arroser vos plantes.",
    "Planifiez vos repas à l’avance pour éviter les achats inutiles.",
    "Cuisinez les restes pour créer de nouveaux plats savoureux.",
    "Stockez les herbes fraîches dans un verre d’eau au réfrigérateur.",
    "Vérifiez régulièrement les dates de péremption et consommez en priorité les produits proches de la date.",
    "Préparez des soupes avec les épluchures de légumes bien lavées."
]

conn = sqlite3.connect('db/greencart.db')
cursor = conn.cursor()

# Récupère les 10 derniers IDs
cursor.execute("SELECT id FROM blog_posts ORDER BY date DESC LIMIT 10;")
ids = [row[0] for row in cursor.fetchall()]

for i, blog_id in enumerate(ids):
    if i < len(astuces):
        cursor.execute("UPDATE blog_posts SET content = ? WHERE id = ?", (astuces[i], blog_id))

conn.commit()
conn.close()