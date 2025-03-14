class Violation:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.violation_content = kwargs.get('violation_content')

    def to_dict(self):
        return self.__dict__