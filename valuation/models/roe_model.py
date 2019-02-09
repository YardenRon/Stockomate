from .valuation_model import ValuationModel
from ..data_extractor import *
from scraper.yahoo_scraper import YahooScraper
import logging

class ROEModel(ValuationModel):

    def __init__(self, simfin_id, years_back = 5, years_to_project = 10):
        super().__init__(simfin_id)
        self.logger = logging.getLogger('app.roe')
        self.company_name = ""
        self.shareholders_equity = 1
        self.current_price = 1
        self.return_on_equity = []
        self.shares_outstanding = 1
        self.dividend_yield = 1
        self.payout_ratio = 1
        self.years_back = years_back
        self.years_to_project = years_to_project
        self.prepare_model_input(self.company_id, self.years_back)

    def prepare_model_input(self, company_id, years_back):
        self.logger.debug("Preparing ROE model inputs for company [%d]", self.company_id)
        company = get_company_from_db(company_id)
        company_prices = get_company_prices_from_db(company_id)
        self.company_name = company.name
        self.current_price = company_prices.prices[0].price
        self.shareholders_equity = self.__get_shareholders_equity(company)
        self.return_on_equity = self.__get_return_on_equity(company, years_back)
        self.shares_outstanding = self.__get_shares_outstanding(company)
        dividends_details = self.__get_dividends_details(company.ticker)
        self.dividend_yield = dividends_details["Forward Dividend Yield"]
        self.payout_ratio = dividends_details["Payout Ratio"]

    def __get_shareholders_equity(self, company_details):
        return list(filter(lambda metric: metric.name == "Total Equity",
                           company_details.metrics_values))[0].value

    def __get_return_on_equity(self, company_details, years_back):
        periods = self.__create_periods_array(years_back)
        return list(filter(lambda metric: metric.name == "Return on Equity" and
                                          metric.period in periods, company_details.metrics_values))

    def __create_periods_array(self, years_back):
        periods = ["TTM"]
        for year in range(1, years_back):
            periods.append("TTM-%d" % year)
        return periods

    def __get_shares_outstanding(self, company_details):
        return list(filter(lambda metric: metric.name == "Common Shares Outstanding",
                           company_details.metrics_values))[0].value

    def __get_dividends_details(self, ticker):
        scraper = YahooScraper()
        return scraper.get_company_dividends_details(ticker)

    def run(self):
        pass

    def save_run_details_to_db(self, *args):
        pass