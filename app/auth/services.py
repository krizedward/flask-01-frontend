from flask import session, redirect, url_for
from functools import wraps

def authenticate_user(username, password):
    # Contoh: Proses otentikasi pengguna
    if username == 'admin' and password == 'password':
        return True
    return False


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'bearer_token' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function