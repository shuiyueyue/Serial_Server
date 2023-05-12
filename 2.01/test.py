import math

x1, y1 = 0, 0  # 第一个坐标点
x2, y2 = 1,-111111111  # 第二个坐标点

dx, dy = x2 - x1, y2 - y1
rads = math.atan2(dy, dx)  # 计算方位角，以弧度返回
a = math.degrees(rads)
if a < 0:
    a = 360 + a
print(a)
rads = math.radians(a)
''''
if rads < 0:
    rads = 2*math.pi + rads
    '''
print(rads)