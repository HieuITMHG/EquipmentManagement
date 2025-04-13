from flask import Blueprint, render_template, request, session, redirect, flash, url_for

from helpers.helpers import login_required, role_required
from services.account_service import AccountService
from services.staff_service import StaffService
from services.manager_service import ManagerService
from services.equipment_service import EquipmentService
from services.borrow_service import BorrowService
from enums.action_type import ActionType
from services.room_service import RoomService
from services.liquidation_slip_service import LiquidationSlipService
from services.repair_ticket import RepairTicketService
from services.violation_service import ViolationService
from services.student_service import StudentService
from services.penalty_service import PenaltyService
from enums.role_type import RoleID

manager_blueprint = Blueprint('manager', __name__)

@manager_blueprint.route('/manager', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value)
def manager():
    if request.method == "GET":
        login_manager = AccountService.get_account_by_person_id (session.get('account_id'))
        return render_template('manager/manager_dashboard.html', login_manager = login_manager)
    
# Route để hiển thị danh sách tài khoản
@manager_blueprint.route('/manager/manage_account', methods=['GET', 'POST'])
@login_required
def manage_account():
    # Lấy danh sách tài khoản từ database
    accounts = AccountService.get_all_account()
    
    # # Tìm kiếm theo person_id
    # keyword = request.args.get('keyword')   
    # if keyword:
    #     account = AccountService.get_account_by_person_id(keyword)
    #     if account:
    #         accounts.append(account)
    #     else:
    #         flash("Không tìm thấy tài khoản với ID đã nhập.", "warning")
    # else:
    #     flash("Vui lòng nhập ID tài khoản để tìm kiếm.", "danger")

    return render_template('manager/manage_account.html', accounts=accounts)

@manager_blueprint.route('/manager/edit_account/<account_id>')
def edit_account(account_id):...

@manager_blueprint.route('/manager/delete_account/<account_id>')
def delete_account(account_id):...

@manager_blueprint.route('/manager/add_account')
def add_account():...

# # @manager_blueprint.route('/manager/manage_staff_account/<int:account_id>', methods=['GET'])
# # @manager_blueprint.route('/manager/manage_staff_account', methods=['GET', 'POST'])
# # @login_required
# # # @role_required(RoleID.MANAGER.value)
# # def manage_staff_account(account_id=None):
# #     if request.method == "GET":
# #         login_manager = AccountService.get_account_by_person_id(session.get('account_id'))
# #         accounts = ManagerService.get_all_accounts()
# #         selected_account = ManagerService.get_account_by_id(account_id) if account_id else None
# #         return render_template("manager/manage_staff_account.html",
# #                                login_manager=login_manager,
# #                                accounts=accounts,
# #                                selected_account=selected_account)

# #     # POST: cập nhật tài khoản
# #     acc_id = request.form.get("account_id")
# #     password = request.form.get("password")
# #     role_id = request.form.get("role_id")

# #     if not acc_id:
# #         flash("Thiếu ID tài khoản", "error")
# #         return redirect("/manager/manage_staff_account")
    
# #     ManagerService.update_account(acc_id, password, role_id)
# #     flash("Cập nhật tài khoản thành công", "success")
# #     return redirect("/manager/manage_staff_account")


# # @manager_blueprint.route('/manager/add_staff_account', methods=['GET', 'POST'])
# # @login_required
# # # @role_required(RoleID.MANAGER.value)
# # def add_staff_account():
# #     login_manager = AccountService.get_account_by_person_id(session.get('account_id'))
# #     if request.method == "GET":
# #         return render_template("manager/add_staff_account.html", login_manager=login_manager)

# #     password = request.form.get("password")
# #     role_id = request.form.get("role_id")

# #     if not password or not role_id:
# #         flash("Thiếu thông tin tài khoản", "error")
# #         return redirect("/manager/manage_staff_account/add")

# #     ManagerService.create_account(password, role_id)
# #     flash("Tạo tài khoản thành công", "success")
# #     return redirect("/manager/manage_staff_account")


# # @manager_blueprint.route('/manager/delete_staff_account', methods=['GET'])
# # @login_required
# # # @role_required(RoleID.MANAGER.value)
# # def delete_staff_account():
# #     acc_id = request.args.get("account_id")
# #     if not acc_id:
# #         flash("Thiếu ID tài khoản", "error")
# #         return redirect("/manager/manage_staff_account")

# #     ManagerService.delete_account(acc_id)
# #     flash("Xoá tài khoản thành công", "success")
# #     return redirect("/manager/manage_staff_account")



# manager_blueprint = Blueprint('manager', __name__)

# # Dashboard
# @manager_blueprint.route('/manager', methods=['GET'])
# @login_required
# # @role_required(RoleID.MANAGER.value)
# def manager():
#     login_manager = AccountService.get_account_by_person_id(session.get('account_id'))
#     return render_template('manager/manager_dashboard.html', login_manager=login_manager)


# # Trang quản lý tất cả tài khoản nhân viên
# @manager_blueprint.route('/manager/manage_staff_account', methods=['GET'])
# @login_required
# # @role_required(RoleID.MANAGER.value)
# def manage_staff_account():
#     login_manager = AccountService.get_account_by_person_id(session.get('account_id'))
#     staff_accounts = AccountService.get_all_account()
#     return render_template("manager/manage_staff_account.html",
#                            login_manager=login_manager,
#                            staff_accounts=staff_accounts)


# # Trang thêm tài khoản
# @manager_blueprint.route('/manager/add_staff_account', methods=['GET', 'POST'])
# @login_required
# # @role_required(RoleID.MANAGER.value)
# def add_staff_account():
#     login_manager = AccountService.get_account_by_person_id(session.get('account_id'))

#     if request.method == "GET":
#         return render_template("manager/add_staff_account.html", login_manager=login_manager)

#     username = request.form.get("username")
#     email = request.form.get("email")
#     password = request.form.get("password")

#     if not username or not email or not password:
#         flash("Vui lòng nhập đầy đủ thông tin", "error")
#         return redirect(url_for("manager.add_staff_account"))

#     ManagerService.create_account()#password, role_id
#     flash("Tạo tài khoản thành công", "success")
#     return redirect(url_for("manager.manage_staff_account"))


# # Trang sửa tài khoản
# @manager_blueprint.route('/manager/edit_staff_account/<int:account_id>', methods=['GET', 'POST'])
# @login_required
# # @role_required(RoleID.MANAGER.value)
# def edit_staff_account(account_id):
#     login_manager = AccountService.get_account_by_person_id(session.get('account_id'))

#     if request.method == "GET":
#         account = ManagerService.get_account_by_id(account_id)
#         if not account:
#             flash("Không tìm thấy tài khoản", "error")
#             return redirect(url_for("manager.manage_staff_account"))
#         return render_template("manager/edit_staff_account.html", account=account, login_manager=login_manager)

#     # POST: Thêm tài khoản
#     password = request.form.get("password")
#     role_id = request.form.get("role_id")


#     if not password or not role_id:
#         flash("Thông tin không đầy đủ", "error")
#         return redirect(url_for("manager.edit_staff_account", account_id=account_id))

#     ManagerService.update_account(account_id, password, role_id)
#     flash("Cập nhật tài khoản thành công", "success")
#     return redirect(url_for("manager.manage_staff_account"))


# # Xóa tài khoản
# @manager_blueprint.route('/manager/delete_staff_account/<int:account_id>', methods=['POST'])
# @login_required
# # @role_required(RoleID.MANAGER.value)
# def delete_staff_account(account_id):
#     ManagerService.delete_account(account_id)
#     flash("Xóa tài khoản thành công", "success")
#     return redirect(url_for("manager.manage_staff_account"))
