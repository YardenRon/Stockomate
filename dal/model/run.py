from mongoengine import *
from .company import Company
from .metric import Metric

class Run(Document):

    id = StringField(required=True)
    company = ReferenceField(Company)
    metrics_values = ListField(EmbeddedDocumentField(Metric))
    timestamp = DateTimeField()