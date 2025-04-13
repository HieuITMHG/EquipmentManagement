from flask import Flask
import os
from dotenv import load_dotenv

def init_app(app: Flask):
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    return app
