from .valuation_model import ValuationModel
from ..data_extractor import *

class PEModel(ValuationModel):

    def __init__(self, simfin_id ,years_back = 5):
        super().__init__(simfin_id)
        self.earnings_per_share = []
        self.price_per_share = []
        self.expected_growth_rate = 1
        self.years_back = years_back
        self.prepare_model_input(self.company_id, self.years_back)

    def prepare_model_input(self, company_id, years_back):
        company = get_company_from_db(company_id)
        company_prices = get_company_prices_from_db(company_id)
        self.earnings_per_share = self.__get_earnings_per_share(company, years_back)
        self.price_per_share = self.__get_price_per_share(company_prices, years_back)
        self.expected_growth_rate = self.__get_expected_growth_rate()

    def __get_earnings_per_share(self, company_details, years_back):
        pass

    def __get_price_per_share(self, company_prices, years_back):
        pass

    def __get_expected_growth_rate(self):
        pass

    def run(self):
        print("Hello")