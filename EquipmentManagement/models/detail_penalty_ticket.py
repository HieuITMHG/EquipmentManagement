class DetailPenaltyTicket:
    def __init__(self, **kwargs):
        self.penalty_ticket_id = kwargs['penalty_ticket_id'] if 'penalty_ticket_id' in kwargs else None
        self.violation_id = kwargs['violation_id'] if 'violation_id' in kwargs else None

    def to_dict(self):
        return self.__dict__