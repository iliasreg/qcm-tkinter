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

from models import Generator
from views import Screen

class Control :
    def __init__(self,parent,model,view):
        self.parent=parent
        self.model=model
        self.view=view
        self.gui()
        self.actions_binding()

    def gui(self):
        self.frame=tk.LabelFrame(self.parent,text=self.model.get_name()) 
        self.scale_frequency()
        self.spinbox_samples()
    
    def scale_frequency(self) :
        self.var_freq=tk.IntVar()
        self.var_freq.set(self.model.get_frequency())
        self.scale_freq=tk.Scale(self.frame,variable=self.var_freq,
                             label="Frequency",
                             orient="horizontal",length=250,
                             from_=0,to=100,tickinterval=10)
    def spinbox_samples(self) :
        self.var_samples=tk.IntVar()
        self.spinbox_samples = tk.Spinbox(self.frame, from_=10, to=500, increment=10, bd=5,textvariable=self.var_samples) #,command=self.on_samples_action)
        self.var_samples.set(self.model.get_samples()) 
        
    def actions_binding(self) :
        self.scale_freq.bind("<B1-Motion>",self.on_frequency_action)
        self.spinbox_samples.bind("<Button-1>",self.on_samples_action)

    def on_frequency_action(self,event):
        if  self.model.get_frequency() != self.var_freq.get() :
            self.model.set_frequency(self.var_freq.get())
            self.model.generate()
    def on_samples_action(self,event):
        samples=int(self.var_samples.get() )
        print(samples)
        if  self.model.get_samples() != samples :
            self.model.set_samples(samples)
            self.model.generate()

    def layout(self,side="top") :
        # self.frame.pack(side=side)
        self.frame.pack(expand=1,fill="x",padx=20)
        self.scale_freq.pack()
        self.spinbox_samples.pack()

if   __name__ == "__main__" :
   root=tk.Tk()
   model=Generator()
   view=Screen(root)
   view.layout()
   model.attach(view)
   model.read()
   control=Control(root,model,view)
   control.layout()
   root.mainloop()

