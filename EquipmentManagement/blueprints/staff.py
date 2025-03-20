from flask import Blueprint, render_template, request, session, redirect

from helpers.helpers import login_required
from services.account_service import AccountService
from services.staff_service import StaffService
from services.borrow_service import BorrowService
from enums.action_type import ActionType

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


@staff_blueprint.route('/staff/staff_manage_equiment', methods=['GET'])
@staff_blueprint.route('/staff/staff_manage_equiment', methods=['GET', 'POST'])
@login_required
def staff_manage_equiment():
    if request.method == "GET":
        login_staff = AccountService.get_account_by_person_id(session.get('account_id'))
        lst_equipment = StaffService.get_all_equipment_with_room()
        for equi in lst_equipment:
            print (equi)
        return render_template('staff/staff_manage_equiment.html', login_staff = login_staff,
                               lst_equipment=lst_equipment)
    