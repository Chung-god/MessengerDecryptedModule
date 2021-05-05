
from PyQt5 import QtCore, QtGui, QtWidgets
from LysnWindow import LysnScreen

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(836, 687)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())

        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(150, 150))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777214))
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())     
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 150))
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 50))
        self.textEdit.setStyleSheet("background-color:rgb(0,0,0,0);")
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_3.addWidget(self.textEdit)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        
        spacerItem = QtWidgets.QSpacerItem(0, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.KakaoTalkButton = QtWidgets.QPushButton(self.centralwidget)    
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.KakaoTalkButton.sizePolicy().hasHeightForWidth())    
        self.KakaoTalkButton.setSizePolicy(sizePolicy)
        self.KakaoTalkButton.setMinimumSize(QtCore.QSize(100, 0))
        self.KakaoTalkButton.setMaximumSize(QtCore.QSize(16777215, 100))
        self.KakaoTalkButton.setStyleSheet("background-image:url(\"image/kakao.png\");")
        self.KakaoTalkButton.setText("")
        self.KakaoTalkButton.setObjectName("KakaoTalkButton")
        self.horizontalLayout_2.addWidget(self.KakaoTalkButton)
        
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.WeChatButton = QtWidgets.QPushButton(self.centralwidget)
        self.WeChatButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.WeChatButton.sizePolicy().hasHeightForWidth())
        self.WeChatButton.setSizePolicy(sizePolicy)
        self.WeChatButton.setMinimumSize(QtCore.QSize(100, 100))
        self.WeChatButton.setMaximumSize(QtCore.QSize(16777215, 100))
        self.WeChatButton.setStyleSheet("background-image:url(\"image/wechat.png\");")
        self.WeChatButton.setText("")
        self.WeChatButton.setObjectName("WeChatButton")
        self.horizontalLayout_2.addWidget(self.WeChatButton)
        
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.LysnButton = QtWidgets.QPushButton(self.centralwidget)
        self.LysnButton.setMinimumSize(QtCore.QSize(100, 0))
        self.LysnButton.setMaximumSize(QtCore.QSize(16777215, 100))
        self.LysnButton.setStyleSheet("background-image:url(\"image/lysn.png\");")
        self.LysnButton.setText("")
        self.LysnButton.setObjectName("LysnButton")
        self.LysnButton.clicked.connect(self.browseLysnWindow)
        self.horizontalLayout_2.addWidget(self.LysnButton)
        
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.TongTongButton = QtWidgets.QPushButton(self.centralwidget)
        self.TongTongButton.setMinimumSize(QtCore.QSize(100, 0))
        self.TongTongButton.setMaximumSize(QtCore.QSize(16777215, 100))
        self.TongTongButton.setStyleSheet("background-image:url(\"image/tong.png\");")
        self.TongTongButton.setText("")
        self.TongTongButton.setObjectName("TongTongButton")
        self.horizontalLayout_2.addWidget(self.TongTongButton)
        
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.WickrButton = QtWidgets.QPushButton(self.centralwidget)
        self.WickrButton.setMinimumSize(QtCore.QSize(100, 0))
        self.WickrButton.setMaximumSize(QtCore.QSize(16777215, 100))
        self.WickrButton.setStyleSheet("background-image:url(\"image/wickr.png\");")
        self.WickrButton.setText("")
        self.WickrButton.setObjectName("WickrButton")
        self.horizontalLayout_2.addWidget(self.WickrButton)
        
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        
        spacerItem7 = QtWidgets.QSpacerItem(20, 120, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 836, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:11pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:11pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:18pt; font-weight:600;\">DB 추출 작업을 진행할 메신저를 선택해주세요 ! </span></p></body></html>"))

    def browseLysnWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = LysnScreen(self.window)
        MainWindow.hide()
        self.window.show()
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
