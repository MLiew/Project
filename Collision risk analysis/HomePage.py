# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HomePage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pandas as pd
from functools import partial
from multiprocessing import Process
import web_crawl_test, data_prepro, tle_clustering, tle_classification, relative_distance, rel_dist_prepro_cluster, produce_latex_report

class MySignals(QtCore.QObject):
    predict_data_signal = QtCore.pyqtSignal(object)

    def __init__(self):
        super(MySignals, self).__init__()

class SavePageThread(QtCore.QThread):
    filename_signal = QtCore.pyqtSignal(str) 
    func_signal = QtCore.pyqtSignal(str)
    method_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(SavePageThread, self).__init__()
        self.file_name = ''
        self.func = ''
        self.method = ''
        self.filename_signal.connect(self.get_file_name)
        self.method_signal.connect(self.get_method)
    
    @QtCore.pyqtSlot(str)
    def get_file_name(self, filename):
        self.file_name = filename

    @QtCore.pyqtSlot(str)
    def get_method(self, method):
        self.method = method
        temp_folder = 'C:/temp_data/'
        with open('%sTLE_method.txt'%temp_folder, 'w') as method_txt:
            method_txt.write(self.method)

    def run(self):
        print(self.file_name)

        self.func = 'f1'
        self.func_signal.emit(self.func)
        print("web crawling......")
        web_crawl_test.main_web_crawl(self.file_name)

        self.func = 'f2'
        self.func_signal.emit(self.func)
        print("data preprocessing......")
        data_prepro.main_prepro_one(self.file_name)

        self.func = 'f3'
        self.func_signal.emit(self.func)
        print("building clustering model......")
        print(self.method)
        sil_avg_data, ch_score, Sum_of_squared_distances, best_num_clusters, tle_norm_trained_data, trained_data, group_density, group_details = tle_clustering.main_tle_cluster(self.file_name, self.method)
        
        
        self.sil_avg_data = sil_avg_data
        self.best_num_clusters_tle = str(best_num_clusters)
        
        self.func = 'f4'
        self.func_signal.emit(self.func)
        print("clustering model built......")

class PredictProgressThread(QtCore.QThread):
    predict_data_signal = QtCore.pyqtSignal(object)
    file_path_signal = QtCore.pyqtSignal(str)
    predict_func_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(PredictProgressThread, self).__init__()
        self.file_path = ''
        self.predict_input = []
        self.file_path_signal.connect(self.get_file_path)
        self.predict_data_signal.connect(self.get_predict_data)
        
    @QtCore.pyqtSlot(str)
    def get_file_path(self, filepath):
        self.file_path = filepath
        print(self.file_path, 'get_file_path method called')
    
    @QtCore.pyqtSlot(object)
    def get_predict_data(self, data):
        self.predict_input = data
        print(self.predict_input,'get_predict_data called')
    
    def get_TLE_method(self):
        temp_folder = 'C:/temp_data/'
        method = open('%sTLE_method.txt'%temp_folder, 'r')
        self.method = method.read()
        return self.method

    def run(self):
        print(self.file_path)
        print(self.predict_input)
        self.predict_func = 'predict_f1'
        self.predict_func_signal.emit(self.predict_func)
        print("building prediction model......")
        self.random_forest, self.max_estimators, self.rf_acc, self.rf_precision, self.rf_recall, self.rf_f1_score, self.rf_predict_input = tle_classification.main_rf(self.file_path, self.predict_input)

        self.predict_func = 'predict_f2'
        self.predict_func_signal.emit(self.predict_func)
        print("Calculating the relative distance......")
        self.total_dist_df = relative_distance.main_rel_dist(self.file_path, self.predict_input, self.rf_predict_input)

        self.predict_func = 'predict_f3'
        self.predict_func_signal.emit(self.predict_func)
        print("Relative distance data preprocessing......")
        self.z_score_df, self.removed_outlier_dist, self.removed_outlier_dist_desc, self.z_score_final_df = rel_dist_prepro_cluster.main_dist_prepro(self.file_path)
        
        self.predict_func = 'predict_f4'
        self.predict_func_signal.emit(self.predict_func)
        print("Building relative distance clustering model......")
        self.sil_avg_data, self.Sum_of_squared_distances, self.best_num_clusters, self.dist_norm_trained_data, self.dist_trained_data = tle_clustering.main_dist_cluster(self.file_path, 'KMeans')

        # Produce report part
        self.predict_func = 'predict_f5'
        self.predict_func_signal.emit(self.predict_func)
        print("Producing risk analysis report")
        # The method here is the clustering method for TLE data
        temp_folder = 'C:/temp_data/'
        method = open('%sTLE_method.txt'%temp_folder, 'r')
        self.method = method.read()
        produce_latex_report.main_report(self.file_path, self.method)

class Ui_Homepage(object):
    def setupUi(self, Homepage):
        Homepage.setObjectName("Homepage")
        Homepage.resize(700, 700)
        self.centralwidget = QtWidgets.QWidget(Homepage)
        self.centralwidget.setObjectName("centralwidget")
        self.hpNextButton = QtWidgets.QPushButton(self.centralwidget)
        self.hpNextButton.setGeometry(QtCore.QRect(230, 390, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.hpNextButton.setFont(font)
        self.hpNextButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.hpNextButton.setStyleSheet("")
        self.hpNextButton.setObjectName("hpNextButton")
        self.hpTitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.hpTitleLabel.setGeometry(QtCore.QRect(80, 10, 401, 141))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.hpTitleLabel.setFont(font)
        self.hpTitleLabel.setLineWidth(1)
        self.hpTitleLabel.setTextFormat(QtCore.Qt.RichText)
        self.hpTitleLabel.setWordWrap(True)
        self.hpTitleLabel.setObjectName("hpTitleLabel")
        self.hpSatellitePicLabel = QtWidgets.QLabel(self.centralwidget)
        self.hpSatellitePicLabel.setGeometry(QtCore.QRect(120, 130, 321, 241))
        self.hpSatellitePicLabel.setText("")
        self.hpSatellitePicLabel.setPixmap(QtGui.QPixmap("PyQt Icon/satellite.jpg"))
        self.hpSatellitePicLabel.setScaledContents(True)
        self.hpSatellitePicLabel.setObjectName("hpSatellitePicLabel")
        self.hpSatellitePicLabel.setAlignment(QtCore.Qt.AlignCenter)
        Homepage.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Homepage)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 569, 21))
        self.menubar.setObjectName("menubar")
        Homepage.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Homepage)
        self.statusbar.setObjectName("statusbar")
        Homepage.setStatusBar(self.statusbar)

        self.retranslateUi(Homepage)
        QtCore.QMetaObject.connectSlotsByName(Homepage)

        self.hpNextButton.clicked.connect(self.openSaveFilePageWindow)

    def retranslateUi(self, Homepage):
        _translate = QtCore.QCoreApplication.translate
        Homepage.setWindowTitle(_translate("Homepage", "Satellite collision risk analysis v0.1"))
        self.hpNextButton.setText(_translate("Homepage", "Next"))
        self.hpTitleLabel.setText(_translate("Homepage", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">SATELLITE COLLISION RISK ANALYSIS BASED ON DATA MINING</span></p><p align=\"center\"><span style=\" font-size:16pt;\">BASED ON DATA MINING</span></p></body></html>"))

    def openSaveFilePageWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SaveFilePage()
        self.ui.setupUi(self.window)
        Homepage.hide()
        self.window.show()

class Ui_SaveFilePage(object):
    def setupUi(self, SaveFilePage):
        SaveFilePage.setObjectName("SaveFilePage")
        SaveFilePage.resize(1000,700)
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
        self.progressBar.setProperty("value", 0)
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
        self.confirmFileButton.setGeometry(QtCore.QRect(370, 220, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.confirmFileButton.setFont(font)
        self.confirmFileButton.setObjectName("confirmFileButton")
        self.chooseClusAlgoLabel = QtWidgets.QLabel(self.centralwidget)
        self.chooseClusAlgoLabel.setGeometry(QtCore.QRect(40, 140, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.chooseClusAlgoLabel.setFont(font)
        self.chooseClusAlgoLabel.setObjectName("chooseClusAlgoLabel")
        self.clusterAlgoComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.clusterAlgoComboBox.setGeometry(QtCore.QRect(280, 140, 171, 41))
        self.clusterAlgoComboBox.addItem("KMeans")
        self.clusterAlgoComboBox.addItem("Spectral")
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
       
        # Create a thread
        self.my_thread = SavePageThread()

        self.progressBar.hide()
        self.InProgressLabel.hide()
        self.nextButton.hide()

        self.getPathButton.clicked.connect(self.get_file_path)
        self.confirmFileButton.clicked.connect(self.start_process)

        # Pass the SaveFilePage QMainWindow into the button click function using partial()
        self.nextButton.clicked.connect(partial(self.openPredictWindow, SaveFilePage))
        
        # Connect function Signal
        self.my_thread.func_signal.connect(self.current_func)

    def retranslateUi(self, SaveFilePage):
        _translate = QtCore.QCoreApplication.translate
        SaveFilePage.setWindowTitle(_translate("SaveFilePage", "MainWindow"))
        self.ChooseFilelabel.setText(_translate("SaveFilePage", "Choose File Directory to save file:"))
        self.InProgressLabel.setText(_translate("SaveFilePage", "In Progress......"))
        self.nextButton.setText(_translate("SaveFilePage", "Next"))
        self.getPathButton.setText(_translate("SaveFilePage", "..."))
        self.confirmFileButton.setText(_translate("SaveFilePage", "Confirm"))
        self.chooseClusAlgoLabel.setText(_translate("SaveFilePage", "Choose Clustering Algorithm:"))

    def get_file_path(self, SaveFilePage):
            file_name = QtWidgets.QFileDialog.getExistingDirectory(None, "Select File Directory to Save File", "")
            print(file_name)
            self.fileTextEdit.setText(file_name)
            self.file_name = file_name

            folder = 'temp_data'
            newpath = 'C:/'+ folder

            if not os.path.exists(newpath):
                os.makedirs(newpath)

            with open('%s/filename.txt'%newpath, 'w') as filename_txt:
                filename_txt.write(self.file_name)

    def current_func(self, func):
        self.func = func
        print(self.func)
    
    def handleTimer(self):
        self.InProgressLabel.show()
        self.progressBar.show()
        self.value = self.progressBar.value() 

        if self.value <= 100:
            if self.func == 'f1':
                if self.value < 30:
                    self.value += 1
                    print("message", self.value)
                    self.progressBar.setValue(self.value)
                    self.InProgressLabel.setText("Web crawling in progress......")                

            elif self.func == 'f2':
                if self.value <= 60:
                    self.value += 1
                    self.progressBar.setValue(self.value)   
                    self.InProgressLabel.setText("Data preprocessing in progress......")
            
            elif self.func == 'f3':
                if self.value <= 90:
                    self.value += 1
                    self.progressBar.setValue(self.value)   
                    self.InProgressLabel.setText("Clustering model building in progress......")
            
            elif self.func =='f4':
                if self.value <= 99:
                    self.value += 1
                    self.InProgressLabel.setText("Clustering model almost done......")
                elif self.value == 100:
                    self.InProgressLabel.setText("Clustering model built......")
                self.progressBar.setValue(self.value)
                self.nextButton.show()

    def start_process(self):
        self.method = self.clusterAlgoComboBox.currentText()
        self.my_thread.method_signal.emit(self.method)        
        print(self.clusterAlgoComboBox.currentText())
        
        self.timer.timeout.connect(self.handleTimer)
        self.timer.start(1000)
        print("timer starts......")
        
        print("thread start......")

        self.my_thread.start()
        self.my_thread.filename_signal.emit(self.file_name)
        
    def openPredictWindow(self, SaveFilePage):
        # Create a QMainWindow for Predict Page
        self.window_predict = QtWidgets.QMainWindow()
        
        # Create an Ui_PredictPageWindow() object
        self.ui_predict = Ui_PredictPageWindow()

        # Pass the Ui_PredictPageWindow() object to the setupUi()
        self.ui_predict.setupUi(self.window_predict)
        
        # Hide the SaveFilePage QMainWindow which get from this class setupUI()
        SaveFilePage.close()

        # Show the Predict Page
        self.window_predict.show()  

class Ui_PredictPageWindow(object):
    def setupUi(self, PredictPageWindow):
        PredictPageWindow.setObjectName("PredictPageWindow")
        PredictPageWindow.resize(579, 452)
        self.centralwidget = QtWidgets.QWidget(PredictPageWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.inputLabel = QtWidgets.QLabel(self.centralwidget)
        self.inputLabel.setGeometry(QtCore.QRect(30, 20, 431, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.inputLabel.setFont(font)
        self.inputLabel.setObjectName("inputLabel")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(60, 70, 471, 291))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.inclineLabel = QtWidgets.QLabel(self.groupBox)
        self.inclineLabel.setGeometry(QtCore.QRect(20, 20, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.inclineLabel.setFont(font)
        self.inclineLabel.setObjectName("inclineLabel")
        self.raanLabel = QtWidgets.QLabel(self.groupBox)
        self.raanLabel.setGeometry(QtCore.QRect(20, 70, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.raanLabel.setFont(font)
        self.raanLabel.setObjectName("raanLabel")
        self.eccenLabel = QtWidgets.QLabel(self.groupBox)
        self.eccenLabel.setGeometry(QtCore.QRect(20, 110, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.eccenLabel.setFont(font)
        self.eccenLabel.setObjectName("eccenLabel")
        self.apLabel = QtWidgets.QLabel(self.groupBox)
        self.apLabel.setGeometry(QtCore.QRect(20, 160, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.apLabel.setFont(font)
        self.apLabel.setObjectName("apLabel")
        self.manomalyLabel = QtWidgets.QLabel(self.groupBox)
        self.manomalyLabel.setGeometry(QtCore.QRect(20, 210, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.manomalyLabel.setFont(font)
        self.manomalyLabel.setObjectName("manomalyLabel")
        self.smaxisLabel = QtWidgets.QLabel(self.groupBox)
        self.smaxisLabel.setGeometry(QtCore.QRect(20, 260, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.smaxisLabel.setFont(font)
        self.smaxisLabel.setObjectName("smaxisLabel")
        self.inclineLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.inclineLineEdit.setGeometry(QtCore.QRect(210, 20, 151, 20))
        self.inclineLineEdit.setObjectName("inclineLineEdit")
        self.raanLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.raanLineEdit.setGeometry(QtCore.QRect(210, 70, 151, 20))
        self.raanLineEdit.setObjectName("raanLineEdit")
        self.eccenLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.eccenLineEdit.setGeometry(QtCore.QRect(210, 110, 151, 20))
        self.eccenLineEdit.setObjectName("eccenLineEdit")
        self.apLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.apLineEdit.setGeometry(QtCore.QRect(210, 160, 151, 20))
        self.apLineEdit.setObjectName("apLineEdit")
        self.manomalyLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.manomalyLineEdit.setGeometry(QtCore.QRect(210, 210, 151, 20))
        self.manomalyLineEdit.setObjectName("manomalyLineEdit")
        self.smaxisLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.smaxisLineEdit.setGeometry(QtCore.QRect(210, 260, 151, 20))
        self.smaxisLineEdit.setObjectName("smaxisLineEdit")
        self.degreeLabel_1 = QtWidgets.QLabel(self.groupBox)
        self.degreeLabel_1.setGeometry(QtCore.QRect(380, 20, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.degreeLabel_1.setFont(font)
        self.degreeLabel_1.setObjectName("degreeLabel_1")
        self.degreeLabel_2 = QtWidgets.QLabel(self.groupBox)
        self.degreeLabel_2.setGeometry(QtCore.QRect(380, 70, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.degreeLabel_2.setFont(font)
        self.degreeLabel_2.setObjectName("degreeLabel_2")
        self.degreeLabel_3 = QtWidgets.QLabel(self.groupBox)
        self.degreeLabel_3.setGeometry(QtCore.QRect(380, 160, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.degreeLabel_3.setFont(font)
        self.degreeLabel_3.setObjectName("degreeLabel_3")
        self.degreeLabel_4 = QtWidgets.QLabel(self.groupBox)
        self.degreeLabel_4.setGeometry(QtCore.QRect(380, 210, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.degreeLabel_4.setFont(font)
        self.degreeLabel_4.setObjectName("degreeLabel_4")
        self.meterLabel_1 = QtWidgets.QLabel(self.groupBox)
        self.meterLabel_1.setGeometry(QtCore.QRect(380, 260, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.meterLabel_1.setFont(font)
        self.meterLabel_1.setObjectName("meterLabel_1")
        self.predictButton = QtWidgets.QPushButton(self.centralwidget)
        self.predictButton.setGeometry(QtCore.QRect(440, 380, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.predictButton.setFont(font)
        self.predictButton.setObjectName("predictButton")
        PredictPageWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PredictPageWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 579, 21))
        self.menubar.setObjectName("menubar")
        PredictPageWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PredictPageWindow)
        self.statusbar.setObjectName("statusbar")
        PredictPageWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(PredictPageWindow)
        QtCore.QMetaObject.connectSlotsByName(PredictPageWindow)

        self.predictButton.clicked.connect(partial(self.get_predict_input, PredictPageWindow))

    def retranslateUi(self, PredictPageWindow):
        _translate = QtCore.QCoreApplication.translate
        PredictPageWindow.setWindowTitle(_translate("PredictPageWindow", "MainWindow"))
        self.inputLabel.setText(_translate("PredictPageWindow", "Please Input Orbital Data for Prediction:"))
        self.inclineLabel.setText(_translate("PredictPageWindow", "Inclination Angle"))
        self.raanLabel.setText(_translate("PredictPageWindow", "RAAN"))
        self.eccenLabel.setText(_translate("PredictPageWindow", "Eccentricity"))
        self.apLabel.setText(_translate("PredictPageWindow", "Argument of Perigee"))
        self.manomalyLabel.setText(_translate("PredictPageWindow", "Mean Anomaly"))
        self.smaxisLabel.setText(_translate("PredictPageWindow", "Semi-major Axis"))
        self.degreeLabel_1.setText(_translate("PredictPageWindow", "(in degree)"))
        self.degreeLabel_2.setText(_translate("PredictPageWindow", "(in degree)"))
        self.degreeLabel_3.setText(_translate("PredictPageWindow", "(in degree)"))
        self.degreeLabel_4.setText(_translate("PredictPageWindow", "(in degree)"))
        self.meterLabel_1.setText(_translate("PredictPageWindow", "(in m)"))
        self.predictButton.setText(_translate("PredictPageWindow", "Predict"))

    def get_predict_input(self, PredictPageWindow):
        incline_data = self.inclineLineEdit.text()
        raan_data = self.raanLineEdit.text()
        eccen_data = self.eccenLineEdit.text()
        ap_data = self.apLineEdit.text()
        manomaly_data = self.manomalyLineEdit.text()
        smaxis_data = self.smaxisLineEdit.text()
        
        if (len(incline_data) == 0) or (len(raan_data) == 0) or (len(eccen_data) == 0) or (len(ap_data) == 0) or (len(manomaly_data) == 0) or (len(smaxis_data) == 0):
            print("Input data not completed......")
        
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Orbital data input")
            msg.setText("Input data not completed!!")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setStandardButtons(QtWidgets.QMessageBox.Retry)
            msg.setDefaultButton(QtWidgets.QMessageBox.Retry)
            msg.exec_()

        else:
            self.incline_data = float(incline_data)
            self.raan_data = float(raan_data)
            self.eccen_data = float(eccen_data)
            self.ap_data = float(ap_data)
            self.manomaly_data = float(manomaly_data)
            self.smaxis_data = float(smaxis_data)
            print("Data completed......")
            
            self.predict_input = np.array([[self.incline_data, self.raan_data, self.eccen_data, self.ap_data, self.manomaly_data, self.smaxis_data]])
            
            # Write predict data into txt file
            np.savetxt('C:/temp_data/predict_input.txt', self.predict_input, delimiter=',')
            print(self.predict_input)
            
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Orbital data input")
            msg.setText("Input data completed!!")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            
            self.openPredictProgressWindow(PredictPageWindow)
    
    def openPredictProgressWindow(self, PredictPageWindow):
        self.window_progress = QtWidgets.QMainWindow()
        self.ui_progress = Ui_predictProgressWindow()
        self.ui_progress.setupUi(self.window_progress)
        PredictPageWindow.close()
        self.window_progress.show()  

        self.ui_progress.startPredict()

class Ui_predictProgressWindow(object):
    def setupUi(self, predictProgressWindow):
        predictProgressWindow.setObjectName("predictProgressWindow")
        predictProgressWindow.resize(556, 244)
        self.centralwidget = QtWidgets.QWidget(predictProgressWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.predictProgressLabel = QtWidgets.QLabel(self.centralwidget)
        self.predictProgressLabel.setGeometry(QtCore.QRect(30, 20, 491, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.predictProgressLabel.setFont(font)
        self.predictProgressLabel.setObjectName("predictProgressLabel")
        self.predictProgressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.predictProgressBar.setGeometry(QtCore.QRect(30, 60, 501, 31))
        self.predictProgressBar.setProperty("value", 0)
        self.predictProgressBar.setObjectName("predictProgressBar")
        self.donePredictButton = QtWidgets.QPushButton(self.centralwidget)
        self.donePredictButton.setGeometry(QtCore.QRect(400, 120, 90, 30))
        self.donePredictButton.setObjectName("donePredictButton")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.donePredictButton.setFont(font)
        predictProgressWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(predictProgressWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 556, 21))
        self.menubar.setObjectName("menubar")
        predictProgressWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(predictProgressWindow)
        self.statusbar.setObjectName("statusbar")
        predictProgressWindow.setStatusBar(self.statusbar)

        self.retranslateUi(predictProgressWindow)
        QtCore.QMetaObject.connectSlotsByName(predictProgressWindow)

        self.predict_timer =QtCore.QTimer()
        self.predict_thread = PredictProgressThread()

        self.donePredictButton.clicked.connect(partial(self.closeWindow, predictProgressWindow))

    def retranslateUi(self, predictProgressWindow):
        _translate = QtCore.QCoreApplication.translate
        predictProgressWindow.setWindowTitle(_translate("predictProgressWindow", "MainWindow"))
        self.predictProgressLabel.setText(_translate("predictProgressWindow", "Prediction in progress......"))
        self.donePredictButton.setText(_translate("predictProgressWindow", "Done"))

    def startPredict(self):
        # Extract filepath selected by the user
        filename_txt = open('C:/temp_data/filename.txt', 'r')
        self.file_name = filename_txt.readline()
        print(self.file_name)
        self.predict_thread.file_path_signal.emit(self.file_name)

        # Extract predict data
        predict_data = np.loadtxt("C:/temp_data/predict_input.txt", delimiter = ',')
        self.predict_data = np.array([predict_data])
        print(self.predict_data)
        self.predict_thread.predict_data_signal.emit(self.predict_data)

        # predictHandleTimer should start here
        self.predict_timer.timeout.connect(self.predictHandleTimer)
        self.predict_timer.start(1000)

        print("timer starts......")
        print("thread start......")

        self.predict_thread.start()
        self.predict_thread.predict_func_signal.connect(self.currentPredictFunc)

    def predictHandleTimer(self):
        self.predictProgressLabel.show()
        self.predictProgressBar.show()
        self.value = self.predictProgressBar.value() 

        if self.value <= 100:
            if self.predict_func == 'predict_f1':
                if self.value < 30:
                    self.value += 1
                    print("message", self.value)
                    self.predictProgressBar.setValue(self.value)
                    self.predictProgressLabel.setText("Prediction model building in progress......")                

            elif self.predict_func == 'predict_f2':
                if self.value <= 50:
                    self.value += 1
                    self.predictProgressBar.setValue(self.value)   
                    self.predictProgressLabel.setText("Relative distance calculating in progress......")
            
            elif self.predict_func == 'predict_f3':
                if self.value <= 70:
                    self.value += 1
                    self.predictProgressBar.setValue(self.value)   
                    self.predictProgressLabel.setText("Data preprocessing in progress......")
            
            elif self.predict_func == 'predict_f4':
                if self.value <= 85:
                    self.value += 1
                    self.predictProgressBar.setValue(self.value)   
                    self.predictProgressLabel.setText("Clustering model building in progress......")
            
            elif self.predict_func =='predict_f5':
                if self.value <= 99:
                    self.value += 1
                    self.predictProgressLabel.setText("Analysis report almost done......")
                elif self.value == 100:
                    self.predictProgressLabel.setText("Analysis report done......")
                self.predictProgressBar.setValue(self.value)
                self.donePredictButton.show()

    def currentPredictFunc(self, predict_func):
        self.predict_func = predict_func
        print(self.predict_func)

    def closeWindow(self, predictProgressWindow):
        predictProgressWindow.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Homepage = QtWidgets.QMainWindow()
    ui = Ui_Homepage()
    ui.setupUi(Homepage)
    Homepage.show()
    sys.exit(app.exec_())