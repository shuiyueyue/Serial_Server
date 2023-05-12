import crcmod.predefined
import struct

class T_CRC:

    def __init__(self, data):
        self.data = data
        pass

    def tocrc(self):
        # 计算CRC32校验码
        crc32_func = crcmod.predefined.Crc("crc-32")
        crc32_func.update(self.data)
        crc32 = crc32_func.crcValue

        # 将CRC32校验码转换为字节序列
        crc32_bytes = struct.pack("<I", crc32)

        # 将图片数据和CRC32校验码合并成一个字节序列
        image_with_crc32 = self.data + crc32_bytes

        return image_with_crc32


if __name__ == '__main__':
    # 读取图片文件
    with open("images.jpg", "rb") as f:
        data = f.read()

    tt = T_CRC(data)
    #tt.data = data
    # 将合并后的数据写入新的文件
    with open("T_CRC.png", "wb") as f:
        f.write(tt.tocrc())

