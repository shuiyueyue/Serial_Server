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



