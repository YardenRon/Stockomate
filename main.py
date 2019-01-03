# from simfinwrapper import SimFin, SearchObject, INDICATORS_TO_IDS as INDICATORS

# simfin = SimFin()
# response = simfin.get_companies_details()
# objects = [SearchObject(INDICATORS["Price to Earnings Ratio"])]
# response = simfin.find(objects)

from financialapi import FinancialApi, DATA_TO_RETRIEVE as METRICS

api = FinancialApi()
response = api.get_valuation_metrics(METRICS)
print("hello")
