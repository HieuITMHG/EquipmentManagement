from .database import db

class DetailRepairTicket(db.Model):
    __tablename__ = 'detail_repair_ticket'

    repair_ticket_id = db.Column(db.String(10), db.ForeignKey('repair_ticket.id'),  primary_key=True)
    equipment_id = db.Column(db.String(10), db.ForeignKey('equipment.id'), primary_key=True)
    price = db.Column(db.Integer)
