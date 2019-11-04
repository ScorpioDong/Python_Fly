from socket import *
from device import Device
from res import Res
from user import User
from threading import Thread

tcpServer = socket(AF_INET, SOCK_STREAM)
tcpDevice = socket(AF_INET, SOCK_STREAM)


def client_listen():
    while True:
        tcpClient, address = tcpServer.accept()
        print("一个新的连接接入")
        user = User(tcpClient, address)
        user_thread = Thread(target=user)
        Res.users.append([user, user_thread])
        user_thread.start()


def device_listen():
    tcpClient, address = tcpDevice.accept()
    print("一个新的设备接入")
    device = Device(tcpClient, address)
    device_thread = Thread(target=device)
    Res.devices.append([device, device_thread])
    device_thread.start()


if __name__ == "__main__":
    tcpServer.bind(Res.tcpServerAddress)
    tcpDevice.bind(Res.tcpDeviceAddress)
    tcpServer.listen(10)
    tcpDevice.listen(10)
    thread_user = Thread(target=client_listen)
    thread_device = Thread(target=device_listen)
    print("开始监听")
    thread_device.start()
    thread_user.start()
    thread_device.join()
    thread_user.join()
