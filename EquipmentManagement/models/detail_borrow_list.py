from .database import db

class DetailBorrowingList(db.Model):
    __tablename__ = 'detail_borrowing_list'

    borrow_list_id = db.Column(db.Integer, db.ForeignKey('borrowing_list.id'), primary_key=True)
    equipment_id = db.Column(db.String(10), db.ForeignKey('equipment.id'), primary_key=True)
    actual_returning_time = db.Column(db.DateTime)

    borrow_list = db.relationship('BorrowingList', backref=db.backref('detail_borrowing_lists', lazy=True))
    equipment = db.relationship('Equipment', backref=db.backref('detail_borrowing_lists', lazy=True))
