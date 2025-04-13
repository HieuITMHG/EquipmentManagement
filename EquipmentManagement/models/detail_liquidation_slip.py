class DetailLiquidationSlip:
    def __init__(self, **kwargs):
        self.liquidation_slip_id = kwargs['liquidation_slip_id'] if 'liquidation_slip_id' in kwargs else None
        self.equipment_id = kwargs['equipment_id'] if 'equipment_id' in kwargs else None

    def to_dict(self):
        return self.__dict__