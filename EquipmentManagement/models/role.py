from .database import db

class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)

    