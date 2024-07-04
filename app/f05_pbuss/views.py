from flask import render_template, jsonify, session, request, redirect, url_for, send_file
from ..mysql.models import get_data_pbuss, get_pbuss_by_kode, add_data_accounting, get_accounting_by_id, update_accounting, delete_data_accounting
from . import f05_pbuss
# import pdfkit

# Tentukan path ke wkhtmltopdf dan buat konfigurasi
# path_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'  # Sesuaikan dengan path di sistem Anda
# config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# index
@f05_pbuss.route('/pdf/<kode>', methods=['GET'])
def index_pbuss(kode):
    data = get_data_pbuss()
    return render_template('f05_pbuss/index.html', users=data, kode=kode)
    # return f'menampilkan kode: {kode}'


@f05_pbuss.route('/pbuss/<kode>')
def show_pbuss(kode):
    pbuss_data = get_pbuss_by_kode(kode)
    return render_template('pbuss_detail.html', pbuss=pbuss_data)

@f05_pbuss.route('/pdf/<kode>/download', methods=['GET'])
def ex_pbuss(kode):
    # Ambil data dari basis data atau sumber lainnya
    data = {
        'title': 'Laporan Bulanan',
        'content': 'Ini adalah contoh laporan bulanan dengan data dinamis yang diambil dari sumber tertentu.'
    }
    pbuss_data = get_pbuss_by_kode(kode)
    return render_template('skeleton/pbuss/template_01.html', data=pbuss_data, kode=kode)
    # return render_template('skeleton/f05_pbuss/template_01.html', data=data)

    # Render template HTML dengan data
    # rendered = render_template('skeleton/f05_pbuss/template_01.html', data=data)
    
    

    # Konversi HTML menjadi PDF menggunakan pdfkit dengan konfigurasi
    # pdf = pdfkit.from_string(rendered, False, configuration=config)
    # Kirim file PDF ke pengguna
    # response = send_file(
    #     pdf,
    #     attachment_filename='report.pdf',
    #     as_attachment=True,
    #     mimetype='application/pdf'
    # )
    # return response
