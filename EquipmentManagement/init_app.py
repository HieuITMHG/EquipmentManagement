from flask import Flask
import os
from dotenv import load_dotenv
from flask_migrate import Migrate

from models.database import db

def init_app(app: Flask):
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    db.init_app(app)
    migrate = Migrate(app, db)

    return app
