from flask import Blueprint, render_template, request, session, flash, redirect

from helpers.helpers import login_required
from models.account import Account

manager_blueprint = Blueprint('manager', __name__)

@manager_blueprint.route('/manager', methods=['GET'])
@login_required
def index():
    if request.method == "GET":
        current_account = Account.query.filter_by(id=int(session.get('account_id'))).first()
        current_manager = current_account.staff
        print(current_account)
        print(current_manager.firstname)

        return render_template('manager/manager_dashboard.html', current_manager = current_manager)