import docx, os, win32print
import variables as vars
import customtkinter as ctk
from CTkXYFrame import *
from invoice import *
from doc_utils import *
from data_utils import *
from records import *
from PIL import Image
from path_manager import resource_path

os.system("cls")
cwd = os.getcwd()

invoice_id = "{:010}".format((read_from_record(cwd) + 1))

# instance of a word document using the template
document = docx.Document(resource_path(cwd + "\\assets\\templates\\invoice.docx"))

write_to_record(cwd, invoice_id)

# Table data in a form of list
data = [
    {"desc": "Affidavit", "qty": 1, "rate": 100, "gst": 0.05, "pst": 0.07},
]

def generate_invoice():
    generate_invoice_info(document, invoice_id)
    generate_items_table(document, data)
    generate_totals_table(document, calculate_totals(data))

    # save the document with the current invoice ID
    document.save(cwd + "\\output\\invoice_" + invoice_id + ".docx")
    os.startfile(cwd + "\\output\\invoice_" + invoice_id + ".docx")


vars.init()

# calculate x and y coordinates for the Tk root window
h = 600
w = 400
x = (vars.screen_sizes['ws']/2) - (w/2)
y = (vars.screen_sizes['hs']/2) - (h/2)

vars.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
vars.root.iconbitmap(resource_path("assets\\icons\\logo.ico"))
vars.root.title("AMCAIM InGen")

gui_font = ctk.CTkFont(family="Roboto Bold")

vars.form['docx_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['docx'], border_width=0, corner_radius=4, fg_color="#383FBC", command=lambda:generate_invoice(), width=36, height=36)
vars.form['docx_btn'].place(x=20, y=540)

vars.form['scr_frame'] = CTkXYFrame(vars.root, corner_radius=4, border_width=0, width=340, height=250)
vars.form['scr_frame'].place(x=20, y=10)

vars.form['totals_frame'] = ctk.CTkFrame(vars.root, corner_radius=4, border_width=1, width=360, height=110, fg_color='#E5E5E5')
vars.form['totals_frame'].place(x=20, y=280)

vars.form['gst_label'] = ctk.CTkLabel(vars.root, text="GST @5%", font=gui_font, bg_color='#E5E5E5')
vars.form['pst_label'] = ctk.CTkLabel(vars.root, text="PST @7%", font=gui_font, bg_color='#E5E5E5')
vars.form['total_label'] = ctk.CTkLabel(vars.root, text="Total", font=gui_font, bg_color='#E5E5E5')
vars.form['gst_label'].place(x=30, y=290)
vars.form['pst_label'].place(x=30, y=320)
vars.form['total_label'].place(x=30, y=350)

vars.form['gst_amount'] = ctk.CTkLabel(vars.root, text="$0.0", font=gui_font, bg_color='#E5E5E5')
vars.form['pst_amount'] = ctk.CTkLabel(vars.root, text="$0.0", font=gui_font, bg_color='#E5E5E5')
vars.form['total_amount'] = ctk.CTkLabel(vars.root, text="$0.0", font=gui_font, bg_color='#E5E5E5')
vars.form['gst_amount'].place(x=340, y=290)
vars.form['pst_amount'].place(x=340, y=320)
vars.form['total_amount'].place(x=340, y=350)

vars.form['description_label'] = ctk.CTkLabel(vars.root, text="Description", font=gui_font)
vars.form['description_label'].place(x=20, y=460)
vars.form['description_input'] = ctk.CTkEntry(vars.root, width=130, border_width=1, corner_radius=4)
vars.form['description_input'].place(x=100, y=460)


vars.root.mainloop()