import os
import pytest
from werkzeug.security import generate_password_hash
from cryptography.fernet import Fernet

# Set env variables before importing app
os.environ.setdefault('JWT_SECRET_KEY', 'test-secret')
os.environ.setdefault('ENCRYPTION_KEY', Fernet.generate_key().decode())

from app import app, db
from models import User

@pytest.fixture
def client():
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        JWT_COOKIE_SECURE=False,
        JWT_COOKIE_CSRF_PROTECT=False
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(email='admin@example.com', password=generate_password_hash('pass'), name='Admin', role='admin')
        prod = User(email='prod@example.com', password=generate_password_hash('pass'), name='Prod', role='producer')
        db.session.add_all([admin, prod])
        db.session.commit()
    with app.test_client() as client:
        yield client


def login(client, email, password='pass'):
    return client.post('/api/auth/login', json={'email': email, 'password': password})


def test_users_requires_auth(client):
    res = client.get('/api/auth/users')
    assert res.status_code == 401


def test_producer_cannot_access_users(client):
    login(client, 'prod@example.com')
    res = client.get('/api/auth/users')
    assert res.status_code == 403


def test_admin_can_access_users(client):
    login(client, 'admin@example.com')
    res = client.get('/api/auth/users')
    assert res.status_code == 200
    assert all('email' not in u for u in res.get_json())
