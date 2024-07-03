from flask import Blueprint

f04_inventory = Blueprint('f04_inventory', __name__)

from . import views