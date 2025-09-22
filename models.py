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
import json
from observer import Subject

class UserModel(Subject):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.conn = sqlite3.connect('qcm.db')

    def register_user(self, username, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                          (username, password))
            self.conn.commit()
            self.notify()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", 
                      (username, password))
        user = cursor.fetchone()
        if user:
            self.current_user = {'id': user[0], 'username': username}
            self.notify()
            return True
        return False

    def get_available_qcms(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT q.id, q.title, q.questions_json, q.creator_id, u.username, s.score
            FROM qcms q
            JOIN users u ON q.creator_id = u.id
            LEFT JOIN scores s ON s.qcm_id = q.id AND s.user_id = ?
        ''', (self.current_user['id'],))
        return cursor.fetchall()
    
    def get_users(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM users;''')
        self.notify()
        return cursor.fetchall()
    
    def delete_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=?;", (username))
        self.conn.commit()
        self.notify()
    
    def update_user_password(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET password=? WHERE username=?;",
                      (password, username))
        self.conn.commit()
        self.notify()

    def save_qcm(self, title, questions):
        questions_json = json.dumps(questions)
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO qcms (title, creator_id, questions_json) VALUES (?, ?, ?)",
                      (title, self.current_user['id'], questions_json))
        self.conn.commit()
        self.notify()

    def save_score(self, qcm_id, score):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO scores (user_id, qcm_id, score)
            VALUES (?, ?, ?)
        ''', (self.current_user['id'], qcm_id, score))
        self.conn.commit()
        self.notify()
    
    def get_qcm_by_title(self, title):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM qcms WHERE title = ?", (title,))
        return cursor.fetchone()
    
    def get_data(self):
        return "Data"

    def get_qcm_by_id(self, qcm_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM qcms WHERE id = ?", (qcm_id,))
        return cursor.fetchone()
    
    def get_qcm_id_by_name(self, qcm_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM qcms WHERE title = ?", (qcm_name,))
        return cursor.fetchone()[0]
    
    def save_score(self, qcm_id, score):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO scores (user_id, qcm_id, score)
            VALUES (?, ?, ?)
        ''', (self.current_user['id'], qcm_id, score))
        self.conn.commit()
        self.notify()


if   __name__ == "__main__" :
    model=UserModel()
    crud = ""
    while crud != "q":
        crud=input("choose CRUD (0,1,2,3) or (q) to quit : ")
        if crud != "q":
            crud=int(crud)
        if crud==0 :
            test_user=["test_user","test_password"]
            model.register_user(test_user[0], test_user[1])
            model.get_users()
        elif  crud==1 :
            for name in model.get_users():
                print("user : ", name)
        elif  crud==2 :
            test_user=["test_user","new_password"]
            model.update_user_password(test_user[0], test_user[1])
            model.get_users()
        elif crud==3 :
            username=input("type username to delete: ")
            model.delete_user(username)
            for name in model.get_users():
                print("user : ", name)