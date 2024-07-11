from flask import Blueprint

f06_student = Blueprint('f06_student', __name__)

from . import views