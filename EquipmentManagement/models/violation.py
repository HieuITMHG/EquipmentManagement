from .database import db

class Violation(db.Model):
    __tablename__ = 'violation'

    id = db.Column(db.String(10), primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    form = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer)
    