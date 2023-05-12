import struct
import serial
from CommunicationProtocol import CommunicationProtocol
import pickle



class Point_Sender:
    def __init__(self, Serial):
        self.ser = Serial
        self.ser.set_buffer_size(tx_size=10000000)

        self.car_point = {'car_direction': 0,  'car_auto': 0 , 'play': 0}
        #direction: 0不改变状态，1前进，2后退，3左转，4右转，5停止
        #auto: 0不改变状态，1自动，2手动
    def send_point(self, direction, auto , play):


        self.car_point['car_direction'] = direction
        self.car_point['car_auto'] = auto
        self.car_point['play'] = play


        data = pickle.dumps(self.car_point)

        # 构建协议数据包
        protocol = CommunicationProtocol(1, len(data), data)
        packet_data = protocol.pack()
        packet_length = struct.pack('!I', len(packet_data))
        packet = packet_length + packet_data

        # 发送数据包
        result = self.ser.write(packet)
        if result != len(packet):
            print("Error: Failed to send all data!")
    def send_path(self,path):
        #print('send_path')
        #print(path)
        data = pickle.dumps(path)

        # 构建协议数据包
        protocol = CommunicationProtocol(4, len(data), data)
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
    ser = serial.Serial('COM2', 115200)
    sender = Point_Sender(ser)
    sender.send_point(1,1)
    #sender.send_info(3, 2, 3, 4, 5, 1)
    sender.close()
