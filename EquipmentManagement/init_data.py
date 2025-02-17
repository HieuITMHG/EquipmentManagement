from models.database import db
from models.role import Role
from models.department import Department
from models.classroom import Classroom
from enums.role_type import RoleType

def initialize_data(app):
    init_role()
    init_department()
    init_class()

def init_role():
    lst_roles = [
        Role(role=RoleType.MANAGER.value),
        Role(role=RoleType.STAFF.value),
        Role(role=RoleType.STUDENT.value)
    ]

    for role in lst_roles:
        # Kiểm tra xem role đã tồn tại chưa
        existing_role = Role.query.filter_by(role=role.role).first()
        if not existing_role:
            db.session.add(role)
            db.session.commit()

def init_department():
    lst_department =[
        Department(id="D001", department_name="Công nghệ thông tin 2"),
        Department(id="D002", department_name="Quản trị kinh doanh 2"),
        Department(id="D003", department_name="Điện tử viễn thông 2"),
    ]
    
    for department in lst_department:
        existing_department = Department.query.filter_by(id=department.id).first()
        if not existing_department:
            db.session.add(department)
            db.session.commit()

def init_class():
    lst_class = [
        Classroom(id="D22CQCN02-N", classroom_name="Ngành Công nghệ thông tin-2022-2", academic_year="2022-2027", department_id="D001"),
        Classroom(id="D24CQKT01-N", classroom_name="Ngành Kế toán-2024-1", academic_year="2024-2029", department_id="D002"),
        Classroom(id="D22CQVT01-N", classroom_name="Ngành Kỹ thuật điện tử viễn thông-2022-1", academic_year="2022-2027", department_id="D003")
    ]

    for class_room in lst_class:
        existing_class = Classroom.query.filter_by(id=class_room.id).first()
        if not existing_class:
            db.session.add(class_room)
            db.session.commit()

