import os
import requests
from .config import SIMFIN_API_KEY

# SIMFIN_API_KEY = os.environ.get('SIMFIN_API_KEY', None)

# class APIKeyMissingError(Exception):
#     pass
#
# if SIMFIN_API_KEY is None:
#     raise APIKeyMissingError(
#         "All methods require an API key. See "
#         "https://simfin.com/data/access/api "
#         "for how to retrieve an authentication token from SimFin"
#     )

session = requests.Session()
session.params = {}
session.params['api-key'] = SIMFIN_API_KEY

from .simfin import SimFin
from .search_object import SearchObject
from .condition import Condition
from .meta_data import MetaData
from .config import INDICATORS_TO_IDS
