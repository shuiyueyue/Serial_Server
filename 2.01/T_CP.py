import struct
import serial
from PyQt5.QtCore import QBuffer

from PyQt5.QtGui import QImage

from CommunicationProtocol import CommunicationProtocol
import pickle
from T_PIC import T_PIC



class info_Sender:
    def __init__(self, ser):
        self.ser = ser
        if self.ser is not None:
            self.ser.set_buffer_size(tx_size=10000000)

        self.car_info = {'car_id': 0, 'car_x': 0, 'car_y': 0, 'car_cor': 0, 'car_speed': 0, 'car_status': 0 , 'pic': None}

    def send_info(self, id, x, y, cor, speed, status ):


        self.car_info['car_id'] = id
        self.car_info['car_x'] = x
        self.car_info['car_y'] = y
        self.car_info['car_cor'] = cor
        self.car_info['car_speed'] = speed
        self.car_info['car_status'] = status
        #self.car_info['pic'] = pic
        #QImage.fromImage(pic).save('4.png')
        #print('pic',pic)


        data = pickle.dumps(self.car_info)

        # 构建协议数据包
        protocol = CommunicationProtocol(3, len(data), data)
        packet_data = protocol.pack()
        packet_length = struct.pack('!I', len(packet_data))
        packet = packet_length + packet_data
        if self.ser is not None:
            # 发送数据包
            result = self.ser.write(packet)
            if result != len(packet):
                print("Error: Failed to send all data!")



    def send_image(self, image_path):
        # 读取图片文件
        with open(image_path, "rb") as f:
            image_data = f.read()
        #print(len(image_data))

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
    sender = info_Sender('COM2')
    #sender.send_image("images.jpg")
    sender.send_info(3, 2.6, 3.9, 4.8, 87, 0)
    sender.close()
