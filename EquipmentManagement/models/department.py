from .database import db

class Department(db.Model):
    __tablename__ = 'department'
    
    id = db.Column(db.String(10), primary_key=True)
    department_name = db.Column(db.String(50), nullable=False, unique=True)

