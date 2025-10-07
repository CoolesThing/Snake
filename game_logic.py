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
        return [[Cell(col, row) for _ in range(cols)] for _ in range(rows)]

class GameLogic:
    def __init__(self, rows, cols):
        self.grid = Cell.create_grid(rows, cols)
        self.rows = rows
        self.cols = cols
        pass
        
    def update(self, input_data):
        # Process input_data and update game state
        keys = input_data['keys']
        mouse_pos = input_data['mouse_pos']
        mouse_buttons = input_data['mouse_buttons']
        
        if keys[pygame.K_a]:
            print("Left key pressed")
        if keys[pygame.K_d]:
            print("Right key pressed")
        if keys[pygame.K_w]:
            print("Up key pressed")
        if keys[pygame.K_s]:
            print("Down key pressed")
            

#width 600; height 530;
# 17 x 15; 17 across the top and 15 down the side