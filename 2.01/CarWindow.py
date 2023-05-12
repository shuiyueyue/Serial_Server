import sys
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


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Car_windows.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ports = {
            'car_1': {'port': 'com2', 'serial': None, 'receiver': None},
            'car_2': {'port': 'com4', 'serial': None, 'receiver': None},
            'car_3': {'port': 'com6', 'serial': None, 'receiver': None},
            'car_4': {'port': 'com8', 'serial': None, 'receiver': None},
        }

        self.Up_Point = {
            'car_1': self.updata_point_1,
            'car_2': self.updata_point_2,
            'car_3': self.updata_point_3,
            'car_4': self.updata_point_4
        }





        self.ui.Com_Open_Car_1.clicked.connect(lambda: self.open_serial('car_1'))
        self.ui.Com_Close_Car_1.clicked.connect(lambda: self.close_serial('car_1'))

        self.ui.Com_Open_Car_2.clicked.connect(lambda: self.open_serial('car_2'))
        self.ui.Com_Close_Car_2.clicked.connect(lambda: self.close_serial('car_2'))

        self.ui.Com_Open_Car_3.clicked.connect(lambda: self.open_serial('car_3'))
        self.ui.Com_Close_Car_3.clicked.connect(lambda: self.close_serial('car_3'))

        self.ui.Com_Open_Car_4.clicked.connect(lambda: self.open_serial('car_4'))
        self.ui.Com_Close_Car_4.clicked.connect(lambda: self.close_serial('car_4'))

        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.Rec)

        self.ui.Status_Send_1.clicked.connect(lambda: self.T_Status_1('car_1'))
        self.ui.Status_Send_2.clicked.connect(lambda: self.T_Status_2('car_2'))
        self.ui.Status_Send_3.clicked.connect(lambda: self.T_Status_3('car_3'))
        self.ui.Status_Send_4.clicked.connect(lambda: self.T_Status_4('car_4'))

        self.ui.Pic_Send_1.clicked.connect(lambda: self.T_Pic_1('car_1'))
        self.ui.Pic_Send_2.clicked.connect(lambda: self.T_Pic_2('car_2'))
        self.ui.Pic_Send_3.clicked.connect(lambda: self.T_Pic_3('car_3'))
        self.ui.Pic_Send_4.clicked.connect(lambda: self.T_Pic_4('car_4'))



    def open_serial(self, port):
        if self.ports[port]['serial'] is not None:
            return
        self.ports[port]['serial'] = Serial(self.ports[port]['port'], 115200, timeout=0.1)

    def close_serial(self, port):
        if self.ports[port]['serial'] is None:
            return
        self.ports[port]['serial'].close()
        self.ports[port]['serial'] = None

    def updata_point_1(self,point):
        if point['car_direction'] == 1:
            self.ui.Car_Dir_1.setText('前进')
        elif point['car_direction'] == 2:
            self.ui.Car_Dir_1.setText('后退')
        elif point['car_direction'] == 3:
            self.ui.Car_Dir_1.setText('左转')
        elif point['car_direction'] == 4:
            self.ui.Car_Dir_1.setText('右转')
        elif point['car_direction'] == 5:
            self.ui.Car_Dir_1.setText('停止')

        if point['car_auto'] == 1:
            self.ui.Car_Mod_1.setText('自动')
        elif point['car_auto'] == 2:
            self.ui.Car_Mod_1.setText('手动')

    def updata_point_2(self,point):
        if point['car_direction'] == 1:
            self.ui.Car_Dir_2.setText('前进')
        elif point['car_direction'] == 2:
            self.ui.Car_Dir_2.setText('后退')
        elif point['car_direction'] == 3:
            self.ui.Car_Dir_2.setText('左转')
        elif point['car_direction'] == 4:
            self.ui.Car_Dir_2.setText('右转')
        elif point['car_direction'] == 5:
            self.ui.Car_Dir_2.setText('停止')

        if point['car_auto'] == 1:
            self.ui.Car_Mod_2.setText('自动')
        elif point['car_auto'] == 2:
            self.ui.Car_Mod_2.setText('手动')

    def updata_point_3(self,point):
        if point['car_direction'] == 1:
            self.ui.Car_Dir_3.setText('前进')
        elif point['car_direction'] == 2:
            self.ui.Car_Dir_3.setText('后退')
        elif point['car_direction'] == 3:
            self.ui.Car_Dir_3.setText('左转')
        elif point['car_direction'] == 4:
            self.ui.Car_Dir_3.setText('右转')
        elif point['car_direction'] == 5:
            self.ui.Car_Dir_3.setText('停止')

        if point['car_auto'] == 1:
            self.ui.Car_Mod_3.setText('自动')
        elif point['car_auto'] == 2:
            self.ui.Car_Mod_3.setText('手动')

    def updata_point_4(self,point):
        if point['car_direction'] == 1:
            self.ui.Car_Dir_4.setText('前进')
        elif point['car_direction'] == 2:
            self.ui.Car_Dir_4.setText('后退')
        elif point['car_direction'] == 3:
            self.ui.Car_Dir_4.setText('左转')
        elif point['car_direction'] == 4:
            self.ui.Car_Dir_4.setText('右转')
        elif point['car_direction'] == 5:
            self.ui.Car_Dir_4.setText('停止')

        if point['car_auto'] == 1:
            self.ui.Car_Mod_4.setText('自动')
        elif point['car_auto'] == 2:
            self.ui.Car_Mod_4.setText('手动')

    def T_Status_1(self,port):
        #port = 'car_1'
        if self.ports[port]['serial'] is not None:
            id = 1

            x = float(self.ui.Car_X_1.text())
            y = float(self.ui.Car_Y_1.text())
            z = float(self.ui.Car_Z_1.text())
            spe = float(self.ui.Car_V_1.text())
            sta = int(self.ui.Car_S_1.text())
            print(id,x,y,z,spe,sta)

            sender = info_Sender(self.ports[port]['serial'])
            #sender.send_info(3, 2.6, 3.9, 4.8, 87, 0)
            sender.send_info(id,x,y,z,spe,sta)

    def T_Status_2(self,port):
        if self.ports[port]['serial'] is not None:
            id = 2
            x = float(self.ui.Car_X_2.text())
            y = float(self.ui.Car_Y_2.text())
            z = float(self.ui.Car_Z_2.text())
            spe = float(self.ui.Car_V_2.text())
            sta = int(self.ui.Car_S_2.text())
            print(id,x,y,z,spe,sta)
            sender = info_Sender(self.ports[port]['serial'])
            sender.send_info(id,x,y,z,spe,sta)

    def T_Status_3(self,port):
        if self.ports[port]['serial'] is not None:
            id = 3
            x = float(self.ui.Car_X_3.text())
            y = float(self.ui.Car_Y_3.text())
            z = float(self.ui.Car_Z_3.text())
            spe = float(self.ui.Car_V_3.text())
            sta = int(self.ui.Car_S_3.text())
            print(id,x,y,z,spe,sta)
            sender = info_Sender(self.ports[port]['serial'])
            sender.send_info(id,x,y,z,spe,sta)

    def T_Status_4(self,port):
        if self.ports[port]['serial'] is not None:
            id = 4
            x = float(self.ui.Car_X_4.text())
            y = float(self.ui.Car_Y_4.text())
            z = float(self.ui.Car_Z_4.text())
            spe = float(self.ui.Car_V_4.text())
            sta = int(self.ui.Car_S_4.text())
            print(id,x,y,z,spe,sta)
            sender = info_Sender(self.ports[port]['serial'])
            sender.send_info(id,x,y,z,spe,sta)

    def T_Pic_1(self,port):
        if self.ports[port]['serial'] is not None:
            print('tab1')
            sender = SerialSender(self.ports[port]['serial'])
            print('tab2')
            img = self.ui.Pic_Sel_1.currentText()
            print(img)
            sender.send_image(img)

    def T_Pic_2(self,port):
        if self.ports[port]['serial'] is not None:
            print('tab1')
            sender = SerialSender(self.ports[port]['serial'])
            print('tab2')
            img = self.ui.Pic_Sel_2.currentText()
            print(img)
            sender.send_image(img)

    def T_Pic_3(self,port):
        if self.ports[port]['serial'] is not None:
            print('tab1')
            sender = SerialSender(self.ports[port]['serial'])
            print('tab2')
            img = self.ui.Pic_Sel_3.currentText()
            print(img)
            sender.send_image(img)

    def T_Pic_4(self,port):
        if self.ports[port]['serial'] is not None:
            print('tab1')
            sender = SerialSender(self.ports[port]['serial'])
            print('tab2')
            img = self.ui.Pic_Sel_4.currentText()
            print(img)
            sender.send_image(img)

    def Rec(self):
        for port in self.ports:
            if self.ports[port]['serial'] is not None:


                if port == 'car_1':
                    self.ui.Com_Close_Car_1.setStyleSheet("background-color: none")
                    self.ui.Com_Open_Car_1.setStyleSheet("background-color: green")
                elif port == 'car_2':
                    self.ui.Com_Close_Car_2.setStyleSheet("background-color: none")
                    self.ui.Com_Open_Car_2.setStyleSheet("background-color: green")
                elif port == 'car_3':
                    self.ui.Com_Close_Car_3.setStyleSheet("background-color: none")
                    self.ui.Com_Open_Car_3.setStyleSheet("background-color: green")
                elif port == 'car_4':
                    self.ui.Com_Close_Car_4.setStyleSheet("background-color: none")
                    self.ui.Com_Open_Car_4.setStyleSheet("background-color: green")


                picname = port + '.jpg'
                #print(picname)

                receiver = R_CP_PIC(self.ports[port]['serial'], picname)
                self.ports[port]['receiver'] = receiver.receive()
                #print('receiver:')
                #print(self.ports[port]['receiver'].data)

                if self.ports[port]['receiver'] is not None:



                    if self.ports[port]['receiver'].message_type == 1:
                        #print('test')
                        point = pickle.loads(self.ports[port]['receiver'].data[0])

                        self.Up_Point[port](point)

                    elif self.ports[port]['receiver'].message_type == 2:
                        #print('test')
                        print(picname)
                        self.Up_Pic[port](picname)

                    elif self.ports[port]['receiver'].message_type == 3:
                        # 反序列化数据
                        car_info = pickle.loads(self.ports[port]['receiver'].data[0])
                        self.Up_Info[port](car_info)
                        print(type(car_info['car_speed']))
            else:
                if port == 'car_1':
                    self.ui.Com_Open_Car_1.setStyleSheet("background-color: none")
                    self.ui.Com_Close_Car_1.setStyleSheet("background-color: red")
                elif port == 'car_2':
                    self.ui.Com_Open_Car_2.setStyleSheet("background-color: none")
                    self.ui.Com_Close_Car_2.setStyleSheet("background-color: red")
                elif port == 'car_3':
                    self.ui.Com_Open_Car_3.setStyleSheet("background-color: none")
                    self.ui.Com_Close_Car_3.setStyleSheet("background-color: red")
                elif port == 'car_4':
                    self.ui.Com_Open_Car_4.setStyleSheet("background-color: none")
                    self.ui.Com_Close_Car_4.setStyleSheet("background-color: red")








if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
