import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from lysn import lysn_userDB, lysn_talkDB
from openpyxl.styles import Font, Border, Side, Alignment
import openpyxl

class DB(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.initUI()
       
    def initUI(self):
        self.f_name = ''
        self.colname = []
        self.rowlist = []

        kakaoButton = QPushButton("KakaoTalk")
        wechatButton = QPushButton("WeChat")
        lysnButton = QPushButton("Lysn")
        tongButton = QPushButton("TongTong")
    
        lysnButton.clicked.connect(self.lysnButtonClicked)

        self.androidIdLabel = QLabel('Android Id : ')
        self.androidIdLabel.setFixedWidth(100)
        self.androidIdLabel.hide()
        self.lysnAndroidId = QLineEdit()
        self.lysnAndroidId.setFixedWidth(300)
        self.lysnAndroidId.hide()

        self.lysnButton_user = QPushButton("User.db")
        self.lysnButton_user.hide()
        self.lysnButton_talk = QPushButton("Talk.db")
        self.lysnButton_talk.hide()

        self.excelButton = QPushButton("Excel Export")
        self.excelButton.clicked.connect(self.excelButtonClicked)

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox5 = QHBoxLayout()
        hbox6 = QHBoxLayout()

        hbox1.addWidget(kakaoButton)
        hbox2.addWidget(wechatButton)

        hbox3.addWidget(lysnButton)
        hbox4.addWidget(self.androidIdLabel)
        hbox4.addWidget(self.lysnAndroidId)   
        hbox4.addWidget(self.lysnButton_user)
        hbox4.addWidget(self.lysnButton_talk)

        hbox5.addWidget(tongButton)
        hbox6.addWidget(self.excelButton)

        layout = QVBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addLayout(hbox3)
        layout.addLayout(hbox4)
        layout.addLayout(hbox5)
        layout.addWidget(self.table)
        layout.addLayout(hbox6)

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
        if self.lysnButton_user.isVisible() == True:
            self.lysnButton_user.hide()
            self.lysnButton_talk.hide()
            self.androidIdLabel.hide()
            self.lysnAndroidId.hide()
        else:
            self.lysnButton_user.show()
            self.lysnButton_talk.show()
            self.androidIdLabel.show()
            self.lysnAndroidId.show()

            self.lysnButton_user.clicked.connect(self.DBClicked)
            self.lysnButton_talk.clicked.connect(self.DBClicked)

    def DBClicked(self):
        
        #android_id = '4f77d977f3f1c488'
        android_id = self.lysnAndroidId.text()
        if android_id == '':
            return
        
        global filename
        filename = QFileDialog.getOpenFileName(self, 'Open File')

        if filename[0][-7:] == 'user.db':
            self.colname, self.rowlist = lysn_userDB(filename[0], android_id)
            self.f_name = "user_db"

        elif filename[0][-7:] == 'talk.db':
            self.colname, self.rowlist = lysn_talkDB(filename[0], android_id)
            self.f_name = "talk_db"
        
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(len(self.colname))
        self.table.setRowCount(len(self.rowlist))
        
        self.table.setHorizontalHeaderLabels(self.colname)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(len(self.rowlist)):
            for j in range(len(self.rowlist[i])):
                self.table.setItem(i, j, QTableWidgetItem(str(self.rowlist[i][j])))
            

    def excelButtonClicked(self):
        if self.f_name == '':
            return

        #create Excel    
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "Lysn"
        col_excel = list(self.colname)[0:5]
        
        for x in range(1, len(col_excel) + 1):
            sheet.cell(row = 1, column = x).value = col_excel[x - 1]
            
        for x in range(0, len(self.rowlist)):
            for y in range(1, len(self.rowlist[x]) + 1):
                sheet.cell(row = x + 2, column = y).value = str(self.rowlist[x][y - 1])
                
                
        #resize the cell
        for x in range(0, len(self.colname)):
            MAX = 1
            for y in range(1, len(self.rowlist) + 1):
                cell_size = len(str(self.rowlist[y - 1][x]))
                if MAX < cell_size:
                    MAX = cell_size
                    sheet.column_dimensions[chr(65 + x)].width = MAX + 5
                sheet.row_dimensions[y].height = 20
        sheet.row_dimensions[y + 1].height = 20
        
        #change the font 
        for x in range(1, len(self.colname) + 1):
            cell = sheet[chr(64 + x) + "1"]
            cell.font = Font(size=11, bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = Border(right=Side(border_style="thick"), bottom=Side(border_style="thick"))

        for x in range(len(self.rowlist)):
            for y in range(len(self.rowlist[x])):
                cell = sheet[chr(65 + y) + str(x + 2)]
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = Border(right=Side(border_style="thick"))
 
        wb.save("Lysn_" + self.f_name + ".xlsx")
        
app = QApplication(sys.argv)
db = DB()
db.show()
sys.exit(app.exec_())
