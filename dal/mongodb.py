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

    def save_run_details(self, run):
        run.save()
        self.logger.debug("Run details saved to the DB")

    def get_company(self, simfin_id):
        return Company.objects.get(simfinId = simfin_id)

    def get_company_prices(self, simfin_id):
        return CompanyPrices.objects.get(simfinId = simfin_id)