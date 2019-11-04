from PySide2 import QtWidgets, QtGui, QtCore
from tcpClient import tcpClient
from mapWindow import MapWindow
from res import Res
from taskWindow import TaskWindow
import json


class ListItem(QtWidgets.QFrame):
    def __init__(self, task_name, start_time):
        super(ListItem, self).__init__()

        label1 = QtWidgets.QLabel(task_name)
        label2 = QtWidgets.QLabel("启动时间")
        label3 = QtWidgets.QLabel(start_time)
        label3.setStyleSheet("color:gray")

        mainlayout = QtWidgets.QHBoxLayout()
        mainlayout.addWidget(label1, 1)
        mainlayout.addStretch(1)
        mainlayout.addWidget(label2, 1)
        mainlayout.addWidget(label3, 3)
        mainlayout.addStretch(1)
        mainlayout.setMargin(2)
        self.setLayout(mainlayout)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon(Res.mainWindowIcon))
        self.setWindowTitle("Demo")
        self.setFixedWidth(640)
        self.setFixedHeight(480)

        self.taskWindow = TaskWindow()
        self.mapWindow = MapWindow()

        username = QtWidgets.QLineEdit("admin")
        password = QtWidgets.QLineEdit("123123")
        link = QtWidgets.QPushButton("连接")
        layout1 = QtWidgets.QHBoxLayout()
        layout1.addWidget(QtWidgets.QLabel("用户名"))
        layout1.addWidget(username)
        layout1.addWidget(QtWidgets.QLabel("密码"))
        layout1.addWidget(password)
        layout1.addWidget(link)
        password.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        link.clicked.connect(self.link_slot)
        self.username = username
        self.password = password
        self.link = link

        device = QtWidgets.QComboBox()
        status = QtWidgets.QLabel("无设备")
        status.setStyleSheet("color:gray")
        power = QtWidgets.QLabel("无设备")
        power.setStyleSheet("color:gray")
        self.device = device
        self.status = status
        self.power = power

        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(QtWidgets.QLabel("设备"), 1)
        layout2.addWidget(device, 8)
        layout2.addWidget(QtWidgets.QLabel("状态"), 1)
        layout2.addWidget(status, 1)
        layout2.addWidget(QtWidgets.QLabel("电量"), 1)
        layout2.addWidget(power, 1)

        add = QtWidgets.QPushButton("添加")
        edit = QtWidgets.QPushButton("修改")
        delete = QtWidgets.QPushButton("删除")
        upload = QtWidgets.QPushButton("上传")
        mmap = QtWidgets.QPushButton("地图")
        add.clicked.connect(self.add_slot)
        edit.clicked.connect(self.edit_slot)
        delete.clicked.connect(self.delete_slot)
        mmap.clicked.connect(self.map_slot)
        upload.clicked.connect(self.upload_slot)
        # add.setEnabled(False)
        # edit.setEnabled(False)
        # delete.setEnabled(False)
        upload.setEnabled(False)
        mmap.setEnabled(False)
        self.add = add
        self.edit = edit
        self.delete = delete
        self.upload = upload
        self.mmap = mmap

        layout3 = QtWidgets.QVBoxLayout()
        layout3.addWidget(add)
        layout3.addWidget(edit)
        layout3.addWidget(delete)
        layout3.addStretch()
        layout3.addWidget(upload)
        layout3.addStretch()
        layout3.addWidget(mmap)

        tasks = QtWidgets.QListWidget()
        tasks.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        layout4 = QtWidgets.QHBoxLayout()
        layout4.addWidget(tasks)
        layout4.addLayout(layout3)
        self.tasks = tasks

        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.addLayout(layout1)
        mainlayout.addLayout(layout2)
        mainlayout.addLayout(layout4)
        self.setLayout(mainlayout)

    def update(self):
        self.tasks.clear()
        for e in Res.tasks:
            item = QtWidgets.QListWidgetItem()
            item_widget = ListItem(e['task_name'], e['start_time'])
            self.tasks.addItem(item)
            self.tasks.setItemWidget(item, item_widget)
        self.tasks.setCurrentRow(self.tasks.count() - 1)

    @QtCore.Slot()
    def add_slot(self):
        self.taskWindow.clear()
        if self.taskWindow.exec_() == 1:
            self.update()

    @QtCore.Slot()
    def edit_slot(self):
        if self.tasks.currentRow() != -1:
            self.taskWindow.edit()

    @QtCore.Slot()
    def map_slot(self):
        self.mapWindow.show()

    @QtCore.Slot()
    def upload_slot(self):
        data = {'cmd': "upload", 'tasks': Res.tasks}
        str = json.dumps(data, ensure_ascii=False)
        tcpClient.tcp_send_string(str)

    @QtCore.Slot()
    def delete_slot(self):
        del (Res.tasks[self.tasks.currentRow()])
        self.update()

    @QtCore.Slot()
    def link_slot(self):
        if self.username.text() == "admin" and self.password.text() == "123123":
            if self.link.text() == "连接":
                if tcpClient.tcp_connect():
                    self.link.setText("断开")
                    self.username.setEnabled(False)
                    self.password.setEnabled(False)
                    self.upload.setEnabled(True)
                    self.mmap.setEnabled(True)
                else:
                    QtWidgets.QMessageBox.information(self, "失败", "连接失败，请检查网络状况！", QtWidgets.QMessageBox.Ok,
                                                      QtWidgets.QMessageBox.Ok)

            else:
                self.link.setText("连接")
                self.username.setEnabled(True)
                self.password.setEnabled(True)
                tcpClient.tcp_close()
        else:
            QtWidgets.QMessageBox.information(self, "失败", "用户名或密码错误！", QtWidgets.QMessageBox.Ok,
                                              QtWidgets.QMessageBox.Ok)
