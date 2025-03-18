from flask import Blueprint, render_template, request, session, redirect, flash

from helpers.helpers import login_required, get_expect_returning_time
from services.student_service import StudentService
from services.room_service import RoomService
from services.equipment_service import EquipmentService
from services.borrow_service import BorrowService
from services.penalty_service import PenaltyService

student_blueprint = Blueprint('student', __name__)

@student_blueprint.route('/student', methods=['GET'])
@login_required
def student_dashboard():
    if request.method == "GET":
        lst_room = RoomService.get_all_room()
        student = StudentService.get_student_by_id(session.get('account_id'))
        selected_room = request.args.get("room", "")
        lst_equipment = EquipmentService.get_borrowable_equipment_by_room(selected_room)
        borrow_equipment = BorrowService.get_borrow_equipment(session.get('account_id'))
        return render_template('student/student_dashboard.html', 
                               student=student, 
                               lst_room=lst_room, 
                               selected_value=selected_room,
                               lst_equipment=lst_equipment,
                               borrow_equipment=borrow_equipment)
    
@student_blueprint.route('/student/borrow', methods=['POST'])
@login_required
def student_borrow():
    if request.method == "POST":
        lst_item = request.form.getlist('items')  
        student_id = session.get("account_id") 

        if not lst_item:
            flash("Vui lòng chọn ít nhất một thiết bị!", "danger")
            return redirect('/student')

        expect_returning_time = get_expect_returning_time()

        if not expect_returning_time:
            flash("Không thể mượn thiết bị ngoài khung giờ quy định!", "danger")
            return redirect('/student')

        # Gọi service để thêm borrow request
        equipment_ids = ",".join(lst_item)  # Chuyển danh sách thành chuỗi "1,2,3"
        print(equipment_ids)
        borrow_request_id = BorrowService.create_borrow_request(student_id, equipment_ids, expect_returning_time)

        if borrow_request_id:
            flash(f"✅ Mượn thiết bị thành công! Mã yêu cầu: {borrow_request_id}", "success")
        else:
            flash("❌ Lỗi khi mượn thiết bị!", "danger")

        return redirect('/student')
    
@student_blueprint.route('/student/profile', methods=['GET'])
@login_required
def student_profile():
    if request.method == "GET":
        student = StudentService.get_student_by_id(session.get('account_id'))
        return render_template('student/student_profile.html', student=student)
    
@student_blueprint.route('/student/borrow_history', methods=['GET', 'POST'])
@login_required
def borrow_history():
    student_id = session.get('account_id')  
    student = StudentService.get_student_by_id(student_id)

    if request.method == 'POST':
        borrowing_time = request.form.get('borrowing_time')  
        lst_borrow = BorrowService.get_borrow_equipment_by_date(student_id, borrowing_time)
    else:
        lst_borrow = BorrowService.get_borrow_equipment(student_id)

    return render_template('student/borrow_history.html', lst_borrow=lst_borrow, student=student)

@student_blueprint.route('/student/violation', methods=['GET'])
@login_required
def violation():
    student_id = session.get('account_id')  
    student = StudentService.get_student_by_id(student_id)
    lst_violation = PenaltyService.get_violation_by__id(student_id)
    return render_template('student/violation.html', lst_violation=lst_violation, student=student)
    