import json
from . import session
from .complex_json_encoder import ComplexEncoder

class SimFin:

    def __init__(self):
        print("SimFin constructor")
        self.base_url = "https://simfin.com/api/v1/" #TODO: Move to config file

    def get_companies_details(self):
        print("Before Http request...")
        url = self.base_url + 'info/all-entities'
        response = session.get(url)
        print("After Http request...")
        return response.json()

    def find(self, search_objects, results_per_page):
        print("Before Http request...")
        url = self.base_url + 'finder'
        data = {}
        data["search"] = search_objects
        data["resultsPerPage"] = results_per_page
        serialized_data = json.dumps(data, cls = ComplexEncoder)
        response = session.post(url, data = serialized_data, headers = {'Content-Type':'application/json'})
        print("After Http request...")
        return response.json()
