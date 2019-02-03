from .actions import *

COMMANDS = {
    1: {
        "message": "Update all companies details and metrics",
        "action": update_companies_details_and_metrics
    },
    2: {
        "message": "Update specific companies prices",
        "action": update_companies_prices
    },
    3: {
        "message": "Run P/E model on specific companies",
        "action": run_pe_model
    },
    4: {
        "message": "Show last runs details",
        "action": get_last_runs_details
    },
    5: {
        "message": "Show runs details ordered by yield",
        "action": get_runs_details_order_by_yield
    },
    6: {
        "message": "Show runs details of specific company",
        "action": get_runs_details_by_company
    },
    7: {
        "message": "Exit"
    }
}

EXIT_COMMAND = 7