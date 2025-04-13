import datetime

class LiquidationSlip:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.liquidation_date = self._parse_datetime(kwargs.get('liquidation_date'))
        self.staff_id = kwargs.get('staff_id')

    def _parse_datetime(self, value):
        if isinstance(value, str):
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return value

    def to_dict(self):
        return self.__dict__