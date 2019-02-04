from mongoengine import *

class ModelInput(EmbeddedDocument):

    name = StringField(max_length=100)
    value = FloatField()