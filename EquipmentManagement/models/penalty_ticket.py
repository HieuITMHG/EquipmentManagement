from datetime import datetime

class PenaltyTicket:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.date = self._parse_date(kwargs.get('date'))
        self.staff_id = kwargs.get('staff_id')
        self.student_id = kwargs.get('student_id')
        self.status = kwargs.get('status')

    def _parse_date(self, value):
        return datetime.strptime(value, '%Y-%m-%d').date() if isinstance(value, str) else value

    def to_dict(self):
        return self.__dict__