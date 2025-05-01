from flask import Blueprint, request, session, render_template, flash, redirect
from helpers.helpers import login_required, role_required
from enums.role_type import RoleID
from services.inventory import InventoryService
from services.account_service import AccountService
from dateutil import parser


inventory_blueprint = Blueprint('inventory', __name__)


from flask import jsonify

@inventory_blueprint.route('/inventory/statistical', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def statistical():
    quarter_id = request.args.get('quarter_id', type=int)  # Lấy quarter_id từ query string
    
    # Gọi hàm để lấy thống kê theo quý
    result = InventoryService.get_num_by_quarter(quarter_id)

    # Trả về kết quả dưới dạng JSON
    return jsonify({
        'total_devices': result[0],
        'total_broken': result[1],
        'total_repairing': result[2],
        'total_liquidated': result[3]
    })

@inventory_blueprint.route('/inventory/inventory_history', methods=['GET'])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def inventory_history():
    staff_id = session.get('account_id')
    login_user = AccountService.get_account_by_person_id(staff_id)
    quarter_id = request.args.get('quarter_id', type=int, default=1)
    room_details = InventoryService.get_room_detail_by_quarter(quarter_id)
    quarters = InventoryService.get_all_quarters() 
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'room_details': room_details})
    if login_user['role_id'] == RoleID.STAFF.value:
        return render_template('staff/inventory.html', login_user=login_user, room_details=room_details, quarters=quarters, quarter_id=quarter_id)
    else:
        return render_template('manager/inventory.html', login_user=login_user, room_details=room_details, quarters=quarters, quarter_id=quarter_id)

@inventory_blueprint.route('/inventory/create_form', methods=['GET', 'POST'])
@login_required
@role_required(RoleID.MANAGER.value, RoleID.STAFF.value)
def create_inventory_form():
    if request.method == 'POST':
        try:
            # Get staff_id, start_date, end_date
            staff_id = request.form.get('staff_id')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')

            # Validate basic inputs
            if not all([staff_id, start_date, end_date]):
                flash('Vui lòng điền đầy đủ thông tin: ID người thực hiện, ngày bắt đầu, ngày kết thúc.', 'error')
                return redirect('/inventory/create_form')

            # Validate staff_id format
            if not staff_id or len(staff_id) > 20:
                flash('ID người thực hiện không hợp lệ (tối đa 20 ký tự).', 'error')
                return redirect('/inventory/create_form')

            # Parse dates
            try:
                start_date = parser.parse(start_date).date()
                end_date = parser.parse(end_date).date()
                if end_date < start_date:
                    flash('Ngày kết thúc phải sau ngày bắt đầu.', 'error')
                    return redirect('/inventory/create_form')
            except ValueError:
                flash('Định dạng ngày không hợp lệ.', 'error')
                return redirect('/inventory/create_form')

            # Get all rooms and collect room details
            rooms = InventoryService.get_all_rooms()
            room_details = []
            for room in rooms:
                room_id = room['id']
                total_devices = request.form.get(f'total_devices_{room_id}')
                broken_count = request.form.get(f'broken_count_{room_id}')
                repairing_count = request.form.get(f'repairing_count_{room_id}')
                liquidated_count = request.form.get(f'liquidated_count_{room_id}')

                # Validate room data
                if not all([total_devices, broken_count, repairing_count, liquidated_count]):
                    flash(f'Vui lòng điền đầy đủ thông tin cho phòng {room_id}.', 'error')
                    return redirect('/inventory/create_form')

                try:
                    room_details.append({
                        'room_id': room_id,
                        'total_devices': int(total_devices),
                        'broken_count': int(broken_count),
                        'repairing_count': int(repairing_count),
                        'liquidated_count': int(liquidated_count)
                    })
                except ValueError:
                    flash(f'Dữ liệu số lượng cho phòng {room_id} phải là số nguyên hợp lệ.', 'error')
                    return redirect('/inventory/create_form')

            # Save to database
            InventoryService.create_inventory_form(staff_id, start_date, end_date, room_details)
            flash('Phiếu kiểm kê đã được lưu thành công.', 'success')
            return redirect('/inventory/inventory_history')
        
        except Exception as e:
            flash(f'Có lỗi xảy ra khi lưu phiếu kiểm kê: {str(e)}', 'error')
            return redirect('/inventory/create_form')
    
    # GET: Render form
    rooms = InventoryService.get_all_rooms()
    return render_template('general/create_inventory_form.html', rooms=rooms)