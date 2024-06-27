from flask import render_template
from . import main
from ..auth.services import login_required 

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html')

@main.route('/main')
# @main.route('/')
@login_required
def home():
    return render_template('main/home.html')

@main.route('/main-about')
@login_required
def about():
    return render_template('main/about.html')
