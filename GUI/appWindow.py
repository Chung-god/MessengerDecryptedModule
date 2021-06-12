from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import subprocess
import os
import shutil
from datetime import datetime

from LysnWindow import LysnScreen
from TongTongWindow import TongTongScreen
from WickrWindow import WickrScreen
from PurpleWindow import PurpleScreen
from KakaoWindow import KakaoScreen
from batch import LysnData, TongTongData, KakaoTalkData, WickrData, PurpleData
from button import Button

class appScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        # Window Setting
        self.setGeometry(500, 70, 1000, 700)
        self.setWindowTitle("main")
        self.setFixedSize(self.rect().size())
        self.setContentsMargins(30, 30, 30, 30)

        # Window Backgrond
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # === 디바이스 정보
        self.text1 = QLabel("Android Smart Phone")

        # 폰트
        font = self.text1.font()
        font.setFamily('맑은 고딕')
        font.setBold(True)
        font.setPointSize(font.pointSize() + 3)
        self.text1.setStyleSheet('color: rgb(55,48,46);')
        self.text1.setFont(font)

        # 핸드폰 사진
        self.phonePhoto = Button(QPixmap("image/phone2.png"), 200)
        self.phonePhoto.setEnabled(False)
        self.phonePhoto.setStyleSheet('background:transparent;')
        self.phonePhoto.setStyleSheet('background:rgb(242, 242, 242);')

        # 정보
        self.serialNo, self.productNo, self.androidVersion = self.deviceInformation()
        self.text2 = QLabel(f"시리얼 넘버 : {self.serialNo}")
        self.text3 = QLabel(f"제품 넘버 : {self.productNo}")
        self.text4 = QLabel(f"안드로이드 버전 : {self.androidVersion}")

        font.setBold(False)
        font.setPointSize(font.pointSize() - 3)
        self.text2.setStyleSheet('color: rgb(55,48,46);')
        self.text2.setFont(font)
        self.text3.setStyleSheet('color: rgb(55,48,46);')
        self.text3.setFont(font)
        self.text4.setStyleSheet('color: rgb(55,48,46);')
        self.text4.setFont(font)

        # 레이아웃1
        v1 = QVBoxLayout()
        v1.addWidget(self.text1)
        v1.addWidget(self.text2)
        v1.addWidget(self.text3)
        v1.addWidget(self.text4)
        v1.setSpacing(0)
        v1.setContentsMargins(10, 30, 10, 30)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.phonePhoto)
        layout1.addLayout(v1)
        layout1.addStretch(1)

        # === APP
        # TEXT
        self.label = QLabel("DB 추출 작업을 진행할 메신저를 선택해주세요")
        self.label.setAlignment(Qt.AlignCenter)
        font.setBold(True)
        font.setPointSize(font.pointSize() + 3)
        self.label.setStyleSheet('color: rgb(55,48,46);')
        self.label.setFont(font)

        # button
        self.KakaoTalkButton = Button(QPixmap("image/kakao.png"), 130, self.showKakaoWindow)
        self.WeChatButton = Button(QPixmap("image/wechat.png"), 130, self.showPurpleWindow)
        self.LysnButton = Button(QPixmap("image/lysn.png"), 130, self.showLysnWindow)
        self.TongTongButton = Button(QPixmap("image/tong.png"), 130, self.showTongTongWindow)
        self.PurpleButton = Button(QPixmap("image/purple.png"), 130, self.showPurpleWindow)
        self.WickrButton = Button(QPixmap("image/wickr.png"), 130, self.showWickrWindow)
        
        # 마우스 커서를 버튼 위에 올리면 모양 바꾸기
        self.KakaoTalkButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.WeChatButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.LysnButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.TongTongButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.PurpleButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.WickrButton.setCursor(QCursor(Qt.PointingHandCursor))

        app1 = QLabel("KakaoTalk ")
        app2 = QLabel("WeChat")
        app3 = QLabel("Lysn")
        app4 = QLabel("TongTong")
        app5 = QLabel(" PurPle")
        app6 = QLabel("  Wickr")
        appname = [app1, app2, app3, app4, app5, app6]

        font.setBold(False)
        font.setPointSize(font.pointSize()-1)
        for app in appname:
            app.setFixedSize(130, 30)
            app.setAlignment(Qt.AlignCenter)
            app.setStyleSheet('color: rgb(55,48,46);')
            app.setFont(font)
            
        # 레이아웃2
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.KakaoTalkButton)
        hbox2.addWidget(self.WeChatButton)
        hbox2.addWidget(self.LysnButton)
        hbox2.addWidget(self.TongTongButton)
        hbox2.addWidget(self.PurpleButton)
        hbox2.addWidget(self.WickrButton)
        
        hbox2.setContentsMargins(20, 0, 20, 0)
        hbox2.setSpacing(15)
        
        # 레이아웃 3
        hbox3 = QHBoxLayout()
        hbox3.addWidget(app1)
        hbox3.addWidget(app2)
        hbox3.addWidget(app3)
        hbox3.addWidget(app4)
        hbox3.addWidget(app5)
        hbox3.addWidget(app6)
        
        hbox3.setContentsMargins(20, 0, 20, 0)
        hbox3.setSpacing(15)
        
        layout2 = QVBoxLayout()
        layout2.addWidget(self.label)
        layout2.addLayout(hbox2)
        layout2.addLayout(hbox3)
        layout2.setSpacing(0)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.setSpacing(50)
        self.setLayout(layout)
        self.center()
        self.show()

    def center(self):
        frame_info = self.frameGeometry()
        display_center = QDesktopWidget().availableGeometry().center()
        frame_info.moveCenter(display_center)
        self.move(frame_info.topLeft())

    # 디바이스 정보 추출
    def deviceInformation(self):
        serialNo, productNo, androidVersion, self.phoneNo = '', '', '', ''
        moveadb = 'cd C:\\Program Files (x86)\\Nox\\bin'
        try:
            r = subprocess.check_output(moveadb + ' && adb get-serialno', shell=True)
            serialNo = r.decode().split()[0]
            s = subprocess.check_output(moveadb + ' && adb shell getprop ro.product.model', shell=True)
            productNo = s.decode().split()[0]
            d = subprocess.check_output(moveadb + ' && adb shell getprop ro.build.version.release', shell=True)
            androidVersion = d.decode().split()[0]
            self.phoneNo = productNo
        except:
            self.text1.setText('devices/emulators를 찾을 수 없습니다.')
            self.text1.setStyleSheet('color: red;')
        return serialNo, productNo, androidVersion
    
    # LysnWindow로 이동
    def showLysnWindow(self):
        self.appName = 'Lysn'

        self.path,self.reply = '','Back'
        dialog = Dialog(self)
        dialog.exec()

        if self.reply == 'Yes':
            LysnData(self.path)  # Kakao 데이터 추출
        elif self.reply == 'Already_Exits_No':
            pass
        elif self.reply == 'Back':
            return
        self.path = f'{self.path}/{self.appName}/'
        self.hide()  # hide main window
        self.lysnWindow = LysnScreen(self.path)
        self.lysnWindow.exec()
        self.show()

    # TongTongWindow로 이동
    def showTongTongWindow(self):
        self.appName = 'TongTong'

        self.path,self.reply = '','Back'
        dialog = Dialog(self)
        dialog.exec()

        if self.reply == 'Yes':
            TongTongData(self.path)  # Kakao 데이터 추출
        elif self.reply == 'Already_Exits_No':
            pass
        elif self.reply == 'Back':
            return
        self.path = f'{self.path}/{self.appName}/'
        self.hide()  # hide main window
        self.tongtongWindow = TongTongScreen(self.path)
        self.tongtongWindow.exec()
        self.show()

    # TongTongWindow로 이동
    def showWickrWindow(self):
        self.appName = 'Wickr'

        self.path,self.reply = '','Back'
        dialog = Dialog(self)
        dialog.exec()

        if self.reply == 'Yes':
            WickrData(self.path)  # Kakao 데이터 추출
        elif self.reply == 'Already_Exits_No':
            pass
        elif self.reply == 'Back':
            return
        self.path = f'{self.path}/{self.appName}/'

        self.hide()  # hide main window
        self.WickrWindow = WickrScreen(self.path)
        self.WickrWindow.exec()
        self.show()

    # PurpleWindow로 이동
    def showPurpleWindow(self):
        self.appName = 'Purple'

        self.path,self.reply = '','Back'
        dialog = Dialog(self)
        dialog.exec()

        if self.reply == 'Yes':
            PurpleData(self.path)  # Kakao 데이터 추출
        elif self.reply == 'Already_Exits_No':
            pass
        elif self.reply == 'Back':
            return

        self.path = f'{self.path}/{self.appName}/'

        self.hide()  # hide main window
        self.PurpleWindow = PurpleScreen(self.path)
        self.PurpleWindow.exec()
        self.show()

    def showKakaoWindow(self):
        self.appName = 'KakaoTalk'

        self.path,self.reply = '','Back'
        dialog = Dialog(self)
        dialog.exec()

        if self.reply == 'Yes':
            KakaoTalkData(self.path) 
        elif self.reply == 'Already_Exits_No':
            pass
        elif self.reply == 'Back':
            return

        self.path = f'{self.path}/{self.appName}/'
        self.hide()  # hide main window
        self.KakaoWindow = KakaoScreen(self.path)
        self.KakaoWindow.exec()
        self.show()

    def checkData(self):
        if os.path.exists(f'{self.path}/{self.appName}'):
            reply = QMessageBox.question(self, 'Message', f'이미 {self.appName} 데이터가 존재합니다.\n{self.appName} 데이터를 다시 추출하시겠습니까?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Close , QMessageBox.Close)
            if reply == QMessageBox.No: return 'Already_Exists_No'
            elif reply == QMessageBox.Close: return 'Back'
            elif reply == QMessageBox.Yes:
                try:
                    shutil.rmtree(f'{self.path}/{self.appName}/')
                except:
                    print('데이터 파일이 열려있습니다. 닫고 다시 실행해주세요.')
                    return 'Back'
                return 'Yes'
        else:
            reply = QMessageBox.question(self, 'Message', f'{self.appName} 데이터를 추출하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes: return 'Yes'
            elif reply == QMessageBox.No: return 'Back'

class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__()
        self.p = parent

        self.createFormGroupBox()
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox1)
        mainLayout.addWidget(self.formGroupBox2)
        mainLayout.addStretch(1)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        self.setWindowTitle("Evidence Item Imformation")
        self.setMinimumWidth(600)
        self.setContentsMargins(10, 5, 10, 5)

    def createFormGroupBox(self):
        self.formGroupBox1 = QGroupBox("Phone Imformation")
        layout = QFormLayout()
        layout.addRow(QLabel("Serial Number :"), QLabel(self.p.serialNo))
        layout.addRow(QLabel("Product Model :"), QLabel(self.p.productNo))
        layout.addRow(QLabel("Android Version :"), QLabel(self.p.androidVersion))
        layout.addRow(QLabel("App :"), QLabel(self.p.appName))
        self.formGroupBox1.setLayout(layout)
    
        self.formGroupBox2 = QGroupBox("Case Imformation")
        layout = QFormLayout()
        self.date = datetime.today().strftime("%Y%m%d")
        self.pa = f'C:/MDTool/{self.p.phoneNo}/{self.date}-{self.p.appName}'
        self.CN, self.UD, self.EX, self.NT, self.PT = QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit(), QLabel(self.pa)
        layout.addRow(QLabel("Date :"), QLabel(self.date))
        layout.addRow(QLabel("Case Number :"), self.CN)
        layout.addRow(QLabel("Unique Description :"), self.UD)
        layout.addRow(QLabel("Examiner :"), self.EX)
        layout.addRow(QLabel("Notes :"), self.NT)
        layout.addRow(QLabel("Path :"), self.PT)
        self.CN.textChanged[str].connect(self.onChanged)
        self.formGroupBox2.setLayout(layout)
        
    def onChanged(self, text):
        self.PT.setText(f'{self.pa}-{text}')
    
    def accept(self):
        self.p.path = self.PT.text()
        
        self.p.reply = self.p.checkData()
        if self.p.reply == 'Back':
            return
        elif self.p.reply == 'Yes':
            os.makedirs(self.p.path, exist_ok=True)
            with open(self.p.path+f'/{self.date}-Case Info-{self.CN.text()}.txt', "w+") as f:
                f.write(f'[Phone Information]\nSerial Number : {self.p.serialNo}\nProduct Model : {self.p.productNo}\n'+
                f'Android Version : {self.p.androidVersion}\nApp : {self.p.appName}\n\n[Case Imformation]\n'+
                f'Date : {self.date}\nCase Number : {self.CN.text()}\nUnique Description : {self.UD.text()}\n'+
                f'Examiner : {self.EX.text()}\nNotes : {self.NT.text()}\nPath : {self.PT.text()}\n')
            self.close()
        else:
            self.close()
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ui = appScreen()
    sys.exit(app.exec_())
