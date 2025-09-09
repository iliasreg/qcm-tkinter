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

import sqlite3

from models import Generator
from views import Screen
from controllers import Control

class MainWindow(tk.Tk) :
    def __init__(self) :
        tk.Tk.__init__(self)
        self.title("CAI : TkInter")
        self.option_readfile("main.opt")
        self.menubar()
        self.create()

    def create(self) :
        model=Generator() 
        frame=tk.LabelFrame(self,name="generator_X") 
        view=Screen(frame)
        frame.pack()
        view.layout()
        model.attach(view)

        control=Control(self,model,view)
        control.layout()

    def menubar(self) :
        self.menubar=tk.Menu(self) 
        self.config(menu=self.menubar)

if __name__=="__main__" :
    app=MainWindow()
    app.mainloop()

