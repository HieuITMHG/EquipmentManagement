from flask import Blueprint, render_template, request, session, redirect

from helpers.helpers import login_required
from services.student_service import StudentService
from services.room_service import RoomService
from services.equipment_service import EquipmentService

student_blueprint = Blueprint('student', __name__)

@student_blueprint.route('/student', methods=['GET'])
@login_required
def student_dashboard():
    if request.method == "GET":
        lst_room = RoomService.get_all_room()
        student = StudentService.get_student_by_id(session.get('account_id'))
        selected_room = request.args.get("room", "")
        lst_equipment = EquipmentService.get_borrowable_equipment_by_room(selected_room)
        return render_template('student/student_dashboard.html', 
                               student=student, 
                               lst_room=lst_room, 
                               selected_value=selected_room,
                               lst_equipment=lst_equipment)
    
@student_blueprint.route('/student/borrow', methods=['POST'])
@login_required
def student_borrow():
    if request.method == "POST":
        lst_item = request.form.getlist('items')
        print(lst_item)
        return redirect('/student')