class Equipment:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.equipment_name = kwargs.get('equipment_name')
        self.equipment_type = kwargs.get('equipment_type')
        self.equipment_status = kwargs.get('equipment_status')
        self.room_id = kwargs.get('room_id')
        self.account_id = kwargs.get('account_id')

    def to_dict(self):
        return self.__dict__