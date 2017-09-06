import socket

class Communicate(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message):
        self.socket.sendto(str.encode(message), (self.ip, self.port))
