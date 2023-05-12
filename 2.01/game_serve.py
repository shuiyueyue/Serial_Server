
import time

from PyQt5 import QtCore, QtGui, QtWidgets

import pickle
from serial import Serial
from R_CP_PIC import R_CP_PIC



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


        self.cargame = None
        self.rec_flag = False
        self.current_point = None
        self.path ={'car_1':None,'car_2':None,'car_3':None,'car_4':None}




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
                    if self.ports[port]['receiver'].message_type == 4:
                        print('收到信息4')
                        path = pickle.loads(self.ports[port]['receiver'].data[0])
                        print(path)
                        self.cargame.path(port,path)

                    if self.ports[port]['receiver'].message_type == 1:
                        print('收到信息')
                        point = pickle.loads(self.ports[port]['receiver'].data[0])
                        print(point)
                        self.rec_flag = True
                        self.current_point = [point,port]




                        self.test(port,point)




    def current_rec(self):
        return self.current_point





    def close_serial(self, port):
        if self.ports[port]['serial'] is None:
            return
        self.ports[port]['serial'].close()
        self.ports[port]['serial'] = None
    def test(self, port, point):
        #print('test')
        cur = time.time()
        if point['car_auto'] == 2:

            # print('updata_point')
            if point['car_direction'] == 1:
                self.cargame.test_run(1,cur,port)
            elif point['car_direction'] == 2:
                self.cargame.test_run(2,cur,port)
            elif point['car_direction'] == 3:
                self.cargame.test_run(3,cur,port)
            elif point['car_direction'] == 4:
                self.cargame.test_run(4,cur,port)
            elif point['car_direction'] == 5:
                self.cargame.test_run(5,cur,port)
            elif point['car_direction'] == 6:
                self.cargame.test_run(6,cur,port)
            elif point['car_direction'] == 7:
                self.cargame.test_run(7,cur,port)
            elif point['car_direction'] == 8:
                self.cargame.test_run(8,cur,port)
            elif point['car_direction'] == 0:
                self.cargame.test_run(0,cur,port)
        elif point['car_auto'] == 1:
            self.cargame.test_auto(0,cur,port)
        ''''''
        if point['play'] != 0 or point['play'] != 3:
            self.cargame.test_play(point['play'],port)


    def show(self,port,x,y,auto,video):
        #print('auto2:  ' + str(auto))
        self.cargame.show(port,x,y,self.ports[port]['serial'],auto,video)

    def hide(self,port):
        self.cargame.hide(port)

















