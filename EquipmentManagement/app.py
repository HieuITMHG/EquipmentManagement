from flask import Flask
from init_app import init_app
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app = init_app(app)

csrf = CSRFProtect(app)

from blueprints import general

app.register_blueprint(general.general_blueprint)

if __name__ == '__main__':
    app.run(debug=True)