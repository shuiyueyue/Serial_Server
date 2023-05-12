#img1即为识别图像 shape数组为图像的像素长宽
#shape=img1.shape

class Obstacle:
    def __init__(self,id,cls, x, y, w, h):
        self.id = id
        self.cls = cls
        self.x1 = int((x-w/2)*shape[0])#左上x
        self.x2 = int((x+w/2)*shape[0])#左上y
        self.y2 = int((y-w/2)*shape[1])#右上x
        self.x2 = int((y+w/2)*shape[1])#右上y

    def getId(self):
        return self.id

    def getX1(self):
        return self.x1

    def getX2(self):
        return self.x2

    def getY1(self):
        return self.y1

    def getY2(self):
        return self.y2

    def getCls(self):
        return self.cls


class Target:
    def __init__(self,id,cls, x, y, w, h):
        self.id = id
        self.cls = cls
        self.x1 = int((x-w/2)*shape[0])#左上x
        self.x2 = int((x+w/2)*shape[0])#左上y
        self.y2 = int((y-w/2)*shape[1])#右上x
        self.x2 = int((y+w/2)*shape[1])#右上y

    def getId(self):
        return self.id

    def getX1(self):
        return self.x1

    def getX2(self):
        return self.x2

    def getY1(self):
        return self.y1

    def getY2(self):
        return self.y2

    def getCls(self):
        return self.cls




