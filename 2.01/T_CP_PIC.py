import struct
import serial
from CommunicationProtocol import CommunicationProtocol
from T_PIC import T_PIC


class SerialSender:
    def __init__(self, ser):
        self.ser = ser
        self.ser.set_buffer_size(tx_size=10000000)

    def send_image(self, image_path):
        # 读取图片文件
        with open(image_path, "rb") as f:
            image_data = f.read()
        print(len(image_data))

        # 封装图片数据
        t_pic = T_PIC(image_data)
        t_pic_data = t_pic.pack()

        # 构建协议数据包
        protocol = CommunicationProtocol(2, len(t_pic_data), t_pic_data)
        packet_data = protocol.pack()
        packet_length = struct.pack('!I', len(packet_data))
        packet = packet_length + packet_data

        # 发送数据包
        result = self.ser.write(packet)
        if result != len(packet):
            print("Error: Failed to send all data!")

    def close(self):
        self.ser.close()

if __name__ == "__main__":
    sender = SerialSender('COM4', 115200, 8192)
    sender.send_image("images.jpg")
    #sender.send_image("image.png")
    sender.close()
