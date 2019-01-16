from mongoengine import *
from .metric import Metric

class MetricValue(EmbeddedDocument):

    metric = ReferenceField(Metric)
    value = FloatField()