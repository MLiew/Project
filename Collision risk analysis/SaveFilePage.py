# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SaveFilePage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from multiprocessing import Process
from time import sleep
from PredictPage import Ui_PredictPageWindow
import test_func, web_crawl_test, data_prepro, tle_clustering, tle_classification


class Ui_SaveFilePage(object):
    def setupUi(self, SaveFilePage):
        SaveFilePage.setObjectName("SaveFilePage")
        SaveFilePage.resize(532, 468)
        self.centralwidget = QtWidgets.QWidget(SaveFilePage)
        self.centralwidget.setObjectName("centralwidget")
        self.ChooseFilelabel = QtWidgets.QLabel(self.centralwidget)
        self.ChooseFilelabel.setGeometry(QtCore.QRect(40, 40, 271, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ChooseFilelabel.setFont(font)
        self.ChooseFilelabel.setObjectName("ChooseFilelabel")
        self.fileTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.fileTextEdit.setGeometry(QtCore.QRect(40, 70, 411, 31))
        self.fileTextEdit.setObjectName("fileTextEdit")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(40, 330, 451, 31))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.InProgressLabel = QtWidgets.QLabel(self.centralwidget)
        self.InProgressLabel.setGeometry(QtCore.QRect(40, 280, 411, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.InProgressLabel.setFont(font)
        self.InProgressLabel.setObjectName("InProgressLabel")
        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(370, 380, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.nextButton.setFont(font)
        self.nextButton.setObjectName("nextButton")
        self.getPathButton = QtWidgets.QToolButton(self.centralwidget)
        self.getPathButton.setGeometry(QtCore.QRect(460, 70, 31, 31))
        self.getPathButton.setObjectName("getPathButton")
        self.confirmFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.confirmFileButton.setGeometry(QtCore.QRect(370, 120, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.confirmFileButton.setFont(font)
        self.confirmFileButton.setObjectName("confirmFileButton")
        self.chooseClusAlgoLabel = QtWidgets.QLabel(self.centralwidget)
        self.chooseClusAlgoLabel.setGeometry(QtCore.QRect(40, 200, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.chooseClusAlgoLabel.setFont(font)
        self.chooseClusAlgoLabel.setObjectName("chooseClusAlgoLabel")
        self.clusterAlgoComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.clusterAlgoComboBox.setGeometry(QtCore.QRect(280, 200, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.clusterAlgoComboBox.setFont(font)
        self.clusterAlgoComboBox.setObjectName("clusterAlgoComboBox")
        SaveFilePage.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SaveFilePage)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 532, 21))
        self.menubar.setObjectName("menubar")
        SaveFilePage.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SaveFilePage)
        self.statusbar.setObjectName("statusbar")
        SaveFilePage.setStatusBar(self.statusbar)

        self.retranslateUi(SaveFilePage)
        QtCore.QMetaObject.connectSlotsByName(SaveFilePage)

        # Create a timer object
        self.timer =QtCore.QTimer()

        self.progressBar.hide()
        self.InProgressLabel.hide()
        self.nextButton.hide()
        self.getPathButton.clicked.connect(self.get_file_path)
        self.confirmFileButton.clicked.connect(self.start_process)

        self.nextButton.clicked.connect(self.openPredictWindow)

    def retranslateUi(self, SaveFilePage):
        _translate = QtCore.QCoreApplication.translate
        SaveFilePage.setWindowTitle(_translate("SaveFilePage", "MainWindow"))
        self.ChooseFilelabel.setText(_translate("SaveFilePage", "Choose File Directory to save file:"))
        self.InProgressLabel.setText(_translate("SaveFilePage", "In Progress......"))
        self.nextButton.setText(_translate("SaveFilePage", "Next"))
        self.getPathButton.setText(_translate("SaveFilePage", "..."))
        self.confirmFileButton.setText(_translate("SaveFilePage", "Confirm"))
        self.chooseClusAlgoLabel.setText(_translate("SaveFilePage", "Choose Clustering Algorithm:"))

    def handleTimer(self):
        # Initial progress bar value is 0
        self.value = self.progressBar.value() 
        # self.progressBar.show()
        # print("Timer is working......", value)
        if self.value < 100:
            if self.function == 'f1':
                if self.value < 30:
                    self.value += 1
                    # print("message", value)
                    self.progressBar.setValue(self.value)                

            elif self.function == 'f2':
                if self.value <= 60:
                    self.value += 1
                    # print("message 2", value)
                    self.progressBar.setValue(self.value)   
            
            elif self.function == 'f3':
                if self.value <= 100:
                    self.value += 1
                    # print("message 3", value)
                    self.progressBar.setValue(self.value)   

    def get_file_path(self, SaveFilePage):
        file_name = QtWidgets.QFileDialog.getExistingDirectory(None, "Select File Directory to Save File", "")
        print(file_name)
        self.fileTextEdit.setText(file_name)
        self.file_name = file_name

    def start_process(self):
        self.InProgressLabel.show()
        # self.InProgressLabel.setText("Web crawling in progress......")
        self.progressBar.show()
        
        self.function = 'f1'        
        
        self.timer.timeout.connect(self.handleTimer)

        self.timer.start(100)
        # print("timer starts......")

        self.InProgressLabel.setText("Web crawling in progress......")
        web_crawl_test.main_web_crawl(self.file_name)

        self.function = 'f2'
        # print("Data prepro in progress......")
        self.InProgressLabel.setText("Data preprocessing in progress......")
        data_prepro.main_prepro_one(self.file_name)


        self.function = 'f3'
        # print("Building clustering model in progress......")
        # tle_clustering.main_tle_cluster(self.file_name, 'KMeans')
    
        self.nextButton.show()
        
    def openPredictWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_PredictPageWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        SaveFilePage.hide()        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SaveFilePage = QtWidgets.QMainWindow()
    ui = Ui_SaveFilePage()
    ui.setupUi(SaveFilePage)
    SaveFilePage.show()
    sys.exit(app.exec_())
