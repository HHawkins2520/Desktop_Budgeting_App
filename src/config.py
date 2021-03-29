from tkinter import *
from Account import *



# CONSTANTS
WINDOW = Tk()
SCREEN_W = WINDOW.winfo_screenwidth()
SCREEN_H = WINDOW.winfo_screenheight()
WIN_W = int(SCREEN_W*0.6)
WIN_H = int(SCREEN_H*0.75)
FONT = "Terminal"
ACCOUNT = Account(name="Hannah", startAmount=100)



# WINDOW CONFIG
WINDOW.title("My Budget App")
WINDOW.configure(width=WIN_W, height=WIN_H)
WINDOW.geometry("+{}+{}".format(int(SCREEN_W/2 - WIN_W/2), int(SCREEN_H/2 - WIN_H/2)))
WINDOW.minsize(360, int(WIN_H*(1/3)+50))
WINDOW.maxsize(WIN_W, WIN_H)