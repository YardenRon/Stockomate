# *** 1 ***

# from simfinwrapper import SimFin, SearchObject, INDICATORS_TO_IDS as INDICATORS

# simfin = SimFin()
# response = simfin.get_companies_details()
# objects = [SearchObject(INDICATORS["Price to Earnings Ratio"])]
# response = simfin.find(objects)

# *** 1 ***

# *** 2 ***

# from financialapi import FinancialApi, DATA_TO_RETRIEVE as METRICS
#
# api = FinancialApi()
# response = api.get_valuation_metrics(METRICS)

# *** 2 ***

from dal import *
from simfinwrapper import INDICATORS_TO_IDS as INDICATORS
db = MongoDB()
metrics_names = INDICATORS.keys()
db.save_metrics(metrics_names)
print("hello")
