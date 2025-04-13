class Staff:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.is_working = kwargs.get('is_working', False)

    def to_dict(self):
        return self.__dict__