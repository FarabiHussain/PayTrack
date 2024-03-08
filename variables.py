from tkinter import StringVar
import customtkinter as ctk, os, docx
from PIL import Image
from path_manager import resource_path


## initalize the variables to be used throughout the app
def init():
    global screen_sizes, form, root, popups, cwd, icons, items
    global drp_values, drp_list, drp_str_var
    global cumulative_gst, cumulative_pst, cumulative_total

    cwd = os.getcwd()

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.resizable(False, False)

    screen_sizes = {"ws": root.winfo_screenwidth(), "hs": root.winfo_screenheight()}
    form = {"version": "v1.0.0", "status": StringVar(value="Ready")}
    popups = {"printer": None, "history": None, "elem": {}}

    icons = {}
    icons_specs = {
        "folder": None,
        "clear": None,
        "docx": None,
        "add": None,
    }

    # define the
    for icon_name in list(icons_specs.keys()):
        icons_specs[icon_name] = Image.open(
            resource_path("assets\\icons\\" + icon_name + ".png")
        )

        icons[icon_name] = ctk.CTkImage(
            light_image=None,
            dark_image=icons_specs[icon_name],
            size=icons_specs[icon_name].size,
        )

    drp_values = {
        "Immigration Services": 500,
        "Notary": 30,
        "Affidavit": 100,
        "Invitation Letter": 100,
    }

    drp_list = list(drp_values.keys())
    drp_str_var = StringVar(root, value='Immigration Services')

    cumulative_gst = 0
    cumulative_pst = 0
    cumulative_total = 0

    # Table data in a form of list
    items = []