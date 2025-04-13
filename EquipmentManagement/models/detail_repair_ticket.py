class DetailRepairTicket:
    def __init__(self, **kwargs):
        self.repair_ticket_id = kwargs['repair_ticket_id'] if 'repair_ticket_id' in kwargs else None
        self.equipment_id = kwargs['equipment_id'] if 'equipment_id' in kwargs else None
        self.price = kwargs['price'] if 'price' in kwargs else None

    def to_dict(self):
        return self.__dict__