from . import *
import logging

class MongoDB:

    def __init__(self):
        self.logger = logging.getLogger('app.db')

    def save_companies(self, companies):
        for company in companies:
            company.save()
        self.logger.debug("Companies saved to the DB")

    def save_company_prices(self, company_prices):
        company_prices.save()
        self.logger.debug("Company share prices saved to the DB")

