class BorrowRequest:
    def __init__(self, **kwargs):
        self.id = kwargs['id'] if 'id' in kwargs else None
        self.student_id = kwargs['student_id'] if 'student_id' in kwargs else None
        self.staff_id = kwargs['staff_id'] if 'staff_id' in kwargs else None

    def to_dict(self):
        return self.__dict__