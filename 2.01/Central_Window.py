import math
import os
import pickle
import sys
import time

import cv2 as cv
import numpy as np
import serial.tools.list_ports
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, \
    QPushButton, QGraphicsPixmapItem, QGraphicsScene, QLabel, QGraphicsView, QFrame
from PyQt5.QtCore import QDir, Qt, QSize, QUrl, QCoreApplication, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QBrush, QFont, QPen, QTransform
from Central import Ui_mainWindow
from T_Point import Point_Sender
from R_CP_PIC import R_CP_PIC
from PyQt5 import QtCore, QtGui, QtWidgets



class BatteryWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(600, 300)

    def paintEvent(self,e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        # 绘制电池外框
        battery_x = 100
        battery_y = 100
        battery_width = 250
        battery_height = 150
        painter.setBrush(QColor('#c4c4c4'))
        painter.drawRoundedRect(battery_x, battery_y, battery_width, battery_height, 4, 4)

        # 绘制电池内部填充
        battery_fill_x = battery_x + 2
        battery_fill_y = battery_y + 2
        battery_fill_width = (battery_width - 6) * self.battery_level / 100
        battery_fill_height = battery_height - 6
        painter.setBrush(QColor('green'))
        painter.drawRoundedRect(int(battery_fill_x), int(battery_fill_y), int(battery_fill_width), int(battery_fill_height), 2, 2)


    def setBatteryLevel(self, level):
        if level > 100:
            level = 100
        elif level < 0:
            level = 0
        self.battery_level = level
        self.update()




class Central_Window(QMainWindow):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.ports = {
            'car_1': {'port': 'com1', 'serial': None, 'receiver': None},
            'car_2': {'port': 'com3', 'serial': None, 'receiver': None},
            'car_3': {'port': 'com5', 'serial': None, 'receiver': None},
            'car_4': {'port': 'com7', 'serial': None, 'receiver': None},
        }

        self.cars = {  # direction: 0不改变状态，1前进，2后退，3左转，4右转，5左上，6右上，7左下，8右下
            # status: 0不改变状态，1自动，2手动
            'car_1': {'status': 0, 'speed': None, 'direction': None, 'angle': None, 'pos': None, 'path': None},
            'car_2': {'status': 0, 'speed': None, 'direction': None, 'angle': None, 'pos': None, 'path': None},
            'car_3': {'status': 0, 'speed': None, 'direction': None, 'angle': None, 'pos': None, 'path': None},
            'car_4': {'status': 0, 'speed': None, 'direction': None, 'angle': None, 'pos': None, 'path': None},
        }

        self.Video = {
            'car_1': cv.VideoCapture('images/car_1.mp4'),
            'car_2': cv.VideoCapture('images/car_2.mp4'),
            'car_3': cv.VideoCapture('images/car_3.mp4'),
            'car_4': cv.VideoCapture('images/car_4.mp4'),
            'car_5': cv.VideoCapture('images/car_5.mp4'),
            'car_6': cv.VideoCapture('images/car_6.mp4'),
        }


        self.LabelWidth = self.ui.videoplayer_1.width()
        self.LabelHeight = self.ui.videoplayer_1.height()
        self.LabelWidth2 = self.ui.battery.width()
        self.LabelHeight2 = self.ui.battery.height()
        self.battery = BatteryWidget()
        self.battery.setBatteryLevel(70)

        self.pixmap_battery = QPixmap(self.battery.size())
        self.battery.render(self.pixmap_battery)

        self.ui.battery.setPixmap(self.pixmap_battery)
        self.ui.battery.setScaledContents(True)



        #self.ui.car_list.clicked.connect(self.play)

        self.ui.Refresh.clicked.connect(self.picture)
        self.ui.up.clicked.connect(self.T_up)
        self.ui.down.clicked.connect(self.T_down)
        self.ui.left.clicked.connect(self.T_left)
        self.ui.right.clicked.connect(self.T_right)
        self.ui.up_left.clicked.connect(self.T_up_left)
        self.ui.up_right.clicked.connect(self.T_up_right)
        self.ui.down_left.clicked.connect(self.T_down_left)
        self.ui.down_right.clicked.connect(self.T_down_right)
        self.ui.pushButton_6.clicked.connect(self.T_auto)
        self.ui.Refresh_2.clicked.connect(self.clean)

        self.timer = QtCore.QTimer()
        self.timer.start(10)
        self.timer.timeout.connect(self.Rec)
        #self.timer.timeout.connect(self.updateAngle)

        self.income = ''
        self.main_List = []
        self.play_flag = False

        self.angle = 0

        # create a QGraphicsScene and set it to the QGraphicsView
        self.ui.arrow.scene = QGraphicsScene(self.ui.arrow)
        self.ui.arrow.setScene(self.ui.arrow.scene)
        self.ui.arrow.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.arrow.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.arrow.setFrameShape(QFrame.NoFrame)

        # create a QPixmap and a QGraphicsPixmapItem
        arrow_pixmap = QPixmap('images/arrow.png')
        self.arrow_item = QGraphicsPixmapItem(arrow_pixmap)

        # set the position and rotation of the arrow item
        self.arrow_item.setOffset(-arrow_pixmap.width()/2, -arrow_pixmap.height()/2)
        #self.arrow_item.setRotation(self.angle)  # set the rotation angle

        # add the arrow item to the scene
        self.ui.arrow.scene.addItem(self.arrow_item)

        self.main_window = None
        self.play = 0
        self.position_str = None

    def updateAngle(self,cor):
        # 每秒钟更新角度，并使用QTransform来旋转图形项
        self.angle = 360-math.degrees(cor)
        #self.angle = 360 - cor
        if self.angle >= 360:
            self.angle -= 360
        # create a QTransform and rotate the arrow item by the angle
        transform = QTransform().rotate(self.angle)
        self.arrow_item.setTransform(transform)




    '''
    '''
    def closeEvent(self, event):
        # 在这里添加您想要实现的中止程序的逻辑
        # 可以使用 event.ignore() 方法来阻止窗口关闭
        # 例如：self.stop_program()

        self.stop_program()

        event.accept()

    def stop_program(self):
        # 在这里添加中止程序的逻辑
        # 例如：self.timer.stop()
        port = self.income
        if self.ports[port]['serial'] is not None:
            sender = Point_Sender(self.ports[port]['serial'])


            sender.send_point(0, 2, 2)
        #self.close_serial('car_1')
        #self.close_serial('car_2')
        #self.close_serial('car_3')
        #self.close_serial('car_4')

        #self.timer.stop()

    def clean(self):
        self.ui.car_list.clear()

    def picture(self):
        if self.play == 2 or self.play == 0:
            self.play = 1
            self.main_list(0, 0, 0)
            self.main_window.info_list()
        else:
            self.play = 2
            self.main_list(0, 0, 2)
            self.main_window.info_list()
        port = self.income
        if self.ports[port]['serial'] is not None:
            sender = Point_Sender(self.ports[port]['serial'])
            sta = 2

            sender.send_point(0,0,self.play)






    def open_serial(self, port):
        if self.ports[port]['serial'] is not None:
            return
        self.ports[port]['serial'] = serial.Serial(self.ports[port]['port'], 115200, timeout=0.1)
        #print(self.income)

    def close_serial(self, port):
        if self.ports[port]['serial'] is not None:
            self.ports[port]['serial'].close()
            return

    def car_list(self):
        self.ui.car_list.clear()
        # 查找可用的串口
        available_ports = serial.tools.list_ports.comports()

        # 添加所有可用的串口到 QListWidget
        for port in available_ports:
            try:
                ser = serial.Serial(port.device)
                ser.close()
                #print(f"{port.device} is available")
            except serial.SerialException:
                #print(f"{port.device} is in use")
                if port.device == 'COM2':
                    self.open_serial('car_1')
                    self.ui.car_list.addItem('car_1')
                elif port.device == 'COM4':
                    self.open_serial('car_2')
                    self.ui.car_list.addItem('car_2')
                elif port.device == 'COM6':
                    self.open_serial('car_3')
                    self.ui.car_list.addItem('car_3')
                elif port.device == 'COM8':
                    self.open_serial('car_4')
                    self.ui.car_list.addItem('car_4')

    def car_list_out(self):

        # 查找可用的串口
        available_ports = serial.tools.list_ports.comports()

        # 添加所有可用的串口到 QListWidget
        car_list = [False,False,False,False]
        print('car_list_out')
        for port in available_ports:
            try:
                ser = serial.Serial(port.device)
                ser.close()
                #print(f"{port.device} is available")
            except serial.SerialException:
                #print(f"{port.device} is in use")
                if port.device == 'COM2':
                    car_list[0] = True
                elif port.device == 'COM4':
                    car_list[1] = True
                elif port.device == 'COM6':
                    car_list[2] = True
                elif port.device == 'COM8':
                    car_list[3] = True
        return car_list

    def stop(self):
        if self.cap_1 is not None:
            self.cap_1.release()
            self.ui.videoplayer_1.clear()

    def play(self):




        port = self.income
        #self.cap_1 = cv.VideoCapture('images/car_1.mp4')
        self.cap_1 = self.Video[port]
        fps = int(self.cap_1.get(cv.CAP_PROP_FPS))
        self.main_list(0,0,0)
        self.main_window.info_list()

        if not self.cap_1.isOpened():
            print("Cannot open camera")
        while True:
            ret,frame = self.cap_1.read()
            if not ret:
                self.cap_1.set(cv.CAP_PROP_POS_FRAMES, 0)  # 重新设置位置指针
                continue
            cv.waitKey(int(1000 / fps))

            img = QImage(frame.data, frame.shape[1], frame.shape[0], 3 * frame.shape[1], QImage.Format.Format_BGR888)
            pixmap = QPixmap.fromImage(img)
            pixmap0 = pixmap.scaled(self.LabelWidth, self.LabelHeight)
            self.ui.videoplayer_1.setPixmap(pixmap0)


    def T_up(self):
        port = self.income
        print(port)
        print('T_up')

        if self.ports[port]['serial'] is not None:
            sender = Point_Sender(self.ports[port]['serial'])
            sta = 2

            sender.send_point(1,sta,self.play)
            self.main_list(1,2,1)
            self.self_list()
            self.main_window.info_list()
    def T_down(self):
        port = self.income
        print(port)
        print('T_down')

        if self.ports[port]['serial'] is not None:
            sender = Point_Sender(self.ports[port]['serial'])
            sta = 2

            sender.send_point(2,sta,self.play)
            self.main_list(2, 2,1)
            self.self_list()
            self.main_window.info_list()
    def T_left(self):
        port = self.income
        print(port)
        print('T_left')

        if self.ports[port]['serial'] is not None:
            sender = Point_Sender(self.ports[port]['serial'])
            sta = 2

            sender.send_point(3,sta,self.play)
            self.main_list(3, 2,1)
            self.self_list()
            self.main_window.info_list()
    def T_right(self):
        port = self.income
        print(port)
        print('T_right')

        if self.ports[port]['serial'] is not None:
            sender = Point_Sender(self.ports[port]['serial'])
            sta = 2

            sender.send_point(4,sta,self.play)
            self.main_list(4, 2,1)
            self.self_list()
            self.main_window.info_list()
    def T_up_left(self):
        port = self.income
        print(port)
        print('T_up_left')

        if self.ports[port]['serial'] is not None:
            sender = Point_Sender(self.ports[port]['serial'])
            sta = 2

            sender.send_point(5,sta,self.play)
            self.main_list(5, 2,1)
            self.self_list()
            self.main_window.info_list()
    def T_up_right(self):
        port = self.income
        print(port)
        print('T_up_right')

        if self.ports[port]['serial'] is not None:
            sender = Point_Sender(self.ports[port]['serial'])
            sta = 2

            sender.send_point(6,sta,self.play)
            self.main_list(6, 2,1)
            self.self_list()
            self.main_window.info_list()
    def T_down_left(self):
        port = self.income
        print(port)
        print('T_down_left')

        if self.ports[port]['serial'] is not None:
            sender = Point_Sender(self.ports[port]['serial'])
            sta = 2

            sender.send_point(7,sta,self.play)
            self.main_list(7, 2,1)
            self.self_list()
            self.main_window.info_list()
    def T_down_right(self):
        port = self.income
        print(port)
        print('T_down_right')

        if self.ports[port]['serial'] is not None:
            sender = Point_Sender(self.ports[port]['serial'])
            sta = 2

            sender.send_point(8,sta,self.play)
            self.main_list(8, 2,1)
            self.self_list()
            self.main_window.info_list()

    def sent_path(self):
        port = self.income
        self.coords = np.load(f"{port}.npy")
        if self.ports[port]['serial'] is not None:
            sender = Point_Sender(self.ports[port]['serial'])
            sender.send_path(self.coords)


    def T_auto(self):
        port = self.income
        # print(port)
        #print('T_auto')
        #print(self.ports[port]['status'])
        self.coords = np.load(f"{port}.npy")
        #print(self.coords)

        if self.ports[port]['serial'] is not None:
            sender = Point_Sender(self.ports[port]['serial'])


            sta = 1

            if self.ports[port]['status'] == 1:
                print('to2')
                sender.send_point(0, 2,self.play)
                self.main_list(0, 2,1)
                self.self_list()
                self.main_window.info_list()
            elif self.ports[port]['status'] == 2:
                print('to1')
                sender.send_path(self.coords)
                sender.send_point(0, sta,self.play)
                self.main_list(0, 1,1)
                #print('test1')
                self.self_list()
                #print('test2')
                self.main_window.info_list()
                #print('test3')
            else:
                print('to1')
                sender.send_path(self.coords)
                sender.send_point(0, sta,self.play)
                self.main_list(0, 1,1)
                #print('test1')
                self.self_list()
                #print('test2')
                self.main_window.info_list()
                #print('test3')
        print(self.ports[port]['status'])


    def Rec(self):
        for port in self.ports:
            if self.ports[port]['serial'] is not None:





                picname = port + '.jpg'
                #print(picname)

                receiver = R_CP_PIC(self.ports[port]['serial'], picname)
                self.ports[port]['receiver'] = receiver.receive()
                #print('receiver:')
                #print(self.ports[port]['receiver'].data)

                if self.ports[port]['receiver'] is not None:


                    if self.ports[port]['receiver'].message_type == 3:
                        # 反序列化数据
                        car_info = pickle.loads(self.ports[port]['receiver'].data[0])
                        #if self.ui.car_list.currentItem() is not None:
                        if self.income == port:
                            #print(type(car_info['car_speed']))

                            self.position_str = [car_info['car_x'], car_info['car_y']]
                            self.main_window.return_position_1(port, self.position_str)
                            self.updata_info(car_info, port)
                            #print(self.position_str)
                    if self.ports[port]['receiver'].message_type == 2:
                        # 反序列化数据
                        #print('2')
                        #car_info = pickle.loads(self.ports[port]['receiver'].data[0])
                        #print(car_info)
                        #if self.ui.car_list.currentItem() is not None:

                        if self.income == port:
                            #print('3')
                            #print(type(car_info['car_speed']))
                            self.update_image(port)

    def returnposition(self):
        return self.position_str





    def updata_info(self,info,port):
        #print('updata_info')
        if port == self.income:

            position_str = " ({:.2f}, {:.2f})".format(info['car_x'], info['car_y'])
            self.ui.position.setText(position_str)
            self.ui.speed.setText(str(info['car_speed']))
            self.ui.cor.setText(str(info['car_cor']))

            self.updateAngle(info['car_cor'])

            if info['car_status'] == 1:
                status = '自动巡航'
                self.ports[port]['status'] = 1
                self.ui.model.setStyleSheet("color:green")
            elif info['car_status'] == 2:
                status = '手动模式'
                self.ports[port]['status'] = 2
                self.ui.model.setStyleSheet("color:blue")
            self.ui.model.setText(status)
            self.ui.car_info.setText(self.income + '状态信息')
            '''
            img = info['pic']
            print(type(img))
            
            pixmap = QPixmap.fromImage(img)
            pixmap0 = pixmap.scaled(self.LabelWidth, self.LabelHeight)
            self.ui.videoplayer_1.setPixmap(pixmap0)
            '''
    def update_image(self,port):
        if port == self.income:
            print('update_image')


            pixmap = QPixmap(f'{port}.jpg')
            pixmap0 = pixmap.scaled(self.LabelWidth, self.LabelHeight)
            self.ui.videoplayer_1.setPixmap(pixmap0)

    def main_list(self,forward,auto,info):
        ti = time.strftime("%Y-%m-%d %H:%M:%S")
        print(ti)
        self.main_List = [forward,auto,ti,info]
        return self.main_List

    def self_list(self):
        from builtins import str


        str = '[' + self.main_List[2] + ']' + ' :' + self.income + ' :{' + 'car_direction:' +str(self.main_List[0]) + ',' + 'car_auto:' + str(self.main_List[1]) + '}'
        self.ui.car_list.addItem(str)

    def first_info(self):
        port = self.income

        if self.ports[port]['serial'] is not None:
            sender = Point_Sender(self.ports[port]['serial'])

            sender.send_point(0, 2,self.play)












if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Central_Window()
    main_window.show()
    sys.exit(app.exec())




