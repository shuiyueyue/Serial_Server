import copy
import sys
import time

import serial
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QLabel

import Terminal

from serial import Serial

from game_serve import Ter_ser
from game_serve import SerialThread
from game import CarGame

import serial.tools.list_ports


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Terminal.Ui_mainWindow()
        self.ui.setupUi(self)

        self.ports = {
            'car_1': {'port': 'com2', 'serial': None, 'receiver': None},
            'car_2': {'port': 'com4', 'serial': None, 'receiver': None},
            'car_3': {'port': 'com6', 'serial': None, 'receiver': None},
            'car_4': {'port': 'com8', 'serial': None, 'receiver': None},
            #'car_5': {'port': 'com10', 'serial': None, 'receiver': None},

        }

        self.serve = Ter_ser()
        #self.serve.ports = copy.deepcopy(self.ports)
        # 创建线程
        thread = SerialThread()

        # 启动线程
        thread.start()

        #self.game = CarGame(640, 480)
        #self.game.run()
        self.car_point = {'car_direction': 0,  'car_auto': 0 , 'play': 0}


        self.serve.cargame = CarGame(640, 480,self.serve)


        self.ui.connnect.clicked.connect(self.open_serial)
        self.ui.disconnect.clicked.connect(self.close_serial)
        self.ui.claer.clicked.connect(self.clean)

        self.timer = QtCore.QTimer()
        self.timer.start(10)
        self.timer.timeout.connect(self.refresh)
        self.timer.timeout.connect(self.info)
        #self.timer.timeout.connect(self.car_list)

        self.ui.up_2.clicked.connect(self.T_up)
        self.ui.down_2.clicked.connect(self.T_down)
        self.ui.left_2.clicked.connect(self.T_left)
        self.ui.right_2.clicked.connect(self.T_right)
        self.ui.pushButton_7.clicked.connect(self.T_auto)
        self.ui.up_left_2.clicked.connect(self.T_up_left)
        self.ui.up_right_2.clicked.connect(self.T_up_right)
        self.ui.down_left_2.clicked.connect(self.T_down_left)
        self.ui.down_right_2.clicked.connect(self.T_down_right)

        self.ui.Refresh_4.clicked.connect(self.car_list)
        self.ui.Refresh_3.clicked.connect(self.clean_3)

        self.if_auto = 0




    def car_list(self):
        self.ui.car_list_3.clear()
        # 查找可用的串口
        available_ports = serial.tools.list_ports.comports()
        print(available_ports)


        # 添加所有可用的串口到 QListWidget
        for port in available_ports:
            try:
                ser = serial.Serial(port.device)
                ser.close()
                #print(f"{port.device} is available")
            except serial.SerialException:
                #print(f"{port.device} is in use")
                if port.device == 'COM2':
                    #self.open_serial('car_1')
                    self.ui.car_list_3.addItem('car_1')
                elif port.device == 'COM4':
                    #self.open_serial('car_2')
                    self.ui.car_list_3.addItem('car_2')
                elif port.device == 'COM6':
                    #self.open_serial('car_3')
                    self.ui.car_list_3.addItem('car_3')
                elif port.device == 'COM8':
                    #self.open_serial('car_4')
                    self.ui.car_list_3.addItem('car_4')

    def self_list(self):
        from builtins import str



        Str = '[' + time.strftime("%Y-%m-%d %H:%M:%S") + ']' + ' :' + self.ui.car_list_3.currentItem().text() \
              + ' :{' + 'car_direction:' +str(self.car_point['car_direction']) + ',' + 'car_auto:' + str(self.car_point['car_auto']) + '}'

        self.ui.car_list_2.addItem(Str)
    def clean_3(self):
        self.ui.car_list_2.clear()

    def open_serial(self):
        port = self.ui.port.currentText()
        x = float(self.ui.car_x.text())
        y = float(self.ui.car_y.text())
        auto = self.ui.model.currentText()

        if port in self.serve.ports:
            if self.serve.ports[port]['serial'] is not None:
                return
            self.serve.ports[port]['serial'] = Serial(self.ports[port]['port'], 115200, timeout=0.1)

            if auto == '手动模式':
                Auto = 2
            elif auto == '自动巡航':
                Auto = 1
            #print('auto1:  ' +str(Auto))
            video = self.ui.video.currentText()


            self.serve.show(port,x,y,Auto,video)
            self.car_list()
            #self.ui.car_list_3.addItem(port)

            if self.serve.ports[port]['serial'] is not None:
                print('已经连接')

    def close_serial(self):
        port = self.ui.port.currentText()
        if port in self.serve.ports:
            if self.serve.ports[port]['serial'] is None:
                return
            self.serve.hide(port)
            self.car_list()
            self.serve.ports[port]['serial'].close()

            self.serve.ports[port]['serial'] = None


    def refresh(self):
        if self.serve.rec_flag:

            self.ui.current_rec.addItem('[' + time.strftime("%Y-%m-%d %H:%M:%S")+']:'+self.serve.current_point[1]+':'+str(self.serve.current_point[0]))

            self.serve.rec_flag = False

    def info(self):
        port = None
        #print('info')

        if self.ui.car_list_3.currentItem() is None:
            #print('info2')
            return
        else:
            #print('info3')
            port = self.ui.car_list_3.currentItem().text()
            #print(port)
            #print(self.serve.cargame.Image[port]['auto'])
            info = self.serve.cargame.info(port)
            #print(info)

            position_str = " ({:.2f}, {:.2f})".format(info[1], info[2])
            self.ui.position_2.setText(position_str)
            self.ui.speed_2.setText(str(info[4]))
            self.ui.cor_2.setText(str(info[3]))

            if info[5] == 1:
                status = '自动巡航'
                self.ui.model_2.setStyleSheet("color:green")
                self.if_auto = 1
            elif info[5] == 2:
                status = '手动模式'
                self.ui.model_2.setStyleSheet("color:blue")
                self.if_auto = 2
            self.ui.model_2.setText(status)

    def clean(self):
        self.ui.current_rec.clear()

    def T_up(self):
        if self.ui.car_list_3.currentItem() is None:
            #print('info2')
            return
        else:
            #print('info3')
            port = self.ui.car_list_3.currentItem().text()
            #print(port)
            self.car_point['car_direction'] = 1
            self.car_point['car_auto'] = 2
            self.serve.test(port,self.car_point)
            self.self_list()
    def T_down(self):
        if self.ui.car_list_3.currentItem() is None:
            #print('info2')
            return
        else:
            #print('info3')
            port = self.ui.car_list_3.currentItem().text()
            #print(port)
            self.car_point['car_direction'] = 2
            self.car_point['car_auto'] = 2
            self.serve.test(port,self.car_point)
            self.self_list()
    def T_left(self):
        if self.ui.car_list_3.currentItem() is None:
            #print('info2')
            return
        else:
            #print('info3')
            port = self.ui.car_list_3.currentItem().text()
            #print(port)
            self.car_point['car_direction'] = 3
            self.car_point['car_auto'] = 2
            self.serve.test(port,self.car_point)
            self.self_list()
    def T_right(self):
        if self.ui.car_list_3.currentItem() is None:
            #print('info2')
            return
        else:
            #print('info3')
            port = self.ui.car_list_3.currentItem().text()
            #print(port)
            self.car_point['car_direction'] = 4
            self.car_point['car_auto'] = 2
            self.serve.test(port,self.car_point)
            self.self_list()

    def T_up_left(self):
        if self.ui.car_list_3.currentItem() is None:
            #print('info2')
            return
        else:
            #print('info3')
            port = self.ui.car_list_3.currentItem().text()
            #print(port)
            self.car_point['car_direction'] = 5
            self.car_point['car_auto'] = 2
            self.serve.test(port,self.car_point)
            self.self_list()
    def T_up_right(self):
        if self.ui.car_list_3.currentItem() is None:
            #print('info2')
            return
        else:
            #print('info3')
            port = self.ui.car_list_3.currentItem().text()
            #print(port)
            self.car_point['car_direction'] = 6
            self.car_point['car_auto'] = 2
            self.serve.test(port,self.car_point)
            self.self_list()
    def T_down_left(self):
        if self.ui.car_list_3.currentItem() is None:
            #print('info2')
            return
        else:
            #print('info3')
            port = self.ui.car_list_3.currentItem().text()
            #print(port)
            self.car_point['car_direction'] = 7
            self.car_point['car_auto'] = 2
            self.serve.test(port,self.car_point)
            self.self_list()
    def T_down_right(self):
        if self.ui.car_list_3.currentItem() is None:
            #print('info2')
            return
        else:
            #print('info3')
            port = self.ui.car_list_3.currentItem().text()
            #print(port)
            self.car_point['car_direction'] = 8
            self.car_point['car_auto'] = 2
            self.serve.test(port,self.car_point)
            self.self_list()
    def T_auto(self):
        if self.ui.car_list_3.currentItem() is None:
            #print('info2')
            return
        else:
            if self.if_auto == 2:
                # print('info3')
                port = self.ui.car_list_3.currentItem().text()
                # print(port)
                self.car_point['car_direction'] = 0
                self.car_point['car_auto'] = 1
                self.if_auto = 1
                self.serve.test(port, self.car_point)
                self.self_list()
            elif self.if_auto == 1:
                # print('info3')
                port = self.ui.car_list_3.currentItem().text()
                # print(port)
                self.car_point['car_direction'] = 0
                self.car_point['car_auto'] = 2
                self.if_auto = 2
                self.serve.test(port, self.car_point)
                self.self_list()









if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.show()
    MainWindow.serve.cargame.run()
    sys.exit(app.exec_())
