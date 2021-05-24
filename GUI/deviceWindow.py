from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import subprocess
from appWindow import appScreen

class deviceScreen(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        # Window Setting
        self.setGeometry(300, 70, 800, 600)
        self.setWindowTitle("main")
        self.setFixedSize(self.rect().size())
        self.setContentsMargins(100,100,100,100)

        # Window Backgrond
        palette = QPalette()
        palette.setColor(QPalette.Background , QColor(235, 237, 240))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # TEXT
        self.label = QLabel("디바이스를 연결해 시작해 보세요.")
        self.label.setAlignment(Qt.AlignCenter)
        
        font = self.label.font()
        font.setFamily('맑은 고딕')
        font.setBold(True)
        font.setPointSize(font.pointSize()+5)
        self.label.setStyleSheet('color: rgb(55,48,46);')
        self.label.setFont(font)
        
        # button
        self.phoneLabel = QLabel()
        self.phoneGif = QMovie("image/phone.gif", QByteArray(), self)
        self.phoneGif.setCacheMode(QMovie.CacheAll)
        self.phoneLabel.setAlignment(Qt.AlignCenter)
        self.phoneLabel.setMovie(self.phoneGif)
        self.phoneGif.start()

        # button
        self.ll = QLabel('연결 후 next를 누르세요')
        self.connectButton = QPushButton('next')
        self.connectButton.clicked.connect(self.checkDevice)

        font.setBold(False)
        font.setPointSize(font.pointSize() - 5)
        self.ll.setFont(font)
        self.connectButton.setFont(font)
        
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.ll)
        hbox3.addStretch(1)
        hbox3.addWidget(self.connectButton)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.phoneLabel)
        layout.addLayout(hbox3)

        self.setLayout(layout)
        self.center()
        self.show()
    
    def center(self):
        frame_info = self.frameGeometry()
        display_center = QDesktopWidget().availableGeometry().center()
        frame_info.moveCenter(display_center)
        self.move(frame_info.topLeft())

    def showAppWindow(self):
        self.appWindow = appScreen()
        self.close()
    
    def checkDevice(self):
        try:
            r = subprocess.check_output("cd C:\\Program Files (x86)\\Nox\\bin && adb get-serialno", shell=True)
            serialno = r.decode().split()[0]
            self.ll.setText(serialno)
            self.showAppWindow()
        except:
            self.ll.setText('devices/emulators를 찾을 수 없습니다.')
            self.ll.setStyleSheet('color: red;')
        
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ui = deviceScreen()
    sys.exit(app.exec_())
