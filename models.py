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
from observer import Subject

class Qcm(Subject) :
    def __init__(self) :
        Subject.__init__(self)
        self.id=id
        self.name=""
        self.filePath=""
    
    def get_name(self) :
        return self.name
    def set_name(self,name) :
        self.name=name
    def get_filePath(self) :
        return self.filePath
    def set_filePath(self,newPath) :
        self.filePath=newPath

    def create(self,db="qcm.db") :
        connect=sqlite3.connect(db)
        cursor=connect.cursor()   
        query="INSERT OR IGNORE INTO qcm(name,filepath) VALUES(?,?)"
        to_insert=self.get_name(),self.get_filePath()
        result = cursor.execute(query,to_insert)
        print(result)
        connect.commit()
        cursor.close()
        connect.close()

    def read(self,db="qcm.db") :
        connect=sqlite3.connect(db)
        cursor=connect.cursor()
        query="SELECT name, filepath FROM qcm;"
        results=cursor.execute(query)
        if results :
            for result in results :
                print("Results: ", result)
        else :
            print("No qcms inserted yet")
        cursor.close()
        connect.close()
        self.notify()

    def update(self,name, filePath, db="qcm.db") :
        connect=sqlite3.connect(db)
        cursor=connect.cursor()
        to_update=name, filePath,  self.get_name()
        query="UPDATE qcm SET name=?, filepath=? WHERE name=?;"
        cursor.execute(query,to_update)
        connect.commit()
        cursor.close()
        connect.close()
        self.notify()

    def delete(self,db="qcm.db") :
        connect=sqlite3.connect(db)
        cursor=connect.cursor()
        to_delete=self.get_name(),
        query="DELETE FROM qcm WHERE name=?;"
        cursor.execute(query,to_delete)
        connect.commit()
        cursor.close()
        connect.close()
        self.notify()


class User(Subject) :
    def __init__(self) :
        Subject.__init__(self)
        self.id=id
        self.name=""
        self.password=""
    
    def get_name(self) :
        return self.name
    def set_name(self,name) :
        self.name=name
    def get_password(self) :
        return self.password
    def set_password(self,newPass) :
        self.password=newPass

    def create(self,db="qcm.db") :
        connect=sqlite3.connect(db)
        cursor=connect.cursor()   
        query="INSERT OR IGNORE INTO users(name,password) VALUES(?,?)"
        to_insert=self.get_name(),self.get_password()
        cursor.execute(query,to_insert)
        connect.commit()
        cursor.close()
        connect.close()

    def read(self,db="qcm.db") :
        connect=sqlite3.connect(db)
        cursor=connect.cursor()
        query="SELECT name, password FROM users;"
        results=cursor.execute(query)
        if results :
            for result in results :
                print("Results: ", result)
        else :
            print("No users inserted yet")
        cursor.close()
        connect.close()
        self.notify()

    def update(self,name, password, db="qcm.db") :
        connect=sqlite3.connect(db)
        cursor=connect.cursor()
        to_update=name, password,  self.get_name()
        query="UPDATE users SET name=?, password=? WHERE name=?;"
        cursor.execute(query,to_update)
        connect.commit()
        cursor.close()
        connect.close()
        self.notify()

    def delete(self,db="qcm.db") :
        connect=sqlite3.connect(db)
        cursor=connect.cursor()
        to_delete=self.get_name(),
        query="DELETE FROM users WHERE name=?;"
        cursor.execute(query,to_delete)
        connect.commit()
        cursor.close()
        connect.close()
        self.notify()


class Game(Subject) :
    def __init__(self) :
        Subject.__init__(self)
        self.id_qcm=id
        self.id_user=id
        self.score=0
    
    def get_score(self) :
        return self.score
    def set_score(self,newScore) :
        self.score = newScore

    def create(self, id_qcm, id_user, db="qcm.db") :
        connect=sqlite3.connect(db)
        cursor=connect.cursor()   
        query="INSERT OR IGNORE INTO game(id_qcm, id_user, score) VALUES(?,?,?)"
        to_insert=id_qcm, id_user, self.get_score()
        cursor.execute(query,to_insert)
        connect.commit()
        cursor.close()
        connect.close()

    def read(self,db="qcm.db") :
        connect=sqlite3.connect(db)
        cursor=connect.cursor()
        query="SELECT id_qcm, id_user, score FROM game;"
        results=cursor.execute(query)
        if results :
            for result in results :
                print("Results: ", result)
        else :
            print("No games inserted yet")
        cursor.close()
        connect.close()
        self.notify()

    def update(self,score, id_qcm, id_user, db="qcm.db") :
        connect=sqlite3.connect(db)
        cursor=connect.cursor()
        to_update=score, id_qcm,  id_user
        query="UPDATE game SET score=? WHERE id_qcm=? AND id_user=?;"
        cursor.execute(query,to_update)
        connect.commit()
        cursor.close()
        connect.close()
        self.notify()

    def delete(self,id_qcm, id_user,db="qcm.db") :
        connect=sqlite3.connect(db)
        cursor=connect.cursor()
        to_delete=id_qcm, id_user
        query="DELETE FROM game WHERE id_qcm=? AND id_user=?;"
        cursor.execute(query,to_delete)
        connect.commit()
        cursor.close()
        connect.close()
        self.notify()


if   __name__ == "__main__" :
    model=Qcm()
    model.set_name("tuto", "filepath")
    model.create()
    model.read()