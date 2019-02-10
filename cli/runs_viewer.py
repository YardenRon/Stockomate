import asciitable
import sys

default_table_columns = ["Company ID", "Company Name", "Model","Model Result ($)",
                 "Company Current Price ($)", "Possible Yield (%)", "Timestamp"]

avg_yield_table_columns = ["Company ID", "Company Name", "Avg Possible Yield (%)"]

def print_default_table(runs_details):
    data = []
    for run in runs_details:
        data.append([
            run.company_id,
            run.company_name,
            run.model,
            run.model_result,
            run.current_price,
            run.possible_yield,
            run.timestamp.strftime("%d/%m/%Y %H:%M:%S")
        ])
    asciitable.write(data, sys.stdout, names=default_table_columns,
                     Writer=asciitable.FixedWidthTwoLine,
                     delimiter_pad=' ', bookend=True, delimiter='|')

def print_avg_yield_table(runs_details):
    data = []
    for run in runs_details:
        data.append([
            run['_id']['company_id'],
            run['_id']['company_name'],
            run['avg_yield']
        ])
    asciitable.write(data, sys.stdout, names=avg_yield_table_columns,
                     Writer=asciitable.FixedWidthTwoLine,
                     delimiter_pad=' ', bookend=True, delimiter='|')