from . import *

class MongoDB:

    def save_companies(self, companies):
        for company in companies:
            company.save()

    def save_company_prices(self, company_prices):
        company_prices.save()

