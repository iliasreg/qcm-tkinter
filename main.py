# coding: utf-8
import sys
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 :
    import tkinter as tk
    from tkinter import filedialog
else :
    if __name__ == "__main__" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 

from tkinter import Menu
from tkinter import messagebox
from models import UserModel
from controllers import Controller

def initialize_menu():
    menubar = Menu(root)
    root.config(menu=menubar)

    file_menu = Menu(menubar, tearoff=False)  # tearoff=False removes the dashed line

    file_menu.add_command(
        label='New',
        underline=0,
        accelerator="Ctrl+N",
        command=lambda: print("New file created!")  # replace with your action
    )

    file_menu.add_command(
        label='Exit',
        underline=0, 
        accelerator="Ctrl+Q",
        command=exit
    )

    menubar.add_cascade(
        label="File",
        menu=file_menu,
        underline=0
    )

    # bind shortcuts to root instead of file_menu
    root.bind_all("<Control-n>", lambda event: print("New file created!"))
    root.bind_all("<Control-q>", exit)

def exit(event= None):
    answer = messagebox.askyesno("Confirm Exit", "Are you sure you want to quit?")
    if answer:
        root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("QCM Application")
    root.geometry("600x400")

    model = UserModel()
    controller = Controller(root, model)
    
    root.mainloop()