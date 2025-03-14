from flask import Flask
from init_app import init_app
from flask_wtf.csrf import CSRFProtect

# from init_data import initialize_data

app = Flask(__name__)
app = init_app(app)

csrf = CSRFProtect(app)

from blueprints import general
# from blueprints import add_data
from blueprints import manager
from blueprints import student
from blueprints import staff

app.register_blueprint(general.general_blueprint)
# app.register_blueprint(add_data.add_data_blueprint)
app.register_blueprint(manager.manager_blueprint)
app.register_blueprint(student.student_blueprint)
app.register_blueprint(staff.staff_blueprint)

# with app.app_context():
#     initialize_data(app) 

if __name__ == '__main__':
    app.run(debug=True)