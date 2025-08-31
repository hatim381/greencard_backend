import pandas as pd
from catboost import CatBoostClassifier

# === Charger le modèle CatBoost ===
model = CatBoostClassifier()
model.load_model("catboost_model.cbm")

# === Charger le dataset pour meilleur_produit ===
df = pd.read_csv("green_cart_dataset_full_100k.csv")
best_products = df.groupby(['categorie', 'mois', 'produit'])['is_good_sale'].mean().reset_index()
best_products_sorted = best_products.sort_values(['categorie', 'mois', 'is_good_sale'], ascending=[True, True, False])
best_products_unique = best_products_sorted.groupby(['categorie', 'mois']).first().reset_index()

def predict_good_sale(input_dict):
    # input_dict: dict avec les clés produit, categorie, mois
    input_df = pd.DataFrame([{
        "produit": input_dict["produit"],
        "categorie": input_dict["categorie"],
        "mois": input_dict["mois"]
    }])
    prediction = model.predict(input_df)[0]
    return int(prediction)

def meilleur_produit(categorie, mois):
    result = best_products_unique.query("categorie == @categorie and mois == @mois")
    return result['produit'].values[0] if not result.empty else None
