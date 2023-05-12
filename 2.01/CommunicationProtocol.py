import struct
'''
在这个通信协议类中，我们使用了struct模块来打包和解包二进制数据。
在类的初始化方法中，我们传入了消息类型和数据作为类的属性。
在pack()方法中，我们使用了struct.pack()函数将消息类型、数据长度和数据打包成二进制数据并返回。
在unpack()方法中，我们使用了struct.unpack()函数将二进制数据解包并返回一个新的CommunicationProtocol对象。
'''
class CommunicationProtocol:
    def __init__(self,message_type,data_length ,data):

        self.message_type = message_type # 1为指令，2为图片，3为状态,4为路径
        self.data_length = data_length
        self.data = data

    def pack(self):
        #data_length = len(self.data)
        packed_data = struct.pack("!BII{}s".format(self.data_length), 0x01, self.message_type, self.data_length, self.data)
        return packed_data

    @classmethod
    def unpack(cls, packed_data):
        unpacked_data = struct.unpack("!BII{}s".format(len(packed_data) - 9), packed_data)
        message_type = unpacked_data[1]
        data_length = unpacked_data[2]
        data = unpacked_data[3:]
        return cls(message_type,data_length,data)
