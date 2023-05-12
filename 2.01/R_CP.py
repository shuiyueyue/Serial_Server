import serial
import struct
import pickle
import time
from CommunicationProtocol import CommunicationProtocol


class InfoReceiver:
    def __init__(self, port, baudrate=115200, rx_size=128000):
        self.ser = serial.Serial(port, baudrate)
        self.ser.set_buffer_size(rx_size=rx_size)

    def receive_info(self):
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
        car_info = pickle.loads(pure_data1)

        return car_info
       else:
        # 没有数据可读，等待一段时间
        time.sleep(0.1)

    def close(self):
        self.ser.close()


if __name__ == "__main__":
    receiver = InfoReceiver('COM1')
    car_info = receiver.receive_info()
    print(car_info)
    receiver.close()
