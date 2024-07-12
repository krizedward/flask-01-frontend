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
            {"ruangan": "Room A", "jam": "10:00 AM", "peminjam": "John Doe"},
            {"ruangan": "Room B", "jam": "11:00 AM", "peminjam": "Jane Smith"},
            {"ruangan": "Room C", "jam": "12:00 PM", "peminjam": "Alice Johnson"},
            {"ruangan": "Room D", "jam": "01:00 PM", "peminjam": "Bob Brown"},
            {"ruangan": "Room E", "jam": "02:00 PM", "peminjam": "Charlie Davis"},
            {"ruangan": "Room F", "jam": "03:00 PM", "peminjam": "Eve Miller"},
            {"ruangan": "Room G", "jam": "04:00 PM", "peminjam": "Frank Wilson"},
            {"ruangan": "Room H", "jam": "05:00 PM", "peminjam": "Grace Lee"},
            {"ruangan": "Room I", "jam": "06:00 PM", "peminjam": "Henry Clark"},
            {"ruangan": "Room J", "jam": "07:00 PM", "peminjam": "Ivy Lewis"}
        ]

        return render_template('f07_booking/show.html', data=data)