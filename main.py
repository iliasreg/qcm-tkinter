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


if __name__ == "__main__":
    root = tk.Tk()
    root.title("QCM Application")
    root.geometry("1000x400")
    root.attributes('-fullscreen', True)
    root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))

    model = UserModel()
    controller = Controller(root, model)
    
    root.mainloop()