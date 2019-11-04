from PySide2 import QtWidgets, QtGui, QtCore
from res import Res

cmd = ('起飞', '降落', '上升', '下降', '前进', '后退', '向左', '向右', '左旋', '右旋')


class EventWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon(Res.mainWindowIcon))
        self.setWindowTitle("事件")
        self.setFixedWidth(480)
        self.setFixedHeight(80)
        self.index = -1

        events = QtWidgets.QComboBox()
        events.addItems(['起飞', '降落', '上升', '下降', '前进', '后退', '向左', '向右', '左旋', '右旋', '悬停'])
        ok = QtWidgets.QPushButton("确定")
        layout1 = QtWidgets.QHBoxLayout()
        layout1.addWidget(QtWidgets.QLabel("事件"), 1)
        layout1.addWidget(events, 6)
        layout1.addStretch(6)
        layout1.addWidget(ok, 1)
        events.currentTextChanged.connect(self.events_changed)
        ok.clicked.connect(self.ok_slot)
        self.events = events

        value = QtWidgets.QLineEdit("0")
        value.setEnabled(False)
        time = QtWidgets.QLineEdit("5")
        time.setEnabled(False)
        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(QtWidgets.QLabel("速度(cm/s、deg/s)"))
        layout2.addWidget(value)
        layout2.addWidget(QtWidgets.QLabel("时间(s)"))
        layout2.addWidget(time)
        self.value = value
        self.time = time

        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.addLayout(layout1)
        mainlayout.addLayout(layout2)
        self.setLayout(mainlayout)

    @QtCore.Slot(str)
    def events_changed(self, text):
        if text == "起飞" or text == "降落":
            self.value.setEnabled(False)
            self.time.setEnabled(False)
        elif text == "悬停":
            self.time.setEnabled(True)
        else:
            self.value.setEnabled(True)
            self.time.setEnabled(True)

    def edit(self, data):
        super(EventWindow, self).exec_()

    @QtCore.Slot()
    def ok_slot(self):
        data = {'cmd': cmd[self.events.currentIndex()], 'value': self.value.text(), 'time': self.time.text()}
        if self.index == -1:
            Res.events.append(data)
        else:
            Res.events.insert(self.index+1, data)
        self.index = -1
        self.accept()
