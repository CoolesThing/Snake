import pygame
from input_handler import InputHandler
from game_logic import GameLogic, Cell
from renderer import Renderer


pygame.init()
size = width, height = 588, 595
col = 19
row =17
cell_size = 31 # pixels

screen = pygame.display.set_mode(size, pygame.NOFRAME, depth = 0, display = 0, vsync = 0)
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

def main():
    cell = Cell()
    game_logic = GameLogic(row, col)
    input_handler = InputHandler()
    renderer = Renderer()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                raise SystemExit
        input_data = input_handler.get_input()
        game_logic.update(input_data)
        renderer.render(screen, cell.create_grid(row, col), cell_size)
        #do logic updates
        #render graphics

        pygame.display.flip()   #update the full display Surface to the screen
        clock.tick(60)          #wait until next frame(60fps)

if __name__ == "__main__":
    main()