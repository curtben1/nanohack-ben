import math
import random
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import traceback
import socket
import pickle
from sys import getsizeof

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from os import urandom

# note: can use window properties to pass variables betwwen


class Window(QWidget):


    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Placeholders
        self.temperature = 0
        self.capacity = 12
        self.people = 0


        self.setGeometry(100, 100, 1280, 720)

        # title label
        self.titleLabel = QLabel("ROOMIFY ROOM 1")
        self.titleLabel.setFont(QFont('Arial',30))

        self.titleRow = QHBoxLayout()
        self.firstRow = QHBoxLayout()

        # capacity
        self.capacityButton = QPushButton("Room Capacity: ")
        self.capacityButton.setFont(QFont('Arial',30))
        self.capacityButton.setFixedSize(500,200)
        self.capacityButton.setStyleSheet("background-color : white")
        self.firstRow.addWidget(self.capacityButton)

        # temperature
        self.temperatureButton = QPushButton("Room Temperature: ")
        self.temperatureButton.setFont(QFont('Arial',30))
        self.temperatureButton.setFixedSize(500,200)
        self.temperatureButton.setStyleSheet("background-color : white")
        self.firstRow.addWidget(self.temperatureButton)

        
        
        self.thread = Worker(self)
        self.thread.start()
        self.thread.finished.connect(self.threadDied)

        self.thread.tempColorSig.connect(self.tempChanger)
        self.thread.capColorSig.connect(self.capacityChanger)


        self.windowLayout = QVBoxLayout()
        self.windowLayout.addWidget(self.titleLabel)
        self.windowLayout.addLayout(self.titleRow)
        self.windowLayout.addLayout(self.firstRow)


        self.setLayout(self.windowLayout)
        self.setWindowTitle(self.tr("Roomify Client"))


    def tempChanger(self):
        self.temperatureButton.setStyleSheet("background-color : "+ self.thread.tempColor)
        self.temperatureButton.setText("Room Temperature: "+str(self.thread.temperature))

    def capacityChanger(self):
        self.capacityButton.setStyleSheet("background-color : "+ self.thread.capColor)
        self.capacityButton.setText("Room Capacity: "+str(self.thread.people) + "/" + str(self.thread.capacity))

    def threadDied(self):
        print("thread died")

        # ran when thread dies, use as when quit program


class Worker(QThread):
    tempColorSig = pyqtSignal()
    capColorSig = pyqtSignal()

    def __init__(self, window, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        
        

    def __del__(self):
        self.exiting = True
        self.wait()



    def run(self):
        while True:
            self.manageTemps()
            self.manageCapacity()

    def manageTemps(self):
        
        self.getTemps()

        if self.temperature >= 22:
            self.tempColor = "red"
        else:
            self.tempColor = "green"
        self.tempColorSig.emit()
        
    def manageCapacity(self):
        
        self.getCapacity()
        

        if self.people > self.capacity:
            self.capColor = "red"
        else:
            self.capColor = "green"
        self.capColorSig.emit()
    
    def getTemps(self):
        self.temperature = 22

    def getCapacity(self):
        self.capacity = 20
        self.people = int(input("how many people"))

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
