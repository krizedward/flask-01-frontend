from flask import render_template, jsonify, session, request, redirect, url_for, send_file, current_app as app
from ..mysql.models import get_data_pbuss, get_pbuss_by_kode, add_data_accounting, get_accounting_by_id, update_accounting, delete_data_accounting
from reportlab.pdfgen import canvas
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from PyPDF2 import PdfReader, PdfWriter
from . import f05_pbuss

import locale
from datetime import datetime

# Set locale to Indonesian (ID) for example
locale.setlocale(locale.LC_ALL, 'id_ID')
# import pdfkit

# Tentukan path ke wkhtmltopdf dan buat konfigurasi
# path_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'  # Sesuaikan dengan path di sistem Anda
# config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# index
@f05_pbuss.route('/pdf/<kode>', methods=['GET'])
def index_pbuss(kode):
    pbuss_data = get_pbuss_by_kode(kode)
    return render_template('f05_pbuss/index.html', data=pbuss_data, kode=kode)
    # return f'menampilkan kode: {kode}'


@f05_pbuss.route('/pbuss/<kode>')
def show_pbuss(kode):
    pbuss_data = get_pbuss_by_kode(kode)
    return render_template('pbuss_detail.html', pbuss=pbuss_data, kode=kode)

@f05_pbuss.route('/pdf/<kode>/download', methods=['GET'])
def ex_pbuss(kode):
    # Ambil data dari basis data atau sumber lainnya
    data = {
        'title': 'Laporan Bulanan',
        'content': 'Ini adalah contoh laporan bulanan dengan data dinamis yang diambil dari sumber tertentu.'
    }
    pbuss_data = get_pbuss_by_kode(kode)
    return render_template('skeleton/pbuss/template_01.html', data=pbuss_data, kode=kode)

    # Send the file back to the user for download
    # return send_file(temp_file_path, as_attachment=True, download_name=filename)

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

@f05_pbuss.route('/upload-pbuss/<kode>', methods=['POST'])
def upload_raport(kode):
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

            # kode = 2021071337
            pbuss_data = get_pbuss_by_kode(kode)
            # pbuss_data = get_pbuss_by_kode(2021071337)

            # Convert to string if needed (assuming 'id' is an integer)
            id = str(pbuss_data['id'])
            nomor_surat_sekolah = str(pbuss_data['nomor_surat_sekolah'])
            nama = str(pbuss_data['nama'])
            sekolah = str(pbuss_data['sekolah'])
            # buss = str(pbuss_data['buss'])
            # us_buss = str(pbuss_data['us_buss'])

            formatted_buss = locale.format_string('%d', pbuss_data['buss'], grouping=True).replace(',', '.')
            formatted_us_buss = locale.format_string('%d', pbuss_data['us_buss'], grouping=True).replace(',', '.')

            # Dapatkan tanggal saat ini
            tanggal_sekarang = datetime.now().strftime('%d %B %Y')

            # Create a new PDF with ReportLab
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("Helvetica", 11)  # Mengatur ukuran font menjadi 6
            # can.drawString(170, 725, id)
            can.drawString(93, 667, nomor_surat_sekolah)
            can.drawString(485, 667, tanggal_sekarang)
            can.drawString(54, 489, 'Menunjuk surat Dewan Pengurus PPPK Petra nomor: ' + nomor_surat_sekolah)
            can.drawString(185, 434, nama)
            can.drawString(185, 419, sekolah)
            can.drawString(313, 392, 'Rp.' + formatted_buss)
            can.drawString(248, 354, 'Rp.' + formatted_us_buss)
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

            # Ensure the upload directory exists
            upload_folder = os.path.join(app.root_path, 'static', 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            # Save the result
            temp_file_path = os.path.join(upload_folder, filename)
            with open(temp_file_path, 'wb') as f:
                output.write(f)

            # Send the file back to the user for download
            return send_file(temp_file_path, as_attachment=True, download_name=filename)

    return 'Gagal mengunggah file.', 400

