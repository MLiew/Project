# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PredictPage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PredictPageWindow(object):
    def __init__(self):
        pass
        # To get data from the Main Window
        # Pass in the parameter from the Main Window
        # self.message = message
        # self.data = data
        # print(self.data)
        # print(self.message)

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PredictPageWindow = QtWidgets.QMainWindow()
    ui = Ui_PredictPageWindow()
    ui.setupUi(PredictPageWindow)
    PredictPageWindow.show()
    sys.exit(app.exec_())
