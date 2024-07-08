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
import zipfile

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
            # output1 = PdfWriter()
            # output2 = PdfWriter()  # Assuming you want to generate two PDFs
            output = PdfWriter()
            pbuss_data = get_pbuss_by_kode(kode)

            # Convert to string if needed (assuming 'id' is an integer)
            nomor_surat_sekolah = str(pbuss_data['nomor_surat_sekolah'])
            nama = str(pbuss_data['nama'])
            sekolah = str(pbuss_data['sekolah'])

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
            can.drawString(51, 583.5, 'Bapak/Ibu') # new_data
            can.drawString(51, 568, 'DARMO INDAH SELATAN HH NO 34, SURABAYA') # new_data
            can.drawString(54, 489, 'Menunjuk surat Dewan Pengurus PPPK Petra nomor: ' + nomor_surat_sekolah)
            can.drawString(337, 460.5, 'Bapak/Ibu,') # new_data
            can.drawString(185, 434, nama)
            can.drawString(185, 419, sekolah)
            can.drawString(185, 405, 'XIA') # new_data
            can.drawString(313, 392, 'Rp.' + formatted_buss)
            can.drawString(248, 354, 'Rp.' + formatted_us_buss)
            can.drawString(188, 326.5, 'Bapak asd, kami ucapkan terima kasih.') # new_data
            can.save()

            # Move to the beginning of the BytesIO buffer
            packet.seek(0)
            new_pdf = PdfReader(packet)

            # # Add the "watermark" (which is the new pdf) on the existing page
            # for page_num in range(len(existing_pdf.pages)):
            #     page = existing_pdf.pages[page_num]
            #     if page_num == 0:  # Add new content only to the first page
            #         page.merge_page(new_pdf.pages[0])
            #     output1.add_page(page)
            #     output2.add_page(page)

            # # Create BytesIO buffers to store the final PDFs
            # final_output1 = BytesIO()
            # output1.write(final_output1)
            # final_output1.seek(0)

            # final_output2 = BytesIO()
            # output2.write(final_output2)
            # final_output2.seek(0)

            # # Create a new filename for the PDFs
            # new_filename1 = f"PBUSS_1.pdf"
            # new_filename2 = f"PBUSS_2.pdf"

            # # Create a BytesIO buffer for the zip file
            # zip_buffer = BytesIO()
            # with zipfile.ZipFile(zip_buffer, 'w') as z:
            #     z.writestr(new_filename1, final_output1.getvalue())
            #     z.writestr(new_filename2, final_output2.getvalue())

            # # Spool back to the beginning of the BytesIO buffer
            # zip_buffer.seek(0)

            # # Send the zip file back to the user
            # return send_file(zip_buffer, as_attachment=True, download_name=f"PBUSS_{nomor_surat_sekolah}.zip")

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

@f05_pbuss.route('/download-all-pbuss', methods=['GET'])
# def download_all_pbuss():
#     pbuss_data = get_data_pbuss()
#     return jsonify(pbuss_data)
def download_all_pbuss():
    pbuss_data = get_data_pbuss()
    # return jsonify(pbuss_data)
    # Group data by school
    data_by_school = {}
    for data in pbuss_data:
        school = data['sekolah']
        if school not in data_by_school:
            data_by_school[school] = []
        data_by_school[school].append(data)
    
    # Create a BytesIO buffer for the zip file
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as z:
        for school, data_list in data_by_school.items():
            for data in data_list:
                # Create a new PDF for each entry
                packet = BytesIO()
                can = canvas.Canvas(packet, pagesize=letter)
                can.setFont("Helvetica", 11)
                
                kode = str(data['kode'])
                nomor_surat_sekolah = str(data['nomor_surat_sekolah'])
                nama = str(data['nama'])
                formatted_buss = locale.format_string('%d', data['buss'], grouping=True).replace(',', '.')
                formatted_us_buss = locale.format_string('%d', data['us_buss'], grouping=True).replace(',', '.')
                # tanggal_sekarang = datetime.now().strftime('%d %B %Y')
                tanggal_sekarang = '16 Juni 2024'

                can.drawString(93, 667, nomor_surat_sekolah)
                can.drawString(485, 667, tanggal_sekarang)
                can.drawString(51, 583.5, data['ortu_murid'] + ' ' + (data['nama_ortu'] if data['nama_ortu'] is not None else ''))
                can.drawString(51, 568, data['almt'] if data['almt'] is not None else '') # Handling None value
                can.drawString(61, 488, 'Menunjuk surat Dewan Pengurus PPPK Petra no : ' + nomor_surat_sekolah)
                can.drawString(338, 460.5, data['ortu_murid'] + ',') # Assuming 'ortu_murid' is always present
                # can.drawString(338, 460.5, data['ortu_murid'] + ' ' + (data['nama_ortu'] if data['nama_ortu'] is not None else '') + ',') # Assuming 'ortu_murid' is always present
                can.drawString(185, 434, nama)
                can.drawString(185, 419, data['nama_sekolah'])
                can.drawString(185, 405, data['nama_kelas'] if data['nama_kelas'] is not None else '') # Handling None value
                can.drawString(185, 392, 'Rp.' + formatted_buss)
                # can.drawString(313, 392, 'Rp.' + formatted_buss)
                can.drawString(248, 354, 'Rp.' + formatted_us_buss)
                can.drawString(188, 326.5, data['ortu_murid'] + ', kami ucapkan terima kasih.') # Assuming 'ortu_murid' is always present
                can.save()

                packet.seek(0)
                new_pdf = PdfReader(packet)

                # Load the template PDF from the static folder
                template_path = os.path.join(app.root_path, 'static', 'template_pbuss.pdf')
                existing_pdf = PdfReader(open(template_path, 'rb'))
                output = PdfWriter()

                # Merge the new content with the template on the first page
                page = existing_pdf.pages[0]
                page.merge_page(new_pdf.pages[0])
                output.add_page(page)

                # Add the remaining pages of the template if any
                for page_num in range(1, len(existing_pdf.pages)):
                    output.add_page(existing_pdf.pages[page_num])

                # Create BytesIO buffer to store the final PDF
                final_output = BytesIO()
                output.write(final_output)
                final_output.seek(0)

                # Create a new filename for the PDF
                new_filename = f"{school}/{kode}.pdf"

                # Add the PDF to the zip file in the respective school folder
                z.writestr(new_filename, final_output.getvalue())

    # Spool back to the beginning of the BytesIO buffer
    zip_buffer.seek(0)

    # Send the zip file back to the user
    return send_file(zip_buffer, as_attachment=True, download_name="PBUSS_PPPK_PETRA_2024.zip")

@f05_pbuss.route('/download-all-pbuss-one-pdf', methods=['GET'])
# def download_all_pbuss():
#     pbuss_data = get_data_pbuss()
#     return jsonify(pbuss_data)
def download_all_pbuss_one_pdf():
    pbuss_data = get_data_pbuss()
    
    # Group data by school
    data_by_school = {}
    for data in pbuss_data:
        school = data['sekolah']
        if school not in data_by_school:
            data_by_school[school] = []
        data_by_school[school].append(data)
    
    # Create a BytesIO buffer for the final PDF
    final_output = BytesIO()
    output = PdfWriter()
    
    for school, data_list in data_by_school.items():
        for data in data_list:
            # Create a new PDF for each entry
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("Helvetica", 11)
            
            kode = str(data['kode'])
            nomor_surat_sekolah = str(data['nomor_surat_sekolah'])
            nama = str(data['nama'])
            formatted_buss = locale.format_string('%d', data['buss'], grouping=True).replace(',', '.')
            formatted_us_buss = locale.format_string('%d', data['us_buss'], grouping=True).replace(',', '.')
            # tanggal_sekarang = datetime.now().strftime('%d %B %Y')
            tanggal_sekarang = '16 Juni 2024'

            can.drawString(93, 667, nomor_surat_sekolah)
            can.drawString(485, 667, tanggal_sekarang)
            can.drawString(51, 583.5, data['ortu_murid'] + ' ' + (data['nama_ortu'] if data['nama_ortu'] is not None else ''))
            can.drawString(51, 568, data['almt'] if data['almt'] is not None else '') # Handling None value
            can.drawString(61, 488, 'Menunjuk surat Dewan Pengurus PPPK Petra no : ' + nomor_surat_sekolah)
            can.drawString(338, 460.5, data['ortu_murid'] + ',') # Assuming 'ortu_murid' is always present
            # can.drawString(338, 460.5, data['ortu_murid'] + ' ' + (data['nama_ortu'] if data['nama_ortu'] is not None else '') + ',') # Assuming 'ortu_murid' is always present
            can.drawString(185, 434, nama)
            can.drawString(185, 419, data['nama_sekolah'])
            can.drawString(185, 405, data['nama_kelas'] if data['nama_kelas'] is not None else '') # Handling None value
            can.drawString(185, 392, 'Rp.' + formatted_buss)
            can.drawString(248, 354, 'Rp.' + formatted_us_buss)
            can.drawString(188, 326.5, data['ortu_murid'] + ', kami ucapkan terima kasih.') # Assuming 'ortu_murid' is always present
            can.save()

            packet.seek(0)
            new_pdf = PdfReader(packet)

            # Load the template PDF from the static folder
            # template_path = os.path.join(os.getcwd(), 'static', 'template_pbuss.pdf')
            # existing_pdf = PdfReader(open(template_path, 'rb'))

            # Load the template PDF from the static folder
            template_path = os.path.join(app.root_path, 'static', 'template_pbuss.pdf')
            existing_pdf = PdfReader(open(template_path, 'rb'))
            
            # Merge the new content with the template on the first page
            page = existing_pdf.pages[0]
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)

            # Add the remaining pages of the template if any
            for page_num in range(1, len(existing_pdf.pages)):
                output.add_page(existing_pdf.pages[page_num])

    # Save the final PDF to the buffer
    output.write(final_output)
    final_output.seek(0)

    # Send the PDF file back to the user
    return send_file(final_output, as_attachment=True, download_name="PBUSS_PPPK_PETRA_2024")

@f05_pbuss.route('/contoh', methods=['GET'])
def download_zip():
    # Menggunakan BytesIO untuk menyimpan data ZIP di dalam memori
    zip_buffer = BytesIO()

    # Membuat objek zipfile.ZipFile untuk menulis data ke zip_buffer
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, False) as z:
        # Contoh data yang akan dimasukkan ke dalam file ZIP
        file_data = b"Contoh data yang akan dimasukkan ke dalam file ZIP"
        
        # Menambahkan file ke dalam ZIP dengan nama file 'contoh.txt'
        z.writestr('contoh.txt', file_data)

        # Jika Anda memiliki lebih dari satu file, dapat menambahkan file lainnya seperti ini:
        # z.writestr('contoh2.txt', b"Isi dari file kedua dalam ZIP")

    # Setelah selesai menulis data ke dalam zip_buffer, pindah ke awal buffer
    zip_buffer.seek(0)

    # Membuat respons HTTP dengan file ZIP sebagai attachment
    # response = make_response(send_file(zip_buffer, mimetype='application/zip', as_attachment=True, attachment_filename='example.zip'))
    return send_file(zip_buffer, as_attachment=True, download_name=f"PBUSS.zip")
    
    # return response