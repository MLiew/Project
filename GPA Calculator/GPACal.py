from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt
import pandas as pd
import numpy as np

class GPA():
    """
    This is a class that calculates beihang gpa, with its own unique calculation method.
    """
    
    @classmethod
    def get_gpa(cls, score):
        if score<60:
            print("Failed")
            gpa_score = 0
        else:
            gpa_score = 4 - 3 * np.power((100-score),2) / 1600
        return gpa_score

    @classmethod
    def cal_score(cls, score_arr, point_arr):
        products = np.sum([score * point for score, point in zip(score_arr, point_arr)])
        # print(products)
        sum_point = np.sum(point_arr)
        # print(sum_point)
        gpa = products/sum_point
        return gpa

class FourGrade(GPA):
    @classmethod
    def convert_mark(cls, score):
        """
        Convert the four grading into gpa system, e.g. 优秀=4， 良好=3.5.
        Return:
            gpa_score(float): The gpa grading mark.
        """
        if score == "优秀":
            gpa_score = 4
        elif score == "良好":
            gpa_score = 3.5
        elif score == "中等":
            gpa_score = 2.8
        elif score == "及格":
            gpa_score = 1.7
        elif score == "不及格":
            gpa_score = 0
        else:
            return False
        return gpa_score

class Ui_GPACal(object):
    def setupUi(self, GPACal):
        GPACal.setObjectName("GPACal")
        GPACal.resize(650, 485)
        self.title = QtWidgets.QWidget(GPACal)
        self.title.setObjectName("title")
        self.calButton = QtWidgets.QPushButton(self.title)
        self.calButton.setGeometry(QtCore.QRect(440, 290, 75, 23))
        self.calButton.setObjectName("calButton")
        self.addItemButton = QtWidgets.QPushButton(self.title)
        self.addItemButton.setGeometry(QtCore.QRect(440, 90, 75, 23))
        self.addItemButton.setObjectName("addItemButton")
        self.markLineEdit = QtWidgets.QLineEdit(self.title)
        self.markLineEdit.setGeometry(QtCore.QRect(140, 90, 113, 20))
        self.markLineEdit.setObjectName("markLineEdit")
        self.pointLineEdit = QtWidgets.QLineEdit(self.title)
        self.pointLineEdit.setGeometry(QtCore.QRect(290, 90, 113, 20))
        self.pointLineEdit.setObjectName("pointLineEdit")
        self.chooseGradeComboBox = QtWidgets.QComboBox(self.title)
        self.chooseGradeComboBox.setGeometry(QtCore.QRect(30, 90, 100, 22))
        self.chooseGradeComboBox.setObjectName("chooseGradeComboBox")
        self.chooseGradeComboBox.addItem("Percentile")
        self.chooseGradeComboBox.addItem("5-point grading")
        self.chooseGradeLabel = QtWidgets.QLabel(self.title)
        self.chooseGradeLabel.setGeometry(QtCore.QRect(30, 70, 47, 13))
        self.chooseGradeLabel.setObjectName("chooseGradeLabel")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.chooseGradeLabel.setFont(font)
        self.markLabel = QtWidgets.QLabel(self.title)
        self.markLabel.setGeometry(QtCore.QRect(140, 70, 47, 13))
        self.markLabel.setObjectName("markLabel")
        self.markLabel.setFont(font)
        self.pointLabel = QtWidgets.QLabel(self.title)
        self.pointLabel.setGeometry(QtCore.QRect(290, 70, 47, 13))
        self.pointLabel.setObjectName("pointLabel")
        self.pointLabel.setFont(font)
        self.titeLabel = QtWidgets.QLabel(self.title)
        self.titeLabel.setGeometry(QtCore.QRect(30, 20, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.titeLabel.setFont(font)
        self.titeLabel.setObjectName("titeLabel")
        self.gpaLabel = QtWidgets.QLabel(self.title)
        self.gpaLabel.setGeometry(QtCore.QRect(440, 200, 47, 13))
        self.gpaLabel.setObjectName("gpaLabel")
        font.setPointSize(10)
        self.gpaLabel.setFont(font)
        self.scoreTableView = QtWidgets.QTableView(self.title)
        self.scoreTableView.setGeometry(QtCore.QRect(30, 140, 381, 291))
        self.scoreTableView.setObjectName("scoreTableView")
        self.gpaLineEdit = QtWidgets.QLineEdit(self.title)
        self.gpaLineEdit.setGeometry(QtCore.QRect(440, 230, 161, 31))
        self.gpaLineEdit.setObjectName("gpaLineEdit")
        self.recalButton = QtWidgets.QPushButton(self.title)
        self.recalButton.setGeometry(QtCore.QRect(530, 290, 75, 23))
        self.recalButton.setObjectName("recalButton")
        GPACal.setCentralWidget(self.title)
        self.menubar = QtWidgets.QMenuBar(GPACal)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 647, 21))
        self.menubar.setObjectName("menubar")
        GPACal.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(GPACal)
        self.statusbar.setObjectName("statusbar")
        GPACal.setStatusBar(self.statusbar)

        self.retranslateUi(GPACal)
        QtCore.QMetaObject.connectSlotsByName(GPACal)

    def retranslateUi(self, GPACal):
        _translate = QtCore.QCoreApplication.translate
        GPACal.setWindowTitle(_translate("GPACal", "GPA Calculator"))
        self.calButton.setText(_translate("GPACal", "Calculate"))
        self.addItemButton.setText(_translate("GPACal", "Add to List"))
        self.chooseGradeLabel.setText(_translate("GPACal", "System"))
        self.markLabel.setText(_translate("GPACal", "Score"))
        self.pointLabel.setText(_translate("GPACal", "Point"))
        self.titeLabel.setText(_translate("GPACal", "Beihang GPA Calculator"))
        self.gpaLabel.setText(_translate("GPACal", "GPA:"))
        self.recalButton.setText(_translate("GPACal", "Recalculation"))
    
class pandasModel(QtCore.QAbstractTableModel):
    """
    PandasModel is a class that create a data model for tableView.
    """
    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

# This class inherit from the Ui_GPACal class
class MainWindow(QtWidgets.QMainWindow, Ui_GPACal):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.button_clicked()
        
        self.score_arr = []
        self.point_arr = []
        self.grade_arr = []
        self.gpa_score_arr = []
    
    def button_clicked(self):
        """
        Connect functions to button. 
        addItemButton: connect to add_score()
        calButton: connect to cal_score()
        recalButton: connect to recal_score()
        """
        self.addItemButton.clicked.connect(self.add_score)
        self.calButton.clicked.connect(self.cal_score)
        self.recalButton.clicked.connect(self.recal_score)

    def keyPressEvent(self, e):
        """
        Detect key press event, specifically F5, Return and Enter key.
        When F5 key is pressed, close the window. 
        Meanwhile, when Return and Enter key are pressed, run add_score().
        """
        if e.key() == Qt.Key_F5:
            print("Window close")
            self.close()
        elif (e.key() == Qt.Key_Return) or (e.key() == Qt.Key_Enter):
            print("Return")
            self.add_score()
        
    def get_grade_system(self):
        """
        Get the current text in the chooseGradeComboBox.
        """
        return self.chooseGradeComboBox.currentText()

    def get_score(self):
        """
        Get current score in the markLineEdit.
        """
        return self.markLineEdit.text()

    def get_point(self):
        """
        Get current point in the pointLineEdit.
        """
        return self.pointLineEdit.text()
    
    def add_score(self):
        """
        Add the scores into the table list view widget for further calcultion.
        """
        print("Add item to list")

        # Get the score, point and grading system
        score = self.get_score()
        point = float(self.get_point())
        grade = self.get_grade_system()
        
        # Determine the grading system and return gpa score
        if grade == "Percentile":
            gpa_score = GPA.get_gpa(float(score))
            self.store_data(score, grade, point, gpa_score)
        elif grade == "5-point grading":
            gpa_score = FourGrade.convert_mark(score)
            if gpa_score == False:          
                # Pop up message box  
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Grade input")
                msg.setText("Grade input is wrong")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setStandardButtons(QtWidgets.QMessageBox.Retry)
                msg.setDefaultButton(QtWidgets.QMessageBox.Retry)
                msg.exec_()
                gpa_score = None
            else:
                self.store_data(score, grade, point, gpa_score)

    def cal_score(self):
        """
        Compute GPA and display it on the UI.
        """
        print("Calculating GPA")
        self.total_gpa = GPA.cal_score(self.gpa_score_arr, self.point_arr)
        self.total_gpa = np.round(self.total_gpa, 2)
        print(self.total_gpa)
        self.gpaLineEdit.setText(str(self.total_gpa))

    def recal_score(self):
        """
        Reset the calculation model.
        """
        print("Recalulating")
        self.score_arr = []
        self.grade_arr = []
        self.point_arr = []
        self.gpa_score_arr = []
       
        # clear the table view
        self.scoreTableView.setModel(None)
    
    def store_data(self, score, grade, point, gpa_score):
        """
        Append score, point and grading sys. into list respectively.
        Args:
            score(float): Score
            grade(float): Grade
            point(float): Point
            gpa_score(float): Converted GPA score
        """
        self.score_arr.append(score)
        self.grade_arr.append(grade)
        self.point_arr.append(point)
        self.gpa_score_arr.append(gpa_score)
        
        print(self.score_arr, self.point_arr, self.gpa_score_arr)

        # Show data in table view
        self.table_view()
    
    def table_view(self):
        """
        Prepare the data into pandas dataframe format. Create a pandasModel and subs data into it.
        """
        df = pd.DataFrame({'Grading System': self.grade_arr,
                   'Score': self.score_arr,
                   'Point': self.point_arr
                    })
        
        model = pandasModel(df)
        self.scoreTableView.setModel(model)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())