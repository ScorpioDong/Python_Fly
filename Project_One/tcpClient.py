from socket import *
from res import Res
from threading import Thread
import json


class TcpClient(object):
    def __init__(self):
        self._tcpReceiveThread = Thread(target=self._tcp_receive)
        self._tcpSocket = socket(AF_INET, SOCK_STREAM)
        self._isRun = False

    def tcp_connect(self):
        self._isRun = True
        try:
            self._tcpSocket = socket(AF_INET, SOCK_STREAM)
            self._tcpSocket.connect(Res.tcpServerAddress)
        except ConnectionRefusedError:
            return False
        self._tcpReceiveThread = Thread(target=self._tcp_receive)
        self._tcpReceiveThread.start()
        return True

    def tcp_close(self):
        self._isRun = False
        self._tcpSocket.close()
        self._tcpReceiveThread.join()

    def tcp_send_bytes(self, data):
        self._tcpSocket.send(data)

    def tcp_send_string(self, string):
        data = bytearray(string.encode('utf-8'))
        self._tcpSocket.send(data)

    def _tcp_receive(self):
        while self._isRun:
            try:
                data = self._tcpSocket.recv(1024)
                if data:
                    print(data)
            except ConnectionAbortedError as e:
                print(e)
                self._isRun = False
            except ConnectionResetError as e:
                print(e)
                self._isRun = False


tcpClient = TcpClient()
