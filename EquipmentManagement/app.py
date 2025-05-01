from flask import Flask
from init_app import init_app
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app = init_app(app)

csrf = CSRFProtect(app)

def format_currency(value):
    try:
        # Convert value to float and format with commas, no decimal places
        return "{:,.0f}".format(float(value))
    except (ValueError, TypeError):
        return value  # Return original value if conversion fails

# Register the filter with Jinja2
app.jinja_env.filters['format_currency'] = format_currency


from blueprints import general
from blueprints import manager
from blueprints import borrow
from blueprints import staff
from blueprints import equipment
from blueprints import inventory
    
app.register_blueprint(general.general_blueprint)
app.register_blueprint(manager.manager_blueprint)
app.register_blueprint(borrow.borrow_blueprint)
app.register_blueprint(staff.staff_blueprint)
app.register_blueprint(equipment.equipment_blueprint)
app.register_blueprint(inventory.inventory_blueprint)

if __name__ == '__main__':
    app.run(debug=True)