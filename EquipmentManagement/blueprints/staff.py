from flask import Blueprint, render_template, request, session, redirect,flash, url_for

from helpers.helpers import login_required, role_required
from services.account_service import AccountService
from services.equipment_service import EquipmentService
from services.liquidation_slip_service import LiquidationSlipService
from services.repair_ticket import RepairTicketService
from enums.role_type import RoleID

staff_blueprint = Blueprint('staff', __name__)

@staff_blueprint.route('/staff/profile', methods=['GET'])
@login_required
@role_required(RoleID.STAFF.value)
def profile():
    if request.method == "GET":
        login_user = AccountService.get_user_info(session.get('account_id'))
        print(login_user)
        return render_template('staff/profile.html', login_user = login_user)

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

@staff_blueprint.route('/staff/liquidation_slip', methods=['GET'])
@login_required
@role_required(RoleID.STAFF.value)
def liquidation_slip():
    staff_id = session.get('account_id')
    create_date = request.args.get("create_date") 
    login_user = AccountService.get_user_info(staff_id)
    broken_equipment = EquipmentService.get_broken_equipment()
    pending_requests = LiquidationSlipService.get_my_liquidation_slip(staff_id=staff_id)
    processed_equipment_id = LiquidationSlipService.get_all_processing_equipment()
    broken_equipment = [e for e in broken_equipment if e['id'] not in processed_equipment_id]
    accepted_requests = LiquidationSlipService.get_history_liquidation_slip(create_date)
    for r in pending_requests:
        r['equipments'] = LiquidationSlipService.get_equipment_in_liquidation(r['id'])
        r['total_cost'] = LiquidationSlipService.get_total_cost(r['id'])
    for r in accepted_requests:
        r['equipments'] = LiquidationSlipService.get_equipment_in_liquidation(r['id'])
        r['total_cost'] = LiquidationSlipService.get_total_cost(r['id'])

    return render_template('staff/liquidation_slip.html', login_user=login_user,
                                                        broken_equipment=broken_equipment,
                                                        pending_requests=pending_requests,
                                                        accepted_requests=accepted_requests,
                                                        create_date=create_date)  
    
@staff_blueprint.route('/staff/add_liquidation_slip', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def add_liquidation_slip():
    staff_id = session.get('account_id')
    equipment_id = request.form.get('equipment_id')
    issue_description = request.form.get('issue_description')
    repair_cost = request.form.get('repair_cost')

    if LiquidationSlipService.add_equipment_to_ticket( staff_id=staff_id,
                                                       equipment_id=equipment_id, 
                                                        price=repair_cost,
                                                       description=issue_description):
        flash("Thêm thiết bị vào phiếu thanh lý thành công", 'sucesss')
    else:
        flash("Thêm thiết bị vào phiếu thanh lý thất bại", 'error')
    return redirect(url_for('staff.liquidation_slip'))

@staff_blueprint.route('/staff/handle_liquidation_slip', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def handle_liquidation_slip():
    login_user = AccountService.get_user_info(session.get('account_id'))
    action = int(request.form['action'])
    request_id = request.form['phieu_thanh_ly_id']
    if action:
        if LiquidationSlipService.confirm_liquidation_slip(request_id, int(login_user['vai_tro_id'])):
            flash("Lâp phiếu sửa chửa thành công", 'success')
        else:
            flash("Lập phiếu sửa chửa thất bại", 'error')
    else:
        if LiquidationSlipService.delete_liquidation_slip(request_id):
            flash("Hủy yêu cầu thanh lý thành công", 'success')
        else:
            flash("Yêu cầu thanh lý không tồn tại hoặc đã được xử lý", 'error')
        return redirect('liquidation_slip')  
    return redirect(url_for('staff.liquidation_slip'))  

@staff_blueprint.route('/staff/handle_repair_ticket', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def handle_repair_ticket():
    login_user = AccountService.get_user_info(session.get('account_id'))
    action = int(request.form['action'])
    request_id = request.form['request_id']
    if action:
        if RepairTicketService.confirm_repair_ticket(request_id, int(login_user['vai_tro_id'])):
            flash("Lâp phiếu sửa chửa thành công", 'success')
        else:
            flash("Lập phiếu sửa chửa thất bại", 'error')
    else:
        if RepairTicketService.delete_repair_ticket(request_id):
            flash("Hủy yêu cầu sửa chửa thành công", 'success')
        else:
            flash("Yêu cầu sửa chửa không tồn tại hoặc đã được xử lý", 'error')
    return redirect(url_for('staff.repair_ticket'))  

@staff_blueprint.route('/staff/repair_ticket', methods=['GET'])
@login_required
@role_required(RoleID.STAFF.value)
def repair_ticket():
    staff_id = session.get('account_id')
    login_user = AccountService.get_account_by_person_id(staff_id)
    broken_equipment = EquipmentService.get_broken_equipment()
    processed_equipment_id =LiquidationSlipService.get_all_processing_equipment()
    pending_requests = RepairTicketService.get_my_repair_ticket(staff_id=staff_id)
    broken_equipment = [e for e in broken_equipment if e['id'] not in processed_equipment_id]
    create_date = request.args.get("create_date")
    accepted_requests = RepairTicketService.get_history_repair_ticket(create_date)
    for r in pending_requests:
        r['equipments'] = RepairTicketService.get_equipment_in_repair_ticket(r['id'])
        r['total_cost'] = RepairTicketService.get_total_cost(r['id'])
    for r in accepted_requests:
        r['equipments'] = RepairTicketService.get_equipment_in_repair_ticket(r['id'])
        r['total_cost'] = RepairTicketService.get_total_cost(r['id'])
    return render_template('staff/repair_ticket.html', login_user=login_user,
                                                        broken_equipment=broken_equipment,
                                                        pending_requests=pending_requests,
                                                        accepted_requests=accepted_requests,
                                                        create_date=create_date)  

@staff_blueprint.route('/staff/add_repair_ticket', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def add_repair_ticket():
    staff_id = session.get('account_id')
    equipment_id = int(request.form.get('equipment_id'))
    issue_description = request.form.get('issue_description')
    repair_cost = request.form.get('repair_cost')
    print(equipment_id)
    if RepairTicketService.add_equipment_to_repair_ticket(staff_id, equipment_id, issue_description, repair_cost):
        flash("Thêm thiết bị vào phiếu sửa chửa thành công", 'sucesss')
    else:
        flash("Thêm thiết bị vào phiếu sửa chửa thất bại", 'error')
    return redirect('repair_ticket') 

@staff_blueprint.route('/staff/remove_repair_equipment', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def remove_repair_equipment():
    try:
        if not request.form.get('csrf_token'):
            flash('CSRF token missing.', 'error')
            return redirect(url_for('staff.repair_ticket'))
        
        repair_ticket_id = int(request.form.get('repair_ticket_id'))
        equipment_id = int(request.form.get('equipment_id'))
        
        result = RepairTicketService.remove_equipment_from_ticket(repair_ticket_id, equipment_id)
        
        if result:
            flash('Đã xóa thiết bị khỏi danh sách', 'success')
        else:
            flash(f'Xóa thiết bị khỏi danh sách thất bại: {result["error"]}', 'error')
        
        return redirect(url_for('staff.repair_ticket'))
    
    except Exception as e:
        flash(f'Error removing equipment: {str(e)}', 'error')
        return redirect(url_for('staff.repair_ticket'))
    
@staff_blueprint.route('/staff/remove_liqui_equipment', methods=['POST'])
@login_required
@role_required(RoleID.STAFF.value)
def remove_liqui_equipment():
    try:       
        repair_ticket_id = int(request.form.get('liquidation_id'))
        equipment_id = int(request.form.get('equipment_id'))
        
        result = LiquidationSlipService.remove_equipment_from_slip(repair_ticket_id, equipment_id)
        
        if result:
            flash('Đã xóa thiết bị khỏi danh sách', 'success')
        else:
            flash(f'Thất bại: {result["error"]}', 'error')
        
        return redirect(url_for('staff.liquidation_slip'))
    
    except Exception as e:
        flash(f'Lỗi xóa thiết bị khỏi danh sách: {str(e)}', 'error')
        return redirect(url_for('staff.liquidation_slip'))

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
