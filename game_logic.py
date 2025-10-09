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
        pass
    
    def place_apple(self):
        import random
        empty_cells = [(x, y) for y in range(1, self.rows - 1) for x in range(1, self.cols - 1) if self.grid[y][x].empty]
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.grid[y][x].set_apple()
    
    def move_snake(self, snake, direction):

        #direction[0] = dx, direction[1] = dy, snake = [(x1,y1), (x2,y2), ...], snake[0][0] = x1, snake[0][1] = y1
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1]) 
        
        x, y = new_head
        if self.grid[y][x].apple:
            new_snake = [new_head] + snake[:]
            self.score += 1
        elif self.grid[y][x].wall or self.grid[y][x].snake:
            print("Game Over! Final Score:", self.score)
            pygame.quit()
            exit()
            raise SystemExit
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
        
        #print(f"Mouse Position: {mouse_pos}, Mouse Buttons: {mouse_buttons}")
        
        # Exit the game if ESC is pressed
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
            raise SystemExit   
        
        # spwan apple if there is none
        if not any(cell.apple for row in self.grid for cell in row):
            self.place_apple()
        
        if keys[pygame.K_a]:
            print("Left key pressed")
            if(self.last_action != (1, 0)): #prevent the snake from going back on itself
                self.direction = (-1, 0)  # Move left
        if keys[pygame.K_d]:
            print("Right key pressed")
            if(self.last_action != (-1, 0)): #prevent the snake from going back on itself
                self.direction = (1, 0)   # Move right
        if keys[pygame.K_w]:
            print("Up key pressed")
            if(self.last_action != (0, 1)): #prevent the snake from going back on itself
                self.direction = (0, -1)  # Move up
        if keys[pygame.K_s]:
            print("Down key pressed")
            if(self.last_action != (0, -1)): #prevent the snake from going back on itself
                self.direction = (0, 1)   # Move down     
        
        # Move the snake only if enough time has passed & 
        if current_time - self.last_move_time >= self.move_delay:
            self.snake = self.move_snake(self.snake, self.direction)
            self.last_move_time = current_time 
            self.last_action = self.direction # Update last action to current direction, used to prevent reversing direction

#width 600; height 530;
# 17 x 15; 17 across the top and 15 down the side