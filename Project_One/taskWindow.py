from PySide2 import QtWidgets, QtGui, QtCore
from eventWindow import EventWindow
from res import Res


class ListItem(QtWidgets.QFrame):
    def __init__(self, cmd, value, time):
        super(ListItem, self).__init__()

        label1 = QtWidgets.QLabel(cmd)
        label2 = QtWidgets.QLabel(str(value))
        label3 = QtWidgets.QLabel(str(time))
        label4 = QtWidgets.QLabel("距离(高度、角度)")
        label5 = QtWidgets.QLabel("持续时间")

        mainlayout = QtWidgets.QHBoxLayout()
        if cmd == "起飞" or cmd == "降落":
            mainlayout.addWidget(label1)
        else:
            mainlayout.addWidget(label1, 1)
            mainlayout.addStretch(1)
            mainlayout.addWidget(label4, 3)
            mainlayout.addWidget(label2, 1)
            mainlayout.addStretch(1)
            mainlayout.addWidget(label5, 2)
            mainlayout.addWidget(label3, 1)
        mainlayout.setMargin(2)
        self.setLayout(mainlayout)


class TaskWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon(Res.mainWindowIcon))
        self.setWindowTitle("任务")
        self.setFixedWidth(640)
        self.setFixedHeight(360)

        self.eventWindow = EventWindow()
        self.index = -1

        taskname = QtWidgets.QLineEdit()
        layout1 = QtWidgets.QHBoxLayout()
        layout1.addWidget(QtWidgets.QLabel("任务名"))
        layout1.addWidget(taskname)
        self.taskname = taskname

        start_time = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime().addSecs(600))
        start_time.setCalendarPopup(True)
        loop_mode = QtWidgets.QComboBox()
        loop_mode.addItems(['单次', '每天', '固定时间'])
        fixed_time = QtWidgets.QLineEdit("0")
        fixed_time.setEnabled(False)
        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(QtWidgets.QLabel("启动时间"))
        layout2.addWidget(start_time)
        layout2.addWidget(QtWidgets.QLabel("循环"))
        layout2.addWidget(loop_mode)
        layout2.addWidget(QtWidgets.QLabel("间隔(min)"))
        layout2.addWidget(fixed_time)
        loop_mode.currentTextChanged.connect(self.loop_mode_changed)
        self.start_time = start_time
        self.loop_mode = loop_mode
        self.fixed_time = fixed_time

        add = QtWidgets.QPushButton("添加")
        edit = QtWidgets.QPushButton("修改")
        delete = QtWidgets.QPushButton("删除")
        ok = QtWidgets.QPushButton("确定")
        add.clicked.connect(self.add_slot)
        edit.clicked.connect(self.edit_slot)
        delete.clicked.connect(self.delete_slot)
        ok.clicked.connect(self.ok_slot)

        layout3 = QtWidgets.QVBoxLayout()
        layout3.addWidget(add)
        layout3.addWidget(edit)
        layout3.addWidget(delete)
        layout3.addStretch()
        layout3.addWidget(ok)

        events = QtWidgets.QListWidget()
        layout4 = QtWidgets.QHBoxLayout()
        layout4.addWidget(events)
        layout4.addLayout(layout3)
        self.events = events

        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.addLayout(layout1)
        mainlayout.addLayout(layout2)
        mainlayout.addLayout(layout4)
        self.setLayout(mainlayout)

    def update(self):
        self.events.clear()
        for e in Res.events:
            item = QtWidgets.QListWidgetItem()
            item_widget = ListItem(e['cmd'], e['value'], e['time'])
            self.events.addItem(item)
            self.events.setItemWidget(item, item_widget)
        self.events.setCurrentRow(self.events.count() - 1)

    @QtCore.Slot()
    def add_slot(self):
        if self.events.currentRow() != self.events.count() - 1:
            self.eventWindow.index = self.events.currentRow()
        if self.eventWindow.exec_() == 1:
            self.update()

    @QtCore.Slot()
    def edit_slot(self):
        if self.events.currentRow() != -1:
            self.eventWindow.edit()

    @QtCore.Slot()
    def delete_slot(self):
        del (Res.events[self.events.currentRow()])
        self.update()

    @QtCore.Slot(str)
    def loop_mode_changed(self, text):
        if text == "固定时间":
            self.fixed_time.setEnabled(True)
        else:
            self.fixed_time.setEnabled(False)

    def edit(self, data):
        super(TaskWindow, self).exec_()

    def ok_slot(self):
        data = {'task_name': self.taskname.text(),
                'start_time': self.start_time.dateTime().toString('yyyy-MM-dd hh:mm:ss'),
                'loop_mode': self.loop_mode.currentText(), 'fixed_time': self.fixed_time.text(),
                'data': Res.events.copy()}
        if self.index == -1:
            Res.tasks.append(data)
        else:
            Res.tasks.insert(self.index + 1, data)
        self.index = -1
        Res.events.clear()
        self.accept()

    def clear(self):
        self.taskname.setText("")
        Res.events.clear()
        self.update()
