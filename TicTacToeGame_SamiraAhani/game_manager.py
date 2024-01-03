import time
from game_logic import GameLogic


class GameManager:
    def __init__(self) -> None:
        self.game_logic = GameLogic()

    def run(self):
        while not self.game_logic.is_exited():
        #for i in range(50):
            try:
                self.game_logic.update()
            except Exception as e:
                print("game manager: ", e)

