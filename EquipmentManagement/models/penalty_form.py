class PenaltyForm:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.form_name = kwargs.get('form_name')
        self.price = kwargs.get('price')

    def to_dict(self):
        return self.__dict__