from flask import render_template, jsonify, session, request, redirect, flash
import requests
from . import f07_booking
from ..mysql.models import get_data_student
from datetime import datetime
import locale
# Set locale to Indonesian
locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

# index
@f07_booking.route('/booking', methods=['GET'])
def index_student():
    data = get_data_student()
    return render_template('f07_booking/index.html', data = data)

@f07_booking.route('/time')
def get_time():
    now = datetime.now().strftime('%A, %d %B %Y %H:%M:%S')
    return jsonify(time=now)

# create
@f07_booking.route('/booking/create', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('f07_booking/create.html')