from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pyg

def show_error(title, message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(title)
    msg.setInformativeText(message)
    msg.setWindowTitle(title)
    msg.exec_()
