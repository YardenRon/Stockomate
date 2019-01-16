from mongoengine import *
from .company import Company
from .metric_value import MetricValue

class Run(Document):

    id = StringField(required=True)
    company = ReferenceField(Company)
    metricsValues = ListField(EmbeddedDocumentField(MetricValue))
    timestamp = DateTimeField()