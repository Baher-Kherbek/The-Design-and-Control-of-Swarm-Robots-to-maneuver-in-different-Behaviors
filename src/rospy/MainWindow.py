"""
Author:
	Baher Kher Bek
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
import numpy as np
import cv2.aruco as aruco
class VideoThread(QThread):
    ImageUpdate = pyqtSignal(QImage)


class VideoThread(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while True:
            _, frame = cap.read()
        
            Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            toQt = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
            Pic = toQt.scaled(1000, 1000, Qt.KeepAspectRatio)
            self.ImageUpdate.emit(Pic)

        # Image = cv2.imread('aruco.png')
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        arucoParameters = aruco.DetectorParameters_create()
        corners, ids, rejectedPoints = aruco.detectMarkers(Image, aruco_dict, parameters=arucoParameters)
        frame = aruco.drawDetectedMarkers(Image, corners)
        toQt = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
        Pic = toQt.scaled(1000, 1000, Qt.KeepAspectRatio)
        self.ImageUpdate.emit(Pic)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.windowWidth = 2560
        self.windowHeight = 1600
        self.buttonWidth = 600
        self.buttonHeight = 200
        self.buttonCounter = 0

        MainWindow.resize(self.windowWidth, self.windowHeight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.start_Button = QtWidgets.QPushButton(self.centralwidget)
        self.start_Button.setGeometry(QtCore.QRect(self.windowWidth // 2 - self.buttonWidth // 2, self.windowHeight // 2 - self.buttonHeight // 2, self.buttonWidth, self.buttonHeight))
        self.start_Button.setObjectName("pushButton")
        self.start_Button.clicked.connect(self.start)
        self.buttonCounter += 1

        self.GoToPose_Button = QtWidgets.QPushButton(self.centralwidget)
        self.GoToPose_Button.setGeometry(QtCore.QRect(200, 100, self.buttonWidth, self.buttonHeight))
        self.GoToPose_Button.setObjectName("pushButton_2")
        self.GoToPose_Button.clicked.connect(self.test)
        self.GoToPose_Button.hide()
        self.buttonCounter += 1

        self.keyboardControl_Button = QtWidgets.QPushButton(self.centralwidget)
        self.keyboardControl_Button.setGeometry(QtCore.QRect(200, 350, self.buttonWidth, self.buttonHeight))
        self.keyboardControl_Button.setObjectName('Keyboard Control')
        self.keyboardControl_Button.hide()
        self.buttonCounter += 1

        


        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 913, 22))
        self.menubar.setObjectName("menubar")

        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(1800, 0, 1000, 1000))
        self.image_label.setObjectName("label")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        # set the vbox layout as the widgets layout

        # create the video capture thread
        self.thread = VideoThread()
        self.thread.start()
        self.thread.ImageUpdate.connect(self.imageUpdateSlot)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_Button.setText(_translate("MainWindow", "Start"))
        self.GoToPose_Button.setText(_translate("MainWindow", "Go To Position"))
        self.keyboardControl_Button.setText(_translate('MainWindow', "Keyboard Control"))

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(500, 500, Qt.KeepAspectRatio)
        qt_image = QPixmap.fromImage(p)
        self.image_label.setPixmap(qt_image)
        cv2.setMouseCallback('qt_image', self.callback())

    def imageUpdateSlot(self, img):
        self.image_label.setPixmap(QPixmap.fromImage(img))

    def start(self):
        self.GoToPose_Button.show()
        self.start_Button.hide()
        self.keyboardControl_Button.show()

    def callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, y)
    

    def test(self):
        print('hi')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
