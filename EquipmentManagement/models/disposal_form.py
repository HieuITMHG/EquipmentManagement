from .database import db

class DisposalForm(db.Model):
    __tablename__ = 'disposal_form'

    id = db.Column(db.String(10), primary_key=True)
    liquidation_date = db.Column(db.Date, nullable=False)
    staff_id = db.Column(db.String(10), db.ForeignKey('staff.id'), nullable=False)

    staff = db.relationship('Staff')
