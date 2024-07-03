import os
from dotenv import load_dotenv
from flask import Flask

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    with app.app_context():
        # Import parts of our application
        from .mysql import db
        from . import routes

        # Create database connection
        db.init_db()

    # Load
    app.secret_key = os.environ.get('SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .f01_commisions import f01_commisions as commisions_blueprint
    app.register_blueprint(commisions_blueprint)

    from .f02_pdf import f02_pdf as pdf_blueprint
    app.register_blueprint(pdf_blueprint)

    from .f03_accounting import f03_accounting as accounting_blueprint
    app.register_blueprint(accounting_blueprint)

    from .f04_inventory import f04_inventory as inventory_blueprint
    app.register_blueprint(inventory_blueprint)

    return app