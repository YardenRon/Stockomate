class SearchObject:

    def __init__(self, indicator_id, meta, condition):
        print("Search Object constructor")
        self.indicator_id = indicator_id
        self.meta = meta
        self.condition = condition

    def to_json(self):
        return dict(indicatorId = self.indicator_id, meta = self.meta, condition = self.condition)