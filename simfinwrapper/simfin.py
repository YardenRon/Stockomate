import json
from . import session
from .complex_json_encoder import ComplexEncoder
from .api_error import ApiError
from .config import SIMFIN_API

class SimFin:

    def __init__(self):
        self.base_url = SIMFIN_API["base_url"]

    def get_companies_details(self):
        url = self.base_url + SIMFIN_API["companies_details"]
        response = session.get(url)

        if response.status_code != 200:
            raise ApiError(url, response.status_code)

        return response.json()

    def find(self, search_objects, results_per_page = 0):
        url = self.base_url + SIMFIN_API["find"]
        data = {
            "search": search_objects,
            "resultsPerPage": results_per_page
        }
        serialized_data = json.dumps(data, cls = ComplexEncoder)
        response = session.post(url, data = serialized_data, headers = {'Content-Type':'application/json'})

        if response.status_code != 200:
            raise ApiError(url, response.status_code)

        return response.json()
