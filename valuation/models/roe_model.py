from .valuation_model import ValuationModel
from ..data_extractor import *
from scraper.yahoo_scraper import YahooScraper
from ..config import *
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
        self.logger.debug("Running ROE model algorithm on company [%d]", self.company_id)
        avg_roe = self.__calculate_avg_historical_roe(self.return_on_equity, self.years_back)
        sustainable_growth_rate = avg_roe * (1-self.payout_ratio)
        conservative_growth_rate = sustainable_growth_rate * (1 - MARGIN_OF_SAFETY)
        equity_per_share = self.shareholders_equity / self.shares_outstanding
        future_shareholders_equity = \
            self.__project_shareholders_equity_to_future(equity_per_share,
                                                         conservative_growth_rate,
                                                         self.years_to_project)
        dividend = self.current_price * self.dividend_yield
        # Returns an array of dividends values over the years
        future_dividend_values = self.__project_dividend_to_future(dividend,
                                                                   conservative_growth_rate,
                                                                   self.years_to_project)
        # Returns array of NPV of the above values
        npv_dividend_values = self.__calculate_npv_dividend(future_dividend_values, self.years_to_project)
        last_year_net_income = future_shareholders_equity * avg_roe
        required_value = last_year_net_income / DISCOUNT_RATE
        npv_required_value = required_value / pow(1+DISCOUNT_RATE, self.years_to_project)
        sum_npv_dividends = sum(npv_dividend_values)
        intrinsic_value = npv_required_value + sum_npv_dividends
        self.logger.debug("ROE model algorithm on company [%d] result=%f",
                          self.company_id, intrinsic_value)
        self.save_run_details_to_db()

    def __calculate_avg_historical_roe(self, return_on_equity, years_back):
        sum_roe = 0
        for year in range(years_back):
            sum_roe += return_on_equity[year].value
        return sum_roe/years_back

    def __project_shareholders_equity_to_future(self, current_equity,
                                                conservative_growth_rate, years_ahead):
        equity_growth = current_equity
        for year in range(1, years_ahead+1):
            equity_growth *= (1+conservative_growth_rate)
        return equity_growth

    def __project_dividend_to_future(self, current_dividend,
                                     conservative_growth_rate, years_to_project):
        dividend_in_future_years = []
        dividend_growth = current_dividend
        for year in range(1, years_to_project+1):
            dividend_growth *= (1+conservative_growth_rate)
            dividend_in_future_years.append(dividend_growth)
        return dividend_in_future_years

    def __calculate_npv_dividend(self, future_dividend_values, years_to_project):
        npv_dividend_in_future_years = []
        for year in range(1, years_to_project+1):
            npv_dividend = future_dividend_values[year-1] / pow(1+DISCOUNT_RATE, year-1)
            npv_dividend_in_future_years.append(npv_dividend)
        return npv_dividend_in_future_years

    def save_run_details_to_db(self, *args):
        pass