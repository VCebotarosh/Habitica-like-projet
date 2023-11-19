import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget,QMainWindow
from PyQt5 import QtGui
import sqlite3
import functions
# from addtask import Ui_AddTaskWindow
# from switchtask import Ui_Dialog
# from deletetask import Ui_deleteTask
import hashlib
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui",self)
        self.pushButton.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotocreate)
    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocreate(self):
        create=CreateAccountScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex()+1)

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.login_function)

    def login_function(self):
        user=self.usernamefield.text()
        password=self.passwordfield.text()
        if len(user)==0 or len(password)==0:
            self.eroare.setText("Please input all the fields")
        else:
            connection=sqlite3.connect("habitica.db")
            cursor=connection.cursor()
            cursor.execute("SELECT password FROM login_info WHERE username=?",(user,))
            if cursor.fetchone()[0]==hashlib.sha256(password.encode('utf-8')).hexdigest():
                self.user=MainScreen(user,password)
                widget.addWidget(self.user)
                widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                self.eroare.setText("Invalid username and/or password")

class MainScreen(QMainWindow):
    def __init__(self,username,password):
        self.username=username
        self.password=password
        super(MainScreen, self).__init__()
        loadUi("mainp.ui",self)
        self.image_label.setPixmap(QtGui.QPixmap("monster-8bit-pet-21.svg"))
        self.progressBar.setValue(0)
        self.updateProgressBar()
        self.tableWidget_today.setColumnWidth(0,221)
        self.tableWidget_today.setHorizontalHeaderLabels(["TOOD"])
        self.tableWidget_month.setColumnWidth(0,221)
        self.tableWidget_month.setHorizontalHeaderLabels(["ToDos"])
        self.tableWidget_year.setColumnWidth(0,221)
        self.tableWidget_year.setHorizontalHeaderLabels(["TODO"])
        self.show_today_Button.clicked.connect(lambda : self.show_data("Today"))
        self.show_month_Button.clicked.connect(lambda : self.show_data("Month"))
        self.show_year_Button.clicked.connect(lambda : self.show_data("Year"))
        self.add_today_Button.clicked.connect(lambda : self.add("Today"))
        self.add_month_Button.clicked.connect(lambda : self.add("Month"))
        self.add_year_Button.clicked.connect(lambda : self.add("Year"))
        self.save_today_Button.clicked.connect(lambda : self.save_changes("Today"))
        self.save_month_Button.clicked.connect(lambda : self.save_changes("Month"))        
        self.save_year_Button.clicked.connect(lambda : self.save_changes("Year"))
        self.remove_today_Button.clicked.connect(lambda : self.remove_task("Today"))
        self.remove_month_Button.clicked.connect(lambda : self.remove_task("Month"))
        self.remove_year_Button.clicked.connect(lambda : self.remove_task("Year"))

    def show_data(self,deadline):
        tabel=""
        print(deadline)
        if deadline=="Today":
            tabel=self.tableWidget_today
        elif deadline=="Month":
            tabel=self.tableWidget_month
        elif deadline=="Year":
            tabel=self.tableWidget_year
        connection=sqlite3.connect("habitica.db")
        cursor=connection.cursor()
        tablerow=0
        tasks=list(cursor.execute("SELECT * FROM tasks WHERE deadline=?",(deadline.lower(),)))
        tabel.setRowCount(len(tasks))
        for task in tasks:    
            tabel.setItem(tablerow,0,QtWidgets.QTableWidgetItem(task[1]))
            tablerow+=1
        connection.close()
    def add(self,deadline):
        if deadline=="Today":
            tabel=self.tableWidget_today
        elif deadline=="Month":
            tabel=self.tableWidget_month
        elif deadline=="Year":
            tabel=self.tableWidget_year
        row=tabel.rowCount()
        tabel.insertRow(row)
        tabel.setItem(row,0,QtWidgets.QTableWidgetItem(""))
    def remove_task(self,deadline):
        if deadline=="Today":
            tabel=self.tableWidget_today
        elif deadline=="Month":
            tabel=self.tableWidget_month
        elif deadline=="Year":
            tabel=self.tableWidget_year
        selected = tabel.selectedIndexes()
        if selected:
           rows = list(i.row() for i in selected)
        else:
            rows=[tabel.rowCount()-1]
        connection=functions.set_database_connection()
        functions.remove_task(connection,rows,deadline.lower())
        for row in sorted(rows, reverse=True):
            tabel.removeRow(row)
    def save_changes(self,deadline):
        if deadline=="Today":
            tabel=self.tableWidget_today
        elif deadline=="Month":
            tabel=self.tableWidget_month
        elif deadline=="Year":
            tabel=self.tableWidget_year
        row=tabel.rowCount()-1
        ceva=list(tabel.item(i,0) for i in range(row+1))
        tasks=list(task.text() for task in ceva)
        connection=functions.set_database_connection()
        cursor=connection.cursor()
        cursor.execute("DELETE FROM tasks where deadline=? ",(deadline.lower(),))
        functions.add_task(connection,tasks,deadline.lower())
    def updateProgressBar(self):
        for i in range(2,100,10):
            self.progressBar.setValue(i)
class CreateAccountScreen(QDialog):
    def __init__(self):
        super(CreateAccountScreen, self).__init__()
        loadUi("create.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.repeatpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.create.clicked.connect(self.create_account_function)
    def create_account_function(self):
        user1=self.usernamefield.text()
        password1=self.passwordfield.text()
        repeated_password1=self.repeatpassword.text()
        if len(user1)==0 or len(password1)==0 or len(repeated_password1)==0:
            self.eroare.setText("Please input all the fields")
        elif password1!=repeated_password1:
            self.eroare.setText("Passwords do not match")
        else:
            connection=sqlite3.connect("habitica.db")
            cursor=connection.cursor()
            data=[user1,hashlib.sha256(password1.encode('utf-8')).hexdigest()]
            cursor.execute("INSERT INTO login_info (username, password) VALUES (?,?)",data)
            connection.commit()
            connection.close()
            print("Successfully created a new account")
            self.eroare.setText("")    
# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")