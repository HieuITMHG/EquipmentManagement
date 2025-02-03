from flask import Blueprint, render_template, request, session, flash

from helpers.helpers import login_required

general_blueprint = Blueprint('general', __name__)


@general_blueprint.route('/', methods=['GET'])
@login_required
def index():
    return render_template('manager/dashboard.html')

@general_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        account_id = request.form.get('account_id')

        print(password)
        print(account_id)
    return render_template('general/login.html')