import pygame
import sys
from tetris import Tetris

# Initialize Pygame
pygame.init()

# Set up display
block_size = 30
grid_width = 10
grid_height = 20
sidebar_width = 200

window_width = grid_width * block_size + sidebar_width
window_height = grid_height * block_size

# Create the game window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Upside-Down Tetris")

# Create the game instance
game = Tetris(window_width, window_height, block_size)

# Set up the clock
clock = pygame.time.Clock()
fps = 60

def main():
    running = True
    
    # Game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_UP:
                    game.drop()  # UP means move upward in our upside-down game
                elif event.key == pygame.K_DOWN:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
                elif event.key == pygame.K_p:
                    game.toggle_pause()
                elif event.key == pygame.K_r:
                    if game.game_over:
                        game.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update game state
        game.update()
        
        # Draw game
        window.fill((0, 0, 0))
        game.draw(window)
        pygame.display.update()
        
        # Cap the frame rate
        clock.tick(fps)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
