import pygame


class GameBoard:
    def __init__(self, screen) -> None:
        self.screen = screen

    def specify_turn(self, name:str, color:tuple) -> None:
        if 'you' in name:
            pygame.draw.polygon(self.screen, color, [(136, 8), (148, 8), (142, 18)])
            pygame.draw.polygon(self.screen, (255 ,255, 255), [(252, 8), (264, 8), (258, 18)])
        else:
            pygame.draw.polygon(self.screen, color, [(252, 8), (264, 8), (258, 18)])
            pygame.draw.polygon(self.screen, (255 ,255, 255), [(136, 8), (148, 8), (142, 18)])

    def set_write(self, position:tuple, text:str, color:tuple=(0, 0, 0), size:int=32) -> None:
        font = pygame. font. SysFont(None, size)
        img = font.render(text, True, color)
        self.screen.blit(img, position)

    def player_score_section(self, scores:tuple, color:tuple) -> None:
        this_player_score, other_player_score = scores
        pygame.draw.rect(self.screen, color, (149, 20, 50, 50), 2)
        self.set_write((164,35), str(this_player_score))
        pygame.draw.rect(self.screen, color, (201, 20, 50, 50), 2)
        self.set_write((216,35), str(other_player_score))

    def draw_table(self, color:tuple) -> None:
        # Horizontal lines:
        pygame.draw.line(self.screen, color, (50, 200), (350, 200), 5)
        pygame.draw.line(self.screen, color, (50, 300), (350, 300), 5)
        # Vertical lines:
        pygame.draw.line(self.screen, color, (150, 100), (150, 400), 5)
        pygame.draw.line(self.screen, color, (250, 100), (250, 400), 5)

    def set_position(self, position:tuple) -> tuple:
        x, y = position
        position = y*100+50, x*100+100
        return position
        
    def draw_x(self, position:tuple, color:tuple) -> None:
        x, y = self.set_position(position)
        pygame.draw.line(self.screen, color, (x+20, y+20), (x+80, y+80), 10)
        pygame.draw.line(self.screen, color, (x+80, y+20), (x+20, y+80), 10)

    def draw_o(self, position:tuple, color:tuple) -> None:
        x, y = self.set_position(position)
        position = x+50, y+50
        pygame.draw.circle(self.screen, color, position, 30, 6)

