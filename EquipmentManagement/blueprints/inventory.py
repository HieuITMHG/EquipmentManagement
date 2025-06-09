from flask import Blueprint, request, session, render_template, flash, redirect, jsonify
from helpers.helpers import login_required, role_required
from enums.role_type import RoleID
from services.inventory import InventoryService
from services.account_service import AccountService
from dateutil import parser

inventory_blueprint = Blueprint('inventory', __name__)

@inventory_blueprint.route('/inventory/statistical', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def statistical():
    phieu_kiem_ke_id = request.args.get('phieu_kiem_ke_id', type=int, default=None)
    if phieu_kiem_ke_id is None:
        return jsonify({
            'total_devices': 0,
            'total_broken': 0,
            'total_repairing': 0,
            'total_liquidated': 0
        })
    result = InventoryService.get_num_by_inventory(phieu_kiem_ke_id)
    return jsonify({
        'total_devices': int(result[0]),
        'total_broken': int(result[1]),
        'total_repairing': int(result[2]),
        'total_liquidated': int(result[3])
    })

@inventory_blueprint.route('/inventory/inventory_history', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def inventory_history():
    staff_id = session.get('account_id')
    login_user = AccountService.get_account_by_person_id(staff_id)
    phieu_kiem_ke_id = request.args.get('phieu_kiem_ke_id', type=int, default=None)
    inventories = InventoryService.get_all_inventories()

    if not inventories:
        flash('Chưa có phiếu kiểm kê nào. Vui lòng tạo phiếu kiểm kê mới.', 'info')
        return render_template(
            'manager/inventory.html' if login_user['vai_tro_id'] == RoleID.MANAGER.value else 'staff/inventory.html',
            login_user=login_user,
            room_details=[],
            inventories=[],
            phieu_kiem_ke_id=None
        )

    if phieu_kiem_ke_id is None:
        phieu_kiem_ke_id = inventories[0]['id']

    if not any(inv['id'] == phieu_kiem_ke_id for inv in inventories):
        flash('Phiếu kiểm kê không hợp lệ. Chọn phiếu đầu tiên.', 'error')
        phieu_kiem_ke_id = inventories[0]['id']

    room_details = InventoryService.get_room_detail_by_inventory(phieu_kiem_ke_id)

    if request.headers.get('Accept') == 'application/json':
        return jsonify({
            'room_details': room_details,
            'inventories': inventories,
            'phieu_kiem_ke_id': phieu_kiem_ke_id
        })

    template = 'manager/inventory.html' if login_user['vai_tro_id'] == RoleID.MANAGER.value else 'staff/inventory.html'
    return render_template(
        template,
        login_user=login_user,
        room_details=room_details,
        inventories=inventories,
        phieu_kiem_ke_id=phieu_kiem_ke_id
    )

@inventory_blueprint.route('/inventory/create_form', methods=['GET', 'POST'])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def create_inventory_form():
    staff_id = session.get('account_id')
    login_user = AccountService.get_account_by_person_id(staff_id)

    if request.method == 'POST':
        try:
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')

            if not all([staff_id, start_date, end_date]):
                flash('Vui lòng điền đầy đủ thông tin: ID người thực hiện, ngày bắt đầu, ngày kết thúc.', 'error')
                return redirect('/inventory/create_form')

            try:
                start_date = parser.parse(start_date)
                end_date = parser.parse(end_date)
                if end_date < start_date:
                    flash('Ngày kết thúc không hợp lệ, phải sau ngày bắt đầu.', 'error')
                    return redirect('/inventory/create_form')
            except ValueError:
                flash('Định dạng ngày không hợp lệ.', 'error')
                return redirect('/inventory/create_form')

            rooms = InventoryService.get_all_rooms()
            room_details = []
            for room in rooms:
                room_id = room['id']
                total_devices = request.form.get(f'total_devices_{room_id}')
                broken_count = request.form.get(f'broken_count_{room_id}')
                repairing_count = request.form.get(f'repairing_count_{room_id}')
                liquidated_count = request.form.get(f'liquidated_count_{room_id}')

                if not all([total_devices, broken_count, repairing_count, liquidated_count]):
                    flash(f'Vui lòng điền đầy đủ thông tin cho phòng {room_id}.', 'error')
                    return redirect('/inventory/create_form')

                try:
                    total = int(total_devices)
                    broken = int(broken_count)
                    repairing = int(repairing_count)
                    liquidated = int(liquidated_count)
                    if total < 0 or broken < 0 or repairing < 0 or liquidated < 0 or (broken + repairing + liquidated > total):
                        flash(f'Dữ liệu số lượng cho phòng {room_id} không hợp lệ.', 'error')
                        return redirect('/inventory/create_form')
                    room_details.append({
                        'room_id': room_id,
                        'total_devices': total,
                        'broken_count': broken,
                        'repairing_count': repairing,
                        'liquidated_count': liquidated
                    })
                except ValueError:
                    flash(f'Dữ liệu số lượng cho phòng {room_id} phải là số nguyên hợp lệ.', 'error')
                    return redirect('/inventory/create_form')

            InventoryService.create_inventory_form(staff_id, start_date, end_date, room_details)
            flash('Phiếu kiểm kê đã được lưu thành công.', 'success')
            return redirect('/inventory/inventory_history')
        
        except Exception as e:
            flash(f'Có lỗi xảy ra khi lưu phiếu kiểm kê: {str(e)}', 'error')
            return redirect('/inventory/create_form')
    
    rooms = InventoryService.get_all_rooms()
    template = 'manager/create_inventory_form.html' if login_user['vai_tro_id'] == RoleID.MANAGER.value else 'general/create_inventory_form.html'
    return render_template(template, rooms=rooms, login_user=login_user)