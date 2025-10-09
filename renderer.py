import pygame

class Renderer:
    def render(self, screen, grid, cell_size):
        #make the header
        pygame.draw.rect(screen, (74, 117, 44), (0, 0, screen.get_width(), 70))  # Dark green header
        
        #Make the background
        for row_iidx, row in enumerate(grid): #enumerate() adds a counter to an iterable and returns it in a form of enumerating object: "index, value"
            for col_idx, cell in enumerate(row):
                x = col_idx * cell_size
                y = row_iidx * cell_size + 70  # Offset for header
                color = (162, 209, 73)  # Tep Color for empty cell
                if (row_iidx + col_idx) % 2 == 0:
                    color = (170, 215, 81)  # Alternate color for checkerboard effect
                if cell.apple:
                    color = (255, 0, 0)  # Red for apple
                if cell.snake:
                    color = (0, 255, 0)  # Green for snake
                elif cell.wall:
                    color = (87, 138, 52)  # Dark green for wall
                pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
                #pygame.draw.rect(screen, (167, 213, 78), (x, y, cell_size, cell_size), 1)  # Cell border
        
#copy() will return a new rectangle having the same position and size as the original!
#move() retuns a new rectangle that is moved by the given offest 
#update() will update the position and size of the rectangle

#dark green box: 162, 209, 73
#light green box: 170, 215, 81
#header: 74, 117, 44
#lines: 167, 213, 78
#wall: 87, 138, 52