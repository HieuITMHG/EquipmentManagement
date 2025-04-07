class Student:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.is_studying = kwargs.get('is_studying', False)
        self.classroom_id = kwargs.get('classroom_id')

    def to_dict(self):
        return self.__dict__
