
from farmer.ext.farmobj import FarmObj


class Plan(FarmObj):
    pass


class CropPlan(Plan):
    pass


class GrazingPlan(Plan):

    @property
    def field_days_bulk_feeding(self) -> int:
        return FarmObj.
