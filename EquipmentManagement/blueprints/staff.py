from flask import Blueprint, render_template, request, session

from helpers.helpers import login_required
from models.account import Account

staff_blueprint = Blueprint('staff', __name__)

@staff_blueprint.route('/staff', methods=['GET'])
@login_required
def index():
    if request.method == "GET":
        current_account = Account.query.filter_by(id=int(session.get('account_id'))).first()
        current_staff = current_account.staff
        print(current_staff)
        return render_template('staff/staff_dashboard.html', current_staff = current_staff)