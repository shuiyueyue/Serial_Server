import struct
import serial
from CommunicationProtocol import CommunicationProtocol
from R_PIC import R_PIC

import pickle


class R_CP_PIC:
    def __init__(self, serial,name):
        self.ser = serial
        self.name = name
        #self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.ser.set_buffer_size(rx_size=262144)

    def receive(self):
        #while True:
            if self.ser.in_waiting > 0:


                # 接收数据长度字段
                data_length_bytes = self.ser.read(4)
                data_length = struct.unpack('!I', data_length_bytes)[0]
                #print(data_length)
                # 如果数据长度为0，说明接收到的是空数据，直接返回空的bytearray
                if data_length == 0:
                    return None

                data = self.ser.read(data_length)
                # self.ser.flushInput()
                pure_data = CommunicationProtocol.unpack(data)
                pure_data1 = pure_data.data[0]
                #print(pure_data.message_type)

                if pure_data.message_type == 1:
                    da = pure_data.data
                    #print('R_CP_PIC:',da)
                    from datetime import datetime

                    now = datetime.now()
                    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    #print("rcp Time =", current_time)
                    return pure_data
                elif pure_data.message_type == 2:
                    p1 = R_PIC(pure_data1, self.name)
                    with open(self.name, "wb") as f:
                        f.write(p1.unpack())
                    return pure_data
                elif pure_data.message_type == 3:
                    # 反序列化数据
                    car_info = pickle.loads(pure_data1)
                    #print('R_CP_PIC:', car_info)
                    return pure_data
                elif pure_data.message_type == 4:
                    return pure_data


    #else:
             #没有数据可读，等待一段时间
            #time.sleep(0.1)

    def close(self):
        self.ser.close()


if __name__ == "__main__":
    ser = serial.Serial('com5', 115200, timeout=0.1)
    receiver = R_CP_PIC(ser,'R_PIC.jpg')
    receiver.receive()
    receiver.close()
