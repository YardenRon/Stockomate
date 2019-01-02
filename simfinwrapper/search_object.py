from .meta_data import MetaData

class SearchObject:

    def __init__(self, indicator_id, meta = MetaData("ttm"), condition = None):
        print("Search Object constructor")
        self.indicator_id = indicator_id
        self.meta = meta
        self.condition = condition

    #TODO: Add function according_to_ttm(ttm) where ttm is the number of years back

    def to_json(self):
        return dict(indicatorId = self.indicator_id, meta = self.meta, condition = self.condition)