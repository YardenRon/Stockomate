from .valuation_model import ValuationModel
from ..data_extractor import *
from dal import ModelInput, Run
from scraper.yahoo_scraper import YahooScraper
from ..config import *
import datetime
import logging

class PEModel(ValuationModel):

    def __init__(self, simfin_id ,years_back = 5):
        super().__init__(simfin_id)
        self.logger = logging.getLogger('app.pe')
        self.company_name = ""
        self.earnings_per_share = []
        self.price_per_share = []
        self.expected_growth_rate = 1
        self.years_back = years_back
        self.prepare_model_input(self.company_id, self.years_back)

    def prepare_model_input(self, company_id, years_back):
        self.logger.debug("Preparing P/E model inputs for company [%d]", self.company_id)
        company = get_company_from_db(company_id)
        company_prices = get_company_prices_from_db(company_id)
        self.company_name = company.name
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
        cleared_current_date = self.__change_weekend_to_middle_of_week(cleared_current_date, -3)
        last_years_dates = [cleared_current_date]

        for year in range(1, years_back):
            years_ago_date = cleared_current_date - datetime.timedelta(days=year*365)
            years_ago_date = self.__change_weekend_to_middle_of_week(years_ago_date, 3)
            last_years_dates.append(years_ago_date)

        return last_years_dates

    def __change_weekend_to_middle_of_week(self, date, days_delta):
        is_sunday_or_saturday = date.weekday() == 5 or date.weekday() == 6
        if is_sunday_or_saturday:
            date = date + datetime.timedelta(days=days_delta)
        return date


    def __get_expected_growth_rate(self, ticker):
        scraper = YahooScraper()
        return scraper.get_company_expected_growth_rate(ticker)

    def run(self):
        self.logger.debug("Running P/E model algorithm on company [%d]", self.company_id)
        avg_pe = self.__calculate_avg_historical_pe(self.price_per_share,
                                                    self.earnings_per_share,
                                                    self.years_back)
        eps_ttm = self.earnings_per_share[0].value
        conservative_growth_rate = self.expected_growth_rate * (1-MARGIN_OF_SAFETY)
        future_eps = self.__project_eps_to_future(eps_ttm, conservative_growth_rate, self.years_back)
        # The price of the company x-years from now
        target_price = future_eps * avg_pe
        # Net Present Value - how much the company worth TODAY
        npv = target_price / pow(1+DISCOUNT_RATE, self.years_back)
        self.logger.debug("P/E model algorithm on company [%d] result=%f", self.company_id, npv)
        self.save_run_details_to_db(self.company_id, self.company_name, npv,
                                    self.price_per_share[0].price, avg_pe, eps_ttm,
                                    self.expected_growth_rate, MARGIN_OF_SAFETY,
                                    DISCOUNT_RATE, GROWTH_DECLINE_RATE, self.years_back)
        return npv

    def __calculate_avg_historical_pe(self, price_per_share, earnings_per_share, years_back):
        sum_pe = 0
        for year in range(years_back):
            sum_pe += price_per_share[year].price / earnings_per_share[year].value
        return sum_pe/years_back

    def __project_eps_to_future(self, eps_ttm, conservative_growth_rate, years_ahead):
        eps_growth = eps_ttm
        for year in range(1, years_ahead+1):
            declined_conservative_growth_rate = \
                conservative_growth_rate* pow(1-GROWTH_DECLINE_RATE, year-1)
            eps_growth *= (1+declined_conservative_growth_rate)
        return eps_growth

    # TODO: Refactor functions with a lot of arguments

    def save_run_details_to_db(self, company_id, company_name, result, current_price,
                               avg_pe, eps_ttm, egr, mos, dr, gdr, years_back):
        model_inputs = self.__create_inputs_object(avg_pe, eps_ttm, egr, mos, dr, gdr, years_back)
        run_details = self.__create_run_details_object(company_id, company_name,
                                                       model_inputs, result, current_price)
        db.save_run_details(run_details)

    def __create_run_details_object(self, company_id, company_name, inputs, result, current_price):
        run = Run(company_id=company_id, company_name=company_name, inputs=inputs,
                  model_result=round(result,2), current_price=round(current_price,2))
        run.model = "P/E model"
        run.possible_yield = round((result-current_price)/current_price*100,2)
        run.timestamp = datetime.datetime.now()
        return run

    def __create_inputs_object(self, avg_pe, eps_ttm, egr, mos, dr, gdr, years_back):
        inputs = [
            ModelInput(name="Avg Historical P/E - %s years back" % years_back, value=round(avg_pe,2)),
            ModelInput(name="Earnings per Share - TTM", value=round(eps_ttm,2)),
            ModelInput(name="Expected Growth Rate - Next 5 years", value=round(egr,2)),
            ModelInput(name="Growth Decline Rate", value=round(gdr,2)),
            ModelInput(name="Margin of Safety", value=round(mos,2)),
            ModelInput(name="Discount Rate", value=round(dr,2)),
        ]
        return inputs
