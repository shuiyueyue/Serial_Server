import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap, QImage
import a_star1
import numpy as np


def overall(obstacles,targets,width,height):
    # set obstacle positions
    ob_x, ob_y = a_star1.calc_obstacle_center_number(obstacles)
    center_x, center_y = a_star1.calc_center_xy(targets)

    for i in range(0, width):#下边框
        ob_x.append(i)
        ob_y.append(0)
    for i in range(0, height+1):#右
        ob_x.append(width)
        ob_y.append(i)
    for i in range(0,width):#上
        ob_x.append(i)
        ob_y.append(height)
    for i in range(0,height):#左
        ob_x.append(0)
        ob_y.append(i)

    figure = plt.figure()
    plt.gca().invert_yaxis()
    plt.plot(ob_x, ob_y, "ok")
    plt.plot(center_x, center_y, "^g")
    plt.axis('equal')

    canvas = figure.canvas
    canvas.draw()
    width1, height1 = canvas.get_width_height()
    image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape(height1, width1, 3)

    qimage = QImage(image.data, width1, height1, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)

    return pixmap










