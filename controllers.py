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

import json
from views import *
from tkinter import Menu,messagebox

class Controller(ConcreteObserver):
    def __init__(self, root, model):
        self.name = "Controller"
        self.root = root
        self.model = model
        self.model.attach(self)

        self.menubar = Menu(self.root)
        self.root.configure(menu=self.menubar)

        self.menubar = Menu(self.root)
        self.root.configure(menu=self.menubar)
        
        self.current_view = None
        self.show_login()

    def setup_menu(self,context="login"):
        self.menubar.delete(0,"end")

        self.root.unbind_all("<Control-n>")
        self.root.unbind_all("<Control-p>")
        self.root.unbind_all("<Control-q>")
        self.root.unbind_all("<Control-l>")
        self.root.unbind_all("<Control-h>")
        self.root.unbind_all("<Control-m>")

        self.file_menu = Menu(self.menubar)

        if context == "login":
            self.file_menu.add_command(label="Quit",accelerator="Ctrl+q",command=self.exit)
            self.root.bind_all("<Control-q>", lambda e: self.exit())

        elif context == "main":
            self.file_menu.add_command(label="New",accelerator="Ctrl+n",command=self.show_create_qcm)
            self.file_menu.add_command(label="Play", accelerator="Ctrl+P",command=self.show_qcm_list)
            self.file_menu.add_command(label="Logout", accelerator="Ctrl+L",command=self.logout)
            self.file_menu.add_separator()
            self.file_menu.add_command(label="Quit", accelerator="Ctrl+Q",command=self.exit)

            self.root.bind_all("<Control-n>", lambda e: self.show_create_qcm())
            self.root.bind_all("<Control-p>", lambda e: self.show_qcm_list())
            self.root.bind_all("<Control-l>", lambda e: self.logout())
            self.root.bind_all("<Control-q>", lambda e: self.exit())

        elif context == "create_qcm":
            self.file_menu.add_command(label="Help", accelerator="Ctrl+H",command=self.show_help)
            self.file_menu.add_command(label="Return to Main Menu", accelerator="Ctrl+M",command=self.show_main_menu)
            self.file_menu.add_separator()
            self.file_menu.add_command(label="Quit", accelerator="Ctrl+Q",command=self.exit)

            self.root.bind_all("<Control-h>", lambda e: self.show_help())
            self.root.bind_all("<Control-m>", lambda e: self.show_main_menu())
            self.root.bind_all("<Control-q>", lambda e: self.exit())

        elif context == "qcm_list":
            self.file_menu.add_command(label="Return to Main Menu", accelerator="Ctrl+M",command=self.show_main_menu)
            self.file_menu.add_separator()
            self.file_menu.add_command(label="Quit", accelerator="Ctrl+Q",command=self.exit)

            self.root.bind_all("<Control-m>", lambda e: self.show_main_menu())
            self.root.bind_all("<Control-q>", lambda e: self.exit())

        self.menubar.add_cascade(label="File", menu=self.file_menu)

    def show_help(self):
        messagebox.showinfo("Help", "Fill in the QCM title, number of questions, then press 'Create Questions'.")

    def exit(self):
        ans = messagebox.askyesno("Confirm Exit", "Are you sure you want to quit?")
        if ans:
            self.root.destroy()
    
    def show_view(self, view_class, *args,context="login"):
        if self.current_view:
            self.current_view.destroy()
        
        self.current_view = view_class(self.root, self, *args)
        self.current_view.pack(fill="both", expand=True)
        self.setup_menu(context)
    
    def show_login(self):
        self.show_view(LoginView,context="login")
    
    def show_main_menu(self):
        self.show_view(MainMenuView,context="main")
    
    def show_qcm_list(self):
        self.show_view(QCMListView,context="qcm_list")
    
    def show_create_qcm(self):
        self.show_view(CreateQCMView,context="create_qcm")
    
    def show_create_questions(self, num_questions, title):
        self.show_view(QuestionsView, num_questions, title)
    
    def play_qcm(self, qcm_id):
        qcm = self.model.get_qcm_by_id(qcm_id)
        qcm_title = qcm[1]
        qcm_questions = qcm[3]
        if qcm:
            questions = json.loads(qcm_questions)
            self.show_view(PlayQCMView, qcm_title, self.model.get_qcm_id_by_name(qcm_title), questions)
    
    def login(self, username, password):
        if self.model.login_user(username, password):
            print("Login successful")
            self.show_main_menu()
        else:
            print("Login failed")
    
    def register(self, username, password):
        if self.model.register_user(username, password):
            print("Registration successful")
            self.model.login_user(username, password)
            self.show_main_menu()
        else:
            print("Registration failed")
    
    def logout(self):
        self.model.current_user = None
        self.model.notify()
        self.show_login()
    
    def get_current_user(self):
        return self.model.current_user['username'] if self.model.current_user else None
    
    def get_available_qcms(self):
        return self.model.get_available_qcms()
    
    def save_qcm(self, title, questions):
        self.model.save_qcm(title, questions)
        self.show_main_menu()
    
    def save_score(self, qcm_id, score):
       self.model.save_score(qcm_id, score)
       self.show_main_menu()


if   __name__ == "__main__" :
    pass

