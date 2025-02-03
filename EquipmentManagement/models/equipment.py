from .database import db

class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = db.Column(db.String(10), primary_key=True)
    equipment_name = db.Column(db.String(50), nullable=True)
    equipment_type = db.Column(db.Integer, nullable=True)
    equipment_status = db.Column(db.Integer, nullable=True)
    room_id = db.Column(db.String(5), db.ForeignKey('room.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    room = db.relationship('Room', backref=db.backref('equipments', lazy=True))
    account = db.relationship('Account', backref=db.backref('students', lazy=True))