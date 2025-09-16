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
from models import UserModel
from controllers import Controller

def initialize_menu():
    menubar = Menu(root)
    root.config(menu=menubar)

    file_menu = Menu(menubar)

    file_menu.add_command(label='New', underline=0, accelerator="CTRL+N")
    
    file_menu.add_command(
        label='Exit',
        underline=0, 
        accelerator="CTRL+Q",
        command=root.destroy
    )

    menubar.add_cascade(
        label="File",
        menu=file_menu,
        underline=0
    )

    #file_menu.bind_all("<Control-n>", lambda x: self.do_something())
    file_menu.bind_all("<Control-q>", lambda x: root.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("QCM Application")
    root.geometry("600x400")

    initialize_menu()

    model = UserModel()
    controller = Controller(root, model)
    
    root.mainloop()