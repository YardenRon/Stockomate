import requests
from .config import SIMFIN_API_KEY

session = requests.Session()
session.params = {
    "api-key": SIMFIN_API_KEY
}

from .simfin import SimFin
from .search_object import SearchObject
from .condition import Condition
from .meta_data import MetaData
from .config import INDICATORS_TO_IDS
