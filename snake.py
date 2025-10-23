import pygame
from input_handler import InputHandler
from game_logic import GameLogic, Cell
from renderer import Renderer
from evo_comp import Bot


pygame.init()
size = width, height = 588, 595
col = 19
row =17
cell_size = 31 # pixels

screen = pygame.display.set_mode(size, pygame.NOFRAME, depth = 0, display = 0, vsync = 0)
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

def main():
    game_logic = GameLogic(row, col)
    input_handler = InputHandler()
    renderer = Renderer()
    bot = Bot()
    alive = False
    
    while True:
        #start screen loop 
        while not alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    raise SystemExit
            input_data = input_handler.get_input()
            #game_logic.update(input_data)#do logic updates Here we can do bot logic while waiting for user to start
            alive = game_logic.start_game(input_data, row, col)
            renderer.render(screen, game_logic.grid, cell_size)#render graphics
            renderer.render_start_screen(screen)
            pygame.display.flip()   #update the full display Surface to the screen
            clock.tick(60)          #wait until next frame(60fps)
        
        #main game loop   
        while alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    raise SystemExit 
            input_data = bot.get_input(game_logic)#input_handler.get_input()
            game_logic.update(input_data)#do logic updates
            alive = game_logic.snake_state()#check if game over
            renderer.render(screen, game_logic.grid, cell_size)#render graphics
            pygame.display.flip()   #update the full display Surface to the screen
            clock.tick(60)          #wait until next frame(60fps)
            
        #end game screen loop 
        while not alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    raise SystemExit
            input_data = input_handler.get_input()
            #game_logic.update(input_data)#do logic updates Here we can do bot logic while waiting for user to start
            alive = game_logic.start_game(input_data, row, col)
            renderer.render(screen, game_logic.grid, cell_size)#render graphics
            renderer.render_end_screen(screen)
            pygame.display.flip()   #update the full display Surface to the screen
            clock.tick(60)          #wait until next frame(60fps)


if __name__ == "__main__":
    main()