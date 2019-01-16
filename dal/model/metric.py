from mongoengine import *

class Metric(Document):

    name = StringField(max_length=100)
    period = StringField(max_length=100)