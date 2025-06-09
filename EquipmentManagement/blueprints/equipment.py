from flask import Blueprint, render_template, request, session, redirect, flash, url_for

from helpers.helpers import login_required, role_required
from services.equipment_service import EquipmentService
from services.room_service import RoomService
from services.account_service import AccountService
from enums.role_type import RoleID
from enums.management_type import ManagementType
import os
from werkzeug.utils import secure_filename
import time

UPLOAD_FOLDER = os.path.join('static', 'img')

equipment_blueprint = Blueprint('equipment', __name__)

@equipment_blueprint.route('/equipment', methods=['GET', 'POST'])
@login_required
@role_required(RoleID.STAFF.value, RoleID.MANAGER.value)
def equipment():
    login_user = AccountService.get_user_info(session.get('account_id'))
    phong_id = request.args.get("phong_id", None)
    loai_thiet_bi = request.args.get("loai_thiet_bi", None)
    trang_thai = request.args.get("trang_thai", None)
    ten_thiet_bi = request.args.get("ten_thiet_bi", None)
    rooms = RoomService.get_all_room()
    lst_equipment = EquipmentService.search_equipment(phong_id=phong_id, trang_thai=trang_thai, loai_thiet_bi=loai_thiet_bi, ten_thiet_bi=ten_thiet_bi)
    nums = EquipmentService.get_statistical_number()
    if login_user['vai_tro_id'] == RoleID.STAFF.value:
        return render_template('equipment/equipment.html', login_user=login_user, lst_equipment=lst_equipment, rooms=rooms, nums=nums)
    return render_template('manager/equipment.html', login_user=login_user, lst_equipment=lst_equipment, rooms=rooms, nums=nums)

@equipment_blueprint.route("/equipment/add", methods=["GET", "POST"])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def add_equipment():
    if request.method == 'GET':
        rooms = RoomService.get_all_room()
        return render_template("equipment/new_equipment.html", rooms=rooms)
    ten_thiet_bi = request.form['ten_thiet_bi']
    loai_thiet_bi = request.form['loai_thiet_bi']
    phong_id = request.form['phong_id']
    anh = request.files['anh']
    anh_url = None
    if anh and anh.filename != '':
        filename = secure_filename(anh.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(save_path):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{int(time.time())}{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, filename)
        anh.save(save_path)
        anh_url = f"img/{filename}"
    if EquipmentService.add_equipment(ten_thiet_bi, loai_thiet_bi, phong_id, anh_url):
        flash("Thêm thiết bị mới thành công", 'success')
    else:
        flash("Thêm thiết bị mới thất bại", 'error')
    return redirect(url_for('equipment.add_equipment'))

@equipment_blueprint.route("/equipment/edit/<equipment_id>", methods=["GET", "POST"])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def edit(equipment_id):
    if request.method == 'GET':
        equipment = EquipmentService.get_equipment_by_id(equipment_id)
        rooms = RoomService.get_all_room()
        return render_template("equipment/edit_equipment.html", rooms=rooms, equipment=equipment)
    ten_thiet_bi = request.form['ten_thiet_bi']
    loai_thiet_bi = request.form['loai_thiet_bi']
    trang_thai = request.form['trang_thai']
    phong_id = request.form['phong_id']
    anh = request.files['anh']
    anh_url = None
    if anh and anh.filename != '':
        filename = secure_filename(anh.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(save_path):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{int(time.time())}{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, filename)
        anh.save(save_path)
        anh_url = f"img/{filename}"
    if EquipmentService.update_equipment_info(equipment_id, ten_thiet_bi, trang_thai, loai_thiet_bi, phong_id, anh_url):
        flash("Cập nhật thông tin thiết bị thành công", 'success')
    else:
        flash("Cập nhật thông tin thiết bị thất bại", 'error')
    return redirect(url_for('equipment.equipment'))

@equipment_blueprint.route("/equipment/delete", methods=["POST"])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def delete():
    if EquipmentService.delete_equipment_by_id(request.form['thiet_bi_id']):
        flash("Xóa thiết bị thành công", 'success')
    else:
        flash("Không thể xóa thiết bị", 'error')
    return redirect(url_for('equipment.equipment'))


