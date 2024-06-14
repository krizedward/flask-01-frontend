from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import requests
import logging
import hashlib

app = Flask(__name__, template_folder='pages')
base_url = "http://192.168.100.105:8000"
app.secret_key = 'supersecretkey' 

# Simulated database
commissions = [
    {'id': 1,'code': 'Surabaya', 'name': 'Edward', 'note': 'note', 'active': 'active',},
    {'id': 2,'code': 'Surabaya', 'name': 'Kristian', 'note': 'note', 'active': 'active',},
    {'id': 3,'code': 'Surabaya', 'name': 'Kristian', 'note': 'note', 'active': 'active',}
]

bearer_token = " "
bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2NvZGUiOiJhZG1pbmlzdHJhdG9yIiwiZXhwIjoxNzE3NTU1NjA4fQ.43CaRX0A523evQmkDc2oo4vR2IdxwxPFk-H0R1-JRds"

##### koding baru

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'Text field is required'}), 400
    
    text = data['text']
    hashed_text = hashlib.md5(text.encode()).hexdigest()
    return jsonify({'hashed_text': hashed_text})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    return jsonify({'error': 'MD5 is a one-way hashing algorithm, decryption is not possible.'}), 400


# proses login
@app.route('/postlogin', methods=['POST','GET'])
def postlogin():
    if request.method == 'POST':
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
            return redirect('/dashboard')
        else:
            return redirect('/login')
    else:
        return 'Login Failed'
    # if request.method == "POST":
    #     headers = {"Authorization": f"Bearer {bearer_token}"}
    #     requests.post(base_url+"/commissions", headers=headers)
    # else:
    #     return 'Login failed'

# @app.route('/success')
# def success():
    # Ambil URL yang ingin diakses dari session
    # next_url = session.pop('next', '/create')
    # return f'Login successful! Redirecting to {next_url}'
#    return redirect(url_for('index'))

# get all commissions
@app.route('/api/commissions', methods=['GET'])
def api_data():
    bearer_token = session.get('bearer_token')
    headers = {"Authorization": f"Bearer {bearer_token}"}

    response = requests.get(base_url+"/commissions", headers=headers)
    return jsonify(response.json()), 200
    # return response.json()
    # return jsonify(commissions)

@app.route('/api/commissions', methods=['GET'])
def get_commissions():
    return jsonify(commissions)

# route
@app.route('/')
def index():
    # commissions = []
    # bearer_token = session.get('bearer_token')
    # headers = {"Authorization": f"Bearer {bearer_token}"}
    # response = requests.get(base_url+"/commissions", headers=headers)
    # commissions = response.json()
    # return render_template('index.html', commissions=commissions)
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/commissions' , methods=['POST','GET'])
def commissions():
    
    bearer_token = session.get('bearer_token')
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    if request.method == 'GET':
        commissions = []
        
        response = requests.get(base_url+"/commissions", headers=headers)
        commissions = response.json()
        token = bearer_token
        return render_template('commissions-index.html', token=token, commissions=commissions)
    
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
        return render_template('commissions-index.html', commissions=commissions)


##### comission pagging
@app.route('/commission_paging')
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

        # filter = {
        #     "filters": [
        #         {
        #             "search": "commission_code",     # Change this as needed
        #             "operator": "is equal to",  # Change this as needed
        #             "value1": "K1",     # Change this as needed
        #             "value2": "K1"      # Change this as needed
        #         }
        #     ],
        #     "filter_type": "AND"            # Change this as needed
        # }
    

    # filter = {
    #     "filters": [
    #         {
    #             "search": "string",     # Change this as needed
    #             "operator": "is equal to",  # Change this as needed
    #             "value1": "string",     # Change this as needed
    #             "value2": "string"      # Change this as needed
    #         }
    #     ],
    #     "filter_type": "AND"            # Change this as needed
    # }

    # sort = {
    #     "sorts": [
    #         {
    #             "field": "string",  # Change this as needed
    #             "order": "ASC"      # Change this as needed
    #         }
    #     ]
    # }

    # Combine all the data into one dictionary
        datas = {**page, **sort}
        # datas = page

        response = requests.post(f"{base_url}/commission_paging", headers=headers, json=datas)
        # response = requests.post(f"{base_url}/login", data=login_data)
    # commissions = response.json()
    # return render_template('commissions-index.html', commissions=commissions)
    
    # Return the JSON response from the API
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Failed to retrieve commissions"}), response.status_code

# @app.route('/create')
# def about():
#     return render_template('commisions-create.html')

@app.route('/commissions/create', methods=['GET','POST'])
def commissions_store():
    if request.method == 'POST':
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
        
    elif request.method == 'GET':

        return render_template('commisions-create.html')
    # return redirect('/commissions')
    # return render_template('commissions-index.html')

# @app.route('/edit')
# def edit():
#     return render_template('edit.html')

@app.route('/commissions/<commission_id>/edit', methods=['GET', 'POST'])
def commissions_edit(commission_id):
    if request.method == 'GET':
        try:
            bearer_token = session.get('bearer_token')
            headers = {"Authorization": f"Bearer {bearer_token}"}
            # Mendapatkan data komisi yang akan diedit
            response = requests.get(f"{base_url}/commission/{commission_id}",headers=headers)
            commissions = response.json()

            # Mengisi formulir dengan data komisi yang diperoleh
            return render_template('commissions-edit.html', commissions=commissions)
        except Exception as e:
            # Tangani kesalahan yang mungkin terjadi
            return f"Error occurred: {str(e)}"
    # elif request.method == 'POST':
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

@app.route('/commissions/<commission_id>/destroy', methods=['GET'])
def commissions_destroy(commission_id):
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
# end commissions

@app.route('/login')
def login():
    return render_template('login.html')

# dummies api
@app.route('/person')
def person():
    data = [
        {
            'name': 'Edward',
            'address': 'Surabaya'
        },
        {
            'name': 'Alice',
            'address': 'Jakarta'
        },
        {
            'name': 'Bob',
            'address': 'Bandung'
        }
    ]
    return jsonify(data)
    # return render_template('index.html', person=data)

@app.route('/dummy-commissions', methods=['GET', 'POST'])
def dummyCommissions():
    bearer_token = session.get('bearer_token')
    headers = {"Authorization": f"Bearer {bearer_token}"}
    if request.method == 'GET':
        commissions = []
        
        response = requests.get(base_url+"/commissions", headers=headers)
        commissions = response.json()
        # return render_template('commissions-index.html', token=token, commissions=commissions)
    

        # page = {
        #     'limit': 10,  # Change this as needed
        #     'page': 1     # Change this as needed
        # }

        # berhasil
        # datas = request.json
        
        # response = requests.get(base_url+"/commissions", headers=headers)
        # response = requests.get(f"{base_url}/commissions", headers=headers, json=datas)        
        # commissions = response.json()
        
        return jsonify(commissions)
    
    if request.method == 'POST':
        commissions = []

        # page = {
        #     'limit': 10,  # Change this as needed
        #     'page': 1     # Change this as needed
        # }

        # berhasil
        datas = request.json
        
        # response = requests.get(base_url+"/commissions", headers=headers)
        response = requests.post(f"{base_url}/commission_paging", headers=headers, json=datas)        
        commissions = response.json()
        
        return jsonify(commissions)
    

@app.route('/api/fetch-data', methods=['GET'])
def fetch_data():
    # URL dari API yang akan diakses
    api_url = 'https://api.example.com/data'
    
    # Auth token yang akan digunakan
    auth_token = 'your_auth_token_here'
    
    # Headers dengan auth token
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    
    # Request ke API
    response = requests.get(api_url, headers=headers)
    
    # Jika response status code 200 (OK)
    if response.status_code == 200:
        # Return data dalam bentuk JSON
        return jsonify(response.json())
    else:
        # Return error message
        return jsonify({'error': 'Failed to fetch data'}), response.status_code


if __name__ == '__main__':
    app.run(debug=True)