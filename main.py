import pygame
from snake import Game
import neat
import os
import pickle

class SnakeGame:
    def __init__(self, screen, width, height):
        self.game = Game(screen, width, height)
        self.game_logic = self.game.game_logic
    
    def get_direction_keys_from_action(self, action):
        """
        Convert relative action (0=left, 1=straight, 2=right) to absolute direction keys.
        Uses current snake direction to compute the new direction.
        Returns keys tuple with the appropriate movement key set to True.
        """
        # Current direction of snake
        dx, dy = self.game_logic.direction
        
        # Map current direction to left/right turns
        if (dx, dy) == (1, 0):  # moving right
            if action == 0:  # turn left
                new_dir = (0, -1)  # up
            elif action == 1:  # straight
                new_dir = (1, 0)  # right
            else:  # turn right
                new_dir = (0, 1)  # down
        elif (dx, dy) == (-1, 0):  # moving left
            if action == 0:  # turn left
                new_dir = (0, 1)  # down
            elif action == 1:  # straight
                new_dir = (-1, 0)  # left
            else:  # turn right
                new_dir = (0, -1)  # up
        elif (dx, dy) == (0, -1):  # moving up
            if action == 0:  # turn left
                new_dir = (-1, 0)  # left
            elif action == 1:  # straight
                new_dir = (0, -1)  # up
            else:  # turn right
                new_dir = (1, 0)  # right
        elif (dx, dy) == (0, 1):  # moving down
            if action == 0:  # turn left
                new_dir = (1, 0)  # right
            elif action == 1:  # straight
                new_dir = (0, 1)  # down
            else:  # turn right
                new_dir = (-1, 0)  # left
        else:
            new_dir = (1, 0)  # default to right
        
        # Convert direction to key
        # Create a tuple large enough for pygame key indices (pygame.K_ESCAPE = 27, pygame.K_z = 122, etc.)
        keys_dict = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False}
        if new_dir == (1, 0):
            keys_dict[pygame.K_d] = True
        elif new_dir == (-1, 0):
            keys_dict[pygame.K_a] = True
        elif new_dir == (0, -1):
            keys_dict[pygame.K_w] = True
        elif new_dir == (0, 1):
            keys_dict[pygame.K_s] = True
        
        # Convert dict to tuple for game_logic.update() which expects keys to be indexable by key code
        keys_tuple = [False] * 512  # Large enough for all pygame key codes
        for key_code, pressed in keys_dict.items():
            keys_tuple[key_code] = pressed
        
        return tuple(keys_tuple)
        
    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(1)  # Limit to 60 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                
            inputs = (
                list(self.game_logic.get_direction(as_onehot=False)) +
                list(self.game_logic.get_immediate_danger()) +
                list(self.game_logic.get_relative_apple_position(normalize=True))
            )
            print(inputs)
            
            # Get neural network output (3 values: left, straight, right)
            output = net.activate(inputs)
            
            # Decide movement: pick argmax of 3 actions (left=0, straight=1, right=2)
            action = output.index(max(output)) if len(output) >= 3 else 1
            
            # Convert relative action to keys using current direction
            keys = self.get_direction_keys_from_action(action)
            
            # Create proper input_data dictionary for game_logic.update()
            input_data = {
                'keys': keys,
                'mouse_pos': (0, 0),
                'mouse_buttons': (False, False, False)
            }
            
            self.game_logic.update(input_data)

            # Render and display
            from snake.snake import CELL_SIZE
            self.game.renderer.render(self.game.screen, self.game_logic.grid, CELL_SIZE)
            pygame.display.update()      
        pygame.quit() 
        
    def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        
        run = True
        steps = 0
        steps_since_apple = 0
        max_steps_without_apple = 30  # Stop if no apple eaten in this many steps
        min_distance_to_apple = float('inf')  # Track closest approach to apple
        
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            
            # Gather inputs for the neural network
            inputs = (
                list(self.game_logic.get_direction(as_onehot= False)) +
                list(self.game_logic.get_immediate_danger()) +
                list(self.game_logic.get_relative_apple_position(normalize=True))
            )
            
            # Get neural network output (3 values: left, straight, right)
            output = net.activate(inputs)
            
            # Decide movement: pick argmax of 3 actions (left=0, straight=1, right=2)
            action = output.index(max(output)) if len(output) >= 3 else 1
            
            # Convert relative action to keys using current direction
            keys = self.get_direction_keys_from_action(action)
            
            # Create proper input_data dictionary for game_logic.update()
            input_data = {
                'keys': keys,
                'mouse_pos': (0, 0),
                'mouse_buttons': (False, False, False)
            }
            
            # Track score before update to detect apple eating
            score_before = self.game_logic.score
            
            # Update game logic with the constructed input
            self.game_logic.update(input_data)
            
            # Track distance to apple for proximity bonus
            dx, dy = self.game_logic.get_relative_apple_position(normalize=False)
            distance_to_apple = abs(dx) + abs(dy)  # Manhattan distance
            if distance_to_apple < min_distance_to_apple:
                min_distance_to_apple = distance_to_apple
            
            # Check if an apple was eaten
            if self.game_logic.score > score_before:
                steps_since_apple = 0  # Reset counter
                min_distance_to_apple = float('inf')  # Reset for next apple
            else:
                steps_since_apple += 1
            
            # Render the game
            from snake.snake import CELL_SIZE
            self.game.renderer.render(self.game.screen, self.game_logic.grid, CELL_SIZE)
            pygame.display.update()
            
            steps += 1
            
            # Check if game is over (death or timeout without eating)
            if not self.game_logic.isalive:
                self.calc_fitness(genome, self.game_logic.score, steps, min_distance_to_apple)
                break
            elif steps_since_apple > max_steps_without_apple:
                # Timeout: snake hasn't eaten in too long, likely spinning
                self.calc_fitness(genome, self.game_logic.score, steps, min_distance_to_apple)
                break
            
    def calc_fitness(self, genome, score, steps, min_distance_to_apple=float('inf')):
        """
        Calculate fitness based on score, efficiency, and proximity to apple.
        Rewards high score, low step count, and getting close to the apple.
        """
        fitness = score * 200
        #fitness += steps * 1.5
        
        # Proximity bonus: reward for getting close to the apple
        # Inverse of distance encourages approach behavior
        if min_distance_to_apple != float('inf'):
            # Grid is ~17x19, so max distance is ~36
            # Convert distance to a bonus: closer = higher bonus
            proximity_bonus = 100 / (1 + min_distance_to_apple)
            fitness += proximity_bonus
        
        if score == 0:
            fitness -= 100
  
        genome.fitness = fitness
        
def eval_genomes(genomes, config):
    width, height = 588, 595
    screen = pygame.display.set_mode((width, height))
    
    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0  # Initialize fitness
        game = SnakeGame(screen, width, height)
        game.train_ai(genome, config)
        
def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-114') # to resume from a checkpoint
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))
    
    winner = p.run(eval_genomes, 50)
    
    with open('best_genome.pkl', 'wb') as f:
        pickle.dump(winner, f)
    
def test_ai(config):
    width, height = 588, 595
    screen = pygame.display.set_mode((width, height))
    with open('best_genome.pkl', 'rb') as f:
        winner = pickle.load(f)
        
    game = SnakeGame(screen, width, height)
    game.test_ai(winner, config)        
        
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run_neat(config)
    test_ai(config)
    
    




