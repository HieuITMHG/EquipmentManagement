from flask import Blueprint, render_template, request, session, redirect, flash

from helpers.helpers import login_required, get_expect_returning_time, role_required
from services.student_service import StudentService
from services.room_service import RoomService
from services.equipment_service import EquipmentService
from services.borrow_service import BorrowService
from services.penalty_service import PenaltyService
from enums.role_type import RoleID

student_blueprint = Blueprint('student', __name__)

@student_blueprint.route('/student', methods=['GET'])

@login_required
@role_required(RoleID.STUDENT.value)
def student_dashboard():
    if request.method == "GET":
        student_id = session.get('account_id')
        lst_room = RoomService.get_all_room()
        student = StudentService.get_student_by_id(student_id)
        selected_room = request.args.get("room", "")
        borrow_equipment = BorrowService.get_borrow_equipment(student_id)
        if len(borrow_equipment) != 0:
            lst_room = [{'id': borrow_equipment[0]['borrow_room_id']}]
            selected_room = borrow_equipment[0]['borrow_room_id']
        lst_equipment = EquipmentService.get_borrowable_equipment_by_room(selected_room)
        if selected_room is None or selected_room == "":
                lst_equipment = []
        return render_template('student/student_dashboard.html', 
                               student=student, 
                               lst_room=lst_room, 
                               selected_value=selected_room,
                               lst_equipment=lst_equipment,
                               borrow_equipment=borrow_equipment)
    
@student_blueprint.route('/student/borrow', methods=['POST'])
@login_required
@role_required(RoleID.STUDENT.value)
def student_borrow():
    if request.method == "POST":
        lst_item = request.form.getlist('items')  
        student_id = session.get("account_id") 
        room_id = request.form.get("room_id")
        if not lst_item:
            flash("Vui lòng chọn ít nhất một thiết bị!", "error")
            return redirect('/student')

        expect_returning_time = get_expect_returning_time()

        if not expect_returning_time:
            flash("Không thể mượn thiết bị ngoài khung giờ quy định!", "error")
            return redirect('/student')

        equipment_ids = ",".join(lst_item)  
        existing_request = BorrowService.get_existing_borrow_request(student_id)
        if len(existing_request) < 1:
            borrow_request_id = BorrowService.create_borrow_request(student_id, equipment_ids, expect_returning_time, room_id)

            if borrow_request_id:
                flash(f"✅ Mượn thiết bị thành công! Mã yêu cầu: {borrow_request_id}", "success")
            else:
                flash("❌ Lỗi khi mượn thiết bị!", "error")
        else:
            if BorrowService.update_borrow_request(equipment_ids, existing_request[0]["id"]):
                flash("Cập nhật yêu cầu mượn thiết bị thành công!", "success")
            else:
                flash("Lỗi khi cập nhật yêu cầu mượn thiết bị!", "error")

        return redirect('/student')
    
@student_blueprint.route('/student/profile', methods=['GET'])
@login_required
@role_required(RoleID.STUDENT.value)
def student_profile():
    if request.method == "GET":
        student = StudentService.get_student_by_id(session.get('account_id'))
        return render_template('student/student_profile.html', student=student)
    
@student_blueprint.route('/student/borrow_history', methods=['GET', 'POST'])
@login_required
@role_required(RoleID.STUDENT.value)
def borrow_history():
    student_id = session.get('account_id')  
    student = StudentService.get_student_by_id(student_id)

    if request.method == 'POST':
        borrowing_time = request.form.get('borrowing_time')  
        lst_borrow = BorrowService.get_borrow_equipment_by_date(student_id, borrowing_time)
    else:
        lst_borrow = BorrowService.get_borrow_history(student_id)

    return render_template('student/borrow_history.html', lst_borrow=lst_borrow, student=student)

@student_blueprint.route('/student/violation', methods=['GET'])
@role_required(RoleID.STUDENT.value)
@login_required
def violation():
    student_id = session.get('account_id')  
    student = StudentService.get_student_by_id(student_id)
    lst_violation = PenaltyService.get_violation_by_id(student_id)
    return render_template('student/violation.html', lst_violation=lst_violation, student=student)
    

@student_blueprint.route('/student/cancel_borrow_equipment', methods=['POST'])
@role_required(RoleID.STUDENT.value)
@login_required
def cancel_borrow_equipment():
    borrow_request_id = request.form.get('borrow_request_id')
    equipment_id = request.form.get('equipment_id')
    if BorrowService.cancel_borrow_equipment(equipment_id, borrow_request_id):
        flash("Bạn đa hủy yêu cầu mượn thành công!", "success")
    else:
        flash("Đã xảy ra lỗi trong quá trình hủy yêu cầu mượn!", "error")
    return redirect('/student')
