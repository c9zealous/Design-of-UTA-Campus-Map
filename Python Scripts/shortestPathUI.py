# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shortestPathUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(518, 372)
        self.source = QtWidgets.QPushButton(Dialog)
        self.source.setGeometry(QtCore.QRect(120, 100, 93, 28))
        self.source.setObjectName("source")
        self.destination = QtWidgets.QPushButton(Dialog)
        self.destination.setGeometry(QtCore.QRect(330, 100, 93, 28))
        self.destination.setObjectName("destination")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 70, 53, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(340, 70, 71, 16))
        self.label_2.setObjectName("label_2")
        self.submitButton = QtWidgets.QPushButton(Dialog)
        self.submitButton.setGeometry(QtCore.QRect(220, 200, 93, 28))
        self.submitButton.setObjectName("submitButton")

        

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.source.setText(_translate("Dialog", "Source"))
        self.destination.setText(_translate("Dialog", "Destination"))
        self.label.setText(_translate("Dialog", "Source"))
        self.label_2.setText(_translate("Dialog", "Destination"))
        self.submitButton.setText(_translate("Dialog", "Submit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

