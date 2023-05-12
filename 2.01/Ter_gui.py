import sys
from typing import List
from T_CP import info_Sender
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QGraphicsView, QGraphicsScene, \
    QGraphicsTextItem, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QPointF, QCoreApplication, QThread, QTimer
from coords import Coords
from Ter_serve import Ter_ser
import threading
import math

class ImageViewer(QGraphicsView):
    def __init__(self):
        super().__init__()





        # 创建场景和添加图片
        self.scene = QGraphicsScene(self)
        self.pixmap = QPixmap("images/car_1.png")
        self.pixmap2 = QPixmap("images/car_2.png")
        self.pixmap3 = QPixmap("images/car_3.png")
        self.pixmap4 = QPixmap("images/car_4.png")

        self.image = None
        self.image2 = None
        self.image3 = None
        self.image4 = None
        '''
        self.image = self.scene.addPixmap(self.pixmap)
        self.image2 = self.scene.addPixmap(self.pixmap2)
        self.image3 = self.scene.addPixmap(self.pixmap3)
        self.image4 = self.scene.addPixmap(self.pixmap4)
        '''

        self.stop_flag = False

        self.serve = Ter_ser()

        self.cars = {
            'car_1': {'first': (100,100), 'second': (-100,100), 'third': (-100,-100), 'fourth': (100,-100)},
            'car_2': {'first': (150,150), 'second': (-150,150), 'third': (-150,-150), 'fourth': (150,-150)},
            'car_3': {'first': (50,50), 'second': (-50,50), 'third': (-50,-50), 'fourth': (50,-50)},
            'car_4': {'first': (200,200), 'second': (-200,200), 'third': (-200,-200), 'fourth': (200,-200)},
        }


        # 添加坐标显示文字
        self.text = QGraphicsTextItem()
        self.text2 = QGraphicsTextItem()
        self.text3 = QGraphicsTextItem()
        self.text4 = QGraphicsTextItem()

        self.Image = {
            'car_1': {'image': self.image, 'text': self.text  , 'direction': 0, 'status': None, 'position': None, 'cor': None, },
            'car_2': {'image': self.image2, 'text': self.text2, 'direction': 0, 'status': None, 'position': None, 'cor': None, },
            'car_3': {'image': self.image3, 'text': self.text3, 'direction': 0, 'status': None, 'position': None, 'cor': None, },
            'car_4': {'image': self.image4, 'text': self.text4, 'direction': 0, 'status': None, 'position': None, 'cor': None, },
        }

        self.itemlist = [self.image, self.image2, self.image3, self.image4]
        self.pathlist = [np.load('car_1.npy')[:, :] * 3 , np.load('car_2.npy')[:, :] * 3, np.load('car_3.npy')[:, :] * 3, np.load('car_4.npy')[:, :] * 3]

        #self.text.setPlainText(f"({self.Image['image1']['image'].pos().x()}, {self.Image['image1']['image'].pos().y()})")
        self.text.setFont(QFont("Arial", 12))
        #self.text.setPos(self.Image['image1']['image'].pos().x(), self.Image['image1']['image'].pos().y() - 20)
        self.scene.addItem(self.text)

        #self.text2.setPlainText(f"({self.Image['image2']['image'].pos().x()}, {self.Image['image2']['image'].pos().y()})")
        self.text2.setFont(QFont("Arial", 12))
        #self.text2.setPos(self.Image['image2']['image'].pos().x(), self.Image['image2']['image'].pos().y() - 20)
        self.scene.addItem(self.text2)

        #self.text3.setPlainText(f"({self.Image['image3']['image'].pos().x()}, {self.Image['image3']['image'].pos().y()})")
        self.text3.setFont(QFont("Arial", 12))
        #self.text3.setPos(self.Image['image3']['image'].pos().x(), self.Image['image3']['image'].pos().y() - 20)
        self.scene.addItem(self.text3)

        #self.text4.setPlainText(f"({self.Image['image4']['image'].pos().x()}, {self.Image['image4']['image'].pos().y()})")
        self.text4.setFont(QFont("Arial", 12))
        #self.text4.setPos(self.Image['image4']['image'].pos().x(), self.Image['image4']['image'].pos().y() - 20)
        self.scene.addItem(self.text4)


        # 将场景设置为视图的场景
        self.setScene(self.scene)

        # 启用拖动
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        # 创建定时器对象
        self.timer = QTimer()
        # 设置定时器时间间隔
        self.timer.setInterval(100)
        # 定时器启动
        self.timer.start()
        # 定时器超时信号连接到槽函数
        #self.timer.timeout.connect(self.test)


    def test(self):
        print(self.stop_flag)


    def show(self,ima,x,y):
        if ima == 'car_1':
            self.image = self.scene.addPixmap(self.pixmap)
            self.Image['car_1']['image'] = self.image
            self.Image['car_1']['image'].setPos(x, y)
        elif ima == 'car_2':
            self.image2 = self.scene.addPixmap(self.pixmap2)
            self.Image['car_2']['image'] = self.image2
            self.Image['car_2']['image'].setPos(x, y)

        elif ima == 'car_3':
            self.image3 = self.scene.addPixmap(self.pixmap3)
            self.Image['car_3']['image'] = self.image3
            self.Image['car_3']['image'].setPos(x, y)

        elif ima == 'car_4':
            self.image4 = self.scene.addPixmap(self.pixmap4)
            self.Image['car_4']['image'] = self.image4
            self.Image['car_4']['image'].setPos(x, y)

    def hide(self,ima):
        if ima == 'car_1':
            self.scene.removeItem(self.image)
        elif ima == 'car_2':
            self.scene.removeItem(self.image2)
        elif ima == 'car_3':
            self.scene.removeItem(self.image3)
        elif ima == 'car_4':
            self.scene.removeItem(self.image4)


    def update_text(self,ima):
        self.Image[ima]['text'].setPlainText(f"({self.Image[ima]['image'].pos().x():.2f}, {self.Image[ima]['image'].pos().y():.2f})")
        self.Image[ima]['text'].setPos(self.Image[ima]['image'].pos().x(), self.Image[ima]['image'].pos().y() - 20)

    def calculate_bearing(self,dx,dy):

        if dx == 0 and dy == 0:
            return 0  # 两个坐标相同，无法计算方位角
        elif dx == 0 and dy > 0:
            return math.pi / 2  # 在y轴正方向上
        elif dx == 0 and dy < 0:
            return 3 * math.pi / 2  # 在y轴负方向上
        elif dy == 0 and dx > 0:
            return 0  # 在x轴正方向上
        elif dy == 0 and dx < 0:
            return math.pi  # 在x轴负方向上

        # 计算方位角
        angle = math.atan(dx / dy)
        if dx > 0 and dy > 0:  # 第一象限
            return math.pi / 2 - angle
        elif dx > 0 and dy < 0:  # 第二象限
            return math.pi + angle
        elif dx < 0 and dy < 0:  # 第三象限
            return math.pi + angle
        elif dx < 0 and dy > 0:  # 第四象限
            return 2 * math.pi + angle

    def smooth_move(self,ima,serial):
        while True:
            for i in range(1, 4):
                # print("smooth_move",ima)
                coords = Coords()
                if i == 1:
                    coords = coords.smooth_coords(
                        (self.Image[ima]['image'].pos().x(), self.Image[ima]['image'].pos().y()),
                        self.cars[ima]['first'], 500, 10)
                elif i == 2:
                    coords = coords.smooth_coords(
                        (self.Image[ima]['image'].pos().x(), self.Image[ima]['image'].pos().y()),
                        self.cars[ima]['second'], 500, 10)
                elif i == 3:
                    coords = coords.smooth_coords(
                        (self.Image[ima]['image'].pos().x(), self.Image[ima]['image'].pos().y()),
                        self.cars[ima]['third'], 500, 10)
                elif i == 4:
                    coords = coords.smooth_coords(
                        (self.Image[ima]['image'].pos().x(), self.Image[ima]['image'].pos().y()),
                        self.cars[ima]['fourth'], 500, 10)

                # print(coords)

                from datetime import datetime

                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                print("move Time =", current_time)

                for coord in coords:
                    if self.Image[ima]['direction'] == 5:
                        break
                    if serial.in_waiting > 0:
                        print('stop')
                        break
                    target_pos = QPointF(coord[0], coord[1])
                    delta = target_pos - self.Image[ima]['image'].pos()
                    # if delta.manhattanLength() > 1:  # 控制移动的最小距离
                    self.Image[ima]['image'].moveBy(delta.x(), delta.y())
                    # 更新坐标显示
                    self.update_text(ima)
                    cor = self.calculate_bearing(delta.x(), delta.y())
                    # print(cor)
                    self.send(ima, serial, cor)
                    # self.text.setPlainText(f"({(self.Image[ima]['image'].pos().x()):.2f}, {(self.Image[ima]['image'].pos().y()):.2f})")
                    # self.text.setPos(self.Image[ima]['image'].pos().x(), self.Image[ima]['image'].pos().y() - 20)
                    QCoreApplication.processEvents()
                    QThread.msleep(10)  # 控制移动的时间间隔

                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                print("move_over Time =", current_time)




    def smooth_move_1(self):
        # 加载四个npy文件，分别为path_1, path_2, path_3, path_4
        car_paths = ['path_1.npy', 'path_2.npy', 'path_3.npy', 'path_4.npy']
        cars = {}
        print('smooth_move_1')

        # 遍历四个文件，将它们的path属性加载到cars字典中
        for car, path in zip(range(1, 5), car_paths):
            cars[f'car_{car}'] = {'path': np.load(path)[2:, 0:3]  }



        # 同时遍历每个字典的path属性
        #stop_flag = False
        for car1, car2, car3, car4 in zip(cars['car_1']['path'], cars['car_2']['path'], cars['car_3']['path'],
                                          cars['car_4']['path']):
            if self.stop_flag:
                break

            if self.Image['car_1']['status'] == 1:
                self.Image['car_1']['image'].moveBy(car1[0], car1[1])
                self.Image['car_2']['image'].moveBy(car2[0], car2[1])
                self.Image['car_3']['image'].moveBy(car3[0], car3[1])
                self.Image['car_4']['image'].moveBy(car4[0], car4[1])
                QCoreApplication.processEvents()
                QThread.msleep(10)  # 控制移动的时间间隔
            else:
                self.stop_flag = True



    def smooth_move_2(self, items, coords):
        num_items = len(items)
        print(num_items)
        deltas = [np.zeros(3) for _ in range(num_items)]  # 初始化deltas为一个长度为num_items的列表，其中每个元素为一个长度为2的全零nparray
        print(len(deltas))
        '''
        '''
        for i in range(num_items):
            for coord in coords[i]:
                target_pos = QPointF(coord[0], coord[1])
                delta = target_pos - items[i].pos()
                items[i].moveBy(delta.x(), delta.y())
                print(coord[3])

                deltas[i] = np.vstack(
                    [deltas[i], [delta.x(), delta.y() ,coord[3] ]])  # 将当前delta添加到deltas[i]的末尾，即将一个长度为2的列表添加到一个二维nparray中
                QCoreApplication.processEvents()
                QThread.msleep(1)




        return deltas

    def send(self,ima,serial,cor):
        id = 1
        x = self.Image[ima]['image'].pos().x()
        y = self.Image[ima]['image'].pos().y()

        spe = 2
        sta = 0
        sender = info_Sender(serial)
        sender.send_info(id,x,y,cor,spe,sta)


    def move_up(self,ima,serial):
        self.Image[ima]['image'].moveBy(0, -1)
        self.update_text(ima)
        self.Image[ima]['direction'] = 1
        self.send(ima,serial,0)
        #self.text.setPlainText(f"({self.Image[ima]['image'].pos().x()}, {self.Image[ima]['image'].pos().y()})")
        #self.text.setPos(self.Image[ima]['image'].pos().x(), self.Image[ima]['image'].pos().y() - 20)

    def move_down(self,ima,serial):
        self.Image[ima]['image'].moveBy(0, 1)
        self.update_text(ima)
        self.Image[ima]['direction'] = 2
        self.send(ima,serial,0)
    def move_left(self,ima,serial):
        self.Image[ima]['image'].moveBy(-1, 0)
        self.update_text(ima)
        self.Image[ima]['direction'] = 3
        self.send(ima,serial,0)
    def move_right(self,ima,serial):
        self.Image[ima]['image'].moveBy(1, 0)
        self.update_text(ima)
        self.Image[ima]['direction'] = 4
        self.send(ima,serial,0)
    def move_up_left(self,ima,serial):
        self.Image[ima]['image'].moveBy(-1, -1)
        self.update_text(ima)
        self.Image[ima]['direction'] = 5
        self.send(ima,serial,0)
    def move_up_right(self,ima,serial):
        self.Image[ima]['image'].moveBy(1, -1)
        self.update_text(ima)
        self.Image[ima]['direction'] = 6
        self.send(ima,serial,0)
    def move_down_left(self,ima,serial):
        self.Image[ima]['image'].moveBy(-1, 1)
        self.update_text(ima)
        self.Image[ima]['direction'] = 7
        self.send(ima,serial,0)
    def move_down_right(self,ima,serial):
        self.Image[ima]['image'].moveBy(1, 1)
        self.update_text(ima)
        self.Image[ima]['direction'] = 8
        self.send(ima,serial,0)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个QWidget
        self.central_widget = QWidget(self)

        # 创建一个QHBoxLayout，并将QGraphicsView添加到它上面
        self.horizontal_layout = QHBoxLayout(self.central_widget)
        self.image_viewer = ImageViewer()
        self.horizontal_layout.addWidget(self.image_viewer)
        self.image_viewer.show( 'car_1', 0, 0)
        self.image_viewer.show( 'car_2', 0, 100)
        self.image_viewer.show( 'car_3', 0, 200)
        self.image_viewer.show( 'car_4', 0, 300)

        # 将QWidget设置为主窗口的中心窗口
        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
