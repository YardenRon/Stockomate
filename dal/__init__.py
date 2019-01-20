from mongoengine import *
from .model.company import Company
from .model.metric import Metric
from .model.run import Run
from .model.company_prices import CompanyPrices
from .model.share_price import SharePrice
from .mongodb import MongoDB

connect('stockomate')

__all__ = ["Company", "Metric", "Run", "CompanyPrices", "SharePrice", "MongoDB"]
