import pygame

class InputHandler:
    def __init__(self):
        pass

    def get_input(self):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        return {
            'keys': keys,
            'mouse_pos': mouse_pos,
            'mouse_buttons': mouse_buttons
        }

