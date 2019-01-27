from . import *

db = MongoDB()

def get_company_from_db(id):
    return db.get_company(id)

def get_company_prices_from_db(id):
    return db.get_company_prices(id)