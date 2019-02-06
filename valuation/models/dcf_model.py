from .valuation_model import ValuationModel
from ..data_extractor import *
from scraper.yahoo_scraper import YahooScraper
import datetime
import logging

class DCFModel(ValuationModel):

    def __init__(self, simfin_id ,years_to_project = 10):
        super().__init__(simfin_id)
        self.logger = logging.getLogger('app.dcf')
        self.company_name = ""
        self.expected_growth_rate = 1
        self.years_to_project = years_to_project
        self.prepare_model_input(self.company_id)

    def prepare_model_input(self, company_id):
        self.logger.debug("Preparing DCF model inputs for company [%d]", self.company_id)
        company = get_company_from_db(company_id)
        self.expected_growth_rate = self.__get_expected_growth_rate(company.ticker)

    def __get_expected_growth_rate(self, ticker):
        scraper = YahooScraper()
        return scraper.get_company_expected_growth_rate(ticker)

    def run(self):
        self.logger.debug("Running DCF model algorithm on company [%d]", self.company_id)
        result = 1
        self.logger.debug("DCF model algorithm on company [%d] result=%f", self.company_id, npv)
        self.save_run_details_to_db()
        return result

    # TODO: Refactor functions with a lot of arguments

    def save_run_details_to_db(self):
        model_inputs = self.__create_inputs_object()
        run_details = self.__create_run_details_object()
        db.save_run_details(run_details)

    def __create_run_details_object(self, company_id, company_name, inputs, result, current_price):
        run = Run(company_id=company_id, company_name=company_name, inputs=inputs,
                  model_result=round(result,2), current_price=round(current_price,2))
        run.model = "DCF model"
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
