from flask import Blueprint, render_template, request, session

from services.equipment_service import EquipmentService

manager_blueprint = Blueprint('manager', __name__)

@manager_blueprint.route('/', methods=['GET'])
def index():
    if request.method == "GET":
        lst_equipment = EquipmentService.get_all_equipment()

        return render_template('manager/manager_dashboard.html', lst_equipment=lst_equipment)