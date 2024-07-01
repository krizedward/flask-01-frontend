from flask import render_template, request, redirect, send_file, send_from_directory, current_app as app
from reportlab.pdfgen import canvas
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from PyPDF2 import PdfReader, PdfWriter
from . import f02_pdf


@f02_pdf.route('/pdf-raport', methods=['GET'])
def index():
    return render_template('f02_pdf/index.html')

@f02_pdf.route('/upload-raport', methods=['POST'])
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
            can = canvas.Canvas(packet, pagesize=letter)
            can.setFont("Helvetica", 6)  # Mengatur ukuran font menjadi 6
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

# Untuk Melihat Pdf

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

@f02_pdf.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(os.path.join(app.root_path, 'static', 'uploads'), filename))
        # return render_template('f02_pdf/index.html')
        return render_template('f02_pdf/index.html', filename=filename)
    return redirect(request.url)

@f02_pdf.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'uploads'), filename)
