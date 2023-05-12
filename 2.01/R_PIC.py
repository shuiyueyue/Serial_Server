from R_CRC import R_CRC

class R_PIC:

    def __init__(self,image,name):
        self.image = image
        self.name = name

        pass


    def unpack(self):

        # 分离出数据和CRC32校验码
        image_data = R_CRC(self.image).crcto()
        return image_data



if __name__ == '__main__':
    # 读取带有CRC32校验码的文件
    with open("T_PIC.png", "rb") as f:
        data = f.read()

    tt = R_PIC(data,'R_PIC.png')
    #tt.image = data
    #tt.name = 'R_PIC.jpg'
    #tt.P_unpack()
    #将图片数据写入新文件
    with open(tt.name, "wb") as f:
        f.write(tt.unpack())

