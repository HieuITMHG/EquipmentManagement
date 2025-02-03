from .database import db

class PenaltyTicket(db.Model):
    __tablename__ = 'penalty_ticket'

    id = db.Column(db.String(10), primary_key=True)
    date = db.Column(db.Date, nullable=False)
    staff_id = db.Column(db.String(10), db.ForeignKey('staff.id'), nullable=False)
    student_id = db.Column(db.String(10), db.ForeignKey('student.id'), nullable=False)
    