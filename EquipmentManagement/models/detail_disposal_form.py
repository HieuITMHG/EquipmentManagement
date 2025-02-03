from .database import db

class DetailDisposalForm(db.Model):
    __tablename__ = 'detail_disposal_form'

    disposal_form_id = db.Column(db.String(10), db.ForeignKey('disposal_form.id'), primary_key=True)
    equipment_id = db.Column(db.String(10), db.ForeignKey('equipment.id'), primary_key=True)