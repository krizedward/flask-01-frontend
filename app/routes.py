from flask import request, jsonify, current_app as app
from .mysql.models import get_all_users, add_user

@app.route('/users', methods=['GET'])
def users():
    users = get_all_users()
    return jsonify(users)

@app.route('/add_user', methods=['POST'])
def add_user_route():
    username = request.form['username']
    email = request.form['email']
    add_user(username, email)
    return 'User added successfully', 201
