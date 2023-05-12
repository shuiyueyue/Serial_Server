import sys
import threading
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import Car_windows
import pickle
from serial import Serial
from R_CP_PIC import R_CP_PIC
from T_CP import info_Sender
from T_CP_PIC import SerialSender

from R_Point import Point_Receiver
from T_Point import Point_Sender
from CommunicationProtocol import CommunicationProtocol

from PyQt5.QtCore import QThread, pyqtSignal

class SerialThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ter_ser = Ter_ser()

    def run(self):
        while True:
            self.ter_ser.Rec()
            time.sleep(0.01)



class Ter_ser:
    def __init__(self):
        super().__init__()


        self.ports = {
            'car_1': {'port': 'com2', 'serial': None, 'receiver': None},
            'car_2': {'port': 'com4', 'serial': None, 'receiver': None},
            'car_3': {'port': 'com6', 'serial': None, 'receiver': None},
            'car_4': {'port': 'com8', 'serial': None, 'receiver': None},
        }

        self.ImageViewer = None





        self.timer = QtCore.QTimer()
        self.timer.start(10)
        self.timer.timeout.connect(self.Rec)
    '''
        self.serial_threads = {}  # 用于存储所有串口接收线程
        self.init_serial_threads()

    def init_serial_threads(self):
        for port in self.ports:
            self.serial_threads[port] = SerialThread(self.ports[port]['port'])
            self.serial_threads[port].received.connect(self.process_serial_data)  # 连接自定义信号和处理函数
            self.serial_threads[port].start()  # 启动线程

    def process_serial_data(self, data):
        # 在这里处理接收到的串口数据
        print(data)
    '''



    def open_serial(self, port):
        if self.ports[port]['serial'] is not None:
            return
        self.ports[port]['serial'] = Serial(self.ports[port]['port'], 115200, timeout=0.1)

    def move_thread_func(self,port, picname):
        receiver = R_CP_PIC(self.ports[port]['serial'], picname)
        self.ports[port]['receiver'] = receiver.receive()
    def Rec(self):
        for port in self.ports:
            if self.ports[port]['serial'] is not None:





                picname = port + '.jpg'
                #print(picname)
                '''
                move_thread = threading.Thread(target=self.move_thread_func, args=(port, picname))
                move_thread.start()



                '''
                receiver = R_CP_PIC(self.ports[port]['serial'], picname)
                self.ports[port]['receiver'] = receiver.receive()

                #print('receiver:')
                #print(self.ports[port]['receiver'].data)

                if self.ports[port]['receiver'] is not None:
                    '''
                    print(self.ports[port]['receiver'].message_type)
                    from datetime import datetime

                    now = datetime.now()
                    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    print("Current Time =", current_time)
                    print(self.ports[port]['receiver'].message_type)
                    point = pickle.loads(self.ports[port]['receiver'].data[0])
                    print(point)

                    #self.updata_point(port, point)
                    '''

                    if self.ports[port]['receiver'].message_type == 1:
                        print('收到信息')
                        point = pickle.loads(self.ports[port]['receiver'].data[0])
                        print(point)


                        self.updata_point(port,point)




    def close_serial(self, port):
        if self.ports[port]['serial'] is None:
            return
        self.ports[port]['serial'].close()
        self.ports[port]['serial'] = None

    def updata_point(self,port,point):
        if point['car_auto'] != 1:
            #print('updata_point')
            if point['car_direction'] == 1:
                self.ImageViewer.Image[port]['direction'] = point['car_direction']
                self.ImageViewer.Image[port]['status'] = point['car_auto']
                self.ImageViewer.stop_flag = True

                self.ImageViewer.move_up(port,self.ports[port]['serial'])
            elif point['car_direction'] == 2:
                self.ImageViewer.Image[port]['direction'] = point['car_direction']
                self.ImageViewer.Image[port]['status'] = point['car_auto']
                self.ImageViewer.stop_flag = True
                self.ImageViewer.move_down(port,self.ports[port]['serial'])
            elif point['car_direction'] == 3:
                self.ImageViewer.Image[port]['direction'] = point['car_direction']
                self.ImageViewer.Image[port]['status'] = point['car_auto']
                self.ImageViewer.stop_flag = True
                self.ImageViewer.move_left(port,self.ports[port]['serial'])
            elif point['car_direction'] == 4:
                self.ImageViewer.Image[port]['direction'] = point['car_direction']
                self.ImageViewer.Image[port]['status'] = point['car_auto']
                self.ImageViewer.stop_flag = True
                self.ImageViewer.move_right(port,self.ports[port]['serial'])
            elif point['car_direction'] == 5:
                self.ImageViewer.Image[port]['direction'] = point['car_direction']
                self.ImageViewer.Image[port]['status'] = point['car_auto']
                self.ImageViewer.stop_flag = True
                self.ImageViewer.move_up_left(port,self.ports[port]['serial'])

            elif point['car_direction'] == 6:
                self.ImageViewer.Image[port]['direction'] = point['car_direction']
                self.ImageViewer.Image[port]['status'] = point['car_auto']
                self.ImageViewer.stop_flag = True
                self.ImageViewer.move_up_right(port,self.ports[port]['serial'])

            elif point['car_direction'] == 7:
                self.ImageViewer.Image[port]['direction'] = point['car_direction']
                self.ImageViewer.Image[port]['status'] = point['car_auto']
                self.ImageViewer.stop_flag = True
                self.ImageViewer.move_down_left(port,self.ports[port]['serial'])

            elif point['car_direction'] == 8:
                self.ImageViewer.Image[port]['direction'] = point['car_direction']
                self.ImageViewer.Image[port]['status'] = point['car_auto']
                self.ImageViewer.stop_flag = True
                self.ImageViewer.move_down_right(port,self.ports[port]['serial'])

        elif point['car_auto'] == 1:
            print('updata_point')
            self.ImageViewer.Image[port]['status'] = point['car_auto']
            self.ImageViewer.stop_flag = False
            self.ImageViewer.smooth_move(port,self.ports[port]['serial'])















