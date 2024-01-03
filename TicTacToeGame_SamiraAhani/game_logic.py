from network_manager import Server
from actions import Action


class GameLogic:
    def __init__(self) -> None:
        self.quit = False
        self.server = Server("127.0.0.1", 58237)
        self.server.start()
        self.map: list = self.map_initialization()
        self.map_position = None
        self.key = False
        self.game_turn = 0  # TODO: method...
        self.players: list = []
        self.rounds = 0
        self.win_counter = 0

    def map_initialization(self) -> list:
        return [[False, False, False], [False, False, False], [False, False, False]]        

    def add_player(self, player):
        self.players.append(player)

    def update(self) -> None:
        #self.server.send_message(f"message: turn {self.game_turn % 2}")
        acts = self.server.get_acts()
        ans = self.parse_actions(acts)
        print(f"{ans = }")
        if ans:
            self.server.turn = self.game_turn
            print("in ans")
            msg = ans[0]
            ls = list(ans[1])
            ls.append(self.key)
            if msg == "continue...":
                self.server.send_data(ls)
            elif msg == "win":
                self.server.send_data(ls)
                self.server.send_message(msg)
                if self.win_counter >= 5:
                    self.quit = True
            elif msg == "equal":
                self.server.send_data(ls)
                self.server.send_message("EQUAL")
            #self.server.turn = self.game_turn

    def parse_actions(self, acts: list):
        if acts is not None and acts != []:
            for a in acts:
                print(f"{a} -> {eval(a)}")
                if eval(a) == Action.QUIT:
                    print("Exited")
                    self.quit = True
                    return False
                else:
                    a = str(a)
                    x, y = int(a[9]), int(a[8])
                    print("turn: ", self.game_turn)
                    if self.game_turn % 2 == 0:
                        msg = self.handle('x', (x, y))
                        print(f"{msg = }")
                        if msg:
                            print("in msg")
                            return msg, self.map_position
                    else:
                        msg = self.handle('o', (x, y))
                        print(f"{msg = }")
                        if msg:
                            print("in msg")
                            return msg, self.map_position
        return False

    def is_empty(self, position):
        x, y = position
        return not (self.map[x][y])

    def is_equal(self, key, ls):
        print(key, ls)
        for item in ls:
            print(f"{item=}")
            if item != key:
                return False
        return True

    def is_win(self, key, position):
        x, y = position
        if self.is_equal(key, [cell for i, row in enumerate(self.map) for j, cell in enumerate(row) if i == x]):
            print("x==")
            return True
        if self.is_equal(key, [cell for i, row in enumerate(self.map) for j, cell in enumerate(row) if j == y]):
            print("y==")
            return True
        if x == y:
            if self.is_equal(key, [cell for i, row in enumerate(self.map) for j, cell in enumerate(row) if i == j]):
                print("x,y ===")
                return True
        if x+y == len(self.map)-1:
            if self.is_equal(key, [cell for i, row in enumerate(self.map) for j, cell in enumerate(row) if i+j == len(self.map)-1]):
                print("x+y ==")
                return True
        print("!=")
        return False

    def is_board_full(self):
        print("check for full")
        for row in self.map:
            for cell in row:
                if not cell:
                    return False
        return True

    def handle(self, key, position):
        x, y = position
        print(f"befor: {self.key = }")
        self.key = key
        print(f"after: {self.key = }")
        self.map_position = y, x
        print(f"{self.map_position = }")
        if self.is_empty(self.map_position):
            print("befor: ", self.map[y][x])
            self.map[y][x] = key
            print("after: ", self.map[y][x])
            print(self.map)
            self.game_turn += 1
            return self.check()
        else:
            return False
        
    def check(self):
        msg = "continue..."
        if self.map_position:
            if self.is_win(self.key, self.map_position):
                self.win_counter += 1
                msg = "win"
                self.map = self.map_initialization()
            elif self.is_board_full():
                msg = "equal"
                self.map = self.map_initialization()
        print(msg)
        return msg

    def is_exited(self):
        return self.quit
