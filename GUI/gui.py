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
            f_name = "user_db"
        elif filename[0][-7:] == 'talk.db':
            colname, rowlist = lysn_talkDB(filename[0])
            f_name = "talk_db"
            
        
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(len(colname))
        self.table.setRowCount(len(rowlist))
        
        
        
        self.table.setHorizontalHeaderLabels(colname)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(len(rowlist)):
            for j in range(len(rowlist[i])):
                self.table.setItem(i, j, QTableWidgetItem(str(rowlist[i][j])))
            
        #create Excel    
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "Lysn"
        col_excel = list(colname)[0:5]
        
        for x in range(1, len(col_excel) + 1):
            sheet.cell(row = 1, column = x).value = col_excel[x - 1]
            
        for x in range(0, len(rowlist)):
            for y in range(1, len(rowlist[i]) + 1):
                sheet.cell(row = x + 2, column = y).value = str(rowlist[x][y - 1])
                
                
        #resize the cell
        for x in range(0, len(colname)):
            MAX = 1
            for y in range(1, len(rowlist) + 1):
                cell_size = len(str(rowlist[y - 1][x]))
                if MAX < cell_size:
                    MAX = cell_size
                    sheet.column_dimensions[chr(65 + x)].width = MAX + 5
                sheet.row_dimensions[y].height = 20
        sheet.row_dimensions[y + 1].height = 20
        
        #change the font 
        for x in range(1, len(colname) + 1):
            cell = sheet[chr(64 + x) + "1"]
            cell.font = Font(size=11, bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = Border(right=Side(border_style="thick"), bottom=Side(border_style="thick"))

        for x in range(len(rowlist)):
            for y in range(len(rowlist[i])):
                cell = sheet[chr(65 + y) + str(x + 2)]
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = Border(right=Side(border_style="thick"))
 
        wb.save("Lysn_" + f_name + ".xlsx")

        
app = QApplication(sys.argv)
db = DB()
db.show()
sys.exit(app.exec_())
