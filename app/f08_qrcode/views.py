from flask import render_template, jsonify, session, request, redirect, flash, send_file
import pyqrcode
import io
import base64
from . import f08_qrcode
import qrcode

# create
@f08_qrcode.route('/qrcode', methods=['GET'])
def create():
    link = request.args.get('link', default='https://www.youtube.com/')
    qr_code = pyqrcode.create(link)
    buffer = io.BytesIO()
    qr_code.png(buffer, scale=5)
    buffer.seek(0)
    
    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name='QRCode.png')


# look 
@f08_qrcode.route('/qrcode/look', methods=['GET'])
def index_qrcode():
    link = request.args.get('link', default='https://www.youtube.com/')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render_template('f08_qrcode/index.html', img_data=img_base64)