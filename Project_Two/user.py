from threading import Thread, Timer
from PySide2 import QtCore
from queue import Queue
import json

from res import Res


class User(QtCore.QObject):
    def __init__(self, tcpClient, address):
        super(User, self).__init__()
        self._tcpSocket = tcpClient
        self.address = address
        self._isRun = False
        self._tcpReceiveThread = Thread(target=self._tcp_receive)
        self._receive_manageThread = Thread(target=self._receive_manage)
        self.receive_queue = Queue()
        self.task_timer = Timer(0.5, self.timer_callback)
        self.tasks = []
        self.current_event = []
        self.timer_stop = False

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

    def _receive_manage(self):
        while True:
            receive = self.receive_queue.get()
            data = json.loads(receive)
            if data['cmd'] == "upload":
                # print(data)
                for d in data['tasks']:
                    events = Queue()
                    time = QtCore.QDateTime.fromString(d['start_time'], "yyyy-MM-dd hh:mm:ss")
                    for e in d['data']:
                        cmd = [e['cmd'], e['value'], e['time']]
                        queue = [time, cmd]
                        events.put(queue)
                        time = time.addSecs(int(e['time']))
                    self.tasks.append(events)
                self.task_timer = Timer(0.5, self.timer_callback)
                self.task_timer.start()

    def timer_callback(self):
        self.task_timer = Timer(0.5, self.timer_callback)
        if not self.tasks or self.timer_stop:
            return
        if (not self.current_event) and self.tasks[0].empty():
            del (self.tasks[0])
            return
        if not self.current_event:
            self.current_event = self.tasks[0].get()
        now = QtCore.QDateTime.currentDateTime()
        secs = now.secsTo(self.current_event[0])
        print(secs)
        if secs < 0:
            del (self.tasks[0])
            self.current_event = []
        elif secs == 0:
            if Res.devices:
                Res.devices[-1][0].tcp_send(self.current_event[1])
                self.current_event = []
            else:
                print("设备未连接")
                return
        self.task_timer.start()
