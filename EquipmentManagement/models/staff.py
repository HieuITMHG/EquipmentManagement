from .database import db

class Staff(db.Model):
    __tablename__ = 'staff'
    
    id = db.Column(db.String(10), primary_key=True)
    lastname = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Boolean, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    is_working = db.Column(db.Boolean, default=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    account = db.relationship('Account', backref=db.backref('staffs', lazy=True))