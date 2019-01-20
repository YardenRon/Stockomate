from mongoengine import *
from .share_price import SharePrice

class CompanyPrices(Document):

    simfinId = IntField()
    prices = ListField(EmbeddedDocumentField(SharePrice))
    last_updated = DateTimeField()