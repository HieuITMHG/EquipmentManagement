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
def profile():
    if request.method == "GET":
        login_user = AccountService.get_account_by_person_id(session.get('account_id'))
        return render_template('manager/profile.html', login_user = login_user)

@manager_blueprint.route('/manager/account/<int:page_num>', methods=['POST', 'GET'])
@login_required
@role_required(RoleID.MANAGER.value)
def account(page_num=None):
    if request.method == "GET":
        lst_role = [
            {'name': 'Quản lý', 'value': '1'},
            {'name': 'Nhân viên', 'value': '2'},
            {'name': 'Giảng viên', 'value': '3'},
            {'name': 'Sinh Viên', 'value': '4'},
        ]
        manager_id = session.get("account_id")
        login_user = AccountService.get_account_by_person_id(manager_id)
        role_id = request.args.get('role_id', "")
        first_name = request.args.get('first_name', "")
        lst_account, total_page = AccountService.search_account_info(role_id=role_id, first_name=first_name, page_num=page_num)
        return render_template('manager/account.html', 
                               login_user=login_user, 
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
        if AccountService.get_account_by_person_id(account_code):
            flash("Mã tài khoản đã được sử dụng", 'error')
            return redirect(url_for('manager.add_account'))
        if AccountService.get_account_by_email(email):
            flash('Email đã được sử dụng', 'error')
            return redirect(url_for('manager.add_account'))

        if AccountService.get_account_by_phone(phone):
            flash('Số điện thoại đã được sử dụng', 'error')
            return redirect(url_for('manager.add_account'))
        
        if AccountService.get_account_by_cccd(cccd):
            flash('CCCD đã được sử dụng', 'error')
            return redirect(url_for('manager.add_account'))

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

        if AccountService.get_account_by_email(email):
            flash('Email đã được sử dụng', 'error')
            return redirect(url_for('manager.edit_account'))

        if AccountService.get_account_by_phone(phone):
            flash('Số điện thoại đã được sử dụng', 'error')
            return redirect(url_for('manager.edit_account'))
        
        if AccountService.get_account_by_cccd(cccd):
            flash('CCCD đã được sử dụng', 'error')
            return redirect(url_for('manager.edit_account'))

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

@manager_blueprint.route('/manager/handle_repair_ticket', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def handle_repair_ticket():
    action = int(request.form['action'])
    request_id = request.form['request_id']
    if action:
        if RepairTicketService.accept_repair_ticket(request_id):
            flash("Lâp phiếu sửa chửa thành công", 'success')
        else:
            flash("Lập phiếu sửa chửa thất bại", 'error')
    else:
        if RepairTicketService.delete_repair_ticket(request_id):
            flash("Hủy yêu cầu sửa chửa thành công", 'success')
        else:
            flash("Yêu cầu sửa chửa không tồn tại hoặc đã được xử lý", 'error')
    return redirect(url_for('manager.repair_ticket'))  

@manager_blueprint.route('/manager/repair_ticket', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value)
def repair_ticket():
    staff_id = session.get('account_id')
    login_user = AccountService.get_account_by_person_id(staff_id)
    broken_equipment = EquipmentService.get_broken_equipment()
    processed_equipment_id = RepairTicketService.get_all_processed_equipment()
    my_requests = RepairTicketService.get_my_repair_ticket(staff_id=staff_id)
    pending_requests = RepairTicketService.get_pending_repair_ticket()
    broken_equipment = [e for e in broken_equipment if e['id'] not in processed_equipment_id]
    create_date = request.args.get("create_date")
    accepted_requests = RepairTicketService.get_history_repair_ticket(create_date)
    for r in my_requests:
        r['equipments'] = RepairTicketService.get_equipment_in_repair_ticket(r['id'])
        r['total_cost'] = RepairTicketService.get_total_cost(r['id'])
    for r in accepted_requests:
        r['equipments'] = RepairTicketService.get_equipment_in_repair_ticket(r['id'])
        r['total_cost'] = RepairTicketService.get_total_cost(r['id'])

    for r in pending_requests:
        r['equipments'] = RepairTicketService.get_equipment_in_repair_ticket(r['id'])
        r['total_cost'] = RepairTicketService.get_total_cost(r['id'])

    print(pending_requests)
    return render_template('manager/repair_ticket.html', login_user=login_user,
                                                        broken_equipment=broken_equipment,
                                                        my_requests=my_requests,
                                                        accepted_requests=accepted_requests,
                                                        create_date=create_date,
                                                        pending_requests=pending_requests)  

@manager_blueprint.route('/manager/add_repair_ticket', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def add_repair_ticket():
    staff_id = session.get('account_id')
    equipment_id = request.form.get('equipment_id')
    issue_description = request.form.get('issue_description')
    repair_cost = request.form.get('repair_cost')
    broken_quantity = request.form.get('broken_quantity')
    existing_request = RepairTicketService.get_existing_ticket(staff_id)
    if existing_request:
        if RepairTicketService.add_equipment_to_ticket(ticket_id = existing_request['id'], 
                                                       equipment_id=equipment_id, 
                                                       quantity=broken_quantity,
                                                       description=issue_description,
                                                       price=repair_cost):
            flash("Thêm thiết bị vào phiếu sửa chửa thành công", 'sucesss')
        else:
            flash("Thêm thiết bị vào phiếu sửa chửa thất bại", 'error')
    else:
        if RepairTicketService.create_repair_ticket_with_equipment(staff_id=staff_id,
                                                                   equipment_id=equipment_id,
                                                                   quantity=broken_quantity,
                                                                   description=issue_description,
                                                                   price=repair_cost):
            flash("Tạo phiếu sửa chửa thành công", 'success')
        else:
            flash("Tạo phiếu sửa chửa thất bại", 'error')
    return redirect('repair_ticket') 

@manager_blueprint.route('/manager/remove_repair_equipment', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def remove_repair_equipment():
    try:
        if not request.form.get('csrf_token'):
            flash('CSRF token missing.', 'error')
            return redirect(url_for('manager.repair_ticket'))
        
        repair_ticket_id = int(request.form.get('repair_ticket_id'))
        equipment_id = int(request.form.get('equipment_id'))
        
        result = RepairTicketService.remove_equipment_from_ticket(repair_ticket_id, equipment_id)
        
        if result['success']:
            if result['ticket_deleted']:
                flash('Equipment removed and repair ticket deleted as no equipment remains.', 'success')
            else:
                flash('Equipment removed from repair ticket successfully.', 'success')
        else:
            flash(f'Failed to remove equipment: {result["error"]}', 'error')
        
        return redirect(url_for('manager.repair_ticket'))
    
    except Exception as e:
        flash(f'Error removing equipment: {str(e)}', 'error')
        return redirect(url_for('manager.repair_ticket'))
    
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

@manager_blueprint.route('/manager/liquidation_slip', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value)
def liquidation_slip():
    staff_id = session.get('account_id')
    create_date = request.args.get("create_date") 
    login_user = AccountService.get_account_by_person_id(staff_id)
    broken_equipment = EquipmentService.get_broken_equipment()
    my_requests = LiquidationSlipService.get_my_liquidation_slip(staff_id=staff_id)
    pending_requests = LiquidationSlipService.get_pending_repair_ticket()
    processed_equipment_id = LiquidationSlipService.get_all_processed_equipment()
    broken_equipment = [e for e in broken_equipment if e['id'] not in processed_equipment_id]
    accepted_requests = LiquidationSlipService.get_history_liquidation_slip(create_date)
    for r in my_requests:
        r['equipments'] = LiquidationSlipService.get_equipment_in_liquidation(r['id'])
        r['total_cost'] = LiquidationSlipService.get_total_cost(r['id'])
    for r in accepted_requests:
        r['equipments'] = LiquidationSlipService.get_equipment_in_liquidation(r['id'])
        r['total_cost'] = LiquidationSlipService.get_total_cost(r['id'])

    for r in pending_requests:
        r['equipments'] = LiquidationSlipService.get_equipment_in_liquidation(r['id'])
        r['total_cost'] = LiquidationSlipService.get_total_cost(r['id'])

    return render_template('manager/liquidation_slip.html', login_user=login_user,
                                                        broken_equipment=broken_equipment,
                                                        pending_requests=pending_requests,
                                                        accepted_requests=accepted_requests,
                                                        create_date=create_date,
                                                        my_requests=my_requests)  
    
@manager_blueprint.route('/manager/add_liquidation_slip', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def add_liquidation_slip():
    staff_id = session.get('account_id')
    equipment_id = request.form.get('equipment_id')
    issue_description = request.form.get('issue_description')
    repair_cost = request.form.get('repair_cost')
    broken_quantity = request.form.get('broken_quantity')
    existing_request = LiquidationSlipService.get_existing_ticket(staff_id)
    if existing_request:
        if LiquidationSlipService.add_equipment_to_ticket(ticket_id = existing_request['id'], 
                                                       equipment_id=equipment_id, 
                                                       quantity=broken_quantity,
                                                       description=issue_description,
                                                       price=repair_cost):
            flash("Thêm thiết bị vào phiếu thanh lý thành công", 'sucesss')
        else:
            flash("Thêm thiết bị vào phiếu thanh lý thất bại", 'error')
    else:
        if LiquidationSlipService.create_liquidation_slip_with_equipment(staff_id=staff_id,
                                                                   equipment_id=equipment_id,
                                                                   quantity=broken_quantity,
                                                                   description=issue_description,
                                                                   price=repair_cost):
            flash("Tạo phiếu thanh lý thành công", 'success')
        else:
            flash("Tạo phiếu thanh lý thất bại", 'error')
    return redirect(url_for('manager.liquidation_slip')) 

@manager_blueprint.route('/manager/handle_liquidation_slip', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def handle_liquidation_slip():
    action = int(request.form['action'])
    request_id = request.form['request_id']
    if action:
        if LiquidationSlipService.accept_liquidation_slip(request_id, session.get('account_id')):
            flash("Lâp phiếu sửa chửa thành công", 'success')
        else:
            flash("Lập phiếu sửa chửa thất bại", 'error')
    else:
        if LiquidationSlipService.delete_liquidation_slip(request_id):
            flash("Hủy yêu cầu thanh lý thành công", 'success')
        else:
            flash("Yêu cầu thanh lý không tồn tại hoặc đã được xử lý", 'error')
        return redirect('liquidation_slip')  
    return redirect(url_for('manager.liquidation_slip'))  

@manager_blueprint.route('/manager/remove_liqui_equipment', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def remove_liqui_equipment():
    try:       
        repair_ticket_id = int(request.form.get('repair_ticket_id'))
        equipment_id = int(request.form.get('equipment_id'))
        
        result = LiquidationSlipService.remove_equipment_from_slip(repair_ticket_id, equipment_id)
        
        if result['success']:
            if result['ticket_deleted']:
                flash('Equipment removed and repair ticket deleted as no equipment remains.', 'success')
            else:
                flash('Equipment removed from repair ticket successfully.', 'success')
        else:
            flash(f'Failed to remove equipment: {result["error"]}', 'error')
        
        return redirect(url_for('manager.liquidation_slip'))
    
    except Exception as e:
        flash(f'Error removing equipment: {str(e)}', 'error')
        return redirect(url_for('manager.liquidation_slip'))
