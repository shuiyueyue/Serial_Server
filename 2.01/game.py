import argparse
import threading
import time

import pygame

from T_CP import info_Sender
import math

import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self, cap ,pic):
        super().__init__()
        self._run_flag = True
        self.cap = cap
        self.pic = pic

    def run(self):

        while self._run_flag:

            ret, frame = self.cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #print(type(rgb_image))

                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(convert_to_qt_format)

                # Save image to file
                pixmap.save('video.png')
                byte_array = QByteArray()
                buffer = QBuffer(byte_array)
                buffer.open(QIODevice.WriteOnly)
                convert_to_qt_format.save(buffer, "PNG")
                self.pic = byte_array.data()


                #print(type(self.pic))
                #print(rgb_image)



                QtCore.QThread.msleep(10) # 添加延迟
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def get_pic(self):
        return self.pic

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()




class CarGame:
    def __init__(self, screen_width, screen_height,gameserve):
        ''''''



        # 初始化 Pygame
        pygame.init()
        self.gameserve = gameserve
        self.angle = 0

        # 设置窗口尺寸
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 创建窗口
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        # 加载背景图片
        self.background_image = pygame.image.load("images/grass.jpg")
        self.background_width, self.background_height = self.background_image.get_size()

        # 加载图片
        self.car_image_1 = pygame.image.load("images/car_1.png")
        self.car_image_2 = pygame.image.load("images/car_2.png")
        self.car_image_3 = pygame.image.load("images/car_3.png")
        self.car_image_4 = pygame.image.load("images/car_4.png")
        #self.car_width, self.car_height = self.car_image.get_size()

        self.Image = {
            'car_1': {'image': self.car_image_1, 'direction': 0, 'status': None, 'position': [100,100],'last_position': [100,100],'path': None,
                      'cor': 0, 'auto': 0 , 'serial': None , 'last_time': 0 , 'site': False, 'ticks_start': None, 'play': 0 , 'flag': 0, 'video': None},
            'car_2': {'image': self.car_image_2, 'direction': 0, 'status': None, 'position': [100,100],'last_position': [100,100],'path': None,
                      'cor': 0, 'auto': 0 , 'serial': None , 'last_time': 0 , 'site': False, 'ticks_start': None, 'play': 0 , 'flag': 0, 'video': None},
            'car_3': {'image': self.car_image_3, 'direction': 0, 'status': None, 'position': [100,100],'last_position': [100,100],'path': None,
                      'cor': 0, 'auto': 0 , 'serial': None , 'last_time': 0 , 'site': False, 'ticks_start': None, 'play': 0 , 'flag': 0, 'video': None},
            'car_4': {'image': self.car_image_4, 'direction': 0, 'status': None, 'position': [100,100],'last_position': [100,100],'path': None,
                      'cor': 0, 'auto': 0 , 'serial': None , 'last_time': 0 , 'site': False, 'ticks_start': None, 'play': 0 , 'flag': 0, 'video': None},
        }


        # 设置移动速度
        self.speed = 5
        self.serial = None

        # 添加自动移动标志位和圆形轨迹的参数
        self.auto_move = True
        self.circle_center = (320, 240)
        self.circle_radius = 100
        self.circle_speed = 2 * math.pi / 10000  # 一圈分 1000 帧完成

        # 设置手动模式的超时时间（秒）
        self.MANUAL_TIMEOUT = 5
        self.last_key_time = time.time()
        self.current_time = time.time()

        self.pic = None
        self.coords1 = np.load('car_1.npy')
        self.len1 = len(self.coords1)
        self.coords2 = np.load('car_2.npy')
        self.len2 = len(self.coords2)
        self.coords3 = np.load('car_3.npy')
        self.len3 = len(self.coords3)
        self.coords4 = np.load('car_4.npy')
        self.len4 = len(self.coords4)


        '''

        self.cap = cv2.VideoCapture('images/car_1.mp4')
        self.thread = VideoThread(self.cap , self.pic)
        self.thread.start()
        '''

        #print(self.Image['car_1']['auto'])
        self.con = 0


    def run(self):
        # 游戏循环
        while True:
            #self.pic = self.thread.get_pic()



            # 处理游戏事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # 获取按键状态
            keys = pygame.key.get_pressed()
            '''
            if self.Image['car_1']['auto'] == 1:  # 自动移动模式
                self.mod_a('car_1')
            elif self.Image['car_1']['auto'] == 2:  # 手动移动模式
                self.mod_p('car_1')
            '''

            self.current_time = time.time()
            #print('auto4:  ' + str(self.Image['car_1']['auto']))
            if self.Image['car_1']['play'] == 1:
                if self.current_time - self.last_key_time > 0.1:
                    self.send_pic('car_1')
            if self.Image['car_1']['auto'] == 1:  # 自动移动模式


                if self.Image['car_1']['flag'] < self.len1 :
                    dy = self.coords1[self.Image['car_1']['flag']][1] - self.Image['car_1']['position'][1]
                    dx = self.coords1[self.Image['car_1']['flag']][0] - self.Image['car_1']['position'][0]
                    rads = math.atan2(dy, dx)  # 计算方位角，以弧度返回

                    rads = math.degrees(rads)
                    '''
                    if a < 0:
                        a = 360 + a
                    # print(a)
                    rads = math.radians(a)
                    '''
                    self.Image['car_1']['cor'] = rads
                    self.Image['car_1']['position'] = [self.coords1[self.Image['car_1']['flag']][0],
                                                       self.coords1[self.Image['car_1']['flag']][1]]
                    #print(self.Image['car_1']['position'])
                    if self.Image['car_1']['serial'] is not None:
                        self.send('car_1', 1)
                    self.Image['car_1']['flag'] += 1
                else:
                    self.Image['car_1']['auto'] = 2
                    self.Image['car_1']['flag'] = 0
                    self.test_run(0,time.time(),'car_1')


                #print('aaa')

            elif self.Image['car_1']['auto'] == 2:  # 手动移动模式
                current_time = time.time()
                self.Image['car_1']['ticks_start'] = None
                self.test_run(0, time.time(), 'car_1')
                #print('bbb')

            if self.Image['car_2']['play'] == 1:
                if self.current_time - self.last_key_time > 0.1:
                    self.send_pic('car_2')

            if self.Image['car_2']['auto'] == 1:  # 自动移动模式

                if self.Image['car_2']['flag'] < self.len2 :
                    dy = self.coords2[self.Image['car_2']['flag']][1] - self.Image['car_2']['position'][1]
                    dx = self.coords2[self.Image['car_2']['flag']][0] - self.Image['car_2']['position'][0]
                    rads = math.atan2(dy, dx)  # 计算方位角，以弧度返回
                    rads = math.degrees(rads)
                    '''
                    a = math.degrees(rads)
                    if a < 0:
                        a = 360 + a
                    #print(a)
                    rads = math.radians(a)
                    '''
                    self.Image['car_2']['cor'] = rads
                    self.Image['car_2']['position'] = [self.coords2[self.Image['car_2']['flag']][0],
                                                       self.coords2[self.Image['car_2']['flag']][1]]
                    #print(self.Image['car_2']['position'])
                    if self.Image['car_2']['serial'] is not None:
                        self.send('car_2', 1)
                    self.Image['car_2']['flag'] += 1
                else:
                    self.Image['car_2']['auto'] = 2
                    self.Image['car_2']['flag'] = 0
                    self.test_run(0, time.time(), 'car_2')

            elif self.Image['car_2']['auto'] == 2:  # 手动移动模式
                current_time = time.time()
                self.Image['car_2']['ticks_start'] = None
                self.test_run(0, time.time(), 'car_2')


            if self.Image['car_3']['play'] == 1:
                if self.current_time - self.last_key_time > 0.1:
                    self.send_pic('car_3')
            if self.Image['car_3']['auto'] == 1:  # 自动移动模式
                con1  = self.Image['car_3']['flag']
                con2 = self.len3


                if self.Image['car_3']['flag'] < self.len3 :
                    print(f'flag:{con1}')
                    dy = self.coords3[self.Image['car_3']['flag']][1] - self.Image['car_3']['position'][1]
                    dx = self.coords3[self.Image['car_3']['flag']][0] - self.Image['car_3']['position'][0]
                    rads = math.atan2(dy, dx)  # 计算方位角，以弧度返回
                    rads = math.degrees(rads)
                    '''
                    a = math.degrees(rads)
                    if a < 0:
                        a = 360 + a
                    #print(a)
                    rads = math.radians(a)
                    '''
                    self.Image['car_3']['cor'] = rads
                    self.Image['car_3']['position'] = [self.coords3[self.Image['car_3']['flag']][0],
                                                       self.coords3[self.Image['car_3']['flag']][1]]
                    #print(self.Image['car_3']['position'])
                    if self.Image['car_3']['serial'] is not None:
                        self.send('car_3', 1)
                    self.Image['car_3']['flag'] += 1
                else:
                    self.Image['car_3']['auto'] = 2
                    self.Image['car_3']['flag'] = 0
                    self.test_run(0, time.time(), 'car_3')

            elif self.Image['car_3']['auto'] == 2:  # 手动移动模式
                current_time = time.time()
                self.Image['car_3']['ticks_start'] = None
                self.test_run(0, time.time(), 'car_3')


            if self.Image['car_4']['play'] == 1:
                if self.current_time - self.last_key_time > 0.1:
                    self.send_pic('car_4')
            if self.Image['car_4']['auto'] == 1:  # 自动移动模式

                if self.Image['car_4']['flag'] < self.len4 :
                    dy = self.coords4[self.Image['car_4']['flag']][1] - self.Image['car_4']['position'][1]
                    dx = self.coords4[self.Image['car_4']['flag']][0] - self.Image['car_4']['position'][0]
                    rads = math.atan2(dy, dx)  # 计算方位角，以弧度返回
                    rads = math.degrees(rads)
                    '''
                    a = math.degrees(rads)
                    if a < 0:
                        a = 360 + a
                    # print(a)
                    rads = math.radians(a)
                    '''
                    self.Image['car_4']['cor'] = rads
                    self.Image['car_4']['position'] = [self.coords4[self.Image['car_4']['flag']][0],
                                                       self.coords4[self.Image['car_4']['flag']][1]]
                    #print(self.Image['car_4']['position'])
                    if self.Image['car_4']['serial'] is not None:
                        self.send('car_4', 1)
                    self.Image['car_4']['flag'] += 1
                else:
                    self.Image['car_4']['auto'] = 2
                    self.Image['car_4']['flag'] = 0
                    self.test_run(0, time.time(), 'car_4')

            elif self.Image['car_4']['auto'] == 2:  # 手动移动模式
                current_time = time.time()
                self.Image['car_4']['ticks_start'] = None
                self.test_run(0, time.time(), 'car_4')








            self.paint()

    def path(self,port,path):
        self.Image[port]['path'] = path
        if port == 'car_1':
            self.coords1 = path
            self.len1 = len(self.coords1)
        elif port == 'car_2':
            self.coords2 = path
            self.len2 = len(self.coords2)
        elif port == 'car_3':
            self.coords3 = path
            self.len3 = len(self.coords3)
        elif port == 'car_4':
            self.coords4 = path
            self.len4 = len(self.coords4)
        #print('test_path')
        print(path)




    def test_auto(self,forward,time,port):
        self.Image[port]['auto'] = 1
        self.Image[port]['flag'] = 0
        #print('test_auto')

    def test_play(self,pic,port):
        self.Image[port]['play'] = pic
        print('test_pic')
        print(pic)


    def test_run(self,forward,time,port):

        if forward == 1:
            self.Image[port]['position'][1] -= self.speed
            self.Image[port]['cor'] = 4.71
        elif forward == 2:
            self.Image[port]['position'][1] += self.speed
            self.Image[port]['cor'] = 1.57
        elif forward == 3:
            self.Image[port]['position'][0] -= self.speed
            self.Image[port]['cor'] = 3.14
        elif forward == 4:
            self.Image[port]['position'][0] += self.speed
            self.Image[port]['cor'] = 0
        elif forward == 5:
            self.Image[port]['position'][1] -= self.speed
            self.Image[port]['position'][0] -= self.speed
            self.Image[port]['cor'] = 3.925
        elif forward == 6:
            self.Image[port]['position'][1] -= self.speed
            self.Image[port]['position'][0] += self.speed
            self.Image[port]['cor'] = 5.495
        elif forward == 7:
            self.Image[port]['position'][1] += self.speed
            self.Image[port]['position'][0] -= self.speed
            self.Image[port]['cor'] = 2.355
        elif forward == 8:
            self.Image[port]['position'][1] += self.speed
            self.Image[port]['position'][0] += self.speed
            self.Image[port]['cor'] = 0.785
        elif forward == 0:
            self.Image[port]['position'][1] += 0
            self.Image[port]['position'][0] += 0


        self.Image[port]['last_time'] = time
        self.Image[port]['auto'] = 2
        self.Image[port]['last_position'] = self.Image[port]['position']
        self.send(port,2)
        self.paint()

    def show(self,port,x,y,ser,auto,video):
        self.Image[port]['position'] = [x,y]
        self.Image[port]['last_position'] = [x, y]
        self.Image[port]['status'] = True
        self.Image[port]['auto'] = auto
        #print('auto3:  ' )
        #print(self.Image[port]['auto'])
        self.Image[port]['last_time'] = time.time()
        self.Image[port]['serial'] = ser
        self.Image[port]['video'] = video
        self.paint()
    def hide(self,port):
        self.Image[port]['status'] = False
        self.Image[port]['serial'] = None
        self.paint()

    def send(self,port,sta):
        id = 1


        spe = 2

        sender = info_Sender(self.Image[port]['serial'])
        sender.send_info(id,self.Image[port]['position'][0],self.Image[port]['position'][1],
        self.Image[port]['cor'],spe,sta)

    def send_pic(self,port):
        self.con += 1
        con = self.con % 3000

        sender = info_Sender(self.Image[port]['serial'])
        sender.send_image(f"{self.Image[port]['video']}/{con}.jpg")
        self.last_key_time = time.time()

        '''
        if self.con%5 == 0:
            sender.send_image('images/1.png')
        elif self.con%5 == 1:
            sender.send_image('images/2.png')
        elif self.con%5 == 2:
            sender.send_image('images/3.png')
        elif self.con%5 == 3:
            sender.send_image('images/4.png')
        elif self.con%5 == 4:
            sender.send_image('images/5.png')
            '''



    def info(self,port):
        #print('hello')
        info = [1,self.Image[port]['position'][0],self.Image[port]['position'][1],
        self.Image[port]['cor'],2,self.Image[port]['auto']]
        #print(info)
        return info

    def paint(self):
        # 清除屏幕
        self.screen.fill((0, 0, 0))

        # 绘制背景图片
        self.screen.blit(self.background_image, (0, 0))

        # 绘制图片
        if self.Image['car_1']['status']:
           self.screen.blit(self.Image['car_1']['image'], self.Image['car_1']['position'])
        if self.Image['car_2']['status']:
           self.screen.blit(self.Image['car_2']['image'], self.Image['car_2']['position'])
        if self.Image['car_3']['status']:
           self.screen.blit(self.Image['car_3']['image'], self.Image['car_3']['position'])
        if self.Image['car_4']['status']:
           self.screen.blit(self.Image['car_4']['image'], self.Image['car_4']['position'])

        # 刷新屏幕
        pygame.display.flip()

        # 控制帧率
        pygame.time.Clock().tick(60)
        time.sleep(0.1)




if __name__ == '__main__':

    game = CarGame(640, 480,1)
    game.run()
