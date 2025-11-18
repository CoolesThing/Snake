import pygame 

class Cell:
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.id = (grid_x, grid_y)
        
        self.apple = False
        self.snake = False
        self.empty = True
        self.wall = False
        
    def set_apple(self):
        self.apple = True
        self.snake = False
        self.empty = False
        self.wall = False
        
    def set_snake(self):
        self.apple = False
        self.snake = True
        self.empty = False
        self.wall = False
        
    def set_empty(self):
        self.apple = False
        self.snake = False
        self.empty = True
        self.wall = False
        
    def set_wall(self):
        self.apple = False
        self.snake = False
        self.empty = False
        self.wall = True
        
    @staticmethod
    def create_grid(rows, cols):
        grid = []
        for y in range(rows):
            row = []
            for x in range(cols):
                cell = Cell(x, y)
                # Set border cells as walls
                if x == 0 or y == 0 or x == cols - 1 or y == rows - 1:
                    cell.set_wall()
                row.append(cell)
            grid.append(row)
        return grid

class GameLogic:
    def get_relative_apple_position(self, normalize=False):
        """
        Returns (dx, dy) from snake head to apple.
        If normalize=True, values are scaled to [-1, 1] by grid size.
        """
        head_x, head_y = self.snake[0]
        apple_pos = None
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell.apple:
                    apple_pos = (x, y)
                    break
            if apple_pos:
                break
        if not apple_pos:
            return (0, 0)  # No apple present
        dx = apple_pos[0] - head_x
        dy = apple_pos[1] - head_y
        if normalize:
            dx = dx / (self.cols - 2)  # exclude walls
            dy = dy / (self.rows - 2)
        return (dx, dy)

    def get_immediate_danger(self):
        """
        Returns (danger_ahead, danger_left, danger_right) as 0/1.
        1 = danger (wall or snake), 0 = safe.
        """
        head = self.snake[0]
        direction = self.direction
        # Map directions to left/right turns
        left = (-direction[1], direction[0])
        right = (direction[1], -direction[0])
        checks = [direction, left, right]
        danger = []
        for vec in checks:
            nx, ny = head[0] + vec[0], head[1] + vec[1]
            if (0 <= ny < self.rows) and (0 <= nx < self.cols):
                cell = self.grid[ny][nx]
                if cell.wall or cell.snake:
                    danger.append(1)
                else:
                    danger.append(0)
            else:
                danger.append(1)  # Out of bounds = danger
        return tuple(danger)

    def get_direction(self, as_onehot=False):
        """
        Returns (dx, dy) or (up, down, left, right) as 0/1 if as_onehot=True.
        """
        dx, dy = self.direction
        if not as_onehot:
            return (dx, dy)
        # One-hot encoding: up, down, left, right
        up = int((dx, dy) == (0, -1))
        down = int((dx, dy) == (0, 1))
        left = int((dx, dy) == (-1, 0))
        right = int((dx, dy) == (1, 0))
        return (up, down, left, right)
    
    def __init__(self, rows, cols):
        self.grid = Cell.create_grid(rows, cols)
        self.rows = rows
        self.cols = cols
        self.snake = [(5, 8), (4, 8), (3, 8)]  # Initial snake position
        self.direction = (1, 0)  # Initial direction (right)
        self.last_action = None
        self.last_move_time = 0
        self.move_delay = 200  # milliseconds between moves (1000 ms / 5 moves per second)
        self.score = 0
        self.isalive = True
        pass
    
    def start_game(self, input_data, rows, cols):
        #enter the main game loop
        if any(input_data['keys']):
            self.isalive = True
            self.grid = Cell.create_grid(rows, cols)
            self.rows = rows
            self.cols = cols
            self.snake = [(5, 8), (4, 8), (3, 8)]  # Initial snake position
            self.direction = (1, 0)  # Initial direction (right)
            self.last_action = None
            self.last_move_time = 0
            self.move_delay = 200  # milliseconds between moves (1000 ms / 5 moves per second)
            self.score = 0
            return self.isalive
    
    def snake_state(self):
        return self.isalive

    def place_apple(self):
        import random
        empty_cells = [(x, y) for y in range(1, self.rows - 1) for x in range(1, self.cols - 1) if self.grid[y][x].empty]
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.grid[y][x].set_apple()
    
    def move_snake(self, snake, direction):
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1]) 
        
        x, y = new_head
        if self.grid[y][x].apple:
            new_snake = [new_head] + snake[:]
            self.score += 1
        elif self.grid[y][x].wall or self.grid[y][x].snake:
            #print("Game Over! Final Score:", self.score)
            self.isalive = False
            new_snake = snake[:]
        else:
            new_snake = [new_head] + snake[:-1]
            
        # sell all cell to snake=false
        for row in self.grid:
            for cell in row:
                if cell.snake:
                    cell.set_empty()
        
        for x, y in new_snake:
            self.grid[y][x].set_snake()
        
        return new_snake
        
    def update(self, input_data):
        # Process input_data and update game state
        keys = input_data['keys']
        mouse_pos = input_data['mouse_pos']
        mouse_buttons = input_data['mouse_buttons']
        current_time = pygame.time.get_ticks()
        
        # Exit the game if ESC is pressed
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
            raise SystemExit   
        
        # spwan apple if there is none
        if not any(cell.apple for row in self.grid for cell in row):
            self.place_apple()
        
        if keys[pygame.K_a]:
            if(self.last_action != (1, 0)): #prevent the snake from going back on itself
                self.direction = (-1, 0)  # Move left
        if keys[pygame.K_d]:
            if(self.last_action != (-1, 0)): #prevent the snake from going back on itself
                self.direction = (1, 0)   # Move right
        if keys[pygame.K_w]:
            if(self.last_action != (0, 1)): #prevent the snake from going back on itself
                self.direction = (0, -1)  # Move up
        if keys[pygame.K_s]:
            if(self.last_action != (0, -1)): #prevent the snake from going back on itself
                self.direction = (0, 1)   # Move down     
        
        self.snake = self.move_snake(self.snake, self.direction)
        self.last_action = self.direction
        