import json

class MetaData:

    def __init__(self, id, value, operator):
        print("MetaData constructor")
        self.id = id
        self.value = value
        self.operator = operator

    def to_json(self):
        return dict(id = self.id, value = self.value, operator = self.operator)