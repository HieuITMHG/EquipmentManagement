from flask import Blueprint, render_template, request, session, flash, redirect

from helpers.helpers import login_required
from models.staff import Staff
from models.student import Student
from enums.role_type import RoleID
from messages import messages_success, messages_failure

general_blueprint = Blueprint('general', __name__)

@general_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        user_id = request.form.get('user_id')

        session.clear()
        if 'NV' in user_id or 'QL' in user_id:
            login_user = Staff.query.get(user_id)
        else:
            login_user = Student.query.get(user_id)

        if login_user == None:
            flash(messages_failure["invalid_information"], 'error')
            return render_template('general/login.html')

        login_account = login_user.account

        if login_account.password == password and login_user.id == user_id:
            session["account_id"] = str(login_account.id)
            flash(messages_success['login_success'],'success')
            if login_account.role_id == RoleID.MANAGER.value:
                return redirect('/manager')
            elif login_account.role_id == RoleID.STAFF.value:
                return redirect('/staff')
            else:
                return redirect('/student')
            
        else:
            flash(messages_failure["invalid_information"], 'error')
            return render_template('general/login.html')


    return render_template('general/login.html')