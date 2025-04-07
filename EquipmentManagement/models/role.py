class Role:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.role = kwargs.get('role')

    def to_dict(self):
        return self.__dict__
