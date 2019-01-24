from mongoengine import *
from .share_price import SharePrice

class CompanyPrices(Document):

    simfinId = IntField(primary_key=True)
    prices = ListField(EmbeddedDocumentField(SharePrice))
    last_updated = DateTimeField()