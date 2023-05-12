from T_CRC import T_CRC

class T_PIC:

    def __init__(self, image):
        self.image = image

        pass

    def pack(self):

        image_with_crc32 = T_CRC(self.image).tocrc()

        return image_with_crc32


if __name__ == '__main__':
    # 读取图片文件
    with open("images.jpg", "rb") as f:
        data = f.read()

    tt = T_PIC(data)
    #tt.data = data
    # 将合并后的数据写入新的文件
    with open("T_PIC.png", "wb") as f:
        f.write(tt.pack())
