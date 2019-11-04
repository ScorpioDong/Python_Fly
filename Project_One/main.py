import sys
from PySide2 import QtWidgets
from mainWindow import MainWindow
from tcpClient import tcpClient

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
