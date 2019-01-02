from simfinwrapper import SimFin
from simfinwrapper import SearchObject

simfin = SimFin()
# response = simfin.get_companies_details()
objects = [SearchObject("4-14")]
response = simfin.find(objects)