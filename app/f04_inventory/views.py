from flask import render_template, jsonify, session, request, redirect, url_for
from ..mysql.models import get_data_accounting, add_data_accounting, get_accounting_by_id, update_accounting, delete_data_accounting
from . import f04_inventory

# index
@f04_inventory.route('/inventory', methods=['GET'])
def index_accounting():
    # users = get_all_users()
    data = get_data_accounting()
    return render_template('f04_inventory/index.html', users=data)

# create
@f04_inventory.route('/inventory/create', methods=['GET','POST'])
def create_accounting():
    if request.method == 'GET':
        return render_template('f03_accounting/create.html')
    elif request.method == 'POST':
        # username = request.form['username']
        # email = request.form['email']
        date = request.form['date']
        amount = request.form['amount']
        deskripsi = request.form['deskripsi']
        # add_user(username, email)
        add_data_accounting(date, amount, deskripsi)
        return redirect('/accounting')
    
# update
@f04_inventory.route('/inventory/<accounting_id>/edit', methods=['GET','POST'])
def edit_accounting(accounting_id):
    if request.method == 'GET':
        # user = get_user_by_id(accounting_id)
        data = get_accounting_by_id(accounting_id)
        if data:
            return render_template('f03_accounting/edit.html', data=data)
        else:
            return 'User not found', 404
    elif request.method == 'POST':
        
        transaction_date = request.form.get('transaction_date')
        transaction_amount = request.form.get('transaction_amount')
        transaction_description = request.form.get('transaction_description')

        # Memanggil fungsi update_accounting
        update_accounting(accounting_id, transaction_date, transaction_amount, transaction_description)
        
        return redirect('/accounting')

# delete
@f04_inventory.route('/inventory/<accounting_id>/delete', methods=['GET'])
def delete_accounting(accounting_id):
    user = get_accounting_by_id(accounting_id)
    
    if user:
        delete_data_accounting(accounting_id)
        return redirect('/accounting')
    else:
        return 'User not found', 404