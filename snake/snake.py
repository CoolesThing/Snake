import pygame
from .input_handler import InputHandler
from .game_logic import GameLogic, Cell
from .renderer import Renderer
from .evo_comp import Bot
pygame.init()

class GameInformation:
    def __init__(self, score, is_alive=True):
        self.score = score
        self.is_alive = is_alive



SIZE = width, height = 588, 595
COL = 19
ROW =17
CELL_SIZE = 31 # pixels
    
class Game:
    def __init__(self, screen, width, height):
        self.width = width
        self.height = height
        self.input_handler = InputHandler()
        self.game_logic = GameLogic(ROW, COL)
        self.renderer = Renderer()
        self.bot = Bot()

        self.screen = screen
        
    def loop(self):
        #executes one iteration of the game loop
        #returns GameInformation object containing score
        # collect input then update game logic
        input_data = self.input_handler.get_input()
        self.game_logic.update(input_data)
        self.renderer.render(self.screen, self.game_logic.grid, CELL_SIZE)
        
        game_info = GameInformation(self.game_logic.score)
        
        return game_info

    def run(self):
        """Full game runner: handles start, main, and end screens (blocking)."""
        clock = pygame.time.Clock()
        alive = False

        while True:
            # Start screen loop
            while not alive:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                input_data = self.input_handler.get_input()
                alive = self.game_logic.start_game(input_data, ROW, COL)
                self.renderer.render(self.screen, self.game_logic.grid, CELL_SIZE)
                self.renderer.render_start_screen(self.screen)
                pygame.display.flip()
                clock.tick(60)

            # Main game loop
            while alive:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                # Bot will handle toggle key and either supply AI input or pass-through real keys
                input_data = self.bot.get_input(self.game_logic)
                self.game_logic.update(input_data)
                alive = self.game_logic.snake_state()
                self.renderer.render(self.screen, self.game_logic.grid, CELL_SIZE)
                pygame.display.flip()
                clock.tick(60)

            # End game screen loop
            while not alive:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                input_data = self.input_handler.get_input()
                alive = self.game_logic.start_game(input_data, ROW, COL)
                self.renderer.render(self.screen, self.game_logic.grid, CELL_SIZE)
                self.renderer.render_end_screen(self.screen)
                pygame.display.flip()
                clock.tick(60)

if __name__ == "__main__":
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Snake Game")
    game = Game(screen, width, height)
    game.run()