from tkinter import StringVar
import customtkinter as ctk, os
from PIL import Image
from path_manager import resource_path


## initalize the variables to be used throughout the app
def init():
    global screen_sizes, form, root, popups, cwd, icons, items, font_family, search_window
    global drp_values, drp_list, drp_str_var
    global cumulative_gst, cumulative_pst, cumulative_total
    global radio_var

    cwd = os.getcwd()

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.resizable(False, False)
    font_family = ctk.CTkFont(family="Roboto Bold")

    screen_sizes = {"ws": root.winfo_screenwidth(), "hs": root.winfo_screenheight()}
    form = {"version": "v1.0.0"}
    popups = {"printer": None, "history": None, "elem": {}}

    icons = {}
    icons_specs = {
        "folder": None,
        "clear": None,
        "search": None,
        "docx": None,
        "add_item": None,
        "adjust_rate": None,
        "select_item": None,
        "delete_item": None,
        "empty_item": None,
        "open": None,
    }

    # define the
    for icon_name in list(icons_specs.keys()):
        icons_specs[icon_name] = Image.open(
            resource_path("assets\\icons\\" + icon_name + ".png")
        )

        img_size = icons_specs[icon_name].size
        img_ratio = img_size[0]/img_size[1]

        icons[icon_name] = ctk.CTkImage(
            light_image=None,
            dark_image=icons_specs[icon_name],
            # size=icons_specs[icon_name].size,
            size=(25*img_ratio, 25),
        )

    drp_values = {
        "Immigration Services": 500.0,
        "Notary": 30.0,
        "Affidavit": 100.0,
        "Invitation Letter": 100.0,
        "Government Fees": 50.0,
    }

    drp_list = list(drp_values.keys())
    drp_str_var = StringVar(root, value='Immigration Services')

    cumulative_gst = 0
    cumulative_pst = 0
    cumulative_total = 0

    # Table data in a form of list
    items = []

    search_window = {
        "popup": None
    }

    radio_var = StringVar(value="")

