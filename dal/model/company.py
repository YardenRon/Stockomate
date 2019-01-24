from mongoengine import *
from .metric import Metric

class Company(Document):

    simfinId = IntField(primary_key=True)
    name = StringField(max_length=100)
    ticker = StringField(max_length=50)
    metrics_values = ListField(EmbeddedDocumentField(Metric))
    last_updated = DateTimeField()