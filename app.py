from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash, make_response, Response, send_file, send_from_directory
from flask_session import Session
import requests
import logging
import hashlib
import os
from dotenv import load_dotenv, dotenv_values

from reportlab.pdfgen import canvas
import io
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from PyPDF2 import PdfReader, PdfWriter

load_dotenv()

app = Flask(__name__, template_folder='pages')
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
base_url = os.environ.get('BASEURL')
# base_url = 'http://192.168.100.105:8000'
app.secret_key = os.environ.get('SECRET_KEY')
# app.secret_key = 'supersecretkey'
# location upload
app.config['UPLOAD_FOLDER'] = './static/uploads'

bearer_token = " "
bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2NvZGUiOiJhZG1pbmlzdHJhdG9yIiwiZXhwIjoxNzE3NTU1NjA4fQ.43CaRX0A523evQmkDc2oo4vR2IdxwxPFk-H0R1-JRds"

@app.route('/generate-pdf')
def generate_pdf():
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file"
    p = canvas.Canvas(buffer)

     # Create a SimpleDocTemplate using the buffer as its "file"
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Create content for the PDF
    content = []

    bearer_token = session.get('bearer_token')
    headers = {"Authorization": f"Bearer {bearer_token}"}

    # Fetch data from API
    response = requests.get(base_url + "/commissions", headers=headers)
    if response.status_code == 200:
        commissions = response.json()
        # Prepare data for the table
        data = [['Commission Code', 'Commission Name', 'Commission Note', 'Is Active']]

        for commission in commissions:
            commission_code = commission.get('commission_code')
            commission_name = commission.get('commission_name')
            commission_note = commission.get('commission_note')
            is_active = 'Yes' if commission.get('is_active') else 'No'
            
            data.append([commission_code, commission_name, commission_note, is_active])

        # Create a Table object
        table = Table(data)

        # Add style to the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)

        # Add table to content
        content.append(table)

        # Build the PDF
        doc.build(content)

        # Get the value of the BytesIO buffer and write it to the response
        pdf_value = buffer.getvalue()
        buffer.close()

        # output pdf
        response = make_response(pdf_value)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'

        return response
    
    else:
        # Handle API request failure
        return "Failed to fetch data from API", response.status_code
    
    # commissions = []
        
    # response = requests.get(base_url+"/commissions", headers=headers)
    # commissions = response.json()
    # token = bearer_token

    # Create a table data
    # data = [
    #     ['Commission Code', 'Commission Name', 'Commission Note', 'Is Active'],
    #     ['Row 1, Col 1', 'Row 1, Col 2', 'Row 1, Col 3', 'Row 1, Col 3'],
    #     ['Row 2, Col 1', 'Row 2, Col 2', 'Row 2, Col 3', 'Row 1, Col 3'],
    # ]

    # Create a Table object
    # table = Table(data)

    

    # # Draw things on the PDF. Here's some basic examples:
    # p.drawString(100, 750, "Hello, World!")
    # p.drawString(100, 730, "This is a PDF document generated with ReportLab.")

    # # Close the PDF object cleanly
    # p.showPage()
    # p.save()

    # # Get the value of the BytesIO buffer and write it to the response
    # pdf_value = buffer.getvalue()
    # buffer.close()

    # response = make_response(pdf_value)
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'

    # return response

##### session
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
Session(app)

@app.route("/set/<string:value>")
def set_session(value):
    session["key"] = value
    return "<h1>Ok</h1>"

@app.route("/get")
def get_session():
    stored_session = session.get("key", "No Session was set")
    return f"<h3>{stored_session}</h3>"

@app.route("/set_data")
def set_data():
    # session['name'] = 'Mike'
    # session['other'] = 'Hello World'
    session['name'] = 'Edward'
    session['other'] = 'Mangare'
    return render_template('auth/index.html', message = 'session get data')

@app.route("/get_data")
def get_data():
    if 'name' in session.keys() and 'other' in session.keys():
        print(session)
        # name = session['name']
        name = session.pop('name')
        print(name)
        print(session)
        other = session['other']
        return render_template('auth/index.html', message = f'Name: {name}, Other: {other}')
    else:
        return render_template('auth/index.html', message = 'No session found.')

@app.route('/clear_session')
def clear_session():
    session.clear()
    # session.pop('name')
    return render_template('auth/index.html', message = 'Session Clear')

##### cookie
@app.route('/set_cookie')
def set_cookie():
    response = make_response(render_template('auth/index.html', message = 'Cookie Set.'))
    response.set_cookie('cookie_name','cookie_value')
    return response

@app.route('/get_cookie')
def get_cookie():
    cookie_value = request.cookies['cookie_name']
    return render_template('auth/index.html', message = f'Cookie Value: {cookie_value}')

@app.route('/remove_cookie')
def remove_cookie():
    response = make_response(render_template('auth/index.html', message = 'Cookie Remove.'))
    response.set_cookie('cookie_name', expires=0)
    return response

@app.route('/form-login', methods=['GET','POST'])
def form_login():
    if request.method == 'GET':
        return render_template('auth/form-login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'edward' and password == '123':
            flash('Login')
            return render_template('auth/index.html', message = '')
        else:
            flash('Gagal Login')
            return render_template('auth/index.html', message = '')
    
    # return render_template('auth/form-login.html')

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
##### filter modal

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
##### create and store

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
##### edit and update

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
##### login

@app.route('/fetch-commissions', methods=['GET', 'POST'])
def dummyCommissions():
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

@app.route('/pdf-raport')
def pdf_raport():
    return render_template('pdf-raport.html')

@app.route('/upload-raport', methods=['POST'])
def upload_raport():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'Tidak ada file yang dipilih untuk diunggah.', 400

        file = request.files['file']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'Tidak ada file yang dipilih untuk diunggah.', 400

        if file:
            filename = file.filename

            # Read the existing PDF
            existing_pdf = PdfReader(file)
            output = PdfWriter()

            # Create a new PDF with ReportLab
            packet = BytesIO()
            can = canvas.Canvas(packet)
            # x dan y
            # can.drawString(100, 750, "Hello, World!")
            # can.drawString(100, 730, "This is a PDF document generated with ReportLab.")
            can.setFont("Helvetica", 6)  # Mengatur ukuran font menjadi 10
            can.drawString(170, 725, "Edward")
            can.drawString(170, 710, "1234567890")
            can.save()

            # Move to the beginning of the BytesIO buffer
            packet.seek(0)
            new_pdf = PdfReader(packet)

            # Add the "watermark" (which is the new pdf) on the existing page
            for page_num in range(len(existing_pdf.pages)):
                page = existing_pdf.pages[page_num]
                if page_num == 0:  # Add new content only to the first page
                    page.merge_page(new_pdf.pages[0])
                output.add_page(page)

            # Save the result
            temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(temp_file_path, 'wb') as f:
                output.write(f)

            # Send the file back to the user for download
            return send_file(temp_file_path, as_attachment=True, download_name=filename)

    return 'Gagal mengunggah file.', 400

# Untuk Melihat Pdf

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return redirect(url_for('uploaded_file', filename=filename))
        return render_template('pdf-raport.html', filename=filename)
    return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)