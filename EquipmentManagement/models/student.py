from .database import db

class Student(db.Model):
    __tablename__ = 'student'
    
    id = db.Column(db.String(10), primary_key=True)
    lastname = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Boolean, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    is_studying = db.Column(db.Boolean, default=False)
    classroom_id = db.Column(db.String(20), db.ForeignKey('classroom.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), unique=True)

    classroom = db.relationship('Classroom', backref=db.backref('students', lazy=True))
    account = db.relationship('Account', back_populates='student', uselist=False)