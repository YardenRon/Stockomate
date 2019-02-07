from financialapi import FinancialApi, DATA_TO_RETRIEVE as METRICS
from dal import *
from utils.formatter import Formatter
from valuation import *
from .config import *
from .runs_viewer import *
import time
import logging

# TODO: This file needs refactor!

db = MongoDB()
api = FinancialApi()
formatter = Formatter()
logger = logging.getLogger('app.cli')

PREDEFINED_COMPANIES_IDS = [111052, 61595, 83548, 59265]
PREDEFINED_COMPANIES_NAMES = []

def update_companies_details_and_metrics():
    logger.debug("Updating all companies details and metrics")

    start_time = time.time()
    companies_details = api.get_companies_details()
    id_to_ticker = formatter.convert_companies_details_to_dict(companies_details)
    companies = api.get_companies_valuation_metrics(METRICS)
    for company in companies:
        company.ticker = id_to_ticker[company.simfinId]
    db.save_companies(companies)

    logger.debug("Finished updating all companies details and metrics (in %s seconds)"
                 % (time.time() - start_time))

def update_companies_prices():
    print("Please choose one of the following options:")
    print("id1, id2, id3... - write the companies ids in one line, comma separated")
    print("* - Take predefined companies ids from a config file")
    print("# - Return to the main menu")

    user_input = input()

    if user_input == '#':
        return
    if user_input == '*':
        companies_ids = PREDEFINED_COMPANIES_IDS
    else:
        companies_ids = __parse_ids_string(user_input)

    if not companies_ids:
        print("No valid ids were found")
    else:
        companies_ids_string = ','.join(map(str,companies_ids))
        logger.debug("Updating prices of the companies with the following ids = [%s]",
                     companies_ids_string)
        start_time = time.time()

        for company_id in companies_ids:
            company_prices = api.get_company_share_prices(company_id)
            db.save_company_prices(company_prices)

        logger.debug("Finished updating companies prices (in %s seconds)"
                     % (time.time() - start_time))

def run_pe_model():
    print("Please choose one of the following options:")
    print("id1, id2, id3... - write the companies ids in one line, comma separated")
    print("* - Take predefined companies ids from a config file")
    print("# - Return to the main menu")

    user_input = input()

    if user_input == '#':
        return
    if user_input == '*':
        companies_ids = PREDEFINED_COMPANIES_IDS
    else:
        companies_ids = __parse_ids_string(user_input)

    if not companies_ids:
        print("No valid ids were found")
    else:
        companies_ids_string = ','.join(map(str, companies_ids))
        logger.debug("Running P/E model for the companies with the following ids = [%s]",
                     companies_ids_string)
        start_time = time.time()

        for company_id in companies_ids:
            model = PEModel(company_id)
            model.run()

        logger.debug("Finished running P/E model on companies (in %s seconds)"
                     % (time.time() - start_time))

def run_dcf_model():
    print("Please choose one of the following options:")
    print("id1, id2, id3... - write the companies ids in one line, comma separated")
    print("* - Take predefined companies ids from a config file")
    print("# - Return to the main menu")

    user_input = input()

    if user_input == '#':
        return
    if user_input == '*':
        companies_ids = PREDEFINED_COMPANIES_IDS
    else:
        companies_ids = __parse_ids_string(user_input)

    if not companies_ids:
        print("No valid ids were found")
    else:
        companies_ids_string = ','.join(map(str, companies_ids))
        logger.debug("Running DCF model for the companies with the following ids = [%s]",
                     companies_ids_string)
        start_time = time.time()

        for company_id in companies_ids:
            model = DCFModel(company_id)
            model.run()

        logger.debug("Finished running DCF model on companies (in %s seconds)"
                     % (time.time() - start_time))

def get_last_runs_details():
    runs_details = db.get_last_runs_details()
    print_table(runs_details)

def get_runs_details_order_by_yield():
    runs_details = db.get_all_runs_details_ordered_by_yield()
    print_table(runs_details)

def get_runs_details_by_company():
    print("Please write the company id you wish to view:")
    user_input = input()

    if not user_input.strip().isdigit():
        print("The id is not valid")
    else:
        company_id = int(user_input)
        runs_details = db.get_company_runs_details(company_id)
        print_table(runs_details)

def __parse_ids_string(string):
    return [int(_id) for _id in string.split(',') if _id.strip().isdigit()]