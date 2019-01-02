from . import session

class SimFin:

    def __init__(self):
        print("SimFin constructor")

    def get_companies_details(self):
        print("Before Http request...")
        path = 'https://simfin.com/api/v1/info/all-entities' #TODO: get from config file
        response = session.get(path)
        print("After Http request...")
        return response.json()
