import datetime

class RepairTicket:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.start_date = self._parse_date(kwargs.get('start_date'))
        self.end_date = self._parse_date(kwargs.get('end_date'))
        self.status = kwargs.get('status')
        self.staff_id = kwargs.get('staff_id')

    def _parse_date(self, value):
        return datetime.strptime(value, '%Y-%m-%d').date() if isinstance(value, str) else value

    def to_dict(self):
        return self.__dict__