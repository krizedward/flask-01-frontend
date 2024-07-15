from flask import render_template, jsonify, session, request, redirect, flash
import requests
from . import f07_booking
from datetime import datetime
import locale
# Set locale to Indonesian
locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

# index
@f07_booking.route('/booking', methods=['GET'])
def index_student():
    return render_template('f07_booking/index.html')

@f07_booking.route('/time')
def get_time():
    now = datetime.now().strftime('%A, %d %B %Y %H:%M:%S')
    return jsonify(time=now)

# create
@f07_booking.route('/booking/create', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('f07_booking/create.html')

# show
@f07_booking.route('/booking/show', methods=['GET','POST'])
def show():
    if request.method == 'GET':
        # Example data array (replace this with actual data fetching logic)
        data = [
            {"ruangan": "Room A", "jam": "7:30 AM", "peminjam": "Pak Edward"},
            {"ruangan": "Room B", "jam": "08:00 AM", "peminjam": "Pak Edward"},
            {"ruangan": "Room C", "jam": "08:30 AM", "peminjam": "Pak Edward"},
            {"ruangan": "Room D", "jam": "09:30 AM", "peminjam": "Pak Edward"},
            {"ruangan": "Room E", "jam": "10:00 AM", "peminjam": "Pak Edward"},
            {"ruangan": "Room F", "jam": "10:30 AM", "peminjam": "Pak Edward"},
            {"ruangan": "Room G", "jam": "11:00 AM", "peminjam": "Pak Edward"},
            {"ruangan": "Room H", "jam": "11:30 AM", "peminjam": "Pak Edward"},
            {"ruangan": "Room I", "jam": "12:00 AM", "peminjam": "Pak Edward"},
            {"ruangan": "Room J", "jam": "12:30 PM", "peminjam": "Pak Edward"},
            {"ruangan": "Room J", "jam": "01:00 PM", "peminjam": "Pak Edward"},
            {"ruangan": "Room J", "jam": "01:30 PM", "peminjam": "Pak Edward"},
            {"ruangan": "Room J", "jam": "02:00 PM", "peminjam": "Pak Edward"},
            {"ruangan": "Room J", "jam": "02:30 PM", "peminjam": "Pak Edward"},
            {"ruangan": "Room J", "jam": "03:00 PM", "peminjam": "Pak Edward"},
            {"ruangan": "Room J", "jam": "03:30 PM", "peminjam": "Pak Edward"},
            {"ruangan": "Room J", "jam": "04:00 PM", "peminjam": "Pak Edward"},
        ]

        return render_template('f07_booking/show.html', data=data)

# profile
@f07_booking.route('/booking/profile', methods=['GET'])
def profile():
    if request.method == 'GET':
        return render_template('f07_booking/profile.html')