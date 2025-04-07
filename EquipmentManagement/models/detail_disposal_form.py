class DetailDisposalForm:
    def __init__(self, **kwargs):
        self.disposal_form_id = kwargs['disposal_form_id'] if 'disposal_form_id' in kwargs else None
        self.equipment_id = kwargs['equipment_id'] if 'equipment_id' in kwargs else None

    def to_dict(self):
        return self.__dict__