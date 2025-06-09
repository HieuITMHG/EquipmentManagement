from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from helpers.helpers import login_required, role_required
from services.account_service import AccountService
from services.equipment_service import EquipmentService
from services.room_service import RoomService
from services.borrow_service import BorrowService
from enums.role_type import RoleID

borrow_blueprint = Blueprint('borrow', __name__)

@borrow_blueprint.route("/borrow/borrow_equipment", methods=["GET"])
@login_required
@role_required(RoleID.STUDENT.value)
def borrow_equipment():
    user_id = session.get("account_id")
    login_user = AccountService.get_user_info(user_id)
    phong_id = request.args.get("room")
    rooms = RoomService.get_available_room()
    borrowed_equipments = EquipmentService.get_borrowed_equipment(user_id) 
    borrowing_equipments = EquipmentService.get_borrowing_equipment(user_id)
    exist_request = BorrowService.get_existing_borrow_request(user_id)
    if exist_request:
        phong_id = exist_request['phong_id']
        rooms = []
    borrowable_equipments = EquipmentService.get_borrowable_equipment_by_room(phong_id) 
    borrowable_equipments = [e for e in borrowable_equipments if e not in borrowing_equipments]
    return render_template("borrow/borrow.html", 
                           rooms=rooms, 
                           login_user=login_user, 
                           borrowable_equipments=borrowable_equipments, 
                           borrowed_equipments=borrowed_equipments,
                           borrowing_equipments=borrowing_equipments,
                           room_id = phong_id)

@borrow_blueprint.route("/borrow/borrow_request", methods=["POST"])
@login_required
@role_required(RoleID.STUDENT.value)
def borrow_request():
    login_user_id = session.get("account_id")
    existing_borrow_request = BorrowService.get_existing_borrow_request(login_user_id)
    lst_equipmment_id = request.form.getlist("lst_equipment_id")
    if existing_borrow_request:
        if BorrowService.add_equipment_to_request(request_id=existing_borrow_request['id'], equipment_ids=lst_equipmment_id, phong_id=existing_borrow_request['phong_id']):
            flash("Đã cập nhật yêu cầu mượn thiết bị!", 'success')
            return redirect(url_for("borrow.borrow_equipment"))
        else:
            flash("Có lỗi xảy ra. Vui lòng thử lại sau!", 'error')
            return redirect(url_for("borrow.borrow_equipment"))
    else:
        if(BorrowService.create_borrow_request_with_details(login_user_id, lst_equipmment_id)):
            flash("Yêu cầu mượn thiết bị thành công!", 'success')
        else:
            flash("Có lỗi xảy ra. Vui lòng thử lại sau!", 'error')
    return redirect(url_for("borrow.borrow_equipment"))

@borrow_blueprint.route("/borrow/borrow_history", methods=["GET"])
@login_required
@role_required(RoleID.STUDENT.value)
def history_borrow():
    user_id = session.get("account_id")
    login_user = AccountService.get_account_by_person_id(user_id)
    phieu_muon = BorrowService.get_borrow_history(person_id=user_id)
    ngay_muon = request.args.get("borrowing_time")
    if ngay_muon != None and ngay_muon != "":
        phieu_muon = BorrowService.get_borrow_history_by_date(person_id=user_id, bdate=ngay_muon)
    return render_template("borrow/borrow_history.html", login_user=login_user, lst_borrow=phieu_muon, borrowing_time=ngay_muon)

@borrow_blueprint.route("/borrow/cancel_borrow_request", methods=["POST"])
@login_required
@role_required(RoleID.STUDENT.value)
def cancel_borrow_request():
    e_id = request.form.get("equipment_id")
    re = BorrowService.get_existing_borrow_request(session.get("account_id"))
    if BorrowService.remove_equipment_from_request(e_id=e_id, request_id=re['id']):
        if BorrowService.count_equipment_in_request(request_id=re['id']) == 0:
            BorrowService.delete_borrow_request(re['id'])
        flash("Hủy yêu cầu mượn thiết bị thành công!", 'success')
    else:
        flash("Có lỗi xảy ra. Vui lòng thử lại sau!", 'error')
    return redirect(url_for("borrow.borrow_equipment"))

@borrow_blueprint.route("/borrow/profile", methods=["GET"])
@role_required(RoleID.STUDENT.value)
@login_required
def profile():
    user_id = session.get("account_id")
    login_user = AccountService.get_user_info(user_id)
    return render_template("borrow/profile.html", login_user=login_user)

@borrow_blueprint.route('/borrow/manage_borrow_request', methods=['GET', 'POST'])
@role_required(RoleID.STAFF.value, RoleID.MANAGER.value )
@login_required
def manage_borrow_request():
    if request.method == "GET":
        login_user = AccountService.get_account_by_person_id(session.get('account_id'))
        hborrow_time = request.args.get('hborrow_time')
        hperson_id = request.args.get('hperson_id')
        borrow_time = request.args.get('borrow_time')
        person_id = request.args.get('person_id')
        lst_request = BorrowService.get_pending_borrow_requests()
        for r in lst_request:
            for e in r['equipments']:
                print(e)
        accepted_requests = BorrowService.get_accepted_borrow_requests()
        history_requests = BorrowService.get_historical_borrow_requests()
        if login_user['vai_tro_id'] == RoleID.STAFF.value:
            return render_template('staff/borrow_request.html', 
                                login_user=login_user,
                                lst_request=lst_request, 
                                accepted_requests = accepted_requests,
                                borrow_time=borrow_time,
                                person_id=person_id,
                                hperson_id=hperson_id,
                                hborrow_time=hborrow_time,
                                history_requests=history_requests)
        return render_template('manager/borrow_request.html', 
                                login_user=login_user,
                                lst_request=lst_request, 
                                accepted_requests = accepted_requests,
                                borrow_time=borrow_time,
                                person_id=person_id,
                                hperson_id=hperson_id,
                                hborrow_time=hborrow_time,
                                history_requests=history_requests)
        
    borrow_request_id = int(request.form.get('request_id'))
    action = int(request.form.get('action'))
    if action == 1:
        if BorrowService.accept_borrow_request(borrow_request_id, session.get('account_id')):
            flash("Đã chấp nhận yêu cầu mượn")
        else:
            flash("Chấp nhận yêu cầu mượn thất bại")
    else:
        if BorrowService.reject_borrow_request(borrow_request_id):
            flash("Đã từ tối yêu cầu mượn")
        else:
            flash("Từ chối yêu cầu mượn thất bại")
    return redirect("manage_borrow_request")

@borrow_blueprint.route('/borrow/finish_borrow_request', methods=['POST'])
@role_required(RoleID.STAFF.value, RoleID.MANAGER.value)
@login_required
def finish_borrow_request():
    request_id = request.form.get('request_id')
    if BorrowService.return_equipment(request_id):
        flash("Duyệt trả thành công", 'success')
    else:
        flash("Có lỗi xảy ra. Vui lòng thử lại sau!", 'error')
    return redirect("manage_borrow_request")

@borrow_blueprint.route('/manage_equipment', methods=['POST'])
@role_required(RoleID.STAFF.value, RoleID.MANAGER.value)
@login_required
def manage_equipment():
    equipment_id = request.form.get('equipment_id')
    action = request.form.get('action')
    if action == 'approve':
        if BorrowService.accept_one_equipment(equipment_id):
            flash("Duyệt yêu cầu mượt thành công")
    elif action == 'reject':
        if BorrowService.reject_one_equipment(equipment_id):
            flash("Từ chối thiết bị thành công")
    elif action == 'return':
        if BorrowService.return_one_equipment(equipment_id):
            flash("Trả thiết bị thành công") 
    elif action == 'lost':
        if BorrowService.update_equipment_status(equipment_id, 'DA_MAT'):
            flash("Xác nhận thiết bị bị mất thành công")
    else:
        if BorrowService.update_damaged_equipment(equipment_id):
            flash("Xác nhận thiết bị bị hư hại thành công")
    return redirect(url_for('borrow.manage_borrow_request'))

@borrow_blueprint.route('/add_addition_equipment', methods=['GET', 'POST'])
def add_addition_equipment():
    if request.method == "GET":
        request_id = request.args.get('request_id')
        phong_id = request.args.get('phong_id')
        lst_borrowable = EquipmentService.get_borrowable_equipment(phong_id)
        return render_template('/borrow/add_addition_equipment.html', request_id=request_id, phong_id=phong_id, lst_borrowable=lst_borrowable)
    request_id = request.form.get('request_id')
    phong_id = request.form.get('phong_id')
    equipment_ids = request.form.getlist('lst_equipment_id') 
    if BorrowService.add_addition_equipment(equipment_ids=equipment_ids, request_id=request_id, phong_id=phong_id):
        flash("Đã cập nhật yêu cầu mượn thiết bị!", 'success')
    return redirect(url_for('borrow.manage_borrow_request'))


