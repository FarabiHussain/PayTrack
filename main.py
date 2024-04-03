from tkinter import StringVar
import docx, os
import variables as vars
import customtkinter as ctk
from ctk_xyframe import *
from logic_document import *
from document_utils import *
from logic_records import *
from logic_gui import *
from path_manager import *

##############################################################################################
## INITIALIZATION
##############################################################################################

vars.init()

# calculate x and y coordinates for the Tk root window
h = 670
w = 400
x = (vars.screen_sizes['ws']/2) - (w/2)
y = (vars.screen_sizes['hs']/2) - (h/2)

os.system("cls")
vars.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

try:
    vars.root.iconbitmap(resource_path("assets\\icons\\logo.ico"))
except Exception as e:
    pass

vars.root.configure(fg_color='white')
vars.root.title(f"AMCAIM PayTrack ({vars.form['version']})")

cwd = os.getcwd()
font_family = vars.font_family
document = docx.Document(resource_path(cwd + "\\assets\\templates\\receipt.docx"))

##############################################################################################
## FRAMES
##############################################################################################

screen_w = str(vars.screen_sizes['ws'])
screen_h = str(vars.screen_sizes['hs'])

vars.form['scr_frame_bg'] = ctk.CTkFrame(vars.root, corner_radius=2, border_width=1, width=360, height=250, fg_color='#E5E5E5')
vars.form['scr_frame_bg'].place(x=20, y=10)
vars.form['scr_frame'] = ctk.CTkScrollableFrame(vars.root, corner_radius=0, border_width=0, width=335, height=230)
vars.form['scr_frame'].place(x=25, y=12)

ctk.CTkLabel(vars.form['scr_frame'], text="Description", corner_radius=2, width=170, fg_color='#CCCCCC', font=font_family).grid(row=0, column=0, pady=5, padx=5)
ctk.CTkLabel(vars.form['scr_frame'], text="Qty", corner_radius=2, width=50, fg_color='#CCCCCC', font=font_family).grid(row=0, column=1, pady=5, padx=5)
ctk.CTkLabel(vars.form['scr_frame'], text="Price", corner_radius=2, width=80, fg_color='#CCCCCC', font=font_family).grid(row=0, column=2, pady=5, padx=5)

##############################################################################################
## TOTALS SECTION
##############################################################################################

vars.form['totals_frame'] = ctk.CTkFrame(vars.root, corner_radius=2, border_width=1, width=360, height=95, fg_color='#E5E5E5')
vars.form['totals_frame'].place(x=20, y=303)
vars.form['gst_display_label'] = ctk.CTkLabel(vars.root, text="GST @5%", font=font_family, bg_color='#E5E5E5')
vars.form['pst_display_label'] = ctk.CTkLabel(vars.root, text="PST @7%", font=font_family, bg_color='#E5E5E5')
vars.form['total_display_label'] = ctk.CTkLabel(vars.root, text="Total", font=font_family, bg_color='#E5E5E5')
vars.form['gst_display_label'].place(x=30, y=306)
vars.form['pst_display_label'].place(x=30, y=336)
vars.form['total_display_label'].place(x=30, y=366)

vars.form['gst_display_amount'] = ctk.CTkLabel(vars.root, width=120, text="$0.00", font=font_family, bg_color='#E5E5E5', anchor="e")
vars.form['pst_display_amount'] = ctk.CTkLabel(vars.root, width=120, text="$0.00", font=font_family, bg_color='#E5E5E5', anchor="e")
vars.form['total_display_amount'] = ctk.CTkLabel(vars.root, width=120, text="$0.00", font=font_family, bg_color='#E5E5E5', anchor="e")
vars.form['gst_display_amount'].place(x=250, y=306)
vars.form['pst_display_amount'].place(x=250, y=336)
vars.form['total_display_amount'].place(x=250, y=366)

##############################################################################################
## INPUT SECTION
##############################################################################################

vars.form['client_textvariable'] = StringVar(value='')
vars.form['client_label'] = ctk.CTkLabel(vars.root, text="Client", font=font_family)
vars.form['client_label'].place(x=20, y=410-2)
vars.form['client_input'] = ctk.CTkEntry(vars.root, width=310, height=32, border_width=1, corner_radius=2, textvariable=vars.form['client_textvariable'])
vars.form['client_input'].place(x=70, y=410-2)

vars.form['description_label'] = ctk.CTkLabel(vars.root, text="Desc", font=font_family)
vars.form['description_label'].place(x=20, y=450-2)
vars.form['description_combo'] = ctk.CTkComboBox(vars.root, border_width=1, corner_radius=2, width=310, height=32, button_color='#808080', dropdown_fg_color='white', values=vars.drp_list, variable=vars.drp_str_var, command=update_fields)
vars.form['description_combo'].place(x=70, y=450-2)
vars.form['description_combo'].set("Immigration Services")

vars.form['qty_textvariable'] = StringVar(value='1')
vars.form['qty_textvariable'].trace('w', update_total)
vars.form['qty_label'] = ctk.CTkLabel(vars.root, text="QTY", font=font_family)
vars.form['qty_input'] = ctk.CTkEntry(vars.root, width=120, height=32, border_width=1, corner_radius=2, textvariable=vars.form['qty_textvariable'])
vars.form['qty_label'].place(x=220, y=490-2)
vars.form['qty_input'].place(x=260, y=490-2)

vars.form['gst_textvariable'] = StringVar(value='5.0')
vars.form['gst_textvariable'].trace('w', update_total)
vars.form['gst_label'] = ctk.CTkLabel(vars.root, text="GST", font=font_family)
vars.form['gst_label'].place(x=20, y=530-2)
vars.form['gst_input'] = ctk.CTkEntry(vars.root, width=120, height=32, border_width=1, corner_radius=2, textvariable=vars.form['gst_textvariable'])
vars.form['gst_input'].place(x=70, y=530-2)

vars.form['pst_textvariable'] = StringVar(value='7.0')
vars.form['pst_textvariable'].trace('w', update_total)
vars.form['pst_label'] = ctk.CTkLabel(vars.root, text="PST", font=font_family)
vars.form['pst_label'].place(x=220, y=530-2)
vars.form['pst_input'] = ctk.CTkEntry(vars.root, width=120, height=32, border_width=1, corner_radius=2, textvariable=vars.form['pst_textvariable'])
vars.form['pst_input'].place(x=260, y=530-2)

vars.form['rate_textvariable'] = StringVar(value='500.0')
vars.form['rate_textvariable'].trace('w', update_total)
vars.form['rate_label'] = ctk.CTkLabel(vars.root, text="Rate", font=font_family)
vars.form['rate_label'].place(x=20, y=490-2)
vars.form['rate_input'] = ctk.CTkEntry(vars.root, width=120, height=32, border_width=1, corner_radius=2, textvariable=vars.form['rate_textvariable'])
vars.form['rate_input'].place(x=70, y=490-2)

vars.form['total_label'] = ctk.CTkLabel(vars.root, text="Total", font=font_family)
vars.form['total_label'].place(x=20, y=570-2)
vars.form['total_input'] = ctk.CTkEntry(vars.root, width=222, height=32, border_width=1, corner_radius=2)
vars.form['total_input'].place(x=70, y=570-2)
vars.form['total_input'].insert('end', '560.0')

##############################################################################################
## BUTTONS
##############################################################################################

vars.form['add_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['add_item'], border_width=0, corner_radius=2, fg_color="#38bc41", command=lambda:add_item(), width=72, height=36)
vars.form['clear_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['clear'], border_width=0, corner_radius=2, fg_color="#c41212", command=lambda:clear_fields(), width=72, height=36)
vars.form['search_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['search'], border_width=0, corner_radius=2, fg_color="#808080", command=lambda:search_documents(), width=72, height=36)
vars.form['docx_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['docx'], border_width=0, corner_radius=2, fg_color="#383FBC", command=lambda:generate_invoice(cwd), width=72, height=36)
vars.form['output_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['folder'], border_width=0, corner_radius=2, fg_color="#808080", command=lambda:os.startfile(cwd + "\\output"), width=36, height=36)
vars.form['adjust_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['adjust_rate'], border_width=0, corner_radius=2, fg_color="#23265e", command=lambda:adjust_rate(), width=100)
vars.form['remove_item_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['empty_item'], border_width=0, corner_radius=2, fg_color="#e0e0e0", command=lambda:remove_item(), width=360, height=28, state="disabled")

vars.form['add_btn'].place(x=20, y=h-55)
vars.form['clear_btn'].place(x=102, y=h-55)
vars.form['docx_btn'].place(x=182, y=h-55)
vars.form['search_btn'].place(x=263, y=h-55)
vars.form['output_btn'].place(x=344, y=h-55)
vars.form['adjust_btn'].place(x=244, y=568)
vars.form['remove_item_btn'].place(x=20, y=266)


vars.root.mainloop()