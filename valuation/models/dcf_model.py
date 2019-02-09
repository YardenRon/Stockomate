from .valuation_model import ValuationModel
from ..data_extractor import *
from scraper.yahoo_scraper import YahooScraper
from ..config import *
import datetime
import logging

class DCFModel(ValuationModel):

    def __init__(self, simfin_id, years_to_project = 10):
        super().__init__(simfin_id)
        self.logger = logging.getLogger('app.dcf')
        self.company_name = ""
        self.current_price = 1
        self.free_cash_flow = 1
        self.cash_and_cash_equivalents = 1
        self.long_term_debt = 1
        self.expected_growth_rate = 1
        self.shares_outstanding = 1
        self.years_to_project = years_to_project
        self.prepare_model_input(self.company_id)

    def prepare_model_input(self, company_id):
        self.logger.debug("Preparing DCF model inputs for company [%d]", self.company_id)
        company = get_company_from_db(company_id)
        company_prices = get_company_prices_from_db(company_id)
        self.company_name = company.name
        self.current_price = company_prices.prices[0].price
        self.free_cash_flow = self.__get_free_cash_flow(company)
        self.cash_and_cash_equivalents = self.__get_cash_and_cash_equivalents(company)
        self.long_term_debt = self.__get_long_term_debt(company)
        self.shares_outstanding = self.__get_shares_outstanding(company)
        self.expected_growth_rate = self.__get_expected_growth_rate(company.ticker)

    # TODO: Refactor duplicated code (unite similar functions)

    def __get_free_cash_flow(self, company_details):
        return list(filter(lambda metric: metric.name == "Free Cash Flow",
                           company_details.metrics_values))[0].value

    def __get_cash_and_cash_equivalents(self, company_details):
        return list(filter(lambda metric: metric.name == "Cash and Cash-equivalents",
                           company_details.metrics_values))[0].value

    def __get_long_term_debt(self, company_details):
        return list(filter(lambda metric: metric.name == "Non-current Debt",
                           company_details.metrics_values))[0].value

    def __get_expected_growth_rate(self, ticker):
        scraper = YahooScraper()
        return scraper.get_company_expected_growth_rate(ticker)

    def __get_shares_outstanding(self, company_details):
        return list(filter(lambda metric: metric.name == "Common Shares Outstanding",
                           company_details.metrics_values))[0].value

    def run(self):
        self.logger.debug("Running DCF model algorithm on company [%d]", self.company_id)
        conservative_growth_rate = self.expected_growth_rate * (1 - MARGIN_OF_SAFETY)
        # Returns an array of FCF values over the years
        future_fcf_values = self.__project_fcf_to_future(self.free_cash_flow,
                                                  conservative_growth_rate,
                                                  self.years_to_project)
        # Returns array of NPV of the above values
        npv_fcf_values = self.__calculate_npv_fcf(future_fcf_values, self.years_to_project)
        total_npv_fcf = sum(npv_fcf_values)
        last_year_multiplied_fcf = npv_fcf_values[self.years_to_project-1] * LAST_YEAR_FCF_MULTIPLIER
        company_value = total_npv_fcf + last_year_multiplied_fcf \
                        + self.cash_and_cash_equivalents - self.long_term_debt
        intrinsic_value = company_value / self.shares_outstanding
        self.logger.debug("DCF model algorithm on company [%d] result=%f",
                          self.company_id, intrinsic_value)
        self.save_run_details_to_db(self.company_id, self.company_name, intrinsic_value,
                                    self.current_price, self.free_cash_flow,
                                    self.cash_and_cash_equivalents, self.long_term_debt,
                                    self.shares_outstanding, self.expected_growth_rate,
                                    MARGIN_OF_SAFETY, DISCOUNT_RATE, GROWTH_DECLINE_RATE,
                                    LAST_YEAR_FCF_MULTIPLIER)
        return intrinsic_value

    # TODO: Think maybe to unite __project_fcf_to_future and __calculate_npv_fcf

    def __project_fcf_to_future(self, free_cash_flow, conservative_growth_rate, years_to_project):
        fcf_in_future_years = []
        fcf_growth = free_cash_flow
        for year in range(1, years_to_project+1):
            declined_conservative_growth_rate = \
                conservative_growth_rate* pow(1-GROWTH_DECLINE_RATE, year-1)
            fcf_growth *= (1+declined_conservative_growth_rate)
            fcf_in_future_years.append(fcf_growth)
        return fcf_in_future_years

    def __calculate_npv_fcf(self, future_fcf_values, years_to_project):
        npv_fcf_in_future_years = []
        for year in range(1, years_to_project+1):
            npv_fcf = future_fcf_values[year-1] / pow(1+DISCOUNT_RATE, year)
            npv_fcf_in_future_years.append(npv_fcf)
        return npv_fcf_in_future_years

    # TODO: Refactor functions with a lot of arguments

    def save_run_details_to_db(self, company_id, company_name, result, current_price, fcf,
                               cce, ltd, shares_num, egr, mos, dr, gdr, last_year_multiplier):
        model_inputs = self.__create_inputs_object(fcf, cce, ltd, shares_num, egr,
                                                   mos, dr, gdr, last_year_multiplier)
        run_details = self.__create_run_details_object(company_id, company_name,
                                                       model_inputs, result, current_price)
        db.save_run_details(run_details)

    def __create_run_details_object(self, company_id, company_name, inputs, result, current_price):
        run = Run(company_id=company_id, company_name=company_name, inputs=inputs,
                  model_result=round(result,2), current_price=round(current_price,2))
        run.model = "DCF model"
        run.possible_yield = round((result-current_price)/current_price*100,2)
        run.timestamp = datetime.datetime.now()
        return run

    def __create_inputs_object(self, fcf, cce, ltd, shares_num, egr,
                               mos, dr, gdr, last_year_multiplier):
        inputs = [
            ModelInput(name="Cash and Cash Equivalents - Last Statement", value=round(cce,2)),
            ModelInput(name="Long Term Debt - Last Statement", value=round(ltd,2)),
            ModelInput(name="Free Cash Flow - Last Statement", value=round(fcf, 2)),
            ModelInput(name="Shares Outstanding - Current", value=round(shares_num, 2)),
            ModelInput(name="Expected Growth Rate - Next 5 years", value=round(egr,2)),
            ModelInput(name="Growth Decline Rate", value=round(gdr,2)),
            ModelInput(name="Margin of Safety", value=round(mos,2)),
            ModelInput(name="Discount Rate", value=round(dr,2)),
            ModelInput(name="Last Year FCF Multiplier", value=round(last_year_multiplier, 2))
        ]
        return inputs
