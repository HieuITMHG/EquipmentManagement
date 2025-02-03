from .database import db

class Account(db.Model):
    __tablename__ = 'account'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    role = db.relationship('Role', backref=db.backref('accounts', lazy=True))
