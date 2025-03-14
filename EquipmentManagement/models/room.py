class Room:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.floor = kwargs.get('floor')
        self.section = kwargs.get('section')
        self.max_people = kwargs.get('max_people')

    def to_dict(self):
        return self.__dict__