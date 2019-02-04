import asciitable
import sys

table_columns = ["Company ID", "Company Name", "Model","Model Result ($)",
                 "Company Current Price ($)", "Possible Yield (%)", "Timestamp"]

def print_table(runs_details):
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
    asciitable.write(data, sys.stdout, names=table_columns,
                     Writer=asciitable.FixedWidthTwoLine,
                     delimiter_pad=' ', bookend=True, delimiter='|')