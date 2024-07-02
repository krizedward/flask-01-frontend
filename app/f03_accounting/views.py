from flask import render_template, jsonify, session, request, redirect, url_for
from ..mysql.models import get_all_users, add_user, get_user_by_id, delete_user
from . import f03_accounting

# index
@f03_accounting.route('/accounting', methods=['GET'])
def index_accounting():
    users = get_all_users()
    return render_template('f03_accounting/index.html', users=users)

# create
@f03_accounting.route('/accounting/create', methods=['GET','POST'])
def create_accounting():
    if request.method == 'GET':
        return render_template('f03_accounting/create.html')
    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        add_user(username, email)
        return redirect('/accounting')
    
# update
@f03_accounting.route('/accounting/<accounting_id>/edit', methods=['GET','POST'])
def edit_accounting(accounting_id):
    if request.method == 'GET':
        user = get_user_by_id(accounting_id)
        if user:
            return render_template('f03_accounting/edit.html', user=user)
        else:
            return 'User not found', 404
    elif request.method == 'POST':
        return redirect('/accounting')

# delete
@f03_accounting.route('/accounting/<accounting_id>/delete', methods=['GET'])
def delete_accounting(accounting_id):
    user = get_user_by_id(accounting_id)
    if user:
        delete_user(accounting_id)
        return redirect('/accounting')
    else:
        return 'User not found', 404