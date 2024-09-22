import numpy as np
import random
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import collections.abc
import collections
collections.MutableMapping = collections.abc.MutableMapping
import math
import cv2
from dronekit import connect, Command, LocationGlobalRelative, VehicleMode
from pymavlink import mavutil
import time
from ultralytics import YOLO
import requests
import json
from datetime import datetime
import time
import torch
import ctypes
from torch import tensor
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui,QtCore,QtSvg
from PyQt5.QtCore import QTimer
from qfi import qfi_ADI, qfi_ALT, qfi_SI, qfi_HSI, qfi_VSI, qfi_TC
import math
import time
from PyQt5.QtCore import QTimer
from datetime import datetime
import  serial
import serial.tools.list_ports

vehicle = connect("tcp:127.0.0.1:5762", wait_ready=True,timeout=100)
#
# self.degerler=["%.2f" % math.degrees(vehicle.attitude.roll),vehicle.heading,"%.2f" % vehicle.location.global_relative_frame.alt
# ,vehicle.location.global_relative_frame.lat,vehicle.location.global_relative_frame.lon,"%.2f" % vehicle.groundspeed,
# "%.2f" % vehicle.airspeed,"%.2f" % (vehicle.attitude.pitch * 180.0 / 3.14159),vehicle.battery.level]
i=0

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setWindowTitle("Stm Real Time Simulator")

        self.mainLayout=QVBoxLayout()
        self.upLayout=QFormLayout()
        self.layout=QGridLayout()

        self.mainLayout.addLayout(self.upLayout,30)
        self.mainLayout.addLayout(self.layout,70)

        
        
        self.adi = qfi_HSI.qfi_HSI(self)
        self.adi.resize(300, 300)
        self.adi.reinit()
        self.layout.addWidget(self.adi, 0, 0)

        self.setLayout(self.mainLayout)
        
        self.timer=QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update1)
        self.show()

        self.timer.start()

    def update1(self):
        global i
        alt = vehicle.location.global_relative_frame.alt
        
        
        print(alt)
        
        #self.adi.setAltitude(float(alt))
        #
        #self.adi.viewUpdate.emit()
        
    def connect_system(self):
        print("Connecting System")
        self.ser = serial.Serial(self.port.currentText(), 9600)
        print(str(self.port)+" Connecting Port")
        self.timer.start()

    def list_port(self):
        ports = list(serial.tools.list_ports.comports())
       
        print(ports)
        for p in ports:
            print(p)
            self.port.addItems(p)

    def exit(self):
        self.timer.stop()
        sys.exit()
        

    
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())