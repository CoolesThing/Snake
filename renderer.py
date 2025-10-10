import pygame

class Renderer:      
    def render_start_screen(self, screen):
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # RGBA: semi-transparent black

        # Blit the overlay onto the screen
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont(None, 55)
        title_text = font.render("Snake Game", True, (255, 255, 255))
        instruction_text = font.render("Press any key to start", True, (255, 255, 255))
        screen.blit(title_text, ((screen.get_width() - title_text.get_width()) // 2, screen.get_height() // 3))
        screen.blit(instruction_text, ((screen.get_width() - instruction_text.get_width()) // 2, screen.get_height() // 2))
        
    def render(self, screen, grid, cell_size):
        #make the header
        pygame.draw.rect(screen, (74, 117, 44), (0, 0, screen.get_width(), 70))  # Dark green header
        
        #Handle drawing the grid + recoloring cells based on their current state(s)
        for row_iidx, row in enumerate(grid): #enumerate() adds a counter to an iterable and returns it in a form of enumerating object: "index, value"
            for col_idx, cell in enumerate(row):
                x = col_idx * cell_size
                y = row_iidx * cell_size + 70  # Offset for header
                color = (162, 209, 73)  # Green color for empty cell
                if (row_iidx + col_idx) % 2 == 0:
                    color = (170, 215, 81)  # Alternate green color for checkerboard effect
                if cell.apple:
                    color = (255, 0, 0)  # Red for apple
                if cell.snake:
                    color = (77, 123, 227)  # Blue for snake
                elif cell.wall:
                    color = (87, 138, 52)  # Dark green for wall
                pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
                
    def render_end_screen(self, screen):
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # RGBA: semi-transparent black

        # Blit the overlay onto the screen
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont(None, 55)
        title_text = font.render("Game over", True, (255, 255, 255))
        instruction_text = font.render("Press any key to start", True, (255, 255, 255))
        screen.blit(title_text, ((screen.get_width() - title_text.get_width()) // 2, screen.get_height() // 3))
        screen.blit(instruction_text, ((screen.get_width() - instruction_text.get_width()) // 2, screen.get_height() // 2))
        
