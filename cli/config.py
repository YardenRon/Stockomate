from .actions import *

COMMANDS = {
    1: {
        "definition": "Update all companies details and metrics",
        "action": update_companies_details_and_metrics
    },
    2: {
        "definition": "Update specific companies prices",
        "action": update_companies_prices
    },
    3: {
        "definition": "Run P/E model on specific companies",
        "action": run_pe_model
    },
    4: {
        "definition": "Run DCF model on specific companies",
        "action": run_dcf_model
    },
    5: {
        "definition": "Run ROE model on specific companies",
        "action": run_roe_model
    },
    6: {
        "definition": "Show last runs details",
        "action": get_last_runs_details
    },
    7: {
        "definition": "Show runs details ordered by yield",
        "action": get_runs_details_order_by_yield
    },
    8: {
        "definition": "Show runs details of specific company",
        "action": get_runs_details_by_company
    },
    9: {
        "definition": "Show average yield of companies (ordered)",
        "action": get_avg_yield_grouped_by_company
    },
    10: {
        "definition": "Exit"
    }
}

EXIT_COMMAND = list(COMMANDS.keys())[-1]
