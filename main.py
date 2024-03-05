# Import docx NOT python-docx 
import docx, os
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.shared import Cm as CM
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

os.system('cls')

def set_cell_color(cell, color='ffffff'):
    cell_xml = cell._tc
    cell_props = cell_xml.get_or_add_tcPr()
    shade_obj = OxmlElement('w:shd')
    shade_obj.set(qn('w:fill'), color)
    cell_props.append(shade_obj)

# Create an instance of a word document 
doc = docx.Document() 

# Add a Title to the document 
doc.add_heading('GeeksForGeeks', 0) 

# Table data in a form of list 
data = [
    {'desc': 'Notary', 'qty': 2, 'amount': 30},
    {'desc': 'Immigration Services', 'qty': 1, 'amount': 500},
    {'desc': 'Government Fees', 'qty': 1, 'amount': 50},
]

# Creating a table object 
table = doc.add_table(rows=1, cols=5) 

# Adding heading in the 1st row of the table 
row = table.rows[0].cells 
row[0].text = 'SL.'
row[1].text = 'DESC'
row[2].text = 'QTY'
row[3].text = 'AMOUNT'
row[4].text = 'TOTAL'

# Adding data from the list to the table 
for index, entry in enumerate(data): 

    # Adding a row and then adding data in it. 
    row = table.add_row().cells

    # Converting id to string as table can only take string input 
    row[0].text = str(index)
    row[1].text = str(entry['desc'])
    row[2].text = str(entry['qty'])
    row[3].text = str(entry['amount'])
    row[4].text = str(entry['qty'] * entry['amount'])


for cell in table.columns[0].cells: cell.width = CM(1.0)
for cell in table.columns[1].cells: cell.width = CM(9.9)
for cell in table.columns[2].cells: cell.width = CM(1.0)
for cell in table.columns[3].cells: cell.width = CM(1.0)
for cell in table.columns[4].cells: cell.width = CM(1.0)

for index, row in enumerate(table.rows):
    row.height = CM(0.5)
    row_color = 'E5E4E2' if index%2 == 0 else 'FFFFFF'

    for cell in row.cells:
        set_cell_color(cell, row_color)
        # cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

# table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.BOTTOM
table.alignment = WD_TABLE_ALIGNMENT.RIGHT

# Now save the document to a location 
doc.save('test.docx')
os.startfile('test.docx')

