import os
from dotenv import load_dotenv
from flask import Flask

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Load
    app.secret_key = os.environ.get('SECRET_KEY')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .f01_commisions import f01_commisions as commisions_blueprint
    app.register_blueprint(commisions_blueprint)

    from .f02_pdf import f02_pdf as pdf_blueprint
    app.register_blueprint(pdf_blueprint)

    return app