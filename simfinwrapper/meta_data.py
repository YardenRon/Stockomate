class MetaData:

    def __init__(self, value, id = 6, operator = "eq"):
        self.id = id
        self.value = value
        self.operator = operator

    def to_json(self):
        return dict(id = self.id, value = self.value, operator = self.operator)