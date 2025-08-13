import os
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from cryptography.fernet import Fernet
import logging

logger = logging.getLogger(__name__)

# --- Role based access decorator ---
def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            identity = get_jwt_identity()
            user_role = None
            if isinstance(identity, dict):
                user_role = identity.get('role')
            if user_role not in roles:
                logger.warning("Unauthorized access attempt for role %s", user_role)
                return jsonify({'error': 'Forbidden'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

# --- Encryption utilities ---
_encryption_key = os.environ.get('ENCRYPTION_KEY')
if _encryption_key is None:
    # In production, this should be strictly provided
    _encryption_key = Fernet.generate_key()
    logger.warning("ENCRYPTION_KEY not set; generated temporary key")
_cipher = Fernet(_encryption_key)

def encrypt_data(data: str) -> str:
    if data is None:
        return None
    return _cipher.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    if token is None:
        return None
    return _cipher.decrypt(token.encode()).decode()
