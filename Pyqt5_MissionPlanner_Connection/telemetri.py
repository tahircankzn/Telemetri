import collections.abc
import collections
collections.MutableMapping = collections.abc.MutableMapping

from dronekit import connect
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QTimer, Qt
from qfi import qfi_VSI
from PyQt5.QtGui import QFont
import sys



vehicle = connect("tcp:127.0.0.1:5762", wait_ready=True, timeout=100)

class Telemetri(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.setWindowTitle("BTÜ-POYRAZ TELEMETRİ SİSTEMİ")
        self.setStyleSheet("background-color: #292929")
        self.setWindowState(Qt.WindowMaximized)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        # Göstergeyi oluştur
        self.adi = qfi_VSI.qfi_VSI(self)
        self.adi.reinit()
        self.adi.setFixedSize(300, 300)  # Kendi boyutunu sabitle
        self.mainLayout.addWidget(self.adi)

        # Pitch değeri için QLabel
        self.pitchdeger = QLabel(self)
        self.pitchdeger.setGeometry(10, 10, 200, 50)  # Sol üst köşe konumu
        self.pitchdeger.setStyleSheet("background-color:white")
        self.pitchdeger.setFont(QFont("Bahnschrift", 25))

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update1)
        self.show()

        self.timer.start()

    def update1(self):
        alt = vehicle.location.global_relative_frame.alt
        # Burada pitch değerini hesaplayın (örnek olarak alt değerini kullanıyoruz)
        pitch_value = vehicle.attitude.pitch  # Gerçek pitch değerini almak için
        self.pitchdeger.setText(f"Pitch: {pitch_value:.2f}")  # QLabel'de güncelle

    def exit(self):
        self.timer.stop()
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Telemetri()
    sys.exit(app.exec_())
