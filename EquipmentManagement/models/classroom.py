class Classroom:
    def __init__(self, **kwargs):
        self.id = kwargs['id'] if 'id' in kwargs else None
        self.classroom_name = kwargs['classroom_name'] if 'classroom_name' in kwargs else None
        self.academic_year = kwargs['academic_year'] if 'academic_year' in kwargs else None
        self.department_id = kwargs['department_id'] if 'department_id' in kwargs else None

    def to_dict(self):
        return self.__dict__