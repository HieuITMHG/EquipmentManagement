from .database import db

class RepairTicket(db.Model):
    __tablename__ = 'repair_ticket'

    id = db.Column(db.String(10), primary_key=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date)
    staff_id = db.Column(db.String(10), db.ForeignKey('staff.id'), nullable=True)

    staff = db.relationship('Staff', backref=db.backref('repair_tickets', lazy=True))
