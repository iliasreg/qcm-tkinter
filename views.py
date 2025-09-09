# coding: utf-8
DEBUG=False

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

from models import Generator
from observer import Observer

class Screen(Observer) :
    def __init__(self,parent,bg="white",width=600,height=300):
        self.parent=parent
        self.bg=bg
        self.width,self.height=width,height
        self.color="red"
        # self.signals={}
        self.gui() 
        self.actions_binding()

    def get_parent(self) :
        return self.parent
    def set_parent(self,parent) :
        self.parent=parent
    def gui(self) :
        self.canvas=tk.Canvas(self.parent,bg=self.bg,width=self.width,height=self.height)
        
    def actions_binding(self) :
        if DEBUG :
            print(type(self).__name__+".actions_binding()")
        self.canvas.bind("<Configure>",self.resize)
        
    def update(self,subject):
        if subject :
            name=subject.get_name()
            if DEBUG :
                print(type(self).__name__+".update()")
                print(type(subject).__name__+".get_name() : ", name)
            signal=subject.get_signal()
            if signal :
                self.plot_signal(name,signal)
            else :
                print("no signal for subject: ",name)
        else :
            print("no subject to observe")
        return

    def resize(self,event):
        if DEBUG :
            print(type(self).__name__+".resize()")
            print("width,height : ",(event.width,event.height))
        self.width,self.height=event.width,event.height
        # TODO : manage grid and signal refresh in resizing()
    def layout(self) :
        self.canvas.pack()

if   __name__ == "__main__" :
   root=tk.Tk()
   model=Generator()
   view=Screen(root)
   view.layout()

   model.attach(view)
   model.set_name("X")
   model.read()
   model.notify()

   root.mainloop()

