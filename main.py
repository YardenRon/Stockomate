from simfinwrapper import SimFin
from simfinwrapper import SearchObject
from simfinwrapper import MetaData

simfin = SimFin()
# response = simfin.get_companies_details()
meta = MetaData(6, "ttm", "eq")
objects = [SearchObject("4-14", meta, None)]
response = simfin.find(objects, 0)