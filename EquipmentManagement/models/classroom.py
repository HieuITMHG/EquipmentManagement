from .database import db

class Classroom(db.Model):
    __tablename__ = 'classroom'
    
    id = db.Column(db.String(20), primary_key=True, nullable=False)
    classroom_name = db.Column(db.String(50), nullable=False)
    academic_year = db.Column(db.String(9), nullable=False)
    department_id = db.Column(db.String(10), db.ForeignKey('department.id'), nullable=False)

    department = db.relationship('Department', backref=db.backref('classrooms', lazy=True))