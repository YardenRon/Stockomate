class Condition:

    def __init__(self, operator, value):
        print("Condition constructor")
        self.operator = operator
        self.value = value

    def to_json(self):
        return dict(operator = self.operator, value = self.value)