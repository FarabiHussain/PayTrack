import os
from datetime import datetime as dt

#
def write_to_record(cwd, invoice_id):
    records_file = (cwd + '\\write\\records.csv').replace('\\write\\write', '\\records')
    invoice_id = '{:010}'.format(invoice_id)

    try:
        with open(records_file, 'a') as log_file:
            log_file.write("[" + dt.now().strftime("%d/%m/%Y-%H:%M:%I" + "],") + str(invoice_id) + "\n")

    except Exception as e:
        print(e)

#
def read_from_record(cwd):
    records_file = (cwd + '\\write\\records.csv').replace('\\write\\write', '\\records')

    try:
        with open(records_file, 'r') as log_file:
            invoice_id = log_file.readlines()[-1]
            invoice_id = invoice_id.split(",")[2]
            invoice_id = int(invoice_id)

            return int(invoice_id)

    except Exception as e:
        print(e)

    return 0
