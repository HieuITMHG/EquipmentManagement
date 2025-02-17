from flask import Blueprint, render_template, request, session

from helpers.helpers import login_required
from models.account import Account

student_blueprint = Blueprint('student', __name__)

@student_blueprint.route('/student', methods=['GET'])
@login_required
def index():
    if request.method == "GET":
        current_account = Account.query.filter_by(id=int(session.get('account_id'))).first()
        current_student = current_account.student

        return render_template('student/student_dashboard.html', current_student = current_student)