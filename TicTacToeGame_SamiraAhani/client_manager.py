import socket
import json
import time
from input_handler import InputHandler
from renderer import Renderer


class Client:
    def __init__(self, server_ip: str, server_port: int):
        self.server_socket_address = (server_ip, server_port)
        self.client_socket = None
        self.name = self.input_name().title()
        self.players = None
        self.input_handler = InputHandler()
        self.renderer = None
        self.is_allowed = False

    def input_name(self) -> str:
        name = input("please enter your name: ")
        while len(name) < 3:
            name = input("This is too short, please re-enter: ")
        return name

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_socket_address)

    def disconnect(self):
        self.client_socket.close()

    def send_data(self):
        while True:
            try:
                acts = self.input_handler.take_input()
                self.renderer.update()
                #print("acts: ", acts)
                if acts == []:
                    pass
                    #time.sleep(0.5)
                    #self.send_data()
                    #return
                else:
                    print("acts: ", acts)
                    json_data = json.dumps(acts)
                    self.client_socket.sendall(json_data.encode())
                    print(f"{acts =} to {json_data =} sending to server")
                    self.is_allowed = False
                    self.receive()
                    break
            except Exception as e:
                print("send_data: ", e)

    def message_analysis(self, msg):
        if "GO" in msg:
            print(msg)
            self.renderer.game_board.specify_turn("you", (0, 200, 0))
            self.renderer.update()
            self.is_allowed = True
           # self.send_data()
        elif "NO" in msg:
            print(msg)
            self.renderer.game_board.specify_turn("wait", (0, 200, 0))
        self.renderer.update()
        if "EQUAL" in msg:
            print(msg)
            self.renderer.end_round(msg)
        elif "WIN" in msg:
            if "YOU" in msg:
                self.renderer.this_player_score += 1
            else:
                self.renderer.other_player_score += 1
            self.renderer.end_round(msg)

    def receive(self):
        while True:
            self.renderer.pump()
            data = self.client_socket.recv(1024).decode()
            print("receive: ",data)
            if not data:
                print("not data received")
                return
            elif "GO" in data or "NO" in data:
                self.message_analysis(data)
                try:
                    new_data = json.loads(data[3:])  # [-1]
                    print(f"{new_data = }")
                    if new_data != []:
                        position = new_data[0], new_data[1]
                        key = new_data[2]
                        print("type data:", type(new_data))
                        self.renderer.render(position, key)
                        if "WIN" in data or "EQUAL" in data:
                            self.message_analysis(data)
                    if "GO" in data:
                        self.send_data()
                except Exception as e:
                    print("receiv_data 2: ", e)
            if "message:" in data:
                self.message_analysis(data[9:])
                if self.is_allowed:
                   break 
            #time.sleep(1)

    def run_game(self):
        while True:
            self.renderer.pump()
            try:
                if not self.is_allowed:
                    print("go to reseive")
                    self.receive()
                else:
                    print("go to send")
                    self.send_data()
            except Exception as e:
                print("run_game: ", e)

    def get_ok_from_server(self):
        while True:
            data = self.client_socket.recv(1024).decode()
            if "you" in data:
                self.players = json.loads(data)
                print(self.players)
            if data == "OK":
                return True

    def start(self):
        print("please wait ...")
        try:
            self.connect()
            print("connected to server")
        except Exception as e:
            # print("start: No connection!")
            print("start: ", e)
        self.client_socket.send(f"{self.name}".encode())
        run = self.get_ok_from_server()
        if run:
            self.renderer = Renderer()
            self.renderer.player_name = self.name
            self.renderer.set_player_names(self.players)
            self.renderer.making_blank_board()
            self.run_game()
        self.disconnect()
