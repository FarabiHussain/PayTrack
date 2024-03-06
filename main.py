import docx, os, datetime
from doc_utils import *
from data_utils import *
from docx.shared import Cm as CM
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

os.system("cls")
timestamp = str(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%I"))
client = 'Awais Saleem'

# Create an instance of a word document
doc = docx.Document("invoice.docx")

insert_paragraph_after(
    doc.add_paragraph(), 
    (
        "Invoice#:\t [invoice id]"
        + "\nDate:\t\t " + timestamp
        + "\nInvoiced to:\t " + client
        + "\n"
    )
)

# Table data in a form of list
columns = [
    {'heading': 'SL.', 'width': 1.0},
    {'heading': 'DESCRIPTION', 'width': 20.0},
    {'heading': 'QTY', 'width': 1.0},
    {'heading': 'RATE', 'width': 1.0},
    {'heading': 'AMOUNT', 'width': 1.0},
]

# Table data in a form of list
data = [
    {"desc": "Notary", "qty": 2, "rate": 30, "gst": 0.05, 'pst': 0.07},
    {"desc": "Immigration Services", "qty": 1, "rate": 500, "gst": 0.05, 'pst': 0.07},
    {"desc": "Government Fees", "qty": 1, "rate": 50, "gst": 0.0, 'pst': 0.0},
]

####################################################################################

# Creating a table object
items_table = doc.add_table(rows=1, cols=5)

# Adding heading in the 1st row of the table
row = items_table.rows[0].cells
for idx, col in enumerate(columns):
    row[idx].text = col['heading']

# Adding data from the list to the table
for index, entry in enumerate(data):

    # Adding a row and then adding data in it.
    row = items_table.add_row().cells

    row[0].text = str(index)
    row[1].text = str(entry["desc"])
    row[2].text = str(entry["qty"])
    row[3].text = str(entry["rate"])
    row[4].text = str(entry["qty"] * entry["rate"])

for cell in items_table.rows[0].cells:
    set_cell_border(cell, bottom={"sz": 6, "color": "#AAAAAA", "val": "single", "space": "10"})
    set_cell_border(cell, top={"sz": 6, "color": "#AAAAAA", "val": "single", "space": "15"})


# set column widths
for idx, col in enumerate(columns):
    for index, cell in enumerate(items_table.columns[idx].cells):
        cell.width = CM(col['width'])

        if (index > 0):
            set_cell_border(cell, bottom={"sz": 6, "color": "#EEEEEE", "val": "single", "space": "8"})

    set_cell_border(cell, bottom={"sz": 6, "color": "#AAAAAA", "val": "single", "space": "0"})


# set row heights
for index, row in enumerate(items_table.rows):
    row.height = CM(1)

make_rows_bold(items_table.rows[0])

#####################################################################################

total_table = doc.add_table(rows=1, cols=5)
res = calculate_totals(data)

total_table_data = [
    [str('GST @5%'), '','','', str(res['gst'])],
    [str('PST @7%'), '','','', str(res['pst'])],
    [str('TOTAL'), '','','', str(res['dollar'])],
]

for total_row in total_table_data:

    row = total_table.add_row().cells

    for idx, col in enumerate(total_row):
        row[idx].text = col 

    make_rows_bold(total_table.rows[-1])
    # items_table.cell(-1,-0).merge(items_table.cell(-1,1))


#####################################################################################

doc.save("invoice-test.docx")
os.startfile("invoice-test.docx")
