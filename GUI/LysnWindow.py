from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from openpyxl.styles import Font, Border, Side, Alignment
import openpyxl
from exportDB import lysn_userDB, lysn_talkDB
import sys

class LysnScreen(QWidget):
    def __init__(self, MainWindow):
        super().__init__()
        self.setupUI(MainWindow)

    def setupUI(self, MainWindow):
        # 초기화
        self.on_off, self.f_name, self.colname, self.rowlist, self.TalkDB = 0, '', [], [], []

        # Ctrl+ F 
        self.shortcut = QShortcut(QKeySequence('Ctrl+F'), self)
        print(self.shortcut)
        self.shortcut.activated.connect(self.handleFind)
        
        saveShortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        saveShortcut.activated.connect(self.excelButtonClicked)
        
        MainWindow.setObjectName("LysnWindow")
        MainWindow.resize(691, 551)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # back button
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backButton.sizePolicy().hasHeightForWidth())
        self.backButton.setSizePolicy(sizePolicy)
        self.backButton.setMinimumSize(QtCore.QSize(75, 0))
        self.backButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.backButton.setStyleSheet("background-image:url(\"image/back.png\");")
        self.backButton.setText("")
        self.backButton.setObjectName("backButton")
        self.horizontalLayout.addWidget(self.backButton)

        self.backButton.clicked.connect(self.search_items) # search
        
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        # search text
        self.searchBox = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchBox.sizePolicy().hasHeightForWidth())
        self.searchBox.setSizePolicy(sizePolicy)
        self.searchBox.setMinimumSize(QtCore.QSize(0, 15))
        self.searchBox.setObjectName("searchBox")
        self.horizontalLayout.addWidget(self.searchBox)

        # search button
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setMinimumSize(QtCore.QSize(0, 30))
        self.searchButton.setMaximumSize(QtCore.QSize(40, 16777215))
        self.searchButton.setStyleSheet("background-image:url(\"image/search.png\");")
        self.searchButton.setText("")
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout.addWidget(self.searchButton)

        self.searchButton.clicked.connect(self.search_items) # search

        # open button
        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openButton.sizePolicy().hasHeightForWidth())
        self.openButton.setSizePolicy(sizePolicy)
        self.openButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.openButton.setObjectName("openButton")
        self.horizontalLayout.addWidget(self.openButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        self.openButton.clicked.connect(self.DBClicked)

        # layout 4
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        
        # combo box
        self.dbComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.dbComboBox.setObjectName("dbComboBox")
        self.dbComboBox.addItem("")
        self.dbComboBox.addItem("")
        self.horizontalLayout_4.addWidget(self.dbComboBox)
        self.dbComboBox.setFixedWidth(100)

        self.dbComboBox.activated.connect(self.comboEvent)
        self.dbComboBox.hide()

        # combo box User
        self.dbComboBoxUser = QtWidgets.QComboBox(self.centralwidget)
        self.dbComboBoxUser.setObjectName("dbComboBoxUser")
        self.dbComboBoxUser.addItem("")
        self.horizontalLayout_4.addWidget(self.dbComboBoxUser)
        self.dbComboBoxUser.setFixedWidth(100)
        self.dbComboBoxUser.hide()

        # excel button
        self.excelSaveButton = QtWidgets.QPushButton(self.centralwidget)
        self.excelSaveButton.setObjectName("excelSaveButton")
        self.dbComboBoxUser.setFixedWidth(100)
        self.horizontalLayout_4.addStretch(1)
        self.horizontalLayout_4.addWidget(self.excelSaveButton)
        self.excelSaveButton.clicked.connect(self.excelButtonClicked)

        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        # table
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 20))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setObjectName("tableWidget")
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        MainWindow.setGeometry(300,300,1500,800)
        LysnScreen.center(MainWindow)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.openButton.setText(_translate("MainWindow", "OPEN"))
        self.dbComboBox.setItemText(0, _translate("MainWindow", "chats"))
        self.dbComboBox.setItemText(1, _translate("MainWindow", "rooms"))
        self.dbComboBoxUser.setItemText(0, _translate("MainWindow", "users"))
        self.excelSaveButton.setText(_translate("MainWindow", "xls"))

    def browseMainWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = LysnScreen(self.window)
        MainWindow.hide()
        self.window.show()

    # ctrl + f
    def handleFind(self):
        self.on_off = 1
        print("11")
        findDialog = QDialog()
        grid = QGridLayout()
        findDialog.setLayout(grid)
        findLabel = QLabel("Search...", findDialog)
        grid.addWidget(findLabel,1,0)
        self.findField = QLineEdit(findDialog)
        grid.addWidget(self.findField,1,1)
        findButton = QPushButton("Find", findDialog)
        findButton.clicked.connect(self.search_items)
        grid.addWidget(findButton,2,1)
        findDialog.setWindowTitle("Search items")
        findDialog.exec_()
        self.on_off = 0
    
    # search box
    def search_items(self):
        
        #rest font
        def reset(self, items):
            for item in items:
                item.setBackground(QBrush(Qt.white))
                item.setForeground(QBrush(Qt.black))
                item.setFont(QFont())
        
        if self.on_off == 0:
            text = self.searchBox.text()
            selected_items = self.tableWidget.findItems(self.searchBox.text(), QtCore.Qt.MatchContains)
        else:
            text = self.findField.text()
            selected_items = self.tableWidget.findItems(self.findField.text(), QtCore.Qt.MatchContains)
            
            
        allitems = self.tableWidget.findItems("", QtCore.Qt.MatchContains)
        
        # reset
        reset(self, allitems)
             
        # highlight the search results
        for item in allitems:
            if item in selected_items:   
                item.setBackground(QBrush(Qt.black))
                item.setForeground(QBrush(Qt.white))
                item.setFont(QFont("Helvetica", 11, QFont.Bold))
               
        if self.searchBox.text() == "":
            reset(self, allitems)
            print("sb None")
        elif self.on_off == 1 and self.findField.text() =="":
            reset(self, allitems)
            print("ff None")

    # table combo select
    def comboEvent(self):
        self.tableWidget.clear()
        self.colname, self.rowlist = [], [[]]

        if self.dbComboBox.currentText() == 'chats':
            self.colname, self.rowlist = self.TalkDB[0], self.TalkDB[1]
            
        elif self.dbComboBox.currentText() == 'rooms':
            self.colname, self.rowlist = self.TalkDB[2], self.TalkDB[3]
            
        self.showTable()

    # DB 버튼 클릭 시
    def DBClicked(self):
        
        android_id = '4f77d977f3f1c488'
        
        # db file 선택해서 경로 받아오기
        global filename
        filename = QFileDialog.getOpenFileName(self, 'Open File')

        self.tableWidget.clear()
        self.colname, self.rowlist = [], [[]]

        # db file 경로에 따라 db안에 있는 아티팩트 가져오기
        # colname에 열 제목 담기, rowlist에 각 행마다 리스트로 담기

        if filename[0][-7:] == 'user.db':
            self.dbComboBox.hide()
            self.dbComboBoxUser.show()
            self.colname, self.rowlist = lysn_userDB(filename[0], android_id)
            self.f_name = "user_db"
        
        elif filename[0][-7:] == 'talk.db':
            self.dbComboBoxUser.hide()
            self.dbComboBox.show()
            self.TalkDB = lysn_talkDB(filename[0], android_id)
            self.colname, self.rowlist = self.TalkDB[0], self.TalkDB[1]
            self.f_name = "talk_db"

        self.showTable()

    def showTable(self):
        self.tableWidget.setColumnCount(len(self.colname)) # col 개수 지정
        self.tableWidget.setRowCount(len(self.rowlist)) # row 개수 지정
        
        self.tableWidget.setHorizontalHeaderLabels(self.colname) # 열 제목 지정
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # 표 너비 지정
        self.tableWidget.setSortingEnabled(True)
        
    
        # rowlist를 표에 지정하기
        for i in range(len(self.rowlist)):
            for j in range(len(self.rowlist[i])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.rowlist[i][j])))
        
        # cell size
        table = self.tableWidget
        header = table.horizontalHeader()
        twidth = header.width()
        width = []
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
            width.append(header.sectionSize(column))
         
        wfactor = twidth / sum(width)
        for column in range(header.count()):
            header.setSectionResizeMode(column, QHeaderView.Interactive)
            header.resizeSection(column, width[column]*wfactor)
        
                
                
    def center(self):
        frame_info = self.frameGeometry()
        display_center = QDesktopWidget().availableGeometry().center()
        frame_info.moveCenter(display_center)
        self.move(frame_info.topLeft())

    # 엑셀 추출 버튼 클릭 시
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
            
        wb.save("Lysn_" + self.f_name + "_" +self.dbComboBox.currentText() + "_table"+ ".xlsx")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = LysnScreen(MainWindow)
    ui.show()
    sys.exit(app.exec_())
