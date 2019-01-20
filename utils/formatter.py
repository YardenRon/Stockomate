from . import *
import copy

class Formatter:

    def convert_to_companies_objects(self, request_results, requested_data):
        companies = []
        metrics = self.__create_metrics_objects_without_value(requested_data)
        for result in request_results:
            self.__add_values_to_metrics(requested_data, metrics, result)
            company = self.__create_company_object(result['simId'], result['name'], metrics)
            companies.append(company)

        return companies

    def __create_metrics_objects_without_value(self, requested_data):
        metrics = []
        for index in range(len(requested_data)):
            metric = Metric(name=requested_data[index]["indicator"], period=requested_data[index]["period"])
            metrics.append(metric)
        return metrics

    def __create_company_object(self, simfin_id, name, metrics_values):
        company = Company(simfinId=simfin_id, name=name)
        company.metrics_values = copy.deepcopy(metrics_values)
        company.last_updated = datetime.datetime.now()
        return company

    def __add_values_to_metrics(self, requested_data, metrics, company_result):
        for index in range(len(requested_data)):
            metric = metrics[index]
            value = company_result['values'][index]['value']
            metric.value = value

    def convert_to_company_prices_object(self, request_results, requested_id):
        company_prices = CompanyPrices(simfinId=requested_id)

        prices = []
        for result in request_results:
            converted_datetime = datetime.datetime.strptime(result['date'], '%Y-%m-%d')
            share_price = SharePrice(date=converted_datetime, price=result['closeAdj'])
            prices.append(share_price)

        company_prices.prices = prices

        company_prices.last_updated = datetime.datetime.now()
        return company_prices