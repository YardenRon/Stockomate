import json
from . import session
from .complex_json_encoder import ComplexEncoder

class SimFin:

    def __init__(self):
        self.base_url = "https://simfin.com/api/v1/" #TODO: Move to config file

    def get_companies_details(self):
        url = self.base_url + 'info/all-entities'
        response = session.get(url)
        return response.json()

    def find(self, search_objects, results_per_page = 0):
        url = self.base_url + 'finder'
        data = {
            "search": search_objects,
            "resultsPerPage": results_per_page
        }
        serialized_data = json.dumps(data, cls = ComplexEncoder)
        response = session.post(url, data = serialized_data, headers = {'Content-Type':'application/json'})
        return response.json()
