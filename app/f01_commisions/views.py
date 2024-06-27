import os
from flask import render_template, jsonify, session, request, redirect, flash
import requests
from . import f01_commisions
from ..auth.services import login_required

base_url = os.environ.get('BASEURL')

# index
@f01_commisions.route('/commissions', methods=['GET'])
@login_required
def index():
    bearer_token = session.get('bearer_token')
    headers = {"Authorization": f"Bearer {bearer_token}"}

    if request.method == 'GET':
        commissions = []

        response = requests.get(base_url+"/commissions", headers=headers)
        commissions = response.json()
        token = bearer_token

        return render_template('f01_commisions/index.html',token=token, commissions=commissions)
    
    if request.method == 'POST':
        page = {
            'limit': 10,  # Change this as needed
            'page': 1     # Change this as needed
        }

        # Dapatkan nilai dari 'search_sort' dan 'sort' dari permintaan POST
        field = request.form.get('search_sort', None)
        order = request.form.get('sort', None)

        sort = {
            "sorts": [
                {
                    "field": field,
                    "order": order 
                }
            ]
        }
    
        # Periksa jika salah satu atau kedua field kosong
        if field is None or order is None:
            sort = {}

        filter_type = request.form.get('filter_type', None)
        search = request.form.get('search_filter', None)
        operator = request.form.get('operator', None)
        value1 = request.form.get('value1', None)
        value2 = request.form.get('value2', None)

        filter = {
            "filters": [
                {
                    "search": search,     # Change this as needed
                    "operator": operator,  # Change this as needed
                    "value1": value1,     # Change this as needed
                    "value2": value2      # Change this as needed
                }
            ],
            "filter_type": filter_type            # Change this as needed
        }

        if filter_type is None or search is None or operator is None or value1 is None or value2 is None:
            filter = {}

        # datas = {**page, **sort}
        datas = {**page, **filter, **sort}

        # datas = page

        response = requests.post(f"{base_url}/commission_paging", headers=headers, json=datas)
        # response = requests.post(f"{base_url}/login", data=login_data)
        commissions = response.json()
        return render_template('f01_commisions/index.html', commissions=commissions)
##### filter modal & index

# create
@f01_commisions.route('/commissions/create', methods=['GET','POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('f01_commisions/create.html')
    elif request.method == 'POST':
        commission_code = request.form['commission_code']
        commission_name = request.form['commission_name']
        commission_note = request.form['commission_note']

        # Data login, sesuaikan dengan endpoint dan format API Anda
        commissions_data = {
            'commission_code': commission_code,
            'commission_name': commission_name,
            'commission_note': commission_note,
            'is_active': 'Y'
        }

        # Mengirim request POST untuk mendapatkan token
        # response = requests.post(f"{base_url}/commissions", json=commissions_data)

        try:
            # Mengirim permintaan POST untuk menyimpan data komisi
            bearer_token = session.get('bearer_token')
            headers = {"Authorization": f"Bearer {bearer_token}"}

            response = requests.post(f"{base_url}/commissions", json=commissions_data, headers=headers)

            # Periksa status kode respons
            if response.status_code == 201:
                flash('invalid','error')
                # flash('berhasil','success')
                # Jika berhasil, redirect ke halaman '/commissions'
                return redirect('/commissions')
            else:
                # Jika gagal, redirect ke halaman '/create' atau halaman lain yang sesuai
                return redirect('/commissions')
        except Exception as e:
            # Tangani kesalahan yang mungkin terjadi selama permintaan
            return f"Error occurred: {str(e)}"
##### form create & store

# update
@f01_commisions.route('/commissions/<commission_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(commission_id):
    if request.method == 'GET':
        try:
            bearer_token = session.get('bearer_token')
            headers = {"Authorization": f"Bearer {bearer_token}"}
            # Mendapatkan data komisi yang akan diedit
            response = requests.get(f"{base_url}/commission/{commission_id}",headers=headers)
            commissions = response.json()

            # Mengisi formulir dengan data komisi yang diperoleh
            # return render_template('commissions-edit.html', commissions=commissions)
            return render_template('f01_commisions/edit.html', commissions=commissions)
        except Exception as e:
            # Tangani kesalahan yang mungkin terjadi
            return f"Error occurred: {str(e)}"
    elif request.method == 'POST':
        # commission_code = request.form['commission_code']
        commission_name = request.form['commission_name']
        commission_note = request.form['commission_note']

        commissions_data = {
            # 'commission_code': commission_code,
            'commission_name': commission_name,
            'commission_note': commission_note,
            'is_active': 'Y'
        }

        # Mengirim permintaan POST untuk menyimpan data komisi
        bearer_token = session.get('bearer_token')
        headers = {"Authorization": f"Bearer {bearer_token}"}

        try:
            response = requests.put(f"{base_url}/commission/{commission_id}",headers=headers , json=commissions_data)
            if response.status_code == 200:
                return redirect('/commissions')
            else:
                return redirect(f"/commissions/{commission_id}/edit")
        except Exception as e:
            return f"Error occurred: {str(e)}"
##### edit and update

# delete
@f01_commisions.route('/commissions/<commission_id>/delete', methods=['GET'])
@login_required
def delete(commission_id):
    bearer_token = session.get('bearer_token')
    headers = {"Authorization": f"Bearer {bearer_token}"}
    try:
        response = requests.delete(f"{base_url}/commission/{commission_id}",headers=headers)
        if response.status_code == 204:
            return redirect('/commissions')
        else:
            return f"Failed to delete commission with ID {commission_id}"
    except Exception as e:
        return f"Error occurred: {str(e)}"
##### delete
  
##### comission pagging
@f01_commisions.route('/commission_paging')
@login_required
def commissionPaging():
    if request.method == 'GET':
        bearer_token = session.get('bearer_token')
        headers = {"Authorization": f"Bearer {bearer_token}"}

        # Example data for pagination, filter, and sort
        page = {
            'limit': 10,  # Change this as needed
            'page': 2     # Change this as needed
        }

        sort = {
            "sorts": [
                {
                    "field": 'commission_code',
                    "order": 'ASC' 
                },
                {
                    "field": 'commission_name',
                    "order": 'ASC' 
                },
            ]
        }

        # Combine all the data into one dictionary
        datas = {**page, **sort}
        # datas = page

        response = requests.post(f"{base_url}/commission_paging", headers=headers, json=datas)
    
    # Return the JSON response from the API
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Failed to retrieve commissions"}), response.status_code
##### paging

@f01_commisions.route('/fetch-commissions', methods=['GET', 'POST'])
@login_required
def fetchCommissions():
    bearer_token = session.get('bearer_token')
    headers = {"Authorization": f"Bearer {bearer_token}"}
    if request.method == 'GET':
        commissions = []
        
        response = requests.get(base_url+"/commissions", headers=headers)
        commissions = response.json()

        return jsonify(commissions)
    
    if request.method == 'POST':
        commissions = []
        # berhasil
        datas = request.json
        
        response = requests.post(f"{base_url}/commission_paging", headers=headers, json=datas)        
        commissions = response.json()
        
        return jsonify(commissions)
##### berhasil