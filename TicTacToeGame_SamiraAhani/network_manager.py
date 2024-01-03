import socket
import json
import time


class Server:
    def __init__(self, ip, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.number_of_clients = 2
        self.clients = []
        self.players = []
        self.turn = 0
        self.rounds = 0
        self.is_round_over = False
        self.acts = None

    def start(self) -> None:
        while len(self.clients) < self.number_of_clients:
            try:
                self.server_socket.listen()
                client = self.accept()
                self.clients.append(client)
                self.players.append(self.get_name(client[0]))
            except Exception as e:
                print("start: ", e)
        print("players: ", self.players)
        self.clients[0][0].sendall(f'["you", "{self.players[1]}"]'.encode())
        self.clients[1][0].sendall(f'["{self.players[0]}", "you"]'.encode())
        self.broadcast("OK".encode())

    def accept(self):
        conn, addr = self.server_socket.accept()
        print(f"client {addr} is connected")
        return conn, addr

    def get_name(self, conn):
        while True:
            data = conn.recv(1024).decode()
            if not data:
                pass
            else:
                return data

    def get_acts(self) -> list:
        try:
            for i in range(5):  # self.rounds < 5:
                for j in range(9):  # while not self.is_round_over:
                    self.send_message()
                    if self.turn % 2 == 0:
                        self.acts = self.client_handler(self.clients[0])
                    else:
                        self.acts = self.client_handler(self.clients[1])
                    if self.acts is not None and self.acts != []:
                        print(f"round: {self.rounds}, turn: {self.turn}")
                        return self.acts
                self.is_round_over = False
                self.rounds += 1
            self.finish()
        except Exception as e:
            print("get_acts: ", e)
            if "[WinError 10054]" in e:
                print("yes")
            else:
                print(type(e), "No0o0o000o0o0")
            return ["Action.QUIT"]

    def client_handler(self, conn: list):
        while True:
            data = conn[0].recv(1024)
            if not data:
                pass
            else:
                try:
                    acts = json.loads(data)
                    print("server recived: ", data.decode())
                    if acts is not None and acts != []:
                        return acts
                    #time.sleep(1)
                except Exception as e:
                    print("client handler: ", e)
                    self.broadcast(data)  # deleted this
                    #time.sleep(1)

    def broadcast(self, data: bytes) -> None:
        for client in self.clients:
            client[0].sendall(data)

    def send_message(self, msg="GO []") -> None:
        print("to send: ", msg)
        if "GO" in msg:
            if self.turn % 2 == 0:
                self.clients[0][0].sendall(msg.encode())
                self.clients[1][0].sendall(("NO "+msg[3:]).encode())
            else:
                self.clients[1][0].sendall(msg.encode())
                self.clients[0][0].sendall(("NO "+msg[3:]).encode())
            print(f"{self.turn = }")
            return
        elif "win" in msg:
            if self.turn % 2 == 1:
                self.clients[0][0].sendall(f"YOU are WIN!".encode())
                self.clients[1][0].sendall(f"{self.players[0]} is WIN!".encode())
            else:
                self.clients[1][0].sendall(f"YOU are WIN!".encode())
                self.clients[0][0].sendall(f"{self.players[1]} is WIN!".encode())
        else:
            self.broadcast(msg.encode())

    def send_data(self, data: list) -> None:
        json_data = json.dumps(data)
        print("send:",json_data)
        self.send_message("GO "+json_data)
        print("send:",json_data)

    def finish(self) -> None:
        for client in self.clients:
            c = client[0]
            c.close()
        self.server_socket.close()
