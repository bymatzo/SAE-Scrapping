from imports import *
from variables import *


ctk.set_default_color_theme("Sources/pink.json")

def combobox_callback(choice):
    print("choix : ", choice)

class App(ctk.CTk):
    def __init__(self): 
        super().__init__()
        self.combobox_var = ctk.StringVar(value="Spotify")
        self.geometry("600x500")
        self.title("Wrap plateformes musicales")

        self.grid_columnconfigure(0, weight=1)
        self.combobox = ctk.CTkComboBox(self, values=["Spotify", "Deezer", "Apple music"], command=combobox_callback, variable = self.combobox_var)
        self.combobox.grid(row = 0 , column = 0 , padx = 20 , pady = 10)