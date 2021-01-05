import socket

class UDPSocketServer:
    def __init__(self, app_logger):
        self.PORT = 21037
        self.HOST = "0.0.0.0"
        self.BUFFER_SIZE = 1280
        self.app_logger = app_logger
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.app_logger.info("start binding")
        self.server_socket.bind((self.HOST, self.PORT))
        self.app_logger.info("server is listening on port "+str(self.PORT))
    
    def recv(self):
        message, address = self.server_socket.recvfrom(self.BUFFER_SIZE)
        return message, address

    def send(self, message, address):
        self.server_socket.sendto(message, address)



