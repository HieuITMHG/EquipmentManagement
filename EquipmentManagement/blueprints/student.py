from flask import Blueprint, render_template, request, session, redirect, flash

from helpers.helpers import login_required, get_expect_returning_time
from services.student_service import StudentService
from services.room_service import RoomService
from services.equipment_service import EquipmentService
from services.borrow_service import BorrowService

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
        lst_item = request.form.getlist('items')  # Danh sách thiết bị
        student_id = session.get("account_id")  # Lấy ID sinh viên từ session

        if not lst_item:
            flash("Vui lòng chọn ít nhất một thiết bị!", "danger")
            return redirect('/student')

        expect_returning_time = get_expect_returning_time()

        if not expect_returning_time:
            flash("Không thể mượn thiết bị ngoài khung giờ quy định!", "danger")
            return redirect('/student')

        # Gọi service để thêm borrow request
        equipment_ids = ",".join(lst_item)  # Chuyển danh sách thành chuỗi "1,2,3"
        borrow_request_id = BorrowService.create_borrow_request(student_id, equipment_ids, expect_returning_time)

        if borrow_request_id:
            flash(f"✅ Mượn thiết bị thành công! Mã yêu cầu: {borrow_request_id}", "success")
        else:
            flash("❌ Lỗi khi mượn thiết bị!", "danger")

        return redirect('/student')