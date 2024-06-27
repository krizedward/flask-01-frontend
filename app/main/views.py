import os
from flask import render_template, jsonify, session
import requests
from . import main
from ..auth.services import login_required 

@main.route('/api/commissions', methods=['GET'])
@login_required
def api_data():
    bearer_token = session.get('bearer_token')
    headers = {"Authorization": f"Bearer {bearer_token}"}
    base_url = os.environ.get('BASEURL')

    if base_url:
        response = requests.get(f"{base_url}/commissions", headers=headers)
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "BASEURL not set in environment variables"}), 500
    
@main.route('/main')
# @main.route('/')
@login_required
def home():
    return render_template('main/home.html')

@main.route('/main-about')
@login_required
def about():
    return render_template('main/about.html')
