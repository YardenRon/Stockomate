from financialapi import FinancialApi, DATA_TO_RETRIEVE as METRICS
from dal import *
from utils.formatter import Formatter
from valuation import *
from utils import ApiError, MissingDataError
from .config import *
from .runs_viewer import *
import time
import logging

# TODO: This file needs refactor!

db = MongoDB()
api = FinancialApi()
formatter = Formatter()
logger = logging.getLogger('app.cli')

# PREDEFINED_COMPANIES_IDS = [111052, 61595, 83548, 59265]
PREDEFINED_COMPANIES_IDS = [378251, 418866, 378250, 815280, 747270, 378249, 694556, 440174, 449291, 124467, 378126, 364942, 823071, 121214, 396684, 378246, 378115, 378245, 641925, 449272, 378242, 564422, 816791, 449267, 198669, 449242, 449237, 332221, 109798, 239962, 344928, 378239, 700084, 651519, 104227, 670940, 449193, 117829, 58953, 217619, 378244, 250582, 745218, 171401, 45730, 664525, 287827, 795980, 202955, 816789, 647182, 372279, 687925, 98663, 660011, 257807, 795507, 734429, 378247, 651859, 781832, 663216, 662912, 247530, 470616, 156298, 721031, 116466, 57524, 90931, 543789, 820561, 659717, 65297, 739365, 359889, 351692, 687927, 449233, 449230, 92543, 543710, 667687, 378243, 721686, 596565, 618274, 97546, 102395, 625612, 646168, 745556, 449198, 90839, 749233, 662182, 651626, 705167, 186213, 116367]
# BAD_COMPANIES_IDS = [171401, 45730, 664525, 287827, 795980, 202955, 816789, 647182, 372279, 687925, 98663, 660011, 257807, 795507, 734429, 378247, 651859, 781832, 663216, 662912, 247530, 470616, 156298, 721031, 116466, 57524, 90931, 543789, 820561, 659717, 65297, 739365, 359889, 351692, 687927, 449233, 449230, 92543, 543710, 667687, 378243, 721686, 596565, 618274, 97546, 102395, 625612, 646168, 745556, 449198, 90839, 749233, 662182, 651626, 705167, 186213, 116367]
PREDEFINED_COMPANIES_NAMES = []

def update_companies_details_and_metrics():
    logger.debug("Updating all companies details and metrics")

    start_time = time.time()
    companies_details = api.get_companies_details()
    id_to_ticker = formatter.convert_companies_details_to_dict(companies_details)
    companies = api.get_companies_valuation_metrics(METRICS)
    for company in companies:
        # TODO: Temporary fix - needs to be changed (if statement should be gone)
        if company.simfinId != 653916:
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
            try:
                company_prices = api.get_company_share_prices(company_id)
                db.save_company_prices(company_prices)
            except ApiError:
                # If there was an API error - we skip retrieving this company prices
                continue

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
            try:
                model = PEModel(company_id)
                model.run()
            except MissingDataError:
                # If a data was missing - we skip retrieving this company prices
                print("MissingDataError")
            except CompanyPrices.DoesNotExist:
                print("DoesNotExist")

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
            try:
                model = DCFModel(company_id)
                model.run()
            except MissingDataError:
                # If a price was missing - we skip retrieving this company prices
                print("MissingDataError")
            except CompanyPrices.DoesNotExist:
                print("DoesNotExist")

        logger.debug("Finished running DCF model on companies (in %s seconds)"
                     % (time.time() - start_time))

def run_roe_model():
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
        logger.debug("Running ROE model for the companies with the following ids = [%s]",
                     companies_ids_string)
        start_time = time.time()

        for company_id in companies_ids:
            try:
                model = ROEModel(company_id)
                model.run()
            except MissingDataError:
                # If a price was missing - we skip retrieving this company prices
                print("MissingDataError")
            except CompanyPrices.DoesNotExist:
                print("DoesNotExist")

        logger.debug("Finished running ROE model on companies (in %s seconds)"
                     % (time.time() - start_time))

def get_last_runs_details():
    runs_details = db.get_last_runs_details()
    print_default_table(runs_details)

def get_runs_details_order_by_yield():
    runs_details = db.get_all_runs_details_ordered_by_yield()
    print_default_table(runs_details)

def get_runs_details_by_company():
    print("Please write the company id you wish to view:")
    user_input = input()

    if not user_input.strip().isdigit():
        print("The id is not valid")
    else:
        company_id = int(user_input)
        runs_details = db.get_company_runs_details(company_id)
        print_default_table(runs_details)

def get_avg_yield_grouped_by_company():
    runs_details = db.get_runs_details_ordered_by_avg_yield()
    print_avg_yield_table(runs_details)

def __parse_ids_string(string):
    return [int(_id) for _id in string.split(',') if _id.strip().isdigit()]