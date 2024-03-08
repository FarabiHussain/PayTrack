import variables as vars
import customtkinter as ctk
from CTkXYFrame import *


def clear_fields():
    vars.form["rate_input"].delete(0, "end")
    vars.form["description_input"].delete(0, "end")
    vars.form["qty_input"].delete(0, "end")
    vars.form["gst_input"].delete(0, "end")
    vars.form["pst_input"].delete(0, "end")

    vars.form["qty_input"].insert("end", 1)
    vars.form["gst_input"].insert("end", 5.0)
    vars.form["pst_input"].insert("end", 7.0)


def add_to_invoice():

    vars.form['scr_frame'].destroy()
    vars.form['scr_frame'] = CTkXYFrame(vars.root, corner_radius=0, border_width=0, width=330, height=230)
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

    print(new_item)

    vars.items.append(new_item)

    for entry in range(len(vars.items)):
        for col_idx, col_name in enumerate(['desc', 'qty']):
            col_width = 0

            if (col_idx == 0):
                col_width = 170
            elif (col_idx == 1):
                col_width = 50

            ctk.CTkLabel(
                vars.form['scr_frame'], text=vars.items[entry][col_name], fg_color='white', corner_radius=4, width=col_width
            ).grid(row=entry, column=col_idx, pady=5, padx=5)

        row_rate = int(vars.items[entry]['rate'])
        row_qty = int(vars.items[entry]['qty'])
        row_gst = float(vars.items[entry]['gst'])
        row_pst = float(vars.items[entry]['pst'])

        row_gst_amount = float((row_rate/100)*row_gst)
        row_pst_amount = float((row_rate/100)*row_pst)

        total_row_charge = (row_rate*row_qty) + row_gst_amount + row_pst_amount

        vars.cumulative_gst += row_gst_amount
        vars.cumulative_pst += row_pst_amount
        vars.cumulative_total += row_rate

        vars.form['gst_display_amount'].configure(text="$" + '{:.2f}'.format(vars.cumulative_gst))
        vars.form['pst_display_amount'].configure(text="$" + '{:.2f}'.format(vars.cumulative_pst))
        vars.form['total_display_amount'].configure(text="$" + '{:.2f}'.format(vars.cumulative_total))

        ctk.CTkLabel(
            vars.form['scr_frame'], text='{:.2f}'.format(total_row_charge), fg_color='white', corner_radius=4, width=80
        ).grid(row=entry, column=(col_idx + 1), pady=5, padx=5)

