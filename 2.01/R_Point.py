import serial
import struct
import pickle
import time
from CommunicationProtocol import CommunicationProtocol


class Point_Receiver:
    def __init__(self, port, baudrate=115200, rx_size=128000):
        self.ser = serial.Serial(port, baudrate)
        self.ser.set_buffer_size(rx_size=rx_size)

    def receive_point(self):
      while True:
       if self.ser.in_waiting > 0:
        # 读取数据包长度
        length_bytes = self.ser.read(4)
        packet_length = struct.unpack('!I', length_bytes)[0]

        # 读取数据包
        packet_data = self.ser.read(packet_length)

        # 解析协议数据包
        pure_data = CommunicationProtocol.unpack(packet_data)
        pure_data1 = pure_data.data[0]
        print(pure_data.message_type)

        # 反序列化数据
        car_point = pickle.loads(pure_data1)

        return car_point
       else:
        # 没有数据可读，等待一段时间
        time.sleep(0.1)

    def close(self):
        self.ser.close()


if __name__ == "__main__":
    while True:
     receiver = Point_Receiver('COM2')
     car_point = receiver.receive_point()
     print(car_point)
     receiver.close()
