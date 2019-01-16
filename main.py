# *** 1 ***

# from simfinwrapper import SimFin, SearchObject, INDICATORS_TO_IDS as INDICATORS

# simfin = SimFin()
# response = simfin.get_companies_details()
# objects = [SearchObject(INDICATORS["Price to Earnings Ratio"])]
# response = simfin.find(objects)

# *** 1 ***

# *** 2 ***

from financialapi import FinancialApi, DATA_TO_RETRIEVE as METRICS
from dal import *
import time

db = MongoDB()
api = FinancialApi()
start_time = time.time()
companies = api.get_companies_valuation_metrics(METRICS)
db.save_companies(companies)
print("--- %s seconds ---" % (time.time() - start_time))
print("hello")

# *** 2 ***

# *** 3 ***

# from dal import *
# from simfinwrapper import INDICATORS_TO_IDS as INDICATORS
# db = MongoDB()
# metrics_names = INDICATORS.keys()
# db.save_metrics(metrics_names)
# print("hello")

# *** 3 ***