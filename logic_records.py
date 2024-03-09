import os
from datetime import datetime as dt


# write the passed doc_id to records.csv
def write_to_record(cwd, doc_id):
    records_file = (cwd + '\\write\\records.csv').replace('\\write\\write', '\\records')
    doc_id = '{:010}'.format(doc_id)

    try:
        with open(records_file, 'a') as log_file:
            log_file.write("[" + dt.now().strftime("%d/%m/%Y-%H:%M:%I" + "],") + str(doc_id) + "\n")

    except Exception as e:
        print(e)


# read records.csv to retrieve the last created receipt id
def read_from_record(cwd):
    records_file = (cwd + '\\write\\records.csv').replace('\\write\\write', '\\records')

    try:
        with open(records_file, 'r') as log_file:
            doc_id = log_file.readlines()[-1]
            doc_id = doc_id.split(",")[1]
            doc_id = int(doc_id)

            return int(doc_id)

    except Exception as e:
        print("no existing IDs - starting with ID 1")

    return 0
