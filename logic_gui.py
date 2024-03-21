import variables as vars
import customtkinter as ctk
import re
from ctk_xyframe import *
from CTkMessagebox import CTkMessagebox as popup


# reset all input fields and delete all receipt items
def clear_fields():
    vars.form['description_combo'].set("Immigration Services")
    vars.form['rate_textvariable'].set("500")
    vars.form['qty_textvariable'].set("1")
    vars.form['gst_textvariable'].set("5.0")
    vars.form['pst_textvariable'].set("7.0")
    vars.form["gst_display_amount"].configure(text="$0.00")
    vars.form["pst_display_amount"].configure(text="$0.00")
    vars.form["total_display_amount"].configure(text="$0.00")

    vars.items = []
    vars.form['scr_frame'].destroy()
    vars.form['scr_frame'] = ctk.CTkScrollableFrame(vars.root, corner_radius=0, border_width=0, width=335, height=230)
    vars.form['scr_frame'].place(x=25, y=12)

    ctk.CTkLabel(vars.form['scr_frame'], text="Description", corner_radius=2, width=170, fg_color='#CCCCCC', font=vars.font_family).grid(row=0, column=0, pady=5, padx=5)
    ctk.CTkLabel(vars.form['scr_frame'], text="Qty", corner_radius=2, width=50, fg_color='#CCCCCC', font=vars.font_family).grid(row=0, column=1, pady=5, padx=5)
    ctk.CTkLabel(vars.form['scr_frame'], text="Price", corner_radius=2, width=80, fg_color='#CCCCCC', font=vars.font_family).grid(row=0, column=2, pady=5, padx=5)

    refresh_table_and_amounts


# read from input fields and add a new item to the receipt
def add_item():
    desc = vars.form['description_combo'].get()
    rate = vars.form['rate_textvariable'].get()
    qty = vars.form['qty_textvariable'].get()
    gst = vars.form['gst_textvariable'].get()
    pst = vars.form['pst_textvariable'].get()
    total = vars.form['total_input'].get()

    variables = [rate, qty, gst, pst, total]

    is_valid = check_special(variables) and check_alphabets(variables) and check_empty(variables)

    if not is_valid:
        return

    vars.form['scr_frame'].destroy()
    vars.form['scr_frame'] = ctk.CTkScrollableFrame(vars.root, corner_radius=0, border_width=0, width=335, height=230)
    vars.form['scr_frame'].place(x=25, y=12)

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

    ctk.CTkLabel(vars.form['scr_frame'], text="Description", corner_radius=2, width=170, fg_color='#CCCCCC', font=vars.font_family).grid(row=0, column=0, pady=5, padx=5)
    ctk.CTkLabel(vars.form['scr_frame'], text="Qty", corner_radius=2, width=50, fg_color='#CCCCCC', font=vars.font_family).grid(row=0, column=1, pady=5, padx=5)
    ctk.CTkLabel(vars.form['scr_frame'], text="Price", corner_radius=2, width=80, fg_color='#CCCCCC', font=vars.font_family).grid(row=0, column=2, pady=5, padx=5)

    for entry in range(len(vars.items)):

        for col_idx, col_name in enumerate(['desc', 'qty']):
            col_width = 0

            if (col_idx == 0):
                col_width = 170
            elif (col_idx == 1):
                col_width = 50

            ctk.CTkLabel(vars.form['scr_frame'], text=vars.items[entry][col_name], fg_color='white', corner_radius=2, width=col_width).grid(row=(entry + 1), column=col_idx, pady=5, padx=5)

        row_rate = float(vars.items[entry]['rate'])
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

        ctk.CTkLabel(vars.form['scr_frame'], text='{:,.2f}'.format(total_row_charge), fg_color='white', corner_radius=2, width=80).grid(row=(entry + 1), column=(col_idx + 1), pady=5, padx=5)


# callback for when an item is selected from the dropdown menu
def update_fields(choice):
    vars.form['rate_input'].delete(0, "end")
    vars.form['rate_input'].insert("end", vars.drp_values[choice])

    if (choice == "Government Fees"):
        vars.form['gst_input'].delete(0, "end")
        vars.form['pst_input'].delete(0, "end")
        vars.form['gst_input'].insert("end", "0.0")
        vars.form['pst_input'].insert("end", "0.0")
        return

    vars.form['gst_input'].delete(0, "end")
    vars.form['pst_input'].delete(0, "end")
    vars.form['gst_input'].insert("end", "5.0")
    vars.form['pst_input'].insert("end", "7.0")


#
def update_total(*args):

    try:
        rate = float(vars.form['rate_textvariable'].get())
        qty = float(vars.form['qty_textvariable'].get())
        gst = float(vars.form['gst_textvariable'].get())
        pst = float(vars.form['pst_textvariable'].get())

        taxes = gst + pst
        total = 0
        total += rate * (taxes / 100)
        total += rate
        total *= qty

        vars.form['total_input'].delete('0', 'end')
        vars.form['total_input'].insert('end', str(total))
        vars.form['add_btn'].configure(state="normal", fg_color="#38bc41")

    except Exception as e:
        print(e)
        vars.form['total_input'].delete('0', 'end')
        vars.form['total_input'].insert('end', str(''))
        vars.form['add_btn'].configure(state="disabled", fg_color="#e0e0e0")


#
def adjust_rate():

    total = vars.form['total_input'].get()

    if (check_special([total]) == False or check_alphabets([total]) == False):
        return

    try:
        total = float(vars.form['total_input'].get())
        qty = float(vars.form['qty_input'].get())
        taxes = (float(vars.form['gst_input'].get()) + float(vars.form['pst_input'].get())) / 100

        rate = 0
        rate += (total / (1 + taxes)) / qty

        vars.form['rate_textvariable'].set(str(round(rate, 2)))
        vars.form['total_input'].delete('0', 'end')
        vars.form['total_input'].insert('end', str(total))

    except Exception as e:
        print(e)


#
def check_special(variables, is_string = False):
    special_chars_list = ["\\", "/", ":", "*", "?", "\"", "<", ">" ,"|"]

    if (is_string is False):
        special_chars_list.append(",")
        special_chars_list.append(" ")

    for var in variables:
        if any(bad_char in var for bad_char in special_chars_list):
            popup(title="", message=f'The following special characters cannot be used:\n{(" ").join(special_chars_list)}', corner_radius=2)
            return False
        
    return True


#
def check_alphabets(variables):
    for var in variables:
        if re.search('[A-Za-z]', var) is not None:
            popup(title="", message=f'Only Client and Desc fields can contain alphabets.', corner_radius=2)
            return False
        
    return True


#
def check_empty(variables):
    for var in variables:
        if len(var) < 1:
            popup(title="", message=f'Fields must not be empty.', corner_radius=2)
            return False

    return True