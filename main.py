import docx, os, win32print
import variables as vars
import customtkinter as ctk
import tkinter as tk
from CTkXYFrame import *
from invoice import *
from doc_utils import *
from data_utils import *
from records import *
from logic import *
from PIL import Image
from path_manager import resource_path

os.system("cls")
cwd = os.getcwd()

invoice_id = "{:010}".format((read_from_record(cwd) + 1))

# instance of a word document using the template
document = docx.Document(resource_path(cwd + "\\assets\\templates\\invoice.docx"))

write_to_record(cwd, invoice_id)

def generate_invoice():
    generate_invoice_info(document, invoice_id)
    generate_items_table(document, vars.items)
    generate_totals_table(document, calculate_totals(vars.items))

    # save the document with the current invoice ID
    document.save(cwd + "\\output\\invoice_" + invoice_id + ".docx")
    os.startfile(cwd + "\\output\\invoice_" + invoice_id + ".docx")

def update_fields(choice):
    vars.form['rate_input'].delete(0, "end")
    vars.form['rate_input'].insert("end", vars.drp_values[choice])


#######################################################################################################
#######################################################################################################
#######################################################################################################


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

vars.form['add_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['add'], border_width=0, corner_radius=4, fg_color="#38bc41", command=lambda:add_to_invoice(), width=36, height=36)
vars.form['clear_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['clear'], border_width=0, corner_radius=4, fg_color="#c41212", command=lambda:clear_fields(), width=36, height=36)
vars.form['docx_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['docx'], border_width=0, corner_radius=4, fg_color="#383FBC", command=lambda:generate_invoice(), width=36, height=36)
vars.form['output_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['folder'], border_width=0, corner_radius=4, fg_color="#808080", command=lambda:os.startfile(cwd + "\\output"), width=36, height=36)
vars.form['add_btn'].place(x=20, y=545)
vars.form['clear_btn'].place(x=60, y=545)
vars.form['docx_btn'].place(x=304, y=545)
vars.form['output_btn'].place(x=344, y=545)

vars.form['scr_frame_bg'] = ctk.CTkFrame(vars.root, corner_radius=4, border_width=1, width=360, height=250, fg_color='#E5E5E5')
vars.form['scr_frame_bg'].place(x=20, y=10)
vars.form['scr_frame'] = CTkXYFrame(vars.root, corner_radius=0, border_width=0, width=330, height=230)
vars.form['scr_frame'].place(x=25, y=12)

vars.form['totals_frame'] = ctk.CTkFrame(vars.root, corner_radius=4, border_width=1, width=360, height=110, fg_color='#E5E5E5')
vars.form['totals_frame'].place(x=20, y=280)

vars.form['gst_display_label'] = ctk.CTkLabel(vars.root, text="GST @5%", font=gui_font, bg_color='#E5E5E5')
vars.form['pst_display_label'] = ctk.CTkLabel(vars.root, text="PST @7%", font=gui_font, bg_color='#E5E5E5')
vars.form['total_display_label'] = ctk.CTkLabel(vars.root, text="Total", font=gui_font, bg_color='#E5E5E5')
vars.form['gst_display_label'].place(x=30, y=290)
vars.form['pst_display_label'].place(x=30, y=320)
vars.form['total_display_label'].place(x=30, y=350)

vars.form['gst_display_amount'] = ctk.CTkLabel(vars.root, width=120, text="$0.00", font=gui_font, bg_color='#E5E5E5', anchor="e")
vars.form['pst_display_amount'] = ctk.CTkLabel(vars.root, width=120, text="$0.00", font=gui_font, bg_color='#E5E5E5', anchor="e")
vars.form['total_display_amount'] = ctk.CTkLabel(vars.root, width=120, text="$0.00", font=gui_font, bg_color='#E5E5E5', anchor="e")
vars.form['gst_display_amount'].place(x=250, y=290)
vars.form['pst_display_amount'].place(x=250, y=320)
vars.form['total_display_amount'].place(x=250, y=350)

vars.form['rate_label'] = ctk.CTkLabel(vars.root, text="Rate", font=gui_font)
vars.form['rate_label'].place(x=20, y=460)
vars.form['rate_input'] = ctk.CTkEntry(vars.root, width=120, border_width=1, corner_radius=4, placeholder_text='0.0')
vars.form['rate_input'].insert("end", '500')
vars.form['rate_input'].place(x=70, y=460)

vars.form['description_label'] = ctk.CTkLabel(vars.root, text="Desc", font=gui_font)
vars.form['description_label'].place(x=20, y=420)
vars.form['description_combo'] = ctk.CTkComboBox(
    vars.root,
    border_width=1,
    corner_radius=4,
    width=310,
    button_color='#808080',
    dropdown_fg_color='white',
    values=vars.drp_list,
    variable=vars.drp_str_var,
    command=update_fields,
)

vars.form['description_combo'].set("Immigration Services")
vars.form['description_combo'].place(x=70, y=420)

vars.form['qty_label'] = ctk.CTkLabel(vars.root, text="QTY", font=gui_font)
vars.form['qty_input'] = ctk.CTkEntry(vars.root, width=120, border_width=1, corner_radius=4, placeholder_text='1')
vars.form['qty_label'].place(x=220, y=460)
vars.form['qty_input'].place(x=260, y=460)

vars.form['gst_label'] = ctk.CTkLabel(vars.root, text="GST", font=gui_font)
vars.form['pst_label'] = ctk.CTkLabel(vars.root, text="PST", font=gui_font)
vars.form['gst_label'].place(x=20, y=500)
vars.form['pst_label'].place(x=220, y=500)

vars.form['gst_input'] = ctk.CTkEntry(vars.root, width=120, border_width=1, corner_radius=4, placeholder_text='5.0')
vars.form['pst_input'] = ctk.CTkEntry(vars.root, width=120, border_width=1, corner_radius=4, placeholder_text='7.0')
vars.form['gst_input'].place(x=70, y=500)
vars.form['pst_input'].place(x=260, y=500)

vars.root.mainloop()