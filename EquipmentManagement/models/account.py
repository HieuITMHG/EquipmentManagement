from  werkzeug.security import generate_password_hash

from enums.account_status import AccountStatus

class Account():
    def __init__(self, **kwargs):
        self.password = generate_password_hash(kwargs['password']) if 'password' in kwargs.keys() else None
        self.role_id = kwargs['role_id'] if 'role_id' in kwargs.keys() else None
        self.is_active = AccountStatus.ACTIVE.value

    def to_dict(self):
        return self.__dict__

    
