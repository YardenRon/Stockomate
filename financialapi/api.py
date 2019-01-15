import json
from . import simfin, SearchObject, MetaData, INDICATORS_TO_IDS as INDICATORS

class FinancialApi:

    def __init__(self):
        print("constructor")

    def get_valuation_metrics(self, metrics):
        search_objects = self.__create_search_objects(metrics)
        response = simfin.find(search_objects)
        return self.__decode_json_results(response.results)

    def __create_search_objects(self, metrics):
        search_objects = []

        for metric in metrics:
            indicator = INDICATORS[metric["indicator"]]
            meta = MetaData(metric["period"])
            search_object = SearchObject(indicator, meta)
            search_objects.append(search_object)

        return search_objects

    def __decode_json_results(self, results_json):
        test = json.loads(results_json)
        print("hello")
