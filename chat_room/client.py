
import socket
import threading
import os
os.system("")   # System call

class Style():
    white = '\033[37m'
    blue = '\033[34m'
    orange = '\033[33m'
    reset = '\033[0m'

#Broadcast

class ChatClient:
    def __init__(self, server_ip:str, server_port:int):
        self.server_socket_address = (server_ip, server_port)
        self.name = self.input_name().title()

    def input_name(self) -> str:
        return input(Style.reset+"please enter your name: ")
        
    def connect(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(self.server_socket_address)

    def disconnect(self):
        self.server_socket.close()
        
    def sending_loop(self):
        while True:
            message = input()
            if message.lower() == 'exit':
                self.server_socket.send(f"{self.name} left the room.".encode())
                self.disconnect()
                break
            else:
                self.server_socket.send(f"{self.name} >> {message}".encode())

    def receiving_loop(self):   
        while True:   
            data = self.server_socket.recv(1024).decode()
            if not data:
                break
            if ' >> ' in data:
                sender_name, message = data.split(' >> ')
                if sender_name == self.name :
                    print(Style.orange+f"me >> {message}"+Style.reset)
                else:
                    print(Style.blue+data+Style.reset)
            else:
                print(Style.white+data+Style.reset)

    def start(self):
        try:
            self.connect()
            self.server_socket.send(f"{self.name} entered the room.".encode())
            sending_loop = threading.Thread(target=self.sending_loop)
            sending_loop.start()
            self.receiving_loop()
            self.disconnect()
        except Exception:
            print("No connection!")

client = ChatClient("127.0.0.1", 58237)
client.start()
