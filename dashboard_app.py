from app import app
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
from flask import session, redirect, url_for, request

from functools import wraps

# --- Protection admin sur /dash ---
def admin_required_dash(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get('user')
        if not user or user.get('role') != 'admin':
            return redirect('http://localhost:3000/login')  # redirige vers le login React
        return f(*args, **kwargs)
    return decorated_function

# Patch Dash pour vérifier la session Flask sur /dash
orig_dispatch = app.wsgi_app
def dash_protect_middleware(environ, start_response):
    if environ.get('PATH_INFO', '').startswith('/dash'):
        with app.request_context(environ):
            user = session.get('user')
            if not user or user.get('role') != 'admin':
                res = redirect('http://localhost:3000/login')
                return res(environ, start_response)
    return orig_dispatch(environ, start_response)
app.wsgi_app = dash_protect_middleware

# --- Chargement des données ---
df_csv = pd.read_csv('green_cart_dataset_full_100k.csv')
conn = sqlite3.connect('db/greencart.db')
df_sql = pd.read_sql_query('SELECT * FROM orders', conn)
conn.close()

dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/', external_stylesheets=[dbc.themes.BOOTSTRAP])
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
        }
    ),
    html.H3('Données SQLite : Nombre de commandes'),
    html.Div(f"Nombre de commandes : {len(df_sql)}")
])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
