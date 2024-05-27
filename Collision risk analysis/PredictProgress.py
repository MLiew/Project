# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PredictProgress.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


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
        self.donePredictButton.setGeometry(QtCore.QRect(420, 120, 75, 23))
        self.donePredictButton.setObjectName("donePredictButton")
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

    def retranslateUi(self, predictProgressWindow):
        _translate = QtCore.QCoreApplication.translate
        predictProgressWindow.setWindowTitle(_translate("predictProgressWindow", "MainWindow"))
        self.predictProgressLabel.setText(_translate("predictProgressWindow", "Prediction in progress......"))
        self.donePredictButton.setText(_translate("predictProgressWindow", "Done"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    predictProgressWindow = QtWidgets.QMainWindow()
    ui = Ui_predictProgressWindow()
    ui.setupUi(predictProgressWindow)
    predictProgressWindow.show()
    sys.exit(app.exec_())
