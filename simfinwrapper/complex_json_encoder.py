import json

class ComplexEncoder(json.JSONEncoder):
    def default(self, object):
        if hasattr(object,'to_json'):
            return object.to_json()
        else:
            return json.JSONEncoder.default(self, object)