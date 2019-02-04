from mongoengine import *
from .model_input import ModelInput

class Run(Document):

    company_id = IntField()
    company_name = StringField(max_length=100)
    model = StringField(max_length=50)
    inputs = ListField(EmbeddedDocumentField(ModelInput))
    model_result = FloatField()
    current_price = FloatField()
    possible_yield = FloatField()
    timestamp = DateTimeField()