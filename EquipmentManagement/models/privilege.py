class Privilege:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.privilege_name = kwargs.get('privilege_name')

    def to_dict(self):
        return self.__dict__
