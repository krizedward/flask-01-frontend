import os
import hashlib
import requests
from flask import render_template, request, session, redirect, g
from . import auth
from .services import login_required

base_url = os.environ.get('BASEURL')


@auth.route('/login')
@auth.route('/')
def login():
    return render_template('auth/login.html', text=base_url)

@auth.route('/postlogin', methods=['POST', 'GET'])
def postlogin():
    if request.method == 'POST':
        session.pop('user', None)

        username = request.form['username']
        password = request.form['password']

        # Hash the password with MD5
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        # Data login, sesuaikan dengan endpoint dan format API Anda
        login_data = {
            'username': username,
            'password': hashed_password
        }
        
        # Mengirim request POST untuk mendapatkan token
        response = requests.post(f"{base_url}/login", data=login_data)

        if response.status_code == 200:
            # Ambil token dari respon dan simpan ke dalam session
            bearer_token = response.json().get('access_token')
            session['bearer_token'] = bearer_token
            return redirect('/main')
        else:
            return redirect('/login')
    else:
        return 'Login Failed'
    
@auth.route('/register')
def register():
    return render_template('auth/register.html')

@auth.route('/protected')
@login_required
def protected():
    return render_template('auth/protected.html')

@auth.before_request
def before_request():
    g.user = None 

    if 'bearer_token' in session:
        g.bearer_token = session['bearer_token']


@auth.route('/logout')
def dropsession():
    session.pop('bearer_token', None)
    return redirect('/login')
    # return render_template('auth/login.html')

