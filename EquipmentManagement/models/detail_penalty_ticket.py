from .database import db

class DetailPenaltyTicket(db.Model):
    __tablename__ = 'detail_penalty_ticket'

    penalty_ticket_id = db.Column(db.String(10), db.ForeignKey('penalty_ticket.id'), primary_key=True)
    violation_id = db.Column(db.String(10), db.ForeignKey('violation.id'), primary_key=True)