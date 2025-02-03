from .database import db

class Room(db.Model):
    __tablename__ = 'room'
    
    id = db.Column(db.String(5), primary_key=True)
    floor = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(1), nullable=False)
    max_people = db.Column(db.Integer, nullable=False)