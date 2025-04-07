class RolePrivilege:
    def __init__(self, **kwargs):
        self.privilege_id = kwargs.get('privilege_id')
        self.role_id = kwargs.get('role_id')

    def to_dict(self):
        return self.__dict__