from threading import Thread, Timer
from PySide2 import QtCore
from queue import Queue
import json

cmd = [
    bytearray([0xAA, 0xAF, 0x05, 0xE0, 0x0B, 0x10, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5A]),
    bytearray([0xAA, 0xAF, 0x05, 0xE0, 0x0B, 0x10, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5B]),
    bytearray([0xAA, 0xAF, 0x05, 0xE0, 0x0B, 0x10, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5B]),
    bytearray([0xAA, 0xAF, 0x05, 0xE0, 0x0B, 0x10, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5B]),
    bytearray([0xAA, 0xAF, 0x05, 0xE0, 0x0B, 0x10, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5B]),
    bytearray([0xAA, 0xAF, 0x05, 0xE0, 0x0B, 0x10, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5B]),
    bytearray([0xAA, 0xAF, 0x05, 0xE0, 0x0B, 0x10, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5B]),
    bytearray([0xAA, 0xAF, 0x05, 0xE0, 0x0B, 0x10, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5B]),
    bytearray([0xAA, 0xAF, 0x05, 0xE0, 0x0B, 0x10, 0x00, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5B]),
    bytearray([0xAA, 0xAF, 0x05, 0xE0, 0x0B, 0x10, 0x00, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5B])]


class Device(QtCore.QObject):
    def __init__(self, tcpClient, address):
        super(Device, self).__init__()
        self._tcpSocket = tcpClient
        self.address = address
        self._isRun = False
        self._tcpReceiveThread = Thread(target=self._tcp_receive)
        self._receive_manageThread = Thread(target=self._receive_manage)
        self.receive_queue = Queue()

    def __call__(self, *args, **kwargs):
        self._isRun = True
        self._tcpReceiveThread.start()
        self._receive_manageThread.start()

    def _tcp_close(self):
        self._isRun = False

    def _tcp_receive(self):
        while self._isRun:
            try:
                receive = self._tcpSocket.recv(1024)
                if receive:
                    self.receive_queue.put(receive)
            except ConnectionResetError as e:
                print(e)
                self._isRun = False

    def tcp_send(self, data):
        send_data = bytearray()
        v = int(data[1])
        t = int(data[2])
        s = v * t
        s_h = s >> 8
        s_l = s & 0x00FF
        v_h = v >> 8
        v_l = v & 0x00FF
        if data[0] == "起飞":
            send_data = cmd[0]
        elif data[0] == "降落":
            send_data = cmd[1]
        elif data[0] == "上升":
            send_data = cmd[2]
            send_data[8] = s_h
            send_data[9] = s_l
            send_data[10] = v_h
            send_data[11] = v_l
        elif data[0] == "下降":
            send_data = cmd[3]
            send_data[8] = s_h
            send_data[9] = s_l
            send_data[10] = v_h
            send_data[11] = v_l
        elif data[0] == "前进":
            send_data = cmd[4]
            send_data[8] = s_h
            send_data[9] = s_l
            send_data[10] = v_h
            send_data[11] = v_l
        elif data[0] == "后退":
            send_data = cmd[5]
            send_data[8] = s_h
            send_data[9] = s_l
            send_data[10] = v_h
            send_data[11] = v_l
        elif data[0] == "向左":
            send_data = cmd[6]
            send_data[8] = s_h
            send_data[9] = s_l
            send_data[10] = v_h
            send_data[11] = v_l
        elif data[0] == "向右":
            send_data = cmd[7]
            send_data[8] = s_h
            send_data[9] = s_l
            send_data[10] = v_h
            send_data[11] = v_l
        elif data[0] == "左旋":
            send_data = cmd[8]
            send_data[8] = s_h
            send_data[9] = s_l
            send_data[10] = v_h
            send_data[11] = v_l
        elif data[0] == "右旋":
            send_data = cmd[9]
            send_data[8] = s_h
            send_data[9] = s_l
            send_data[10] = v_h
            send_data[11] = v_l
        else:
            print("数据错误！")
            return
        check = 0
        for i in range(16):
            check += send_data[i]
        check = check & 0x00FF
        send_data[16] = check
        self._tcpSocket.send(send_data)

    def _receive_manage(self):
        while True:
            receive = self.receive_queue.get()
            print(receive)
