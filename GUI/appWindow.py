from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import subprocess
import os
import shutil

from LysnWindow import LysnScreen
from TongTongWindow import TongTongScreen
from batch import LysnData, TongTongData, KakaoTalkData
from button import Button


class appScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        # Window Setting
        self.setGeometry(500, 70, 800, 600)
        self.setWindowTitle("main")
        self.setFixedSize(self.rect().size())
        self.setContentsMargins(30, 50, 30, 50)

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
        self.phonePhoto = Button(QPixmap("image/phone2.png"), 170)
        self.phonePhoto.setEnabled(False)
        self.phonePhoto.setStyleSheet('background:transparent;')
        self.phonePhoto.setStyleSheet('background:rgb(242, 242, 242);')

        # 정보
        serialNo, productNo, androidVersion = self.deviceInformation()
        self.text2 = QLabel(f"시리얼 넘버 : {serialNo}")
        self.text3 = QLabel(f"제품 넘버 : {productNo}")
        self.text4 = QLabel(f"안드로이드 버전 : {androidVersion}")

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
        self.KakaoTalkButton = Button(QPixmap("image/kakao.png"), 130)
        self.WeChatButton = Button(QPixmap("image/wechat.png"), 130)
        self.LysnButton = Button(QPixmap("image/lysn.png"), 130, self.showLysnWindow)
        self.TongTongButton = Button(QPixmap("image/tong.png"), 130, self.showTongTongWindow)
        self.WickrButton = Button(QPixmap("image/wickr.png"), 130)

        # 마우스 커서를 버튼 위에 올리면 모양 바꾸기
        self.KakaoTalkButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.WeChatButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.LysnButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.TongTongButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.WickrButton.setCursor(QCursor(Qt.PointingHandCursor))

        # 레이아웃2
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.KakaoTalkButton)
        hbox2.addWidget(self.WeChatButton)
        hbox2.addWidget(self.LysnButton)
        hbox2.addWidget(self.TongTongButton)
        hbox2.addWidget(self.WickrButton)
        hbox2.setContentsMargins(20, 0, 20, 0)
        hbox2.setSpacing(15)

        layout2 = QVBoxLayout()
        layout2.addWidget(self.label)
        layout2.addLayout(hbox2)

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
        reply = self.checkData('Lysn')
        if reply == 'Yes':
            LysnData(self.phoneNo)  # Lysn 데이터 추출
        elif reply == 'back':
            return

        self.hide()  # hide main window
        self.lysnWindow = LysnScreen(self.phoneNo)
        self.lysnWindow.exec()
        self.show()

    # TongTongWindow로 이동
    def showTongTongWindow(self):
        reply = self.checkData('TongTong')
        if reply == 'Yes':
            TongTongData(self.phoneNo)  # Lysn 데이터 추출
        elif reply == 'back':
            return

        self.hide()  # hide main window
        self.tongtongWindow = TongTongScreen(self.phoneNo)
        self.tongtongWindow.exec()
        self.show()

    def checkData(self, app):
        if os.path.exists(f'C:/AppData/{self.phoneNo}/{app}'):
            reply = QMessageBox.question(self, 'Message', f'이미 {app} 데이터가 존재합니다.\n{app} 데이터를 다시 추출하시겠습니까?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return 'No'
            elif reply == QMessageBox.Yes:
                try:
                    shutil.rmtree(f'C:/AppData/{self.phoneNo}/{app}/')
                except:
                    print('데이터 파일이 열려있습니다. 닫고 다시 실행해주세요.')
                return 'Yes'
            return 'No'
        else:
            reply = QMessageBox.question(self, 'Message', f'{app} 데이터를 추출하시겠습니까?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.No:
                return 'back'
            elif reply == QMessageBox.Yes:
                os.makedirs(f'C:/AppData/{self.phoneNo}')
            return 'Yes'


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = appScreen()
    sys.exit(app.exec_())
