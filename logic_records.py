import os
from datetime import datetime as dt


# write the passed doc_id to records.csv
def write_to_record(cwd, doc_id, client_name):

    # set up the write directory
    records_dir = os.getcwd() + "\\write\\"
    if not os.path.exists(records_dir):
        os.makedirs(records_dir)

        # set up the csv for the records
        try: 
            f = open(records_dir + "\\records.csv", "x")
            f.write(",".join(['created_date', 'document_id', 'client_name']))
            f.write("\n")
            f.close()

        except Exception as e:
            print(e)

    records_file = (cwd + '\\write\\records.csv').replace('\\write\\write', '\\records')
    doc_id = '{:010}'.format(doc_id)

    try:
        with open(records_file, 'a') as log_file:
            log_file.write(f"[{dt.now().strftime("%d/%m/%Y-%H:%M:%I")}],[{str(doc_id)}],{client_name},{os.environ['COMPUTERNAME']}\n")

    except Exception as e:
        print(e)


# read records.csv to retrieve the last created receipt id
def read_from_record(cwd):
    records_file = (cwd + '\\write\\records.csv').replace('\\write\\write', '\\records')

    try:
        with open(records_file, 'r') as log_file:
            doc_id = log_file.readlines()[-1]
            doc_id = doc_id.split(",")[1]
            doc_id = doc_id.replace("[","").replace("]","")

            return int(doc_id)

    except Exception as e:
        print("no existing IDs - starting with ID 1")

    return 0
