from flask import Blueprint, render_template, request, session, flash, redirect

from helpers.helpers import login_required
from services.student_service import StudentService
from enums.role_type import RoleID
from messages import messages_success, messages_failure

general_blueprint = Blueprint('general', __name__)

@general_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        user_id = request.form.get('user_id')

        login_account = StudentService.get_student_by_id(user_id)

        if login_account == None:
            flash(messages_failure["invalid_information"], 'error')
            return render_template('general/login.html')
        login_user_id = login_account['person_id']
        if login_account['password'] == password and login_user_id == user_id:
            session["account_id"] = str(login_user_id)
            flash(messages_success['login_success'],'success')
            if login_user_id == RoleID.MANAGER.value:
                return redirect('/manager')
            elif login_user_id == RoleID.STAFF.value:
                return redirect('/staff')
            else:
                return redirect('/student')
            
        else:
            flash(messages_failure["invalid_information"], 'error')
            return render_template('general/login.html')
    return render_template('general/login.html')
