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
h = 600
w = 400
x = (vars.screen_sizes['ws']/2) - (w/2)
y = (vars.screen_sizes['hs']/2) - (h/2)

os.system("cls")
vars.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
vars.root.iconbitmap(resource_path("assets\\icons\\logo.ico"))
vars.root.configure(fg_color='white')
vars.root.title(f"AMCAIM PayTrack ({vars.form['version']})")

cwd = os.getcwd()
font_family = vars.font_family
document = docx.Document(resource_path(cwd + "\\assets\\templates\\receipt.docx"))

#########################################c#####################################################
## BUTTONS
##############################################################################################

vars.form['add_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['add'], border_width=0, corner_radius=4, fg_color="#38bc41", command=lambda:add_item(), width=36, height=36)
vars.form['clear_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['clear'], border_width=0, corner_radius=4, fg_color="#c41212", command=lambda:clear_fields(), width=36, height=36)
vars.form['search_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['search'], border_width=0, corner_radius=4, fg_color="#ff9900", command=lambda:search_documents(), width=36, height=36)
vars.form['docx_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['docx'], border_width=0, corner_radius=4, fg_color="#383FBC", command=lambda:generate_invoice(cwd), width=36, height=36)
vars.form['output_btn'] = ctk.CTkButton(vars.root, text="", image=vars.icons['folder'], border_width=0, corner_radius=4, fg_color="#808080", command=lambda:os.startfile(cwd + "\\output"), width=36, height=36)

vars.form['add_btn'].place(x=20, y=545)
vars.form['clear_btn'].place(x=60, y=545)
vars.form['search_btn'].place(x=100, y=545)
vars.form['docx_btn'].place(x=304, y=545)
vars.form['output_btn'].place(x=344, y=545)

##############################################################################################
## FRAMES
##############################################################################################

vars.form['scr_frame_bg'] = ctk.CTkFrame(vars.root, corner_radius=4, border_width=1, width=360, height=250, fg_color='#E5E5E5')
vars.form['scr_frame_bg'].place(x=20, y=10)
vars.form['scr_frame'] = CTkXYFrame(vars.root, corner_radius=0, border_width=0, width=vars.screen_sizes['ws']*0.18, height=vars.screen_sizes['hs']*0.22) # 700 * 480
vars.form['scr_frame'].place(x=25, y=12)

ctk.CTkLabel(vars.form['scr_frame'], text="Description", corner_radius=4, width=170, fg_color='#CCCCCC', font=font_family).grid(row=0, column=0, pady=5, padx=5)
ctk.CTkLabel(vars.form['scr_frame'], text="Qty", corner_radius=4, width=50, fg_color='#CCCCCC', font=font_family).grid(row=0, column=1, pady=5, padx=5)
ctk.CTkLabel(vars.form['scr_frame'], text="Price", corner_radius=4, width=80, fg_color='#CCCCCC', font=font_family).grid(row=0, column=2, pady=5, padx=5)

##############################################################################################
## TOTALS SECTION
##############################################################################################

vars.form['totals_frame'] = ctk.CTkFrame(vars.root, corner_radius=4, border_width=1, width=360, height=95, fg_color='#E5E5E5')
vars.form['totals_frame'].place(x=20, y=273)
vars.form['gst_display_label'] = ctk.CTkLabel(vars.root, text="GST @5%", font=font_family, bg_color='#E5E5E5')
vars.form['pst_display_label'] = ctk.CTkLabel(vars.root, text="PST @7%", font=font_family, bg_color='#E5E5E5')
vars.form['total_display_label'] = ctk.CTkLabel(vars.root, text="Total", font=font_family, bg_color='#E5E5E5')
vars.form['gst_display_label'].place(x=30, y=290-14)
vars.form['pst_display_label'].place(x=30, y=320-14)
vars.form['total_display_label'].place(x=30, y=350-14)

vars.form['gst_display_amount'] = ctk.CTkLabel(vars.root, width=120, text="$0.00", font=font_family, bg_color='#E5E5E5', anchor="e")
vars.form['pst_display_amount'] = ctk.CTkLabel(vars.root, width=120, text="$0.00", font=font_family, bg_color='#E5E5E5', anchor="e")
vars.form['total_display_amount'] = ctk.CTkLabel(vars.root, width=120, text="$0.00", font=font_family, bg_color='#E5E5E5', anchor="e")
vars.form['gst_display_amount'].place(x=250, y=290-14)
vars.form['pst_display_amount'].place(x=250, y=320-14)
vars.form['total_display_amount'].place(x=250, y=350-14)

##############################################################################################
## INPUT SECTION
##############################################################################################

vars.form['client_label'] = ctk.CTkLabel(vars.root, text="Client", font=font_family)
vars.form['client_label'].place(x=20, y=380)
vars.form['client_input'] = ctk.CTkEntry(vars.root, width=310, border_width=1, corner_radius=4)
vars.form['client_input'].place(x=70, y=380)

vars.form['description_label'] = ctk.CTkLabel(vars.root, text="Desc", font=font_family)
vars.form['description_label'].place(x=20, y=420)
vars.form['description_combo'] = ctk.CTkComboBox(vars.root, border_width=1, corner_radius=4, width=310, button_color='#808080', dropdown_fg_color='white', values=vars.drp_list, variable=vars.drp_str_var, command=update_fields)
vars.form['description_combo'].place(x=70, y=420)
vars.form['description_combo'].set("Immigration Services")

vars.form['rate_label'] = ctk.CTkLabel(vars.root, text="Rate", font=font_family)
vars.form['rate_label'].place(x=20, y=460)
vars.form['rate_input'] = ctk.CTkEntry(vars.root, width=120, border_width=1, corner_radius=4)
vars.form['rate_input'].insert("end", '500')
vars.form['rate_input'].place(x=70, y=460)

vars.form['qty_label'] = ctk.CTkLabel(vars.root, text="QTY", font=font_family)
vars.form['qty_input'] = ctk.CTkEntry(vars.root, width=120, border_width=1, corner_radius=4)
vars.form['qty_input'].insert("end", '1')
vars.form['qty_label'].place(x=220, y=460)
vars.form['qty_input'].place(x=260, y=460)

vars.form['gst_label'] = ctk.CTkLabel(vars.root, text="GST", font=font_family)
vars.form['pst_label'] = ctk.CTkLabel(vars.root, text="PST", font=font_family)
vars.form['gst_label'].place(x=20, y=500)
vars.form['pst_label'].place(x=220, y=500)

vars.form['gst_input'] = ctk.CTkEntry(vars.root, width=120, border_width=1, corner_radius=4)
vars.form['gst_input'].insert("end", '5.0')
vars.form['pst_input'] = ctk.CTkEntry(vars.root, width=120, border_width=1, corner_radius=4)
vars.form['pst_input'].insert("end", '7.0')
vars.form['gst_input'].place(x=70, y=500)
vars.form['pst_input'].place(x=260, y=500)

vars.root.mainloop()