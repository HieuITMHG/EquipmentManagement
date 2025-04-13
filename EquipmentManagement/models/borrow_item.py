from datetime import datetime

class BorrowItems:
    def __init__(self, **kwargs):
        self.borrow_list_id = kwargs['borrow_list_id'] if 'borrow_list_id' in kwargs else None
        self.borrowing_time = kwargs['borrowing_time'] if 'borrowing_time' in kwargs else datetime.now()
        self.equipment_id = kwargs['equipment_id'] if 'equipment_id' in kwargs else None
        self.actual_returning_time = kwargs['actual_returning_time'] if 'actual_returning_time' in kwargs else None

    def to_dict(self):
        return self.__dict__