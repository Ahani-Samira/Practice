import socket
import threading

# Chat Server
# Broadcast every message to others.
# S ---- c1
# S ---- c2
class ChatServer:
    def __init__(self, ip:str, port:int):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()
        self.clients = []

    def accept(self):
        conn, addr = self.server_socket.accept()
        print(f"client {addr} is connected")
        return conn
    
    def clientHandler(self, conn:socket):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data.decode())
            # DO SOME OTHER STUFF HERE
            self.broadcast(data)

    def broadcast(self, data:bytes)->None:
        for client in self.clients:
            client.send(data)

    def start(self)->None:
        while True:
            client = self.accept()
            self.clients.append(client)
            clientHandlerThead =threading.Thread(target=self.clientHandler, args=(client,))
            clientHandlerThead.start()

server = ChatServer("127.0.0.1", 58237)
server.start()
