from .valuation_model import ValuationModel
from ..data_extractor import *
from scraper.yahoo_scraper import YahooScraper
import datetime

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
        self.price_per_share = self.__get_price_per_share(company_prices,
                                                          company.last_updated,
                                                          years_back)
        self.expected_growth_rate = self.__get_expected_growth_rate(company.ticker)

    def __get_earnings_per_share(self, company_details, years_back):
        periods = self.__create_periods_array(years_back)
        return list(filter(lambda metric: metric.name == "Earnings per Share, Basic" and
                                          metric.period in periods, company_details.metrics_values))

    def __create_periods_array(self, years_back):
        periods = ["TTM"]
        for year in range(1, years_back):
            periods.append("TTM-%d" % year)
        return periods

    def __get_price_per_share(self, company_prices, company_last_updated, years_back):
        last_years_dates = self.__get_last_years_dates(company_last_updated, years_back)
        return list(filter(lambda price_and_date: price_and_date.date in last_years_dates,
                           company_prices.prices))

    def __get_last_years_dates(self, current_date, years_back):
        cleared_current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        cleared_current_date = self.__change_weekend_to_middle_of_week(cleared_current_date)
        last_years_dates = [cleared_current_date]

        for year in range(1, years_back):
            years_ago_date = cleared_current_date - datetime.timedelta(days=year*365)
            years_ago_date = self.__change_weekend_to_middle_of_week(years_ago_date)
            last_years_dates.append(years_ago_date)

        return last_years_dates

    def __change_weekend_to_middle_of_week(self, date):
        is_sunday_or_saturday = date.weekday() == 5 or date.weekday() == 6
        if is_sunday_or_saturday:
            date = date + datetime.timedelta(days=3)
        return date


    def __get_expected_growth_rate(self, ticker):
        scraper = YahooScraper()
        return scraper.get_company_expected_growth_rate(ticker)

    def run(self):
        print("Hello")