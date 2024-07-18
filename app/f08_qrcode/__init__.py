from flask import Blueprint

f08_qrcode = Blueprint('f08_qrcode', __name__)

from . import views