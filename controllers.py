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

class Controller(ConcreteObserver):
    def __init__(self, root, model):
        self.name = "Controller"
        self.root = root
        self.model = model
        self.model.attach(self)
        
        self.current_view = None
        self.show_login()
    
    def show_view(self, view_class, *args):
        if self.current_view:
            self.current_view.destroy()
        
        self.current_view = view_class(self.root, self, *args)
        self.current_view.pack()
    
    def show_login(self):
        self.show_view(LoginView)
    
    def show_main_menu(self):
        self.show_view(MainMenuView)
    
    def show_qcm_list(self):
        self.show_view(QCMListView)
    
    def show_create_qcm(self):
        self.show_view(CreateQCMView)
    
    def show_create_questions(self, num_questions, title):
        self.show_view(CreateQuestionsView, num_questions, title)
    
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


