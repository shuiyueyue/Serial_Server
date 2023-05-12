import copy
import sys
import time

import numpy as np
from PyQt5.QtGui import QPixmap, QImage,QIcon
from PyQt5.QtCore import QFile, QTextStream, QDir, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication,QToolTip,QTextEdit
from qtpy import QtCore

from UI import Ui_MainWindow
from PyQt5.QtGui import QPixmap, QImage,QIcon
from PyQt5.QtCore import QFile, QTextStream, Qt, QDir,QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication,QToolTip,QTextEdit,QFileDialog


import Central_Window
import serial
import serial.tools.list_ports
import a_star
import a_star1
import path_planning
import detect

from utils.general import (cv2)

class Target:
    def __init__(self, id, cls, x1, y1, x2, y2):
        self.id = id
        self.cls = cls
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Robot:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Obstacle:
    def __init__(self, id, cls, x1, y1, x2, y2):
        self.id = id
        self.cls = cls
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Path:
    def __init__(self, path_id, points):
        self.path_id = path_id  # 路径编号
        self.points = points  # 路径上的点列表


class UiRobot(QMainWindow):

    def __init__(self,parent = None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.label_width = 411
        self.label_height = 175
        self.filename = ""
        self.flag_refresh = 1
        self.flag_import = 0
        self.flag_recognize = 0
        self.flag_ToSituationMap = 0
        self.flag_PathPlanning = 0
        self.flag_begin = 0
        self.flg_ToSituation = 0
        self.flg_import = 0
        self.flg_PathPlanning = 0
        self.flg_recogenize = 0
        self.count = 0
        self.paths = []
        self.robots = []
        self.obstacles = []
        self.targets = []
        self.width = 0
        self.height = 0
        self.image = ''
        self.image_path = ''
        self.image_rec = ''
        self.pixmap = QPixmap()
        self.flg_begin = 0
        self.position_pre = {'car_1': [0, -1], 'car_2': [0, -1], 'car_3': [0, -1], 'car_4': [0, -1]}
        self.position = {'car_1': [0, 0], 'car_2': [0, 0], 'car_3': [0, 0], 'car_4': [0, 0]}
        robot0 = Robot(1, self.position_pre['car_1'][0], self.position['car_1'][1])
        robot1 = Robot(2, self.position['car_2'][0], self.position['car_2'][1])
        robot2 = Robot(3, self.position['car_3'][0], self.position['car_3'][1])
        robot3 = Robot(4, self.position['car_4'][0], self.position['car_4'][1])
        self.robots = [robot0, robot1, robot2, robot3]

        self.ui.btn_begin.setIcon(QIcon("begin.png"))
        self.ui.btn_begin.setToolTip('行进开始')
        self.ui.btn_import.setIcon(QIcon("import.jpg"))
        self.ui.btn_import.setToolTip('导入图片')
        self.ui.btn_refresh.setIcon(QIcon("refresh.jpg"))
        self.ui.btn_refresh.setToolTip('刷新机器人列表')
        self.ui.btn_recognize.setIcon(QIcon("recognize.jpg"))
        self.ui.btn_recognize.setToolTip('识别图片')
        self.ui.btn_PathPlanning.setIcon(QIcon("PathPlanning.jpg"))
        self.ui.btn_PathPlanning.setToolTip('路径规划')
        self.ui.btn_ToSituationMap.setIcon(QIcon("ToSituationMap.png"))
        self.ui.btn_ToSituationMap.setToolTip('转换态势图')


        #self.ui.btn_begin.clicked.connect(self.auto)
        self.ui.btn_refresh.pressed.connect(self.car_list)
        self.ui.RobotList.itemClicked.connect(self.on_item_clicked)


        self.current_window = None

        self.central_window1 = Central_Window.Central_Window()
        self.central_window1.income = 'car_1'
        self.central_window1.open_serial('car_1')
        self.central_window1.first_info()
        self.central_window1.main_window = self

        self.central_window2 = Central_Window.Central_Window()
        self.central_window2.income = 'car_2'
        self.central_window2.open_serial('car_2')
        self.central_window2.first_info()
        self.central_window2.main_window = self

        self.central_window3 = Central_Window.Central_Window()
        self.central_window3.income = 'car_3'
        self.central_window3.open_serial('car_3')
        self.central_window3.first_info()
        self.central_window3.main_window = self

        self.central_window4 = Central_Window.Central_Window()
        self.central_window4.income = 'car_4'
        self.central_window4.open_serial('car_4')
        self.central_window4.first_info()
        self.central_window4.main_window = self

    def resizeEvent(self, event):

        pixmap = self.ui.label.pixmap()
        if pixmap:
            self.ui.label.setPixmap(pixmap.scaled(self.ui.label.size(),Qt.KeepAspectRatio))
        pixmap2 = self.ui.label_2.pixmap()
        if pixmap2:
            self.ui.label_2.setPixmap(pixmap2.scaled(self.ui.label_2.size(), Qt.KeepAspectRatio))
        pixmap3 = self.ui.label_3.pixmap()
        if pixmap3:
            self.ui.label_3.setPixmap(pixmap3.scaled(self.ui.label_3.size(), Qt.KeepAspectRatio))
        pixmap4 = self.ui.label_4.pixmap()
        if pixmap4:
            self.ui.label_4.setPixmap(pixmap4.scaled(self.ui.label_4.size(), Qt.KeepAspectRatio))

        if self.flg_ToSituation == 1:
            self.on_btn_ToSituationMap_pressed()
        if self.flg_import == 1:
            pixmap_import = QPixmap(self.filename)
            self.ui.label.setPixmap(pixmap_import.scaled(self.ui.label.size(), Qt.KeepAspectRatio))
        if self.flg_recogenize == 1:
            pixmap_recognize = QPixmap(self.image_rec)
            self.ui.label_2.setPixmap(pixmap_recognize.scaled(self.ui.label_2.size(),Qt.KeepAspectRatio))
        if self.flg_PathPlanning ==1:
            self.on_btn_PathPlanning_pressed()
        #if self.flg_begin == 1:
            #path_planning.draw_car_circle(self.obstacles,self.targets,self.robots,self.width,self.height,self.ui.label_4)

    def on_btn_import_pressed(self):
        if self.flag_import == 0:
            self.ui.textEdit.append('请先连接到机器人')
        if self.flag_import == 1:
            curPath = QDir.currentPath()
            title = "选择图片"
            filt = "视频文件（*.jpg *.png *.xpm *.bmp）"
            self.filename, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)
            if self.filename == "":
                return
            else:
                pixmap = QPixmap(self.filename)
                self.ui.label.setPixmap(pixmap.scaled(self.ui.label.size(), Qt.KeepAspectRatio))
                self.flg_import = 1

            self.flag_recognize = 1

    def on_btn_recognize_pressed(self):
        if self.flag_recognize == 0:
            self.ui.textEdit.append('请先导入地图')
        if self.flag_recognize == 1:
            opt = detect.parse_opt('runs/train/exp/weights/best.pt',self.filename,'playground/playground_parameter.yaml')
            self.obstacles,self.targets,self.image,self.width,self.height = detect.main(opt)

            cv2.imwrite('img_rec.png',self.image)
            self.image_rec = 'img_rec.png'
            pixmap = QPixmap(self.image_rec)
            self.ui.label_2.setPixmap(pixmap.scaled(self.ui.label_2.size(),Qt.KeepAspectRatio))
            self.flg_recogenize = 1

            self.flag_ToSituationMap = 1



    def on_btn_ToSituationMap_pressed(self):
        if self.flag_ToSituationMap == 0:
            self.ui.textEdit.append('请先对导入的图片进行识别')
        if self.flag_ToSituationMap == 1:

            ob_ToS = copy.deepcopy(self.obstacles)
            tar_ToS = copy.deepcopy(self.targets)
            pixmap = path_planning.overall(ob_ToS,tar_ToS,self.width,self.height)

            self.ui.label_3.setPixmap(pixmap.scaled(self.ui.label_3.size(), Qt.KeepAspectRatio))
            self.flg_ToSituation = 1
            self.flg_PathPlanning = 0
            self.flag_PathPlanning = 1

    def on_btn_PathPlanning_pressed(self):
        self.flg_ToSituation = 0

        if self.flag_PathPlanning == 0:
            self.ui.textEdit.append('请先转换态势图')
        if self.flag_PathPlanning == 1:

            self.return_position()
            '''print(self.obstacles[0].id, self.obstacles[0].x1, self.obstacles[0].y1, self.obstacles[0].x2,
                  self.obstacles[1].y2, self.obstacles[1].id, self.obstacles[1].x1, self.obstacles[1].y1,
                  self.obstacles[2].x2, self.obstacles[2].y2, self.obstacles[2].id, self.obstacles[2].x1,
                  self.obstacles[3].y1, self.obstacles[3].x2, self.obstacles[3].y2, self.obstacles[3].id,
                  self.obstacles[4].x1, self.obstacles[4].y1, self.obstacles[4].x2, self.obstacles[4].y2,
                  self.obstacles[5].x1, self.obstacles[5].y1, self.obstacles[5].x2, self.obstacles[5].y2)'''
            ob_Pat = copy.deepcopy(self.obstacles)
            tar_Pat = copy.deepcopy(self.targets)
            self.paths,pixmap = path_planning.robot_less_equal_target(ob_Pat, tar_Pat, self.robots, self.width, self.height)
            self.ui.label_3.setPixmap(pixmap.scaled(self.ui.label_3.size(), Qt.KeepAspectRatio))
            # 打开文本文件
            #print(self.paths)
            filename = "paths.txt"
            with open(filename, "w") as file:
                # 遍历每个Path对象
                for path in self.paths:
                    # 写入路径编号
                    file.write(f"Path ID: {path.path_id}\n")

                    # 写入每个坐标点
                    for point in path.points:
                        file.write(f"Point: {point}\n")

                    # 写入路径结束标记
                    file.write("End of Path\n\n")
            with open(filename,"r")as file:
                content = file.read()
                self.ui.textEdit.setPlainText(content)
            self.flg_PathPlanning = 1
            self.flag_begin = 1
            #print(self.paths[0].points)
            np.save('car_1.npy', self.paths[0].points)
            print(type(self.paths[0].points))
            np.save('car_2.npy', self.paths[1].points)
            np.save('car_3.npy', self.paths[2].points)
            np.save('car_4.npy', self.paths[3].points)









    def open_new_window(self):
        self.central_window = Central_Window.Central_Window()
        self.central_window.show()


    def car_list(self):
        if self.count == 0:
            pixmap = QPixmap('background_label.png')
            self.ui.label.setPixmap(pixmap.scaled(self.ui.label.size(), Qt.KeepAspectRatio))
            pixmap2 = QPixmap('background_label.png')
            self.ui.label_2.setPixmap(pixmap2.scaled(self.ui.label_2.size(), Qt.KeepAspectRatio))
            pixmap3 = QPixmap('background_label.png')
            self.ui.label_3.setPixmap(pixmap3.scaled(self.ui.label_3.size(), Qt.KeepAspectRatio))
            pixmap4 = QPixmap('background_label.png')
            self.ui.label_4.setPixmap(pixmap4.scaled(self.ui.label_4.size(), Qt.KeepAspectRatio))
            self.count = 1

        self.ui.RobotList.clear()
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
                    #self.open_serial('car_1')
                    self.ui.RobotList.addItem('car_1')


                elif port.device == 'COM4':
                    #self.open_serial('car_2')
                    self.ui.RobotList.addItem('car_2')

                elif port.device == 'COM6':
                    #self.open_serial('car_3')
                    self.ui.RobotList.addItem('car_3')

                elif port.device == 'COM8':
                    #self.open_serial('car_4')
                    self.ui.RobotList.addItem('car_4')





        if self.ui.RobotList.count() == 0:
            self.ui.textEdit.append('机器人未连接，请再次刷新')
        else:
            self.ui.textEdit.append('机器人列表已刷新')
            self.flag_import = 1


    def on_item_clicked(self):
        # Get the text of the clicked item
        item = self.ui.RobotList.currentItem()
        '''

        self.central_window = Central_Window.Central_Window()
        self.central_window.income = item.text()
        self.central_window.open_serial(item.text())

        self.central_window.first_info()
        self.central_window.main_window = self
        '''
        if item.text() == 'car_1':
            self.central_window1.show()
            self.central_window1.first_info()
            self.current_window = self.central_window1
        elif item.text() == 'car_2':
            self.central_window2.show()
            self.central_window2.first_info()
            self.current_window = self.central_window2
        elif item.text() == 'car_3':
            self.central_window3.show()
            self.central_window3.first_info()
            self.current_window = self.central_window3
        elif item.text() == 'car_4':
            self.central_window4.show()
            self.central_window4.first_info()
            self.current_window = self.central_window4




    def return_position(self):




        self.position['car_1'] = self.central_window1.returnposition()
        self.position['car_2'] = self.central_window2.returnposition()
        self.position['car_3'] = self.central_window3.returnposition()
        self.position['car_4'] = self.central_window4.returnposition()

        robot0 = Robot(1, self.position['car_1'][0], self.position['car_1'][1])
        robot1 = Robot(2, self.position['car_2'][0], self.position['car_2'][1])
        robot2 = Robot(3, self.position['car_3'][0], self.position['car_3'][1])
        robot3 = Robot(4, self.position['car_4'][0], self.position['car_4'][1])
        self.robots = [robot0,robot1,robot2,robot3]

        print(self.position)




    def auto(self):
        self.current_window = self.central_window1
        self.central_window1.T_auto()

        self.current_window = self.central_window2
        self.central_window2.T_auto()

        self.current_window = self.central_window3
        self.central_window3.T_auto()

        self.current_window = self.central_window4
        self.central_window4.T_auto()


        #self.central_window2.T_auto()
        #self.central_window3.T_auto()
        #self.central_window4.T_auto()
    def time_fun(self):
        self.return_position()
        ob_beg = copy.deepcopy(self.obstacles)
        tar_beg = copy.deepcopy(self.targets)
        path_planning.draw_car_circle(self.robots,self.width,self.height,self.ui.label_4,self.filename)

        if time.time() - self.time >10:
            self.timer.stop()
        #if self.position_pre != self.position:
        #self.if_equal()







    def on_btn_begin_pressed(self):#自动行进，使全体小车自动行进，没0.1秒返回一次位置


        self.time = time.time()
        if self.flag_begin == 0:
            self.ui.textEdit.append('请先进行路径规划')
        if self.flag_begin == 1:
            #self.flg_begin = 1
            print(self.flag_begin)
            self.auto()
            self.timer = QtCore.QTimer()
            self.timer.start(500)
            self.timer.timeout.connect(self.time_fun)


            #self.timer.timeout.connect(lambda :path_planning.draw_car_circle(self.obstacles,self.targets,self.robots,self.width,self.height,self.ui.label_4))
            #self.timer.timeout.connect(self.if_equal)
            '''self.timer.timeout.connect(path_planning.draw_car_circle(self.obstacles,self.targets,self.robots,self.width,self.height))
            self.pixmap = path_planning.draw_car_circle(self.obstacles,self.targets,self.robots,self.width,self.height)
            self.ui.label_4.setPixmap(self.pixmap.scaled(self.ui.label_4.size(),Qt.KeepAspectRatio))
            self.timer = QTimer()
            self.timer.timeout.connect(self.time_fun())
            self.timer.start(500)
            self.return_position()
            path_planning.draw_car_circle(self.obstacles, self.targets, self.robots, self.width, self.height,self.ui.label_4)'''














    def info_list(self):
        #print('info_list')
        mod = ''
        forward = ''
        info = self.current_window.main_List

        str =''
        if info[3] == 1:
            if info[1] == 1:
                mod = '自动模式'
            elif info[1] == 2:
                mod = '手动模式'

            if info[0] == 0:
                forward = '无方向指令'
            elif info[0] == 1:
                forward = '前进'
            elif info[0] == 2:
                forward = '后退'
            elif info[0] == 3:
                forward = '左转'
            elif info[0] == 4:
                forward = '右转'
            elif info[0] == 5:
                forward = '左上'
            elif info[0] == 6:
                forward = '右上'
            elif info[0] == 7:
                forward = '左下'
            elif info[0] == 8:
                forward = '右下'



            str = '[' + info[
                2] + '] :' + self.current_window.income + '接受指令：（ 模式： “' + mod + ' ” ， 方向：“ ' + forward + ' ” ）'

        elif info[3] == 0:
            str = '[' + info[2] + '] :' + self.current_window.income + '连接摄像头'
        elif info[3] == 2:
            str = '[' + info[2] + '] :' + self.current_window.income + '断开摄像头'

        self.ui.textEdit.append(str)
    def return_position_1(self,port,position):
        #print(position)

        self.position[port] = position



if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_file = QFile('style.qss')
    style_file.open(QFile.ReadOnly|QFile.Text)
    stream = QTextStream(style_file)
    stylesheet = stream.readAll()
    app.setStyleSheet(stylesheet)
    main_window = UiRobot()
    main_window.show()
    sys.exit(app.exec())