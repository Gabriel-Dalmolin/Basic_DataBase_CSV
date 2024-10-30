from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer
import sys
import pandas as pd
import csv
import datetime

diretorio = "H:data.csv"
pd.set_option('display.max_rows', 9999)

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("DatabaseUI.ui", self)
        self.setWindowTitle("Pagina de input")
        self.setStyleSheet("""
        font-size: 18px;
                           """)
        
        self.Timer = QTimer()
        self.Timer.setInterval(2000)
        self.Timer.timeout.connect(self.afterClick)

        self.inputUsuario = self.findChild(QtWidgets.QLineEdit, "inputUsuario")
        self.inputID = self.findChild(QtWidgets.QLineEdit, "inputID")
        self.inputTempo = self.findChild(QtWidgets.QLineEdit, "inputTempo")
        self.inputProjeto = self.findChild(QtWidgets.QLineEdit, "inputProjeto")
        self.buttonAcess = self.findChild(QtWidgets.QPushButton, "botaoAcessar")
        self.buttonOk = self.findChild(QtWidgets.QPushButton, "botaoOk")
        self.buttonCancel = self.findChild(QtWidgets.QPushButton, "botaoCancelar")
        
        self.buttonOk.clicked.connect(self.submit)
        self.buttonAcess.clicked.connect(self.openAccess)
        self.buttonCancel.clicked.connect(self.cancel)

    def cancel(self):
        quit()

    def submit(self):
        now = datetime.datetime.now() ## Pegando data
        now_input = str(now.day) + "/" + str(now.month) + "/" + str(now.year) + " " + str(now.hour) + ":" + str(now.minute)

        self.usuario = self.inputUsuario.text()
        self.ID = self.inputID.text()


        self.tempo = self.inputTempo.text().replace(" ", "").replace(",",".")
        if ":" in self.tempo:
            horas, minutos = self.tempo.split(":")
            self.tempo = int(horas)+(int(minutos)/60)



        self.Projeto = self.inputProjeto.text()
        self.insert_data = [self.usuario, self.ID, self.tempo, self.Projeto, now_input]
        if diretorio == "":
            with open("data.csv", mode="a", newline="", encoding="utf-8") as data:
                writer = csv.writer(data)
                writer.writerow(self.insert_data)
        else:
            with open(diretorio, mode="a", newline="", encoding="utf-8") as data:
                writer = csv.writer(data)
                writer.writerow(self.insert_data)
        self.buttonOk.setText("Dados inseridos")
        
        self.Timer.start()
        
    def afterClick(self):
        self.buttonOk.setText("Ok")
        self.Timer.stop()
        
    def openAccess(self):
        self.window = Table()
        self.window.show()



class Table(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Base de dados")
        self.setStyleSheet("""
        font-size: 18px;
                           """)
        
        if diretorio == "":
            self.df = pd.read_csv("data.csv")
        else:
            self.df = pd.read_csv(diretorio)

        self.layout = QtWidgets.QGridLayout()

        self.tableWidget = QtWidgets.QTableWidget()
        self.layout.addWidget(self.tableWidget,0,0)
        
        self.idInput = QtWidgets.QLineEdit()
        self.layout.addWidget(self.idInput,1,0)

        self.sumButton1 = QtWidgets.QPushButton("Somar tempo pelo Projeto")
        self.sumButton1.clicked.connect(self.sum_by_project)
        self.layout.addWidget(self.sumButton1,2,0)

        self.sumButton2 = QtWidgets.QPushButton("Somar tempo pela Maquina")
        self.sumButton2.clicked.connect(self.sum_by_machine)
        self.layout.addWidget(self.sumButton2,3,0)

        self.setLayout(self.layout)

        self.loadData()


    def loadData(self):
        self.tableWidget.setRowCount(len(self.df))
        self.tableWidget.setColumnCount(len(self.df.columns))
        self.tableWidget.setHorizontalHeaderLabels(self.df.columns)

        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(self.df.iat[i, j])))

    def sum_by_project(self):
        valuesSum = self.df[self.df["Projeto"] == self.idInput.text().replace(" ", "")]["Tempo"].sum()
        self.sumButton1.setText("Somar tempo pelo Projeto:  " + str(valuesSum))

    def sum_by_machine(self):
        valuesSum = self.df[self.df["ID"] == str(self.idInput.text().replace(" ", ""))]["Tempo"].sum()
        self.sumButton2.setText("Somar tempo pela Maquina:  " + str(valuesSum))

app = QtWidgets.QApplication(sys.argv)
UI = MainWindow()
UI.show()
app.exec()
