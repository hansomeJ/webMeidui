# coding=utf-8
from typing import Optional, Callable, Any, Iterable, Mapping

import serial
import threading
import time
from multiprocessing import Process, Queue
import queue


# print('开始！')


# print('创建数据实例')
# x.write([0X8A, 0X01, 0X17, 0X11, 0x11])
# print('发送数据')
# print(x.read(10))
def send(*kwargs):  # 发送函数
    x = kwargs[0]
    y = kwargs[1][0]
    t1 = time.time()
    t2 = time.time()
    while t2 - t1 <= 60:
        time.sleep(3)
        # myinput= bytes([0X8A,0X01,0X17,0X11])
        # 这是我要发送的命令，原本命令是：8a 01 17 11 11
        x.write(y)
        t2 = time.time()
        print('send')
        # x.write([0X8A, 0X02, 0X17, 0X11, 0x11])
    print('end send!')


def recv(*kwargs):  # 接收函数
    x = kwargs[0]
    t1 = time.time()
    t2 = time.time()
    while t2 - t1 <= 60:
        myout = x.read(10)  # 读取串口传过来的字节流，这里我根据文档只接收7个字节的数据
        t2 = time.time()
        print(myout, type(myout))
        if myout == "":
            return
    print('end receive!')


class Data():
    flag = 0

    def __init__(self, port, rate, deviceID) -> None:
        self.port = port
        self.rate = rate
        self.deviceID = deviceID
        self.serial = self.serial()
        # 发送线程
        self.sen = self.sen(send, 'sen', self.serial, (self.deviceID,))
        # 接收数据线程
        self.rec = self.rec(recv, 'rec', self.serial, )

    def serial(self):
        s = serial.Serial(self.port, self.rate)
        return s

    def start(self, ):
        self.sen.start()  # 开启线程1
        self.rec.start()  # 开启线程2
        # self.sen.join()
        # self.rec.join()

    def sen(self, func, name, arg1, arg2):
        function = threading.Thread(target=func, name=name, args=(arg1, arg2))
        return function

    def rec(self, func, name, arg1):
        function = threading.Thread(target=func, name=name, args=(arg1,))
        return function


# mydata = Data('COM4', 9600, [0X8A, 0X01, 0X17, 0X11])
# mydata.start()
# print('开始')


