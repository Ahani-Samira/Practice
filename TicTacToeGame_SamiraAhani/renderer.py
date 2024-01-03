import pygame
from game_board import GameBoard


class Color:
    white: tuple = (255, 255, 255)
    green: tuple = (0, 150, 0)
    red: tuple = (255, 0, 0)
    black: tuple = (0, 0, 0)
    blue: tuple = (0, 0, 255)
    gray: tuple = (100, 100, 100)


class Renderer:
    def __init__(self) -> None:
        window_width, window_height = 400, 450
        pygame.init()
        self.window = pygame.display.set_mode((window_width, window_height))
        self.game_board = GameBoard(self.window)
        self.player_name = None
        self.this_player = None
        self.other_player = None
        self.other_player_score = 0
        self.this_player_score = 0

    def set_player_names(self, names:list) -> None:
        self.this_player = self.player_name+"(you)"
        self.other_player = list(filter(lambda x: x != 'you', names))[0]
        
    def making_blank_board(self) -> None:
        pygame.display.set_caption("X O X")
        self.window.fill(Color.white)
        self.game_board.draw_table(Color.black)
        self.game_board.set_write((260, 35), self.other_player, Color.black)
        self.game_board.set_write((45, 35), self.this_player, Color.black)
        self.game_board.player_score_section((self.this_player_score, self.other_player_score), Color.black)
        self.update()

    def update(self) -> None:
        pygame.display.update()

    def pump(self) -> None:
        pygame.event.pump()

    def render(self, position:tuple, key:str, msg:str="") -> None:
        if key == 'x':
            self.game_board.draw_x(position, Color.red)
        elif key == 'o':
            self.game_board.draw_o(position, Color.blue)
        elif key == self.player_name:
            pass
        self.update()

    def show_message(self, msg:str) -> None:
        self.window.fill(Color.white)
        if "EQUAL" in msg:
            self.game_board.set_write((50, 200), "You are equal!", Color.gray, 72)
        elif "WIN" in msg:
            if "YOU" in msg:
                self.game_board.set_write((50, 200), msg[:-5].title(), Color.green, 72)
            else:
                self.game_board.set_write((50, 200), msg[:-5].title(), Color.red, 72)
        else:
            self.game_board.set_write((100, 200), msg.title(), Color.red, 72)
        self.update()
        pygame.time.delay(5000)

    def end_round(self, msg:str) -> None:
        pygame.display.set_caption(msg)
        self.update()
        pygame.time.delay(500)
        self.show_message(msg)
        self.making_blank_board()
