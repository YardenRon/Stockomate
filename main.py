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
from utils.formatter import Formatter
import time

db = MongoDB()
api = FinancialApi()
formatter = Formatter()
start_time = time.time()
companies_details = api.get_companies_details()
id_to_ticker = formatter.convert_companies_details_to_dict(companies_details)
companies = api.get_companies_valuation_metrics(METRICS)
for company in companies:
    company.ticker = id_to_ticker[company.simfinId]
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

# *** 4 ***

from financialapi import FinancialApi
from dal import *

# ids = [111052, 61595, 83548, 59265]
# ids = [111052]
#
# db = MongoDB()
# api = FinancialApi()
#
# for id in ids:
#     company_prices = api.get_company_share_prices(id)
#     db.save_company_prices(company_prices)

# *** 4 ***

# *** 5 ***

# from valuation import *
#
# model = PEModel(111052)

# *** 5 ***

