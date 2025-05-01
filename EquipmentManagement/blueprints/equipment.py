from flask import Blueprint, render_template, request, session, redirect,flash, url_for

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
    it = request.args.get("it")
    nums = EquipmentService.get_statistical_number()
    login_user = AccountService.get_account_by_person_id(session.get('account_id'))
    room_id = request.args.get("room_id", None)
    equipment_type = request.args.get("equipment_type", None)
    status = request.args.get("status", None)
    equipment_name = request.args.get("equipment_name", None)
    rooms = RoomService.get_all_room()
    lst_equipment = EquipmentService.search_equipment(room_id=room_id,status=status,equipment_type=equipment_type, equipment_name=equipment_name, management_type=ManagementType.INDIVIDUAL.value)
    lst_equipments = EquipmentService.search_equipment(room_id=room_id, equipment_type=equipment_type, equipment_name=equipment_name, management_type=ManagementType.QUANTITY.value)
    for e in lst_equipments:
        kho = EquipmentService.get_equipment_by_name_and_room(e['equipment_name'], 'HVCS')
        e['hvcs'] = kho['quantity'] - kho['broken_quantity'] - kho['under_repair_quantity']
        print(e['hvcs'])
    if login_user['role_id'] == RoleID.STAFF.value:
        return render_template('equipment/equipment.html', 
                           login_user = login_user, 
                           lst_equipment = lst_equipment, 
                           rooms = rooms, 
                           lst_equipments = lst_equipments, 
                           it=it,
                           nums = nums) 
    return render_template('manager/equipment.html', 
                           login_user = login_user, 
                           lst_equipment = lst_equipment, 
                           rooms = rooms, 
                           lst_equipments = lst_equipments, 
                           it=it,
                           nums = nums)  

@equipment_blueprint.route("/equipment/add", methods=["GET", "POST"])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def add_equipment():
    if request.method == 'GET':
        rooms = RoomService.get_all_room()
        return render_template("equipment/new_equipment.html", rooms=rooms)

    # Lấy dữ liệu từ form
    quantity = 1
    equipment_name = request.form['equipment_name']
    equipment_type = request.form['equipment_type']
    management_type = request.form['management_type']
    room_id = request.form['room_id']
    image = request.files['image']

    if management_type == ManagementType.QUANTITY.value:
        quantity = int(request.form['quantity'])

    # Xử lý hình ảnh
    image_url = None
    if image and image.filename != '':
        filename = secure_filename(image.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(save_path):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{int(time.time())}{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, filename)
        
        image.save(save_path)
        image_url = f"img/{filename}"

    # Kiểm tra nếu thiết bị quản lý theo QUANTITY và đã tồn tại
    existing_equipment = EquipmentService.get_equipment_by_name_and_room(equipment_name, room_id)

    if existing_equipment and management_type == ManagementType.QUANTITY.value:
        # Nếu tồn tại -> Update tăng số lượng
        new_quantity = existing_equipment['quantity'] + quantity
        EquipmentService.update_quantity(existing_equipment['id'], new_quantity)
        flash("Thêm thiết bị mới thành công", 'success')
    else:
        # Nếu không tồn tại -> Tạo thiết bị mới
        EquipmentService.add_equipment(
            equipment_name,
            equipment_type,
            management_type,
            room_id,
            quantity,
            image_url
        )
        flash("Tạo thiết bị mới thành công", 'success')

    return redirect(url_for('equipment.add_equipment'))

@equipment_blueprint.route("/equipment/edit/<equipment_id>", methods=["GET", "POST"])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def edit(equipment_id):
    if request.method == 'GET':
        equipment = EquipmentService.get_equipment_by_id(equipment_id)
        rooms = RoomService.get_all_room()
        return render_template("equipment/edit_equipment.html", rooms = rooms, equipment = equipment)
    equipment_name = request.form['equipment_name']
    room_id = request.form['room_id']
    status = request.form['status']
    image = request.files['image']
    image_url = None
    if image and image.filename != '':
        filename = secure_filename(image.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(save_path):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{int(time.time())}{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, filename)
        
        image.save(save_path)
        image_url = f"img/{filename}"
    if EquipmentService.update_equipment_info(equipment_id, equipment_name, status, room_id, image_url):
        flash("Cập nhật thông tin thiết bị thành công", 'success')
    else:
        flash("Cập nhật thông tin thiết bị thất bại", 'error')
    return redirect(url_for('equipment.equipment', it=True))


@equipment_blueprint.route("/equipment/delete", methods=["POST"])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def delete():
    if EquipmentService.delete_equipment_by_id(request.form['equipment_id']):
        flash("Xóa thiết bị thành công", 'success')
    else:
        flash("Không thể xóa vì đang được thêm vào phiếu", 'error')
    return redirect(url_for('equipment.equipment'))

@equipment_blueprint.route("/equipment/edit_quantity", methods=["POST"])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def edit_quantity():
    quantity = request.form["quantity"]
    equipment_id = request.form["equipment_id"]
    broken_quantity = request.form["broken_quantity"]
    if EquipmentService.update_equipment_quantities(equipment_id, quantity, broken_quantity):
        flash("Sửa số lượng thiết bị thành công", 'success')
    else:
        flash("Sửa số lượng thiết bị thất bại", 'error')
    return redirect(url_for('equipment.equipment', it=False))


@equipment_blueprint.route('/equipment/allocate', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def allocate_equipment():
    equipment_id = request.form.get('equipment_id')
    allocate_quantity = request.form.get('allocate_quantity')
    try:
        equipment_id = int(equipment_id)
        allocate_quantity = int(allocate_quantity)
    except (ValueError, TypeError):
        flash('Dữ liệu không hợp lệ', 'error')
        return redirect(url_for('equipment.list'))
    success, message = EquipmentService.allocate_equipment(equipment_id, allocate_quantity)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('equipment.equipment', it=False))  

@equipment_blueprint.route('/equipment/retrieve', methods=['POST'])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def retrieve_equipment():
    equipment_id = request.form.get('equipment_id')
    available_quantity = request.form.get('available_quantity')
    broken_quantity = request.form.get('broken_quantity')
    under_repair_quantity = request.form.get('under_repair_quantity')
    
    # Validate inputs
    try:
        equipment_id = int(equipment_id)
        available_quantity = int(available_quantity)
        broken_quantity = int(broken_quantity)
        under_repair_quantity = int(under_repair_quantity)
    except (ValueError, TypeError):
        flash('Dữ liệu không hợp lệ', 'error')
        return redirect(url_for('equipment.list'))
    
    # Call service to retrieve equipment
    success, message = EquipmentService.retrieve_equipment(
        equipment_id, available_quantity, broken_quantity, under_repair_quantity
    )
    
    # Provide feedback
    flash(message, 'success' if success else 'error')
    return redirect(url_for('equipment.equipment', it=False))  # Adjust to your equipment list route