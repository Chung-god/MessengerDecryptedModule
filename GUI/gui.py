import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from lysn import lysn_userDB, lysn_talkDB

class DB(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.initUI()

    def initUI(self):
        appname = QLabel('choose app')
        kakaoButton = QPushButton("KakaoTalk")
        wechatButton = QPushButton("WeChat")
        lysnButton = QPushButton("Lysn")
        tongButton = QPushButton("TongTong")

        lysnButton.clicked.connect(self.lysnButtonClicked)

        hButtonbox1 = QHBoxLayout()
        hButtonbox1.addWidget(kakaoButton)
        hButtonbox1.addWidget(wechatButton)
        hButtonbox2 = QHBoxLayout()
        hButtonbox2.addWidget(lysnButton)
        hButtonbox2.addWidget(tongButton)

        layout = QVBoxLayout()
        layout.addWidget(appname)
        layout.addLayout(hButtonbox1)
        layout.addLayout(hButtonbox2)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.setGeometry(1000,1000,1000,1000)
        self.setWindowTitle('messenger app artifact')
        self.center()
        self.show()

    def center(self):
        frame_info = self.frameGeometry()
        display_center = QDesktopWidget().availableGeometry().center()
        frame_info.moveCenter(display_center)
        self.move(frame_info.topLeft())

    def lysnButtonClicked(self):
        global filename
        filename = QFileDialog.getOpenFileName(self, 'Open File')

        if filename[0][-7:] == 'user.db':
            colname, rowlist = lysn_userDB(filename[0])
        elif filename[0][-7:] == 'talk.db':
            colname, rowlist = lysn_talkDB(filename[0])

        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(len(colname))
        self.table.setRowCount(len(rowlist))

        self.table.setHorizontalHeaderLabels(colname)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(len(rowlist)):
            for j in range(len(rowlist[i])):
                self.table.setItem(i, j, QTableWidgetItem(str(rowlist[i][j])))


app = QApplication(sys.argv)
db = DB()
db.show()
sys.exit(app.exec_())
