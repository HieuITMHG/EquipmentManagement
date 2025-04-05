from flask import Blueprint, render_template, request, session, redirect,flash

from helpers.helpers import login_required
from services.account_service import AccountService
from services.staff_service import StaffService
from services.equipment_service import EquipmentService
from services.borrow_service import BorrowService
from enums.action_type import ActionType
from services.room_service import RoomService

staff_blueprint = Blueprint('staff', __name__)

@staff_blueprint.route('/staff', methods=['GET'])
@login_required
def staff():
    if request.method == "GET":
        login_staff = AccountService.get_account_by_person_id(session.get('account_id'))
        return render_template('staff/staff_profile.html', login_staff = login_staff)
    
@staff_blueprint.route('/staff/borrow_request/<int:request_id>', methods=['GET'])
@staff_blueprint.route('/staff/borrow_request', methods=['GET', 'POST'])
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


@staff_blueprint.route('/staff/staff_manage_equipment/<int:equipment_id>', methods=['GET'])
@staff_blueprint.route('/staff/staff_manage_equipment', methods=['GET', 'POST'])
@login_required
def staff_manage_equipment(equipment_id=None):
    if request.method == "GET":
        login_staff = AccountService.get_account_by_person_id(session.get('account_id'))
        lst_equipment = StaffService.get_all_equipment()
        room=RoomService.get_all_room()

        if equipment_id==None:
            return render_template('staff/staff_manage_equipment.html', login_staff = login_staff,
                               lst_equipment=lst_equipment,equi=None)
        equi=EquipmentService.get_equipment_by_id(equipment_id)
        print(equi)
        
        return render_template('staff/staff_manage_equipment.html', login_staff = login_staff,
                                lst_equipment=lst_equipment,
                                equi=equi,
                                room=room)
    
    
    
    new_name=request.form.get("equi_name")
    new_id=request.form.get("equi_id")
    new_room=request.form.get("room")
    print(new_name) 
    print(new_id)
    print(new_room)
    StaffService.change_equi_info(new_id,new_name,new_room)
    return redirect("staff_manage_equipment")


@staff_blueprint.route('/staff/add_items', methods=['GET', 'POST'])
@login_required
def add_items():
    login_staff = AccountService.get_account_by_person_id(session.get('account_id'))
    if request.method == "GET":
        equi=EquipmentService.get_all_equipment()
        room=RoomService.get_all_room()
        equi_type=('MOBILE', 'FIXED', 'SHARED')
        return render_template("staff/add_items.html",login_staff=login_staff,equi=equi,room=room,equi_type=equi_type)
    
    equi_name = request.form.get('equi_name')  # Tên thiết bị
    room_id = request.form.get('room')  # ID phòng
    equi_type = request.form.get('equi_t')  # Kiểu thiết bị (BỊ TRÙNG NAME -> CẦN SỬA)
    equi_status = "AVAILABLE"  # Mặc định là AVAILABLE  
    print(request.form.get('equi_t'))
    print(equi_name)
    print(room_id)
    print(equi_status)
    if(equi_name):
        EquipmentService.add_equipment(equi_name, "AVAILABLE", equi_type, room_id)
    return redirect("staff_manage_equipment")

@staff_blueprint.route('/staff/delete_equipment', methods=['GET'])
@login_required
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
def bh_filter(request_id=None):
    if request.method == "GET":
        login_staff = AccountService.get_account_by_person_id(session.get('account_id'))
        lst_borrow_equipment = BorrowService.get_equipment_by_request_id(request_id)
        status = request.args.get("status", "")
        if (status==''):
            lst_request = BorrowService.get_accepted_or_returned_borrow_request()
        if (status=='ACCEPTED'):
            print("1")
            lst_request = BorrowService.get_accepted_borrow_request()
            print(lst_request)
        if (status=='RETURNED'):
            print("returned")
            print("1")
            lst_request = BorrowService.get_returned_borrow_request()
            print(lst_request)
        return render_template('staff/borrow_history.html', login_staff=login_staff,lst_request=lst_request, lst_borrow_equipment=lst_borrow_equipment,status=status) 
        


@staff_blueprint.route('/staff/repair_ticket/<int:repair_ticket_id>', methods=['GET'])
@staff_blueprint.route('/staff/repair_ticket', methods=['GET', 'POST'])
@login_required
def repair_ticket(repair_ticket_id=None):
    login_staff = AccountService.get_account_by_person_id(session.get('account_id'))
    if (request.method=="GET"):
        if (repair_ticket_id==None):
            ticket = StaffService.get_all_repair_ticket()
            for t in ticket:
                print(t)
            return render_template('staff/repair_ticket.html',login_staff=login_staff,ticket=ticket)
        ticket = StaffService.get_all_repair_ticket()
        infor_detail_ticket=StaffService.get_infor_detail_ticket(repair_ticket_id)

        return render_template('staff/repair_ticket.html',login_staff=login_staff,ticket=ticket,infor_detail_ticket=infor_detail_ticket)
    
    