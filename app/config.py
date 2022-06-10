from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from os import environ

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
csrf = CSRFProtect()

#firebase crednetials
FIREBASE_CREDENTIALS = {
    "apiKey": environ.get('FIREBASE_API_KEY'),
    "authDomain": environ.get('AUTH_DOMAIN'),
    "projectId": environ.get('PROJECT_ID'),
    "databaseURL": environ.get('DATABASE_URL'),
    "storageBucket": environ.get('STORAGE_BUCKET'),
    "messagingSenderId": environ.get('MESSAGING_SENDER_ID'),
    "appId": environ.get('APP_ID'),
    "measurementId": environ.get('MEAUREMENT_ID'),
}

GOOGLE_CLIENT_ID = environ.get('GOOGLE_CLIENT_ID')

DOMAIN_NAME = environ.get('DOMAIN_NAME')

def create_app():
    app = Flask(__name__)
    app.secret_key = environ.get('SECRET_KEY')
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.main.routes import main
    app.register_blueprint(main)

    from app.something.routes import something
    app.register_blueprint(something)

    return app