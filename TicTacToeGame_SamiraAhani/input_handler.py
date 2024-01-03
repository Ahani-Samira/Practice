import pygame


class InputHandler:
    def __init__(self) -> None:
        pass

    def take_input(self):
        acts = []
        #pygame.time.delay(50)  # new
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                acts.append("Action.QUIT")
        mouse_position = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        x, y = mouse_position
        j = (x-50) // 100
        i = (y // 100) - 1
        if click[0] and (2 >= i >= 0) and (2 >= j >= 0):
            b = f"Action.B{i}{j}"
            acts.append(b)
        return acts
