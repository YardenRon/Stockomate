import requests

from .config import SIMFIN_API_KEY

session = requests.Session()
session.params = {
    "api-key": SIMFIN_API_KEY
}

from .simfin import SimFin
from simfinwrapper.model.search_object import SearchObject
from simfinwrapper.model.condition import Condition
from simfinwrapper.model.meta_data import MetaData
from .config import INDICATORS_TO_IDS
