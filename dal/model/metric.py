from mongoengine import *

class Metric(EmbeddedDocument):

    name = StringField(max_length=100)
    period = StringField(max_length=100)
    value = FloatField()