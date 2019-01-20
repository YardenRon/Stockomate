from mongoengine import *

class SharePrice(EmbeddedDocument):

    date = DateTimeField()
    price = FloatField()