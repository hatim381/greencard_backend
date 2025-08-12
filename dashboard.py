from flask import Flask, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3

# --- Flask app et config ---
app = Flask(__name__)
app.secret_key = 'votre-cle-secrete'  # à personnaliser
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/greencart.db'
db = SQLAlchemy(app)

# --- Dash app ---
# Ajout de meta_tags pour assurer le responsive sur tous les appareils
dash_app = dash.Dash(
    __name__,
    server=app,
    url_base_pathname='/dashboard/',
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)

# --- Protection admin ---
@app.before_request
def restrict_dashboard():
    if request.path.startswith('/dashboard'):
        user = session.get('user')
        if not user or user.get('role') != 'admin':
            return redirect(url_for('login'))  # à adapter selon ta route de login

# --- Chargement des données ---
# CSV
df_csv = pd.read_csv('green_cart_dataset_full_100k.csv')
# SQLite
conn = sqlite3.connect('db/greencart.db')
df_sql = pd.read_sql_query('SELECT * FROM orders', conn)
conn.close()

# --- Layout Dash ---
dash_app.layout = dbc.Container([
    html.H1('Tableau de bord GreenCart'),
    html.Hr(),
    html.H3('Données CSV : Bonnes ventes par mois'),
    dcc.Graph(
        figure={
            'data': [
                {'x': df_csv['mois'], 'y': df_csv['is_good_sale'], 'type': 'bar', 'name': 'Bonnes ventes'}
            ],
            'layout': {'title': 'Bonnes ventes par mois (CSV)'}
        },
        style={'width': '100%'}
    ),
    html.H3('Données SQLite : Nombre de commandes'),
    html.Div(f"Nombre de commandes : {len(df_sql)}")
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
