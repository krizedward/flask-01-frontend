from flask import Blueprint

f03_accounting = Blueprint('f03_accounting', __name__)

from . import views