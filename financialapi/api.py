import json
from . import simfin, SearchObject, MetaData, INDICATORS_TO_IDS as INDICATORS
from . import formatter

class FinancialApi:

    def get_company_share_prices(self, simfin_id):
        return simfin.get_company_share_price(simfin_id)

    def get_companies_valuation_metrics(self, metrics):
        search_objects = self.__create_search_objects(metrics)
        response = simfin.find(search_objects)
        return self.__decode_json_results(response['results'], metrics)

    def __create_search_objects(self, metrics):
        search_objects = []

        for metric in metrics:
            indicator = INDICATORS[metric["indicator"]]
            meta = MetaData(metric["period"])
            search_object = SearchObject(indicator, meta)
            search_objects.append(search_object)

        return search_objects

    def __decode_json_results(self, results_json, metrics):
        return formatter.convert_to_companies_objects(results_json, metrics)
