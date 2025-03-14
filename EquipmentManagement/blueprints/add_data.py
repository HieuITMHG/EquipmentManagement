# from flask import Blueprint, render_template, request

# from models.database import db
# from models.role import Role
# from models.account import Account
# from models.classroom import Classroom
# from models.student import Student
# from models.staff import Staff

# from enums.role_type import RoleID

# add_data_blueprint = Blueprint('add_data', __name__)

# @add_data_blueprint.route('/add_account', methods=['GET', 'POST'])
# def add_data():
#     if request.method == 'POST':
#         role_id = int(request.form['role'])
#         password = request.form['password']
#         user_id = request.form['user_id']

#         firstname = request.form['firstname']
#         lastname = request.form['lastname']
#         phone = request.form['phone']
#         email = request.form['email']
#         address = request.form['address']
#         birthdate = request.form['birthdate']
#         gender = bool(int(request.form['gender']))
#         class_id = request.form['class']

#         new_account = Account(password=password, role_id=role_id)
#         db.session.add(new_account)
#         db.session.commit()



#         if role_id == RoleID.STUDENT.value:
#             new_user = Student(id=user_id, lastname=lastname, firstname=firstname, gender=gender, birthdate=birthdate, address=address,
#                                 phone = phone, email = email, is_studying=True, classroom_id = class_id, account_id=new_account.id)
#         else:
#             new_user = Staff(id=user_id, lastname=lastname, firstname=firstname, gender=gender, birthdate=birthdate, address=address,
#                                 phone = phone, email = email, is_working=True, account_id=new_account.id)
        
#         db.session.add(new_user)
#         db.session.commit()
        
#     lst_role = Role.query.all()
#     lst_class = Classroom.query.all()
#     return render_template('general/add_account.html', lst_role = lst_role, lst_class=lst_class)
