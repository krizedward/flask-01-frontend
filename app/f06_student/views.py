from flask import render_template, jsonify, session, request, redirect, flash
import requests
from . import f06_student
# from ..mysql.models import get_data_student

# index
@f06_student.route('/student', methods=['GET'])
def index_student():
    # data = get_data_student()
    return render_template('f06_student/index.html', data = data)


# create
@f06_student.route('/student/create', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('f06_student/create.html')
    # elif request.method == 'POST':
    #     commission_code = request.form['commission_code']
    #     commission_name = request.form['commission_name']
    #     commission_note = request.form['commission_note']

    #     # Data login, sesuaikan dengan endpoint dan format API Anda
    #     commissions_data = {
    #         'commission_code': commission_code,
    #         'commission_name': commission_name,
    #         'commission_note': commission_note,
    #         'is_active': 'Y'
    #     }

    #     # Mengirim request POST untuk mendapatkan token
    #     # response = requests.post(f"{base_url}/commissions", json=commissions_data)

    #     try:
    #         # Mengirim permintaan POST untuk menyimpan data komisi
    #         bearer_token = session.get('bearer_token')
    #         headers = {"Authorization": f"Bearer {bearer_token}"}

    #         # response = requests.post(f"{base_url}/commissions", json=commissions_data, headers=headers)

    #         # Periksa status kode respons
    #         if response.status_code == 201:
    #             flash('invalid','error')
    #             # flash('berhasil','success')
    #             # Jika berhasil, redirect ke halaman '/commissions'
    #             return redirect('/commissions')
    #         else:
    #             # Jika gagal, redirect ke halaman '/create' atau halaman lain yang sesuai
    #             return redirect('/commissions')
    #     except Exception as e:
    #         # Tangani kesalahan yang mungkin terjadi selama permintaan
    #         return f"Error occurred: {str(e)}"
##### form create & store