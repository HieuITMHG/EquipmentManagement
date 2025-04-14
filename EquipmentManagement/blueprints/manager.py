from flask import Blueprint, render_template, request, session, redirect,flash, url_for

from helpers.helpers import login_required, role_required
from services.account_service import AccountService
from services.manager_service import ManagerService
from services.equipment_service import EquipmentService
from services.room_service import RoomService
from services.liquidation_slip_service import LiquidationSlipService
from services.repair_ticket import RepairTicketService
from services.violation_service import ViolationService
from services.student_service import StudentService
from services.penalty_service import PenaltyService
from services.class_service import ClassService
from services.borrow_service import BorrowService
from enums.action_type import ActionType
from enums.role_type import RoleID


manager_blueprint = Blueprint('manager', __name__)

@manager_blueprint.route('/', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value)
def manager():
    login_manager = AccountService.get_account_by_person_id(session.get('account_id'))
    return render_template('manager/manager_profile.html', login_manager=login_manager)

@manager_blueprint.route('/manager/manager_manage_equipment/<int:equipment_id>/', methods=['GET'])
@manager_blueprint.route('/manager/manager_manage_equipment', methods=['GET', 'POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def manager_manage_equipment(equipment_id=None):
    if request.method == "GET":
        lst_status = [
            {'name': 'Khả dụng', 'value': 'AVAILABLE'},
            {'name': 'Đang sửa', 'value': 'UNDERREPAIR'},
            {'name': 'Đang được mượn', 'value': 'BORROWED'},
            {'name': 'Bị hỏng', 'value': 'BROKEN'},
            {'name': 'Đã thanh lý', 'value': 'LIQUIDATED'}
        ]
        lst_equipment_type = [
            {'name': 'Di động', 'value': 'MOBILE'},
            {'name': 'Cố định', 'value': 'FIXED'},
            {'name': 'Học viện', 'value': 'SHARED'}
        ]
        login_manager = AccountService.get_account_by_person_id(session.get('account_id'))
        room_id = request.args.get("room_id", None)
        equipment_type = request.args.get("equipment_type", None)
        status = request.args.get("status", None)
        lst_equipment = EquipmentService.search_equipment(room_id=room_id,status=status,equipment_type=equipment_type)
        room=RoomService.get_all_room()
        equipment = None
        if equipment_id != None:
            equipment = EquipmentService.get_equipment_by_id(equipment_id)

        return render_template('manager/manager_manage_equipment.html',
                                lst_equipment=lst_equipment,
                                equi=equipment,
                                room=room,
                                login_manager=login_manager,
                                room_id=room_id,
                                status=status,
                                equipment_type=equipment_type,
                                lst_status=lst_status,
                                lst_equipment_type=lst_equipment_type)
    new_name=request.form.get("equi_name")
    new_id=request.form.get("equi_id")
    new_room=request.form.get("room")
    if RoomService.get_room_by_id(new_room) == None:
        flash("Phòng không tồn tại", "error")
        return redirect("manager_manage_equipment")

    ManagerService.change_equi_info(new_id,new_name,new_room)
    return redirect("manager_manage_equipment")


@manager_blueprint.route('/manager/add_items', methods=['GET', 'POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def add_items():
    if request.method == "GET":
        login_manager = AccountService.get_account_by_person_id(session.get('account_id'))
        equi=EquipmentService.get_all_equipment()
        room=RoomService.get_all_room()
        equi_type=('MOBILE', 'FIXED', 'SHARED')
        return render_template("manager/add_items.html",equi=equi,room=room,equi_type=equi_type, login_manager=login_manager)
    
    equi_name = request.form.get('equi_name')  # Tên thiết bị
    room_id = request.form.get('room')  # ID phòng
    if RoomService.get_room_by_id(room_id) == None:
        flash("Phòng không tồn tại", "error")
        return redirect("/manager/add_items")
    equi_type = request.form.get('equi_t')  # Kiểu thiết bị (BỊ TRÙNG NAME -> CẦN SỬA)  
    if(equi_name):
        EquipmentService.add_equipment(equi_name, "AVAILABLE", equi_type, room_id)
    return redirect("manager_manage_equipment")

@manager_blueprint.route('/manager/delete_equipment', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value)
def delete_equipment():
    equipment_id = request.args.get('equipment_id')  # Lấy equipment_id từ URL

    if equipment_id:
        check_d=EquipmentService.delete_equipment_by_id(equipment_id)
        if(check_d):
            flash("Thiết bị đã được xóa!", "success")  # Thông báo xóa thành công
        else:
            flash("Không thể xóa vì đang được thêm vào phiếu","error")
    
    return redirect(('manager_manage_equipment'))
    
@manager_blueprint.route('/manager/liquidation_slip', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value)
def liquidation_slip():
    create_date = request.args.get("create_date")
    login_manager = AccountService.get_account_by_person_id(session.get('account_id'))
    broken_equipment = EquipmentService.get_broken_equipment()
    pending_requests = LiquidationSlipService.get_liquidation_slip(status='PENDING')
    accepted_requests = LiquidationSlipService.get_history_liquidation_slip(create_date)
    for r in pending_requests:
        r['equipments'] = LiquidationSlipService.get_equipment_in_liquidation(r['id'])
    for r in accepted_requests:
        r['equipments'] = LiquidationSlipService.get_equipment_in_liquidation(r['id'])

    return render_template('manager/liquidation_slip.html', broken_equipment=broken_equipment,
                                                            pending_requests=pending_requests,
                                                            accepted_requests=accepted_requests,
                                                            login_manager=login_manager,
                                                            create_date=create_date)  
    
@manager_blueprint.route('/manager/add_liquidation_slip', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def add_liquidation_slip():
    lst_item_id = request.form.getlist('items') 
    role = 'manager'  
    liquidation_slip_id = LiquidationSlipService.create_liquidation_slip(session.get("account_id"), lst_item_id, role)
    if liquidation_slip_id is None:  
        flash("Có lỗi xảy ra khi tạo phiếu thanh lý", "error")
    else:
        flash("Đã tạo phiếu thanh lý thành công", "success")  
    
    return redirect('liquidation_slip')  

@manager_blueprint.route('/manager/accept_liquidation_request', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def accept_liquidation_request():
    request_id = request.form.get('request_id')
    if LiquidationSlipService.accept_liquidation_slip(request_id):
        flash("Duyệt phiếu thanh lý thành công")
    else:
        flash("Phiếu thanh lý không tồn tại hoặc đã duyệt")
    return redirect('liquidation_slip')  

@manager_blueprint.route('/manager/accept_repair_ticket', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def accept_repair_ticket():
    request_id = request.form.get('request_id')
    if RepairTicketService.accept_repair_ticket(request_id):
        flash("Duyệt phiếu sửa chữa thành công")
    else:
        flash("Phiếu sửa chữa không tồn tại hoặc đã duyệt")
    return redirect('repair_ticket')  

@manager_blueprint.route('/manager/accept_penalty_ticket', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def accept_penalty_ticket():
    request_id = request.form.get('request_id')
    if PenaltyService.accept_penalty_ticket(request_id):
        flash("Duyệt phiếu phạt thành công")
    else:
        flash("Phiếu phạt không tồn tại hoặc đã duyệt")
    return redirect('penalty_ticket')  

@manager_blueprint.route('/manager/repair_ticket', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value)
def repair_ticket():
    login_manager = AccountService.get_account_by_person_id(session.get('account_id'))
    broken_equipment = EquipmentService.get_broken_equipment()
    broken_equipment = EquipmentService.get_broken_equipment()
    pending_requests = RepairTicketService.get_repair_ticket(status='PENDING')
    create_date = request.args.get("create_date")
    accepted_requests = RepairTicketService.get_history_repair_ticket(create_date)
    for r in pending_requests:
        r['equipments'] = RepairTicketService.get_equipment_in_repair_ticket(r['id'])
        r['total_cost'] = RepairTicketService.get_total_cost(r['id'])
    for r in accepted_requests:
        r['equipments'] = RepairTicketService.get_equipment_in_repair_ticket(r['id'])
        r['total_cost'] = RepairTicketService.get_total_cost(r['id'])


    return render_template('manager/repair_ticket.html', broken_equipment=broken_equipment,
                                                       pending_requests=pending_requests,
                                                       accepted_requests=accepted_requests,
                                                       login_manager=login_manager,
                                                       create_date=create_date)  



@manager_blueprint.route('/manager/add_repair_ticket', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def add_repair_ticket():
    role = 'manager'
    form_data = request.form
    equipment_price_list = []

    for key in form_data:
        if key.endswith('[id]'):  #
            equipment_id = form_data[key]
            price_key = f"items[{equipment_id}][price]" 
            if price_key in form_data:
                price = form_data[price_key]
                equipment_price_list.append((int(equipment_id), int(price)))

    if not equipment_price_list:
        flash("Không có thiết bị nào được chọn")

    repair_ticket_id = RepairTicketService.create_repair_ticket(session.get("account_id"),equipment_price_list, role)
    if repair_ticket_id:
        flash("Tạo phiếu sửa chữa thành công")
    else:
        flash("Lỗi khi tạo phiếu sửa chữa")
    return redirect('repair_ticket') 

@manager_blueprint.route('/manager/finish_repair_ticket', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def finish_repair_ticket():
    request_id = request.form.get('request_id')
    if RepairTicketService.complete_repair_ticket(request_id):
        flash("Hoàn tất phiếu sửa chữa thành công")
    else:
        flash("Phiếu sửa chữa không tồn tại hoặc đã hoàn tất")
    return redirect('repair_ticket') 

@manager_blueprint.route('/manager/finish_liquidation_slip', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def finish_liquidation_slip():
    request_id = request.form.get('request_id')
    if LiquidationSlipService.complete_liquidation_slip(request_id):
        flash("Hoàn tất phiếu sửa chữa thành công")
    else:
        flash("Phiếu sửa chữa không tồn tại hoặc đã hoàn tất")
    return redirect('repair_ticket') 

@manager_blueprint.route('/manager/penalty_ticket', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value)
def penalty_ticket():
    manager_id = session.get('account_id')
    login_manager = AccountService.get_account_by_person_id(manager_id)
    lst_violation = ViolationService.get_all_violation()
    pending_penalty = PenaltyService.get_pending_penalty_ticket(manager_id)
    
    create_date = request.args.get("create_date")
    history_penalties = PenaltyService.get_history_penalty_ticket(start_time=create_date)
    for r in pending_penalty:
        r['violation'] = PenaltyService.get_violation_by_in_ticket(r['id'])
    for r in history_penalties:
        r['violation'] = PenaltyService.get_violation_by_in_ticket(r['id'])

    return render_template('manager/penalty_ticket.html',  
                           lst_violation=lst_violation, 
                           pending_penalty=pending_penalty,
                           history_penalties=history_penalties,
                           login_manager=login_manager,
                           create_date=create_date)  

@manager_blueprint.route('/manager/add_penalty_ticket', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def add_penalty_ticket():
    lst_violation = request.form.getlist('violation')
    mssv = request.form.get('mssv')

    if not StudentService.get_student_by_id(mssv):
        flash("Mã số sinh viên không hợp lệ!", "error")
        return redirect(url_for('manager.penalty_ticket'))

    if not lst_violation:
        flash("Vui lòng chọn ít nhất một vi phạm!", "warning")
        return redirect(url_for('manager.penalty_ticket'))

    user_role = "manager"  

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

    return redirect(url_for('manager.penalty_ticket'))

@manager_blueprint.route('/manager/finish_penalty_ticket', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def finish_penalty_ticket():
    request_id = request.form.get('request_id')
    if PenaltyService.complete_penalty_ticket_by_id(request_id):
        flash("Hoàn tất phiếu phạt thành công") 
    else:
        flash("Phiếu phạt không tồn tại hoặc đã hoàn tất") 
    return redirect('penalty_ticket') 

@manager_blueprint.route('/manager/account/<int:page_num>', methods=['POST', 'GET'])
@login_required
@role_required(RoleID.MANAGER.value)
def account(page_num=None):
    if request.method == "GET":
        lst_role = [
            {'name': 'Quản lý', 'value': '1'},
            {'name': 'Sinh Viên', 'value': '2'},
            {'name': 'Nhân viên', 'value': '3'}
        ]
        manager_id = session.get("account_id")
        login_manager = AccountService.get_account_by_person_id(manager_id)
        role_id = request.args.get('role_id', "")
        first_name = request.args.get('first_name', "")
        lst_account, total_page = AccountService.search_account_info(role_id=role_id, first_name=first_name, page_num=page_num)
        return render_template('manager/account.html', 
                               login_manager=login_manager, 
                               lst_account=lst_account, 
                               page_num=page_num,
                               first_name=first_name,
                               role_id=role_id,
                               lst_role=lst_role,
                               total_page=total_page)
    
@manager_blueprint.route('/manager/add_account', methods=['POST', 'GET'])
@login_required
@role_required(RoleID.MANAGER.value)
def add_account():
    if request.method == "GET":
        lst_class = ClassService.get_all_class()
        return render_template('manager/add_account.html', lst_class=lst_class)

    try:
        # Lấy dữ liệu từ form
        cccd = request.form.get('cccd')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = int(request.form.get('gender'))
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        role_id = int(request.form.get('role_id')) 
        class_id = request.form.get('class')
        account_code = request.form.get('account_code')
        password = request.form.get('password', account_code)  
        # Kiểm tra đầu vào
        if not all([cccd, first_name, last_name, email, phone, address, role_id, account_code]):
            flash("Vui lòng điền đầy đủ các thông tin bắt buộc.", "error")
            return redirect(url_for('manager.add_account'))
        
        if role_id == 2 and not class_id:
            flash("Sinh viên cần chọn lớp.", "error")
            return redirect(url_for('manager.add_account'))
        elif role_id == 2 and class_id:
            if not ClassService.get_class_by_id(class_id):
                flash("Lớp không tồn tại.", "error")
                return redirect(url_for('manager.add_account'))

        # Gọi phương thức create_new_account
        success = AccountService.create_new_account(
            cccd=cccd,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            email=email,
            phone=phone,
            address=address,
            role_id=role_id,
            class_id=class_id,
            account_code=account_code,
            password=password
        )

        if success:
            flash("Tạo tài khoản thành công!", "success")
        else:
            flash("Lỗi khi tạo tài khoản. Vui lòng thử lại.", "error")

        return redirect(url_for('manager.add_account'))

    except ValueError as e:
        flash(f"Lỗi: Dữ liệu không hợp lệ ({str(e)}).", "error")
        return redirect(url_for('manager.add_account'))
    except Exception as e:
        flash(f"Lỗi không xác định: {str(e)}.", "error")
        return redirect(url_for('manager.add_account'))

@manager_blueprint.route('/manager/view_account/<user_id>', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value)
def view_account(user_id=None):
    user = AccountService.get_account_by_person_id(user_id)
    if user['role_id'] == RoleID.STUDENT.value:
        user = StudentService.get_student_by_id(user_id)
    return render_template('manager/view_account.html', user=user)
@manager_blueprint.route('/manager/edit_account/<user_id>', methods=['GET', 'POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def edit_account(user_id=None):
    if request.method == "GET":
        user = AccountService.get_account_by_person_id(user_id)
        if user['role_id'] == RoleID.STUDENT.value:
            user = StudentService.get_student_by_id(user_id)
        if not user:
            flash("Tài khoản không tồn tại.", "error")
            return redirect(url_for('manager.account_list'))  # Giả định route danh sách tài khoản

        lst_class = ClassService.get_all_class()
        return render_template('manager/edit_account.html', user=user, lst_class=lst_class)

    try:
        # Lấy dữ liệu từ form
        cccd = request.form.get('cccd')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = int(request.form.get('gender'))
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        role_id = int(request.form.get('role_id'))  
        class_id = request.form.get('class')
        is_studing = request.form.get('is_studing') == '1' if role_id == 2 else None
        is_working = request.form.get('is_working') == '1' if role_id in (1, 3) else None

        # Kiểm tra đầu vào
        if not all([cccd, first_name, last_name, email, phone, address, role_id]):
            flash("Vui lòng điền đầy đủ các thông tin bắt buộc.", "error")
            return redirect(url_for('manager.edit_account', user_id=user_id))

        if role_id == 2:
            if not class_id:
                flash("Sinh viên cần chọn lớp.", "error")
                return redirect(url_for('manager.edit_account', user_id=user_id))
            if not ClassService.get_class_by_id(class_id):
                flash("Lớp không tồn tại.", "error")
                return redirect(url_for('manager.edit_account', user_id=user_id))

        # Gọi stored procedure qua AccountService
        success = AccountService.update_account(
            person_id=user_id,
            cccd=cccd,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            email=email,
            phone=phone,
            address=address,
            role_id=role_id,
            class_id=class_id,
            is_studing=is_studing,
            is_working=is_working
        )

        if success:
            flash("Cập nhật tài khoản thành công!", "success")
            return redirect(url_for('manager.account', page_num=1))   # Chuyển về danh sách tài khoản
        else:
            flash("Lỗi khi cập nhật tài khoản. Vui lòng thử lại.", "error")
            return redirect(url_for('manager.edit_account', user_id=user_id))

    except ValueError as e:
        flash(f"Lỗi: Dữ liệu không hợp lệ ({str(e)}).", "error")
        return redirect(url_for('manager.edit_account', user_id=user_id))
    except Exception as e:
        flash(f"Lỗi không xác định: {str(e)}.", "error")
        return redirect(url_for('manager.edit_account', user_id=user_id))
    
@manager_blueprint.route('/manager/delete_account', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def delete_account():
    try:
        person_id = request.form.get('person_id')
        print(person_id)
        if not person_id:
            flash("Không tìm thấy mã tài khoản.", "error")
            return redirect(url_for('manager.account', page_num=1))

        success = AccountService.delete_account(person_id)
        if success:
            flash("Xóa tài khoản thành công!", "success")
        else:
            flash("Lỗi khi xóa tài khoản. Vui lòng thử lại.", "error")

        return redirect(url_for('manager.account', page_num=1))

    except Exception as e:
        print(e)
        flash(f"Lỗi không xác định: {str(e)}.", "error")
        return redirect(url_for('manager.account', page_num=1))
       
@manager_blueprint.route('/manager/borrow_request/<int:request_id>', methods=['GET'])
@manager_blueprint.route('/manager/borrow_request', methods=['GET', 'POST'])
@role_required(RoleID.MANAGER.value)
@login_required
def manager_borrow_request(request_id=None):
    if request.method == "GET":
        login_manager = AccountService.get_account_by_person_id(session.get('account_id'))
        lst_request = BorrowService.get_pending_borrow_request()
        if request_id == None:
            return render_template('manager/borrow_request.html', login_manager = login_manager, lst_request=lst_request)
        lst_borrow_equipment = BorrowService.get_equipment_by_request_id(request_id)
        return render_template('manager/borrow_request.html', login_manager=login_manager,lst_request=lst_request, lst_borrow_equipment=lst_borrow_equipment)
    borrow_request_id = int(request.form.get('request_id'))
    action = int(request.form.get('action'))
    if action == ActionType.ACCEPT.value:
        BorrowService.accept_borrow_request(borrow_request_id, session.get('account_id'))
    else:
        BorrowService.reject_borrow_request(borrow_request_id, session.get('account_id'))
    return redirect("borrow_request")

@manager_blueprint.route('/manager/borrow_history/<int:request_id>', methods=['GET'])
@manager_blueprint.route('/manager/borrow_history', methods=['GET', 'POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def borrow_history(request_id=None):
    lst_status =[
        {'name': 'Chờ duyệt', 'value': 'PENDING'},
        {'name': 'Chưa trả', 'value': 'ACCEPTED'},
        {'name': 'Đã trả', 'value': 'RETURNED'}
    ]
    if request.method == "GET":
        create_date = request.args.get("create_date")
        print(create_date)
        status = request.args.get("status")
        login_manager = AccountService.get_account_by_person_id(session.get('account_id'))
        lst_request = BorrowService.search_borrow_request_by_date_and_status(create_date, status)
        if(request_id!=None):
            lst_borrow_equipment = BorrowService.get_equipment_by_request_id(request_id)
            return render_template('manager/borrow_history.html', 
                                   login_manager=login_manager,
                                   lst_request=lst_request, 
                                   lst_borrow_equipment=lst_borrow_equipment, 
                                   lst_status=lst_status,
                                   create_date=create_date,
                                   status=status)
        return render_template('manager/borrow_history.html', 
                               login_manager = login_manager,
                               lst_request=lst_request, 
                               lst_status=lst_status,
                               create_date=create_date,
                               status=status)
    
    borrow_request_id = int(request.form.get('request_id'))
    BorrowService.return_equi(borrow_request_id)
    return redirect("borrow_history")