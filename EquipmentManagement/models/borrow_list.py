from .database import db

class BorrowingList(db.Model):
    __tablename__ = 'borrowing_list'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    borrowing_time = db.Column(db.DateTime, nullable=False)
    returning_time = db.Column(db.DateTime, nullable=False)

    student_id = db.Column(db.String(10), db.ForeignKey('student.id'), nullable=False)
    room_id = db.Column(db.String(5), db.ForeignKey('room.id'), nullable=False)
    staff_id = db.Column(db.String(10), db.ForeignKey('staff.id'))
