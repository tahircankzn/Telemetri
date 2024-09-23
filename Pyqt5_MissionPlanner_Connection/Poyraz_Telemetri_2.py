# 22.09.24 
# Telemetri gösterge panelleri eklendi ve test edildi
# 23.09.24 
# Telemetri gösterge panellerinin doğruluğu düzeltildi

import collections.abc
import collections
collections.MutableMapping = collections.abc.MutableMapping
from dronekit import connect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from qfi import qfi_ADI, qfi_ALT, qfi_SI, qfi_HSI, qfi_VSI, qfi_TC
import numpy as np
import math


class Telemetri(QWidget):
    def __init__(self):
        super().__init__()

        self.vehicle = connect("tcp:127.0.0.1:5762", wait_ready=True, timeout=100)
        print("bağlandı")

        # Gerekli Değişkenler
        self.telemetri_verileri = None

        # Arayüzün çalışması için başlatıcılar
        self.telemetriler()
        self.UI_starter()

    def UI_starter(self): # Gösterge panelini açar ve timer ile değerleri yeniler
        self.gostergeler()
        self.timerlar()

    def telemetriler(self): # Telemetri verileri güncellenir
    
        self.telemetri_verileri = {
            'altitude': self.vehicle.location.global_relative_frame.alt,
            'latitude': self.vehicle.location.global_frame.lat,
            'longitude': self.vehicle.location.global_frame.lon,
            'pitch': self.vehicle.attitude.pitch,
            'roll': self.vehicle.attitude.roll,
            'yaw': self.vehicle.attitude.yaw,
            'airspeed': self.vehicle.airspeed,
            'groundspeed': self.vehicle.groundspeed,
            'battery_voltage': self.vehicle.battery.voltage if self.vehicle.battery else None,
            'battery_current': self.vehicle.battery.current if self.vehicle.battery else None,
            'battery_percentage': self.vehicle.battery.level if self.vehicle.battery else None,
            'mode': self.vehicle.mode.name,
            'armed': self.vehicle.armed,
            'vertical_speed': self.vehicle.velocity[2]
        }

    def AnaDikeyLyout(self): # ANA DİKEY LAYOUT

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

    def IlkYatayLayout(self):
        
        self.horizontalLayout = QHBoxLayout()

        # qfi_ADI
        self.qfi_ADI = qfi_ADI.qfi_ADI(self)
        self.qfi_ADI.reinit()
        self.qfi_ADI.setFixedSize(300, 300)  
        self.horizontalLayout.addWidget(self.qfi_ADI) 

        # qfi_ALT
        self.qfi_ALT = qfi_ALT.qfi_ALT(self)
        self.qfi_ALT.reinit()
        self.qfi_ALT.setFixedSize(300, 300)  
        self.horizontalLayout.addWidget(self.qfi_ALT) 

        # qfi_SI
        self.qfi_SI = qfi_SI.qfi_SI(self)
        self.qfi_SI.reinit()
        self.qfi_SI.setFixedSize(300, 300)  
        self.horizontalLayout.addWidget(self.qfi_SI)

    def IkiciYatayLayout(self):
        
        self.horizontalLayout2 = QHBoxLayout()

        # qfi_HSI
        self.qfi_HSI = qfi_HSI.qfi_HSI(self)
        self.qfi_HSI.reinit()
        self.qfi_HSI.setFixedSize(300, 300)  
        self.horizontalLayout2.addWidget(self.qfi_HSI) 

        # qfi_VSI
        self.qfi_VSI = qfi_VSI.qfi_VSI(self)
        self.qfi_VSI.reinit()
        self.qfi_VSI.setFixedSize(300, 300)  
        self.horizontalLayout2.addWidget(self.qfi_VSI) 

        # qfi_TC
        self.qfi_TC = qfi_TC.qfi_TC(self)
        self.qfi_TC.reinit()
        self.qfi_TC.setFixedSize(300, 300)  
        self.horizontalLayout2.addWidget(self.qfi_TC)


    def gostergeler(self): # Gösterge panelleri

        self.setWindowTitle("BTÜ-POYRAZ TELEMETRİ SİSTEMİ")
        self.setStyleSheet("background-color: #292929")
        self.setWindowState(Qt.WindowMaximized)


        self.AnaDikeyLyout()
         
        self.IlkYatayLayout()
        self.mainLayout.addLayout(self.horizontalLayout)

        self.IkiciYatayLayout()
        self.mainLayout.addLayout(self.horizontalLayout2)

        self.show()


    def timerlar(self):

        # Telemetri Güncelleme
        self.telemetriler_t=QTimer()
        self.telemetriler_t.setInterval(1000)
        self.telemetriler_t.start()
        self.telemetriler_t.timeout.connect(self.telemetriler)

        # Gösterge Panel değerlerinin güncellenmesi
        self.degeryeinle_t=QTimer()
        self.degeryeinle_t.setInterval(100)
        self.degeryeinle_t.start()
        self.degeryeinle_t.timeout.connect(self.degeryeinle)
  

    def calculate_turn_rate(self):
        # Zaman aralığı ve yaw açısındaki değişimi kullanarak dönüş oranını hesabı
        delta_time = 1
        #yaw_change = self.vehicle.attitude.yaw - self.telemetri_verileri["yaw"]  
        yaw_change = self.telemetri_verileri["roll"]  
        return (yaw_change / delta_time )*10 * (1)
    

    def calculate_slip_skid(self):
        # Yüksek hız ve dönüş oranlarını dikkate alarak kayma hesabı
        slip = self.vehicle.groundspeed * math.sin(self.vehicle.attitude.roll) * (1)
        return slip


    def degeryeinle(self):
        

        self.qfi_ADI.setRoll(float(self.telemetri_verileri["roll"]*100))
        self.qfi_ADI.setPitch(float(self.telemetri_verileri["pitch"]*100))
        self.qfi_ADI.viewUpdate.emit()

        self.qfi_ALT.setAltitude(float(self.telemetri_verileri["altitude"]))
        self.qfi_ALT.viewUpdate.emit()
        
        self.qfi_SI.setSpeed(float(self.telemetri_verileri["groundspeed"]/2))
        self.qfi_SI.viewUpdate.emit()
        
        self.qfi_HSI.setHeading(float(self.telemetri_verileri["yaw"]* (180.0 / np.pi)))
        self.qfi_HSI.viewUpdate.emit()

        self.qfi_VSI.setClimbRate(float(self.telemetri_verileri["vertical_speed"]))
        self.qfi_VSI.viewUpdate.emit()
        
        self.qfi_TC.setTurnRate(float(self.calculate_turn_rate()))
        self.qfi_TC.setSlipSkid(float(self.calculate_slip_skid()))
        self.qfi_TC.viewUpdate.emit()

        print(float(self.calculate_turn_rate()),self.telemetri_verileri["yaw"]  )


    def exit(self):
        self.timer.stop()
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Telemetri()
    sys.exit(app.exec_())
