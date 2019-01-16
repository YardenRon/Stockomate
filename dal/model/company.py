from mongoengine import *
from .metric_value import MetricValue

class Company(Document):

    name = StringField(max_length=100)
    ticker = StringField(max_length=50)
    metricsValues = ListField(EmbeddedDocumentField(MetricValue))
    lastUpdated = DateTimeField()