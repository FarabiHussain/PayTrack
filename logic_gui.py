import variables as vars
import customtkinter as ctk
from ctk_xyframe import *

xyframe_sizes = {
    '1920': 330,
    '1080': 230,
}

# reset all input fields and delete all receipt items
def clear_fields():
    vars.form["rate_input"].delete(0, "end")
    vars.form['description_combo'].set("Immigration Services")
    vars.form["qty_input"].delete(0, "end")
    vars.form["gst_input"].delete(0, "end")
    vars.form["pst_input"].delete(0, "end")
    vars.form["client_input"].delete(0, "end")

    vars.form["rate_input"].insert("end", 500)
    vars.form["qty_input"].insert("end", 1)
    vars.form["gst_input"].insert("end", 5.0)
    vars.form["pst_input"].insert("end", 7.0)
    vars.form["gst_display_amount"].configure(text="$0.00")
    vars.form["pst_display_amount"].configure(text="$0.00")
    vars.form["total_display_amount"].configure(text="$0.00")

    screen_w = str(vars.screen_sizes['ws'])
    screen_h = str(vars.screen_sizes['hs'])
    vars.items = []
    vars.form['scr_frame'].destroy()
    vars.form['scr_frame'] = CTkXYFrame(vars.root, corner_radius=0, border_width=0, width=xyframe_sizes[screen_w] if screen_w in xyframe_sizes else 700, height=xyframe_sizes[screen_h] if screen_h in xyframe_sizes else 480)
    vars.form['scr_frame'].place(x=25, y=12)

    ctk.CTkLabel(vars.form['scr_frame'], text="Description", corner_radius=4, width=170, fg_color='#CCCCCC', font=vars.font_family).grid(row=0, column=0, pady=5, padx=5)
    ctk.CTkLabel(vars.form['scr_frame'], text="Qty", corner_radius=4, width=50, fg_color='#CCCCCC', font=vars.font_family).grid(row=0, column=1, pady=5, padx=5)
    ctk.CTkLabel(vars.form['scr_frame'], text="Price", corner_radius=4, width=80, fg_color='#CCCCCC', font=vars.font_family).grid(row=0, column=2, pady=5, padx=5)

    refresh_table_and_amounts


# read from input fields and add a new item to the receipt
def add_item():
    screen_w = str(vars.screen_sizes['ws'])
    screen_h = str(vars.screen_sizes['hs'])
    vars.form['scr_frame'].destroy()
    vars.form['scr_frame'] = CTkXYFrame(vars.root, corner_radius=0, border_width=0, width=xyframe_sizes[screen_w] if screen_w in xyframe_sizes else 700, height=xyframe_sizes[screen_h] if screen_h in xyframe_sizes else 480)
    vars.form['scr_frame'].place(x=25, y=12)

    desc = vars.form['description_combo'].get()
    rate = vars.form['rate_input'].get()
    qty = vars.form['qty_input'].get()
    gst = vars.form['gst_input'].get()
    pst = vars.form['pst_input'].get()

    new_item = {
        "desc": desc,
        "rate": rate,
        "qty": qty if len(qty) > 0 else 1,
        "gst": gst if len(gst) > 0 else 5.0,
        "pst": pst if len(pst) > 0 else 7.0,
    }

    qty_increased = False

    # search for a matching item
    for curr_item in vars.items:

        # if a match is found, add the qty to that line instead of adding a new row for the new item
        if (
            curr_item['desc'] == new_item['desc']
            and float(curr_item['rate']) == float(new_item['rate'])
            and float(curr_item['gst']) == float(new_item['gst'])
            and float(curr_item['pst']) == float(new_item['pst'])
        ):
            curr_item['qty'] = str(int(curr_item['qty']) + int(new_item['qty']))
            qty_increased = True
            break

    # a match was not found, so we create a new row for the new item
    if not qty_increased:
        vars.items.append(new_item)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

    refresh_table_and_amounts()


# refresh table and amount to show new data
def refresh_table_and_amounts():
    cumulative_gst = 0
    cumulative_pst = 0
    cumulative_total = 0

    ctk.CTkLabel(vars.form['scr_frame'], text="Description", corner_radius=4, width=170, fg_color='#CCCCCC', font=vars.font_family).grid(row=0, column=0, pady=5, padx=5)
    ctk.CTkLabel(vars.form['scr_frame'], text="Qty", corner_radius=4, width=50, fg_color='#CCCCCC', font=vars.font_family).grid(row=0, column=1, pady=5, padx=5)
    ctk.CTkLabel(vars.form['scr_frame'], text="Price", corner_radius=4, width=80, fg_color='#CCCCCC', font=vars.font_family).grid(row=0, column=2, pady=5, padx=5)

    for entry in range(len(vars.items)):

        for col_idx, col_name in enumerate(['desc', 'qty']):
            col_width = 0

            if (col_idx == 0):
                col_width = 170
            elif (col_idx == 1):
                col_width = 50

            ctk.CTkLabel(vars.form['scr_frame'], text=vars.items[entry][col_name], fg_color='white', corner_radius=4, width=col_width).grid(row=(entry + 1), column=col_idx, pady=5, padx=5)

        row_rate = int(vars.items[entry]['rate'])
        row_qty = int(vars.items[entry]['qty'])
        row_gst = float(vars.items[entry]['gst'])
        row_pst = float(vars.items[entry]['pst'])

        row_gst_amount = float((row_rate/100)*row_gst)
        row_pst_amount = float((row_rate/100)*row_pst)

        total_row_charge = (row_rate + row_gst_amount + row_pst_amount)*row_qty

        cumulative_gst += row_gst_amount*row_qty
        cumulative_pst += row_pst_amount*row_qty
        cumulative_total += total_row_charge

        vars.form['gst_display_amount'].configure(text="$" + '{:,.2f}'.format(cumulative_gst))
        vars.form['pst_display_amount'].configure(text="$" + '{:,.2f}'.format(cumulative_pst))
        vars.form['total_display_amount'].configure(text="$" + '{:,.2f}'.format(cumulative_total))

        ctk.CTkLabel(vars.form['scr_frame'], text='{:,.2f}'.format(total_row_charge), fg_color='white', corner_radius=4, width=80).grid(row=(entry + 1), column=(col_idx + 1), pady=5, padx=5)


# callback for when an item is selected from the dropdown menu
def update_fields(choice):
    vars.form['rate_input'].delete(0, "end")
    vars.form['rate_input'].insert("end", vars.drp_values[choice])