import crcmod.predefined
import struct

class R_CRC:
    def __init__(self, data):
        self.data = data
        pass

    def crcto(self):
        # 分离出数据和CRC32校验码
        pure_data = self.data[:-4]
        crc32_bytes = self.data[-4:]

        crc32_func = crcmod.predefined.Crc("crc-32")
        crc32_func.update(pure_data)
        crc32 = crc32_func.crcValue

        # 将CRC32校验码转换为字节序列
        crc32_bytes_calculated = struct.pack("<I", crc32)

        # 验证CRC32校验码是否正确
        if crc32_bytes != crc32_bytes_calculated:
            print("CRC32校验失败！")
            return pure_data

        else:
            return pure_data

if __name__ == '__main__':
    # 读取带有CRC32校验码的文件
    with open("T_PIC.png", "rb") as f:
        data = f.read()

    tt = R_CRC(data)
    #tt.data = data
    #tt.R_CRC()
    #将图片数据写入新文件
    with open('R_CRC.jpg', "wb") as f:
        f.write(tt.crcto())


