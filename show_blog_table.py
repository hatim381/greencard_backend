import sqlite3
from tabulate import tabulate

# Connexion à la base de données
conn = sqlite3.connect('db/greencart.db')
cursor = conn.cursor()

# Exécution de la requête
cursor.execute("SELECT id, title, content, date, author FROM blog_posts ORDER BY date DESC LIMIT 10;")
rows = cursor.fetchall()

# Affichage formaté
headers = ["ID", "Titre", "Contenu", "Date", "Auteur"]
print(tabulate(rows, headers, tablefmt="grid", showindex=False))

conn.close()
