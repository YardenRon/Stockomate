import json

import logging
from utils import ApiError, ComplexEncoder
from . import session
from .config import SIMFIN_API

class SimFin:

    def __init__(self):
        self.base_url = SIMFIN_API["base_url"]
        self.logger = logging.getLogger('app.simfin')

    def get_companies_details(self):
        url = self.base_url + SIMFIN_API["companies_details"]
        self.logger.debug("Getting all companies details from SimFin, url=%s", url)
        response = session.get(url)

        if response.status_code != 200:
            raise ApiError(url, response.status_code)

        self.logger.debug("Successfully retrieved all companies details from SimFin, url=%s", url)
        return response.json()

    def find(self, search_objects, results_per_page = 0):
        url = self.base_url + SIMFIN_API["find"]
        self.logger.debug("Getting metrics data from SimFin, url=%s", url)
        data = {
            "search": search_objects,
            "resultsPerPage": results_per_page
        }
        serialized_data = json.dumps(data, cls = ComplexEncoder)
        response = session.post(url, data = serialized_data, headers = {'Content-Type':'application/json'})

        if response.status_code != 200:
            raise ApiError(url, response.status_code)

        self.logger.debug("Successfully retrieved metrics data from SimFin, url=%s", url)

        return response.json()

    def get_company_share_price(self, simfin_id, start_date = None, end_date = None):
        url = self.base_url + SIMFIN_API["share_price"] % simfin_id
        self.__add_param_to_url("start", start_date)
        self.__add_param_to_url("end", end_date)
        self.logger.debug("Getting historical share prices of company [%d] from SimFin, url=%s", simfin_id, url)

        response = session.get(url)

        self.__remove_param_from_url("start")
        self.__remove_param_from_url("end")

        if response.status_code != 200:
            raise ApiError(url, response.status_code)

        self.logger.debug("Successfully retrieved historical share prices of company [%d] from SimFin, url=%s", simfin_id, url)

        return response.json()

    def __add_param_to_url(self, param, value):
        if param is not None:
            session.params[param] = value

    def __remove_param_from_url(self, param):
        if param is not None:
            del session.params[param]

