class Person:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.cccd = kwargs.get('cccd')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.gender = kwargs.get('gender')
        self.email = kwargs.get('email')
        self.phone = kwargs.get('phone')
        self.address = kwargs.get('address')
        self.img_url = kwargs.get('img_url')
        self.account_id = kwargs.get('account_id')

    def to_dict(self):
        return self.__dict__