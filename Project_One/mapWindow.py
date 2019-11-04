from PySide2 import QtWidgets, QtGui, QtWebEngineWidgets, QtCore
from res import Res
import os


class MapWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon(Res.mainWindowIcon))
        self.setWindowTitle("地图")
        self.resize(1280, 860)

        map_view = QtWebEngineWidgets.QWebEngineView()
        url = "file:///" + os.getcwd() + Res.mapUrl
        url = eval(repr(url).replace('\\\\', '/'))
        map_view.load(QtCore.QUrl(url))

        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.addWidget(map_view)
        self.setLayout(mainlayout)
