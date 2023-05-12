"""

A* grid planning

author: Atsushi Sakai(@Atsushi_twi)
        Nikos Kanargias (nkana@tee.gr)

See Wikipedia article (https://en.wikipedia.org/wiki/A*_search_algorithm)

"""

import math

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from utils.general import (cv2)
from matplotlib.backends.backend_template import FigureCanvas



show_animation = True


class AStarPlanner:

    def __init__(self, ox, oy, resolution, rr):
        """
        Initialize grid map for a star planning

        ox: x position list of Obstacles [m]
        oy: y position list of Obstacles [m]
        resolution: grid resolution [m],地图的像素
        rr: robot radius[m]
        """

        self.resolution = resolution
        self.rr = rr
        self.min_x, self.min_y = 0, 0
        self.max_x, self.max_y = 0, 0
        self.obstacle_map = None
        self.x_width, self.y_width = 0, 0
        self.motion = self.get_motion_model()
        self.calc_obstacle_map(ox, oy)


    class Node:
        """定义搜索区域节点类,每个Node都包含坐标x和y, 移动代价cost和父节点索引。
        """
        def __init__(self, x, y, cost, parent_index):
            self.x = x  # index of grid
            self.y = y  # index of grid
            self.cost = cost
            self.parent_index = parent_index

        def __str__(self):
            return str(self.x) + "," + str(self.y) + "," + str(
                self.cost) + "," + str(self.parent_index)

    def planning(self, sx, sy, gx, gy):
        """
        A star path search
        输入起始点和目标点的坐标(sx,sy)和(gx,gy)，
        最终输出的结果是路径包含的点的坐标集合rx和ry。
        input:
            s_x: start x position [m]
            s_y: start y position [m]
            gx: goal x position [m]
            gy: goal y position [m]

        output:
            rx: x position list of the final path
            ry: y position list of the final path
        """

        start_node = self.Node(self.calc_xy_index(sx, self.min_x),
                               self.calc_xy_index(sy, self.min_y), 0.0, -1)
        goal_node = self.Node(self.calc_xy_index(gx, self.min_x),
                              self.calc_xy_index(gy, self.min_y), 0.0, -1)

        open_set, closed_set = dict(), dict()
        open_set[self.calc_grid_index(start_node)] = start_node

        while 1:
            if len(open_set) == 0:
                print("Open set is empty..")
                break

            c_id = min(
                open_set,
                key=lambda o: open_set[o].cost + self.calc_heuristic(goal_node, open_set[o]))
            current = open_set[c_id]

            # show graph
            '''if show_animation:  # pragma: no cover
                plt.plot(self.calc_grid_position(current.x, self.min_x),
                         self.calc_grid_position(current.y, self.min_y), color = 'blue',marker = 'x',markersize = '5')
                # for stopping simulation with the esc key.
                plt.gcf().canvas.mpl_connect('key_release_event', lambda event: [exit(0) if event.key == 'escape' else None])'''

            # 通过追踪当前位置current.x和current.y来动态展示路径寻找
            if current.x == goal_node.x and current.y == goal_node.y:
                print("Find goal")
                goal_node.parent_index = current.parent_index
                goal_node.cost = current.cost
                break

            # Remove the item from the open set
            del open_set[c_id]

            # Add it to the closed set
            closed_set[c_id] = current

            # expand_grid search grid based on motion model
            for i, _ in enumerate(self.motion):
                node = self.Node(current.x + self.motion[i][0],
                                 current.y + self.motion[i][1],
                                 current.cost + self.motion[i][2], c_id)
                n_id = self.calc_grid_index(node)

                # If the node is not safe, do nothing
                if not self.verify_node(node):
                    continue

                if n_id in closed_set:
                    continue

                if n_id not in open_set:
                    open_set[n_id] = node  # discovered a new node
                else:
                    if open_set[n_id].cost > node.cost:
                        # This path is the best until now. record it
                        open_set[n_id] = node

        rx, ry = self.calc_final_path(goal_node, closed_set)

        return rx, ry

    def calc_final_path(self, goal_node, closed_set):
        # generate final course
        rx, ry = [self.calc_grid_position(goal_node.x, self.min_x)], [
            self.calc_grid_position(goal_node.y, self.min_y)]
        parent_index = goal_node.parent_index
        while parent_index != -1:
            n = closed_set[parent_index]
            rx.append(self.calc_grid_position(n.x, self.min_x))
            ry.append(self.calc_grid_position(n.y, self.min_y))
            parent_index = n.parent_index

        return rx, ry

    @staticmethod
    def calc_heuristic(n1, n2):
        """计算启发函数

        Args:
            n1 (_type_): _description_
            n2 (_type_): _description_

        Returns:
            _type_: _description_
        """
        w = 1.0  # weight of heuristic
        d = w * math.hypot(n1.x - n2.x, n1.y - n2.y)
        return d

    def calc_grid_position(self, index, min_position):
        """
        calc grid position

        :param index:
        :param min_position:
        :return:
        """
        pos = index * self.resolution + min_position
        return pos


    def calc_xy_index(self, position, min_pos):
        return round((position - min_pos) / self.resolution)

    def calc_grid_index(self, node):
        return (node.y - self.min_y) * self.x_width + (node.x - self.min_x)

    def verify_node(self, node):
        px = self.calc_grid_position(node.x, self.min_x)
        py = self.calc_grid_position(node.y, self.min_y)

        if px < self.min_x:
            return False
        elif py < self.min_y:
            return False
        elif px >= self.max_x:
            return False
        elif py >= self.max_y:
            return False

        # collision check
        if self.obstacle_map[node.x][node.y]:
            return False

        return True

    def calc_obstacle_map(self, ox, oy):

        self.min_x = round(min(ox))
        self.min_y = round(min(oy))
        self.max_x = round(max(ox))
        self.max_y = round(max(oy))
        print("min_x:", self.min_x)
        print("min_y:", self.min_y)
        print("max_x:", self.max_x)
        print("max_y:", self.max_y)

        self.x_width = round((self.max_x - self.min_x) / self.resolution)
        self.y_width = round((self.max_y - self.min_y) / self.resolution)
        print("x_width:", self.x_width)
        print("y_width:", self.y_width)

        # obstacle map generation
        self.obstacle_map = [[False for _ in range(self.y_width)]
                             for _ in range(self.x_width)]
        for ix in range(self.x_width):
            x = self.calc_grid_position(ix, self.min_x)
            for iy in range(self.y_width):
                y = self.calc_grid_position(iy, self.min_y)
                for iox, ioy in zip(ox, oy):
                    d = math.hypot(iox - x, ioy - y)
                    if d <= self.rr:
                        self.obstacle_map[ix][iy] = True
                        break


    @staticmethod
    def get_motion_model():
        # dx, dy, cost
        motion = [[1, 0, 1],
                  [0, 1, 1],
                  [-1, 0, 1],
                  [0, -1, 1],
                  [-1, -1, math.sqrt(2)],
                  [-1, 1, math.sqrt(2)],
                  [1, -1, math.sqrt(2)],
                  [1, 1, math.sqrt(2)]]

        return motion






class Target:
    def __init__(self, id, cls, x1, y1, x2, y2):
        self.id = id
        self.cls = cls
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


# 计算传过来的左上右下目标点的中心位置
def calc_center_xy(targets):
    size = len(targets)
    center_x, center_y = [ ], [ ]
    for i in range(0, size):
        center_x.append((targets[i].x1 + targets[i].x2) / 2)
        center_y.append((targets[i].y1 + targets[i].y2) / 2)
    return center_x, center_y


class Robot:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y


def overall(obstacles,targets,width,height):
    # set obstacle positions
    ob_x, ob_y = calc_obstacle_center_number(obstacles)
    center_x, center_y = calc_center_xy(targets)

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

    figure = plt.figure(figsize=(width/10,height/10))
    plt.gca().invert_yaxis()
    plt.plot(ob_x, ob_y, "ok")
    plt.plot(center_x, center_y, "^g")
    plt.axis('equal')

    canvas = figure.canvas
    canvas.draw()
    width, height = canvas.get_width_height()
    image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape(height, width, 3)

    qimage = QImage(image.data, width, height, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)

    return pixmap


def set_robot_init_xy(robots):
    size = len(robots)
    robot_x,robot_y = [ ],[ ]
    for i in range(0,size):
        robot_x.append(robots[i].x)
        robot_y.append(robots[i].y)
    return robot_x, robot_y


class Obstacle:
    def __init__(self, id, cls, x1, y1, x2, y2):
        self.id = id
        self.cls = cls
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2



def calc_obstacle_center_number(obstacles):
    size = len(obstacles)
    ob_x, ob_y = [], []
    for i in range(0, size):
        with_number = abs(obstacles[i].x2 - obstacles[i].x1)
        high_number = abs(obstacles[i].y2 - obstacles[i].y1)
        init_x = obstacles[i].x1
        init_y = obstacles[i].y2
        for j in range(0, high_number+1):
            obstacles[i].y2 = init_y + j
            again_init_x = init_x
            for k in range(0, with_number+1):
                ob_x.append(obstacles[i].x1)
                ob_y.append(obstacles[i].y2)
                obstacles[i].x1 = again_init_x + k + 1
                if obstacles[i].x1 <=obstacles[i].x2:
                    continue
                else:
                    obstacles[i].x1=(obstacles[i].x1%obstacles[i].x2)+init_x-1
    return ob_x, ob_y


class Path:
    def __init__(self, path_id, points):
        self.path_id = path_id  # 路径编号
        self.points = points  # 路径上的点列表
    def __str__(self):
        path_str = f"Path ID: {self.path_id}\nPoints:\n"
        for point in self.points:
            path_str += f"({point[0]}, {point[1]})\n"
        return path_str


def robot_less_equal_target(obstacles, targets, robots, width, height):
    path0 = Path(0,[])
    path1 = Path(1,[])
    path2 = Path(2,[])
    path3 = Path(3,[])
    paths = [path0,path1,path2,path3]
    figure = plt.figure(figsize=(width/10,height/10))


    plt.gca().invert_yaxis()
    index = 1
    size1 = len(targets)
    size2 = len(robots)#size1<=size2
    ox, oy = calc_obstacle_center_number(obstacles)
    for q in range(0, width):  # 下边框
        ox.append(q)
        oy.append(0)
    for q in range(0, height + 1):  # 右
        ox.append(width)
        oy.append(q)
    for q in range(0, width):  # 上
        ox.append(q)
        oy.append(height)
    for q in range(0, height):  # 左
        ox.append(0)
        oy.append(q)
    plt.plot(ox, oy, ".k")
        # paths[i].path_id = i+1
    center_x, center_y = calc_center_xy(targets)
    for i in range(0,size1):
        plt.plot(center_x[i], center_y[i],"^k")

    robot_x, robot_y = set_robot_init_xy(robots)
    plt.plot(robot_x[0],robot_y[0],"ok")
    plt.plot(robot_x[1],robot_y[1],"og")
    plt.plot(robot_x[2],robot_y[2],"oy")
    plt.plot(robot_x[3],robot_y[3],"oc")
   # plt.plot(center_x, center_y, "^g")
    plt.grid(True)
    plt.axis('equal')

    astar = AStarPlanner(ox, oy, 2.0, 1.0)
    while size1>size2:
         center_x, center_y = calc_center_xy(targets)
         robot_x, robot_y = set_robot_init_xy(robots)
         for i in range(0, size2):
            rx,ry = astar.planning(robot_x[i],robot_y[i],center_x[i],center_y[i])
            rx.reverse()
            ry.reverse()
         #   all_rx.append(rx)
        #    all_ry.append(ry)
            if i%4 ==0:
                plt.plot(rx,ry, "-r")
            elif i%4 ==1:
                plt.plot(rx, ry, "-g")
            elif i%4 ==2:
                plt.plot(rx,ry, "-y")
            elif i%4 ==3:
                plt.plot(rx, ry, "-c")

            points = np.column_stack((rx,ry))
            paths[i%4].points.append(points)
            robots[i].x = center_x[i]
            robots[i].y = center_y[i]
      #   plt.plot(all_rx, all_ry, "-r")
         del targets[0:size2]
         size1 = len(targets)
         size2 = len(robots)

    center_x, center_y = calc_center_xy(targets)
    robot_x, robot_y = set_robot_init_xy(robots)
    print(center_x[:])
    for j in range(0,size1):
   #     astar = AStarPlanner(ox, oy, 2.0, 1.0)
        rrx, rry = astar.planning(robot_x[j], robot_y[j], center_x[j], center_y[j])
        rrx.reverse()
        rry.reverse()
        plt.plot(rrx, rry, "-r")
        if j % 4 == 0:
            plt.plot(rrx, rry, "-r")
        elif j % 4 == 1:
            plt.plot(rrx, rry, "-g")
        elif j % 4 == 2:
            plt.plot(rrx, rry, "-y")
        elif j % 4 == 3:
            plt.plot(rrx, rry, "-c")
        path_id = index
        index = index + 1
        points = np.column_stack((rrx,rry))
        paths[j%4].points.append(points)

    canvas = figure.canvas
    canvas.draw()
    width, height = canvas.get_width_height()
    image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape(height, width, 3)
    qimage = QImage(image.data, width, height, QImage.Format_RGB888)
    pixmap = QPixmap(qimage)
    paths[0].points = np.concatenate(paths[0].points)
    paths[1].points = np.concatenate(paths[1].points)
    paths[2].points = np.concatenate(paths[2].points)
    paths[3].points = np.concatenate(paths[3].points)
    return paths,pixmap

def draw_car_circle( robots,width,height,label,filename):

    img = plt.imread(filename)
    img_flipped = np.flipud(img)
    fig, ax = plt.subplots(figsize=(width/10,height/10))
    ax.imshow(img_flipped, extent=[0, width, 0, height])
    plt.gca().invert_yaxis()


    for i in range(0,4):
        if i % 4 ==0:
            plt.plot(robots[i].x, robots[i].y, "or")
        elif i % 4 == 1:
            plt.plot(robots[i].x, robots[i].y, "og")
        elif i % 4 == 2:
            plt.plot(robots[i].x, robots[i].y, "oy")
        elif i % 4 == 3:
            plt.plot(robots[i].x, robots[i].y, "oc")


    plt.axis('off')
    plt.savefig('plot_begin.png',bbox_inches='tight')
    canvas = fig.canvas

    pixmap = QPixmap('plot_begin.png')
    label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio))







'''robot1 = Robot(1, 20, 50)
robot2 = Robot(2, 40, 50)
robot3 = Robot(3, 80, 10)
robot4 = Robot(4, 100, 10)
robots = [robot1,robot2,robot3,robot4]

target1 = Target(1,1,69, 32, 73, 27)
target2 = Target(1,1 ,65, 20, 68, 16)
target3 = Target(1,1, 76 ,29, 80, 25)
target4 = Target(1,1 ,45, 20, 49, 15)
targets = [target1,target2,target3,target4]

obstacle1 = Obstacle(1,1, 17, 19, 23 ,14)
obstacle2 = Obstacle(1,1, 71, 21 ,87 ,14)
obstacle3 = Obstacle(1,1, 97, 45, 106 ,38)
obstacle4 = Obstacle(1,1, 2, 6 ,10, 0 )
obstacle5 = Obstacle(1,1, 38 ,45 ,55 ,38)
obstacle6 = Obstacle(1,1, 15, 32, 21, 26)

obstacles = [obstacle1,obstacle2,obstacle3,obstacle4,obstacle5,obstacle6]
draw_car_circle( robots,120,56)'''




