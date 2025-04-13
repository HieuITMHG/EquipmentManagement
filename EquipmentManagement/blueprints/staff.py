from flask import Blueprint, render_template, request, session, redirect,flash, url_for

from helpers.helpers import login_required, role_required
from services.account_service import AccountService
from services.staff_service import StaffService
from services.equipment_service import EquipmentService
from services.borrow_service import BorrowService
from enums.action_type import ActionType
from services.room_service import RoomService
from services.liquidation_slip_service import LiquidationSlipService
from services.repair_ticket import RepairTicketService
from services.violation_service import ViolationService
from services.student_service import StudentService
from services.penalty_service import PenaltyService
from enums.role_type import RoleID

staff_blueprint = Blueprint('staff', __name__)

@staff_blueprint.route('/staff', methods=['GET'])
@login_required
@role_required(RoleID.STAFF.value)
def staff():
    if request.method == "GET":
        login_staff = AccountService.get_account_by_person_id(session.get('account_id'))
        return render_template('staff/staff_profile.html', login_staff = login_staff)
    
@staff_blueprint.route('/staff/borrow_request/<int:request_id>', methods=['GET'])
@staff_blueprint.route('/staff/borrow_request', methods=['GET', 'POST'])
@role_required(RoleID.STAFF.value)
@login_required
def staff_borrow_request(request_id=None):
    if request.method == "GET":
        login_staff = AccountService.get_account_by_person_id(session.get('account_id'))
        lst_request = BorrowService.get_pending_borrow_request()
        if request_id == None:
            return render_template('staff/borrow_request.html', login_staff = login_staff, lst_request=lst_request)
        lst_borrow_equipment = BorrowService.get_equipment_by_request_id(request_id)
        return render_template('staff/borrow_request.html', login_staff=login_staff,lst_request=lst_request, lst_borrow_equipment=lst_borrow_equipment)
    borrow_request_id = int(request.form.get('request_id'))
    action = int(request.form.get('action'))
    if action == ActionType.ACCEPT.value:
        BorrowService.accept_borrow_request(borrow_request_id, session.get('account_id'))
    else:
        BorrowService.reject_borrow_request(borrow_request_id, session.get('account_id'))
    return redirect("borrow_request")


@staff_blueprint.route('/staff/staff_manage_equipment/<int:equipment_id>/', methods=['GET'])
@staff_blueprint.route('/staff/staff_manage_equipment', methods=['GET', 'POST'])
@login_required
@role_required(RoleID.STAFF.value)
def staff_manage_equipment(equipment_id=None):
    if request.method == "GET":
        room_id = request.args.get("room", "")
        login_staff = AccountService.get_account_by_person_id(session.get('account_id'))
        lst_equipment = StaffService.get_all_equipment()
        room=RoomService.get_all_room()
        equipment = None
        if equipment_id != None:
            equipment = EquipmentService.get_equipment_by_id(equipment_id)
        if room_id != "":
            lst_equipment = EquipmentService.get_equipment_by_room(room_id)

        return render_template('staff/staff_manage_equipment.html', login_staff = login_staff,
                                lst_equipment=lst_equipment,
                                equi=equipment,
                                room=room)
        
    new_name=request.form.get("equi_name")
    new_id=request.form.get("equi_id")
    new_room=request.form.get("room")
    if RoomService.get_room_by_id(new_room) == None:
        flash("Phòng không tồn tại", "error")
        return redirect("staff_manage_equipment")

    StaffService.change_equi_info(new_id,new_name,new_room)
    return redirect("staff_manage_equipment")


@staff_blueprint.route('/staff/add_items', methods=['GET', 'POST'])
@login_required
@role_required(RoleID.STAFF.value)
def add_items():
    login_staff = AccountService.get_account_by_person_id(session.get('account_id'))
    if request.method == "GET":
        equi=EquipmentService.get_all_equipment()
        room=RoomService.get_all_room()
        equi_type=('MOBILE', 'FIXED', 'SHARED')
        return render_template("staff/add_items.html",login_staff=login_staff,equi=equi,room=room,equi_type=equi_type)
    
    equi_name = request.form.get('equi_name')  # Tên thiết bị
    room_id = request.form.get('room')  # ID phòng
    if RoomService.get_room_by_id(room_id) == None:
        flash("Phòng không tồn tại", "error")
        return redirect("/staff/add_items")
    equi_type = request.form.get('equi_t')  # Kiểu thiết bị (BỊ TRÙNG NAME -> CẦN SỬA)  
    if(equi_name):
        EquipmentService.add_equipment(equi_name, "AVAILABLE", equi_type, room_id)
    return redirect("staff_manage_equipment")

@staff_blueprint.route('/staff/delete_equipment', methods=['GET'])
@login_required
@role_required(RoleID.STAFF.value)
def delete_equipment():
    equipment_id = request.args.get('equipment_id')  # Lấy equipment_id từ URL

    if equipment_id:
        check_d=EquipmentService.delete_equipment_by_id(equipment_id)
        if(check_d):
            flash("Thiết bị đã được xóa!", "success")  # Thông báo xóa thành công
        else:
            flash("Không thể xóa vì đang được thêm vào phiếu","error")
    
    return redirect(('staff_manage_equipment'))

@staff_blueprint.route('/staff/borrow_history/<int:request_id>', methods=['GET'])
@staff_blueprint.route('/staff/borrow_history', methods=['GET', 'POST'])
@login_required
@role_required(RoleID.STAFF.value)
def borrow_history(request_id=None):
    if request.method == "GET":
        login_staff = AccountService.get_account_by_person_id(session.get('account_id'))
        lst_request = BorrowService.get_accepted_or_returned_borrow_request()
        #print(lst_request,"***")
        if(request_id!=None):
            lst_borrow_equipment = BorrowService.get_equipment_by_request_id(request_id)
            return render_template('staff/borrow_history.html', login_staff=login_staff,lst_request=lst_request, lst_borrow_equipment=lst_borrow_equipment)
        return render_template('staff/borrow_history.html', login_staff = login_staff,lst_request=lst_request)
    
    borrow_request_id = int(request.form.get('request_id'))
    BorrowService.return_equi(borrow_request_id)
    print(borrow_request_id)
    return redirect("borrow_history")
    
@staff_blueprint.route('/staff/bh_filter', methods=['GET'])
@login_required
@role_required(RoleID.STAFF.value)
def bh_filter(request_id=None):
    if request.method == "GET":
        login_staff = AccountService.get_account_by_person_id(session.get('account_id'))
        lst_borrow_equipment = BorrowService.get_equipment_by_request_id(request_id)
        status = request.args.get("status", "")
        if (status==''):
            lst_request = BorrowService.get_accepted_or_returned_borrow_request()
        if (status=='ACCEPTED'):
            lst_request = BorrowService.get_accepted_borrow_request()
        if (status=='RETURNED'):
            lst_request = BorrowService.get_returned_borrow_request()
        return render_template('staff/borrow_history.html', login_staff=login_staff,lst_request=lst_request, lst_borrow_equipment=lst_borrow_equipment,status=status) 

@staff_blueprint.route('/staff/liquidation_slip', methods=['GET'])
@login_required
@role_required(RoleID.STAFF.value)
def liquidation_slip():
    staff_id = session.get('account_id')
    login_staff = AccountService.get_account_by_person_id(staff_id)
    broken_equipment = EquipmentService.get_broken_equipment()
    pending_requests = LiquidationSlipService.get_liquidation_slip(staff_id=staff_id, status='PENDING')
    accepted_requests = LiquidationSlipService.get_history_liquidation_slip()
    for r in pending_requests:
        r['equipments'] = LiquidationSlipService.get_equipment_in_liquidation(r['id'])
    for r in accepted_requests:
        r['equipments'] = LiquidationSlipService.get_equipment_in_liquidation(r['id'])

    return render_template('staff/liquidation_slip.html', login_staff=login_staff,
                                                        broken_equipment=broken_equipment,
                                                        pending_requests=pending_requests,
                                                        accepted_requests=accepted_requests)  
    
@staff_blueprint.route('/staff/add_liquidation_slip', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def add_liquidation_slip():
    lst_item_id = request.form.getlist('items') 
    if not lst_item_id:
        flash("Chưa chọn thiết bị cần thanh lý", "error")
        return redirect('liquidation_slip') 
    staff_id = session.get('account_id')  
    role = 'staff'  
    liquidation_slip_id = LiquidationSlipService.create_liquidation_slip(staff_id, lst_item_id, role)
    if liquidation_slip_id is None:  
        flash("Có lỗi xảy ra khi tạo phiếu thanh lý", "error")
    else:
        flash("Đã tạo phiếu thanh lý thành công", "success")  
    
    return redirect('liquidation_slip')  

@staff_blueprint.route('/staff/cancel_liquidation_request', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def cancel_liquidation_request():
    request_id = request.form.get('request_id')
    if LiquidationSlipService.delete_liquidation_slip(request_id):
        flash("Hủy yêu cầu thanh lý thành công")
    else:
        flash("Yêu cầu thanh lý không tồn tại hoặc đã được xử lý")
    return redirect('liquidation_slip')  

@staff_blueprint.route('/staff/cancel_repair_ticket', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def cancel_repair_ticket():
    request_id = request.form.get('request_id')
    if RepairTicketService.delete_repair_ticket(request_id):
        flash("Hủy yêu cầu sửa chửa thành công")
    else:
        flash("Yêu cầu sửa chửa không tồn tại hoặc đã được xử lý")
    return redirect('repair_ticket')  

@staff_blueprint.route('/staff/repair_ticket', methods=['GET'])
@login_required
@role_required(RoleID.STAFF.value)
def repair_ticket():
    staff_id = session.get('account_id')
    login_staff = AccountService.get_account_by_person_id(staff_id)
    broken_equipment = EquipmentService.get_broken_equipment()
    broken_equipment = EquipmentService.get_broken_equipment()
    pending_requests = RepairTicketService.get_repair_ticket(staff_id=staff_id, status='PENDING')
    accepted_requests = RepairTicketService.get_history_repair_ticket()
    for r in pending_requests:
        r['equipments'] = RepairTicketService.get_equipment_in_repair_ticket(r['id'])
        r['total_cost'] = RepairTicketService.get_total_cost(r['id'])
    for r in accepted_requests:
        r['equipments'] = RepairTicketService.get_equipment_in_repair_ticket(r['id'])
        r['total_cost'] = RepairTicketService.get_total_cost(r['id'])


    return render_template('staff/repair_ticket.html', login_staff=login_staff,
                                                        broken_equipment=broken_equipment,
                                                        pending_requests=pending_requests,
                                                        accepted_requests=accepted_requests)  

@staff_blueprint.route('/staff/add_repair_ticket', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def add_repair_ticket():
    staff_id = session.get('account_id')
    role = 'staff'
    form_data = request.form
    equipment_price_list = []
    
    for key in form_data:
        if key.endswith('[id]'):  # Chỉ xử lý các checkbox được chọn
            equipment_id = form_data[key]
            price_key = f"items[{equipment_id}][price]" 
            if price_key in form_data:
                price = form_data[price_key]
                equipment_price_list.append((int(equipment_id), int(price)))

    if not equipment_price_list:
        flash("Không có thiết bị nào được chọn")

    repair_ticket_id = RepairTicketService.create_repair_ticket(staff_id, equipment_price_list, role)
    if repair_ticket_id:
        flash("Tạo phiếu sửa chữa thành công")
    else:
        flash("Lỗi khi tạo phiếu sửa chữa")
    return redirect('repair_ticket') 

@staff_blueprint.route('/staff/finish_repair_ticket', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def finish_repair_ticket():
    request_id = request.form.get('request_id')
    if RepairTicketService.complete_repair_ticket(request_id):
        flash("Hoàn tất phiếu sửa chữa thành công")
    else:
        flash("Phiếu sửa chữa không tồn tại hoặc đã hoàn tất")
    return redirect('repair_ticket') 

@staff_blueprint.route('/staff/finish_liquidation_slip', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def finish_liquidation_slip():
    request_id = request.form.get('request_id')
    if LiquidationSlipService.complete_liquidation_slip(request_id):
        flash("Hoàn tất phiếu sửa chữa thành công")
    else:
        flash("Phiếu sửa chữa không tồn tại hoặc đã hoàn tất")
    return redirect('repair_ticket') 

@staff_blueprint.route('/staff/penalty_ticket', methods=['GET'])
@login_required
@role_required(RoleID.STAFF.value)
def penalty_ticket():
    staff_id = session.get('account_id')
    login_staff = AccountService.get_account_by_person_id(staff_id)
    lst_violation = ViolationService.get_all_violation()
    pending_penalty = PenaltyService.get_pending_penalty_ticket(staff_id)
    history_penalties = PenaltyService.get_history_penalty_ticket()

    for r in pending_penalty:
        r['violation'] = PenaltyService.get_violation_by_in_ticket(r['id'])
    for r in history_penalties:
        r['violation'] = PenaltyService.get_violation_by_in_ticket(r['id'])

    return render_template('staff/penalty_ticket.html', 
                           login_staff=login_staff, 
                           lst_violation=lst_violation, 
                           pending_penalty=pending_penalty,
                           history_penalties=history_penalties)  

@staff_blueprint.route('/staff/cancel_penalty_ticket', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def cancel_penalty_ticket():
    request_id = request.form.get('request_id')
    print(request_id)
    if PenaltyService.delete_penalty_ticket_by_id(request_id):
        flash("Hủy phiếu phạt thành công!")
    else:
        flash("Phiếu phạt không tồn tại hoặc đã được xử lý!")
    return redirect('penalty_ticket') 

@staff_blueprint.route('/staff/add_penalty_ticket', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def add_penalty_ticket():
    lst_violation = request.form.getlist('violation')
    mssv = request.form.get('mssv')

    if not StudentService.get_student_by_id(mssv):
        flash("Mã số sinh viên không hợp lệ!", "error")
        return redirect(url_for('staff.penalty_ticket'))

    if not lst_violation:
        flash("Vui lòng chọn ít nhất một vi phạm!", "warning")
        return redirect(url_for('staff.penalty_ticket'))

    user_role = "staff"  

    # Gọi service để tạo phiếu phạt
    success = PenaltyService.create_penalty_ticket(
        student_id=mssv,
        staff_id=session.get('account_id'),
        violation_ids=list(map(int, lst_violation)),
        role=user_role
    )

    if success:
        flash("Tạo phiếu phạt thành công!", "success")
    else:
        flash("Tạo phiếu phạt thất bại!", "error")

    return redirect(url_for('staff.penalty_ticket'))

@staff_blueprint.route('/staff/finish_penalty_ticket', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def finish_penalty_ticket():
    request_id = request.form.get('request_id')
    if PenaltyService.complete_penalty_ticket_by_id(request_id):
        flash("Hoàn tất phiếu phạt thành công")
    else:
        flash("Phiếu phạt không tồn tại hoặc đã hoàn tất")
    return redirect('penalty_ticket') 