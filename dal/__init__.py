from mongoengine import *
from .model.company import Company
from .model.metric import Metric
from .model.run import Run
from .mongodb import MongoDB

connect('stockomate')

__all__ = ["Company", "Metric", "Run", "MongoDB"]
