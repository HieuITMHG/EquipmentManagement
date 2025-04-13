class Department:
    def __init__(self, **kwargs):
        self.id = kwargs['id'] if 'id' in kwargs else None
        self.department_name = kwargs['department_name'] if 'department_name' in kwargs else None

    def to_dict(self):
        return self.__dict__