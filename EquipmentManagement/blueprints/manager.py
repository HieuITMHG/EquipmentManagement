from flask import Blueprint, render_template, request, session, redirect,flash, url_for

from helpers.helpers import login_required, role_required
from services.account_service import AccountService
from services.manager_service import ManagerService
from services.equipment_service import EquipmentService
from enums.action_type import ActionType
from services.room_service import RoomService
from services.liquidation_slip_service import LiquidationSlipService
from services.repair_ticket import RepairTicketService
from services.violation_service import ViolationService
from services.student_service import StudentService
from services.penalty_service import PenaltyService
from enums.role_type import RoleID

manager_blueprint = Blueprint('manager', __name__)

@manager_blueprint.route('/manager/manager_manage_equipment/<int:equipment_id>/', methods=['GET'])
@manager_blueprint.route('/manager/manager_manage_equipment', methods=['GET', 'POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def manager_manage_equipment(equipment_id=None):
    if request.method == "GET":
        room_id = request.args.get("room", "")
        lst_equipment = ManagerService.get_all_equipment()
        room=RoomService.get_all_room()
        equipment = None
        if equipment_id != None:
            equipment = EquipmentService.get_equipment_by_id(equipment_id)
        if room_id != "":
            lst_equipment = EquipmentService.get_equipment_by_room(room_id)

        return render_template('manager/manager_manage_equipment.html',
                                lst_equipment=lst_equipment,
                                equi=equipment,
                                room=room)
        
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
        equi=EquipmentService.get_all_equipment()
        room=RoomService.get_all_room()
        equi_type=('MOBILE', 'FIXED', 'SHARED')
        return render_template("manager/add_items.html",equi=equi,room=room,equi_type=equi_type)
    
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
    broken_equipment = EquipmentService.get_broken_equipment()
    pending_requests = LiquidationSlipService.get_liquidation_slip(status='PENDING')
    accepted_requests = LiquidationSlipService.get_history_liquidation_slip()
    for r in pending_requests:
        r['equipments'] = LiquidationSlipService.get_equipment_in_liquidation(r['id'])
    for r in accepted_requests:
        r['equipments'] = LiquidationSlipService.get_equipment_in_liquidation(r['id'])

    return render_template('manager/liquidation_slip.html', broken_equipment=broken_equipment,
                                                            pending_requests=pending_requests,
                                                            accepted_requests=accepted_requests)  
    
@manager_blueprint.route('/manager/add_liquidation_slip', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def add_liquidation_slip():
    lst_item_id = request.form.getlist('items') 
    role = 'manager'  
    liquidation_slip_id = LiquidationSlipService.create_liquidation_slip(lst_item_id, role)
    if liquidation_slip_id is None:  
        flash("Có lỗi xảy ra khi tạo phiếu thanh lý", "error")
    else:
        flash("Đã tạo phiếu thanh lý thành công", "success")  
    
    return redirect('liquidation_slip')  

@manager_blueprint.route('/manager/cancel_liquidation_request', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def cancel_liquidation_request():
    request_id = request.form.get('request_id')
    if LiquidationSlipService.delete_liquidation_slip(request_id):
        flash("Hủy yêu cầu thanh lý thành công")
    else:
        flash("Yêu cầu thanh lý không tồn tại hoặc đã được xử lý")
    return redirect('liquidation_slip')  

@manager_blueprint.route('/manager/cancel_repair_ticket', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def cancel_repair_ticket():
    request_id = request.form.get('request_id')
    if RepairTicketService.delete_repair_ticket(request_id):
        flash("Hủy yêu cầu sửa chửa thành công")
    else:
        flash("Yêu cầu sửa chửa không tồn tại hoặc đã được xử lý")
    return redirect('repair_ticket')  

@manager_blueprint.route('/manager/repair_ticket', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value)
def repair_ticket():
    broken_equipment = EquipmentService.get_broken_equipment()
    broken_equipment = EquipmentService.get_broken_equipment()
    pending_requests = RepairTicketService.get_repair_ticket(status='PENDING')
    accepted_requests = RepairTicketService.get_history_repair_ticket()
    for r in pending_requests:
        r['equipments'] = RepairTicketService.get_equipment_in_repair_ticket(r['id'])
        r['total_cost'] = RepairTicketService.get_total_cost(r['id'])
    for r in accepted_requests:
        r['equipments'] = RepairTicketService.get_equipment_in_repair_ticket(r['id'])
        r['total_cost'] = RepairTicketService.get_total_cost(r['id'])


    return render_template('manager/repair_ticket.html', broken_equipment=broken_equipment,
                                                       pending_requests=pending_requests,
                                                       accepted_requests=accepted_requests)  

@manager_blueprint.route('/manager/add_repair_ticket', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def add_repair_ticket():
    role = 'manager'
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

    repair_ticket_id = RepairTicketService.create_repair_ticket(equipment_price_list, role)
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
    lst_violation = ViolationService.get_all_violation()
    pending_penalty = PenaltyService.get_pending_penalty_ticket(staff_id)
    history_penalties = PenaltyService.get_history_penalty_ticket()

    for r in pending_penalty:
        r['violation'] = PenaltyService.get_violation_by_in_ticket(r['id'])
    for r in history_penalties:
        r['violation'] = PenaltyService.get_violation_by_in_ticket(r['id'])

    return render_template('manager/penalty_ticket.html',  
                           lst_violation=lst_violation, 
                           pending_penalty=pending_penalty,
                           history_penalties=history_penalties)  

@manager_blueprint.route('/manager/cancel_penalty_ticket', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def cancel_penalty_ticket():
    request_id = request.form.get('request_id')
    print(request_id)
    if PenaltyService.delete_penalty_ticket_by_id(request_id):
        flash("Hủy phiếu phạt thành công!")
    else:
        flash("Phiếu phạt không tồn tại hoặc đã được xử lý!")
    return redirect('penalty_ticket') 

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



@manager_blueprint.route('/pending/<form_type>')
@login_required
@role_required(RoleID.MANAGER.value)
def view_pending_forms(form_type):
    model_map = {
        'liquidation': LiquidationSlip,
        'violation': ViolationReport,
        'repair': RepairRequest
    }

    if form_type not in model_map:
        return "Invalid form type", 404

    model = model_map[form_type]
    slips = model.query.filter_by(status='pending').all()

    return render_template('manager/pending_forms.html', slips=slips, form_type=form_type)


@manager_blueprint.route('/approve/<form_type>/<int:slip_id>', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def approve_form(form_type, slip_id):
    model = _get_model(form_type)
    slip = model.query.get_or_404(slip_id)
    slip.status = 'approved'
    db.session.commit()
    return redirect(url_for('manager.view_pending_forms', form_type=form_type))


@manager_blueprint.route('/reject/<form_type>/<int:slip_id>', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value)
def reject_form(form_type, slip_id):
    model = _get_model(form_type)
    slip = model.query.get_or_404(slip_id)
    slip.status = 'rejected'
    db.session.commit()
    return redirect(url_for('manager.view_pending_forms', form_type=form_type))


def _get_model(form_type):
    model_map = {
        'liquidation': LiquidationSlip,
        'violation': ViolationReport,
        'repair': RepairRequest
    }
    return model_map.get(form_type)
