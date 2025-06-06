import pygame
import random
from colors import BG_COLOR, GRID_COLOR, TEXT_COLOR, BORDER_COLOR, COLORS
from tetromino import Tetromino

class Tetris:
    def __init__(self, width, height, block_size=30):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.grid_width = 10
        self.grid_height = 20
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.current_piece = None
        self.next_piece = None
        self.spawn_piece()
        
        # Initialize game speed
        self.drop_speed = 1000  # milliseconds between automatic drops
        self.last_drop_time = pygame.time.get_ticks()
        
        # Fonts
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 36)

    def create_surface(self):
        """Create a new surface for the game."""
        # Main game area plus sidebar for next piece and score
        total_width = self.grid_width * self.block_size + 200
        total_height = self.grid_height * self.block_size
        return pygame.Surface((total_width, total_height))

    def spawn_piece(self):
        """Spawn a new tetromino at the bottom of the grid."""
        shapes = ["I", "J", "L", "O", "S", "T", "Z"]
        
        if self.next_piece:
            self.current_piece = self.next_piece
        else:
            shape = random.choice(shapes)
            self.current_piece = Tetromino(self.grid_width // 2 - 2, self.grid_height - 5, shape)
            
        # Generate the next piece
        shape = random.choice(shapes)
        self.next_piece = Tetromino(self.grid_width // 2 - 2, self.grid_height - 5, shape)
        
        # Check if the new piece can be placed
        if self.check_collision():
            self.game_over = True

    def check_collision(self, dx=0, dy=0, rotated_piece=None):
        """Check if the tetromino collides with the grid or boundaries."""
        piece_to_check = rotated_piece if rotated_piece else self.current_piece
        blocks = piece_to_check.get_blocks()
        
        for x, y in blocks:
            x += dx
            y += dy
            
            if x < 0 or x >= self.grid_width or y < 0 or y >= self.grid_height:
                return True
                
            if 0 <= y < self.grid_height and self.grid[y][x] != 0:
                return True
                
        return False

    def merge_piece_with_grid(self):
        """Merge the current piece with the grid."""
        blocks = self.current_piece.get_blocks()
        
        for x, y in blocks:
            if y >= 0:
                self.grid[y][x] = self.current_piece.color
                
        self.check_lines()
        self.spawn_piece()
        
    def check_lines(self):
        """Check and clear completed lines."""
        lines_to_clear = []
        
        for y in range(self.grid_height):
            if all(self.grid[y][x] != 0 for x in range(self.grid_width)):
                lines_to_clear.append(y)
                
        for y in lines_to_clear:
            # Clear the line
            # Move everything down instead of up (since we're playing upside down)
            for i in range(y, self.grid_height-1):
                self.grid[i] = self.grid[i+1].copy()
            self.grid[self.grid_height-1] = [0 for _ in range(self.grid_width)]
        
        # Update score
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            self.score += (100 * len(lines_to_clear)) * len(lines_to_clear)  # More lines = higher score multiplier
            self.level = self.lines_cleared // 10 + 1
            self.drop_speed = max(100, 1000 - (self.level - 1) * 100)  # Speed up as level increases
    
    def move(self, dx, dy):
        """Move the current piece if possible."""
        if not self.game_over and not self.paused:
            if not self.check_collision(dx, dy):
                self.current_piece.x += dx
                self.current_piece.y += dy
                return True
        return False
    
    def rotate(self):
        """Rotate the current piece if possible."""
        if not self.game_over and not self.paused:
            # Create a temporary piece for rotation
            rotated = Tetromino(self.current_piece.x, self.current_piece.y, self.current_piece.shape)
            rotated.rotation = self.current_piece.rotation
            rotated.rotate()
            
            # Check if rotation is possible
            if not self.check_collision(0, 0, rotated):
                self.current_piece.rotate()
                return True
                
            # Try wall kicks
            for dx in [-1, 1, -2, 2]:
                if not self.check_collision(dx, 0, rotated):
                    self.current_piece.rotate()
                    self.current_piece.x += dx
                    return True
                    
        return False
    
    def drop(self):
        """Drop (move up) the current piece by one cell."""
        if not self.game_over and not self.paused:
            if not self.check_collision(0, -1):
                self.current_piece.y -= 1
                return True
            else:
                self.merge_piece_with_grid()
                return False
        return False
    
    def hard_drop(self):
        """Drop the current piece to the top."""
        if not self.game_over and not self.paused:
            while not self.check_collision(0, -1):
                self.current_piece.y -= 1
            self.merge_piece_with_grid()
    
    def update(self):
        """Update game state."""
        if not self.game_over and not self.paused:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_drop_time > self.drop_speed:
                self.drop()
                self.last_drop_time = current_time
    
    def toggle_pause(self):
        """Toggle game pause state."""
        self.paused = not self.paused
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.spawn_piece()
        self.drop_speed = 1000
        self.last_drop_time = pygame.time.get_ticks()
    
    def draw(self, surface):
        """Draw the game state to the given surface."""
        surface.fill(BG_COLOR)
        
        # Draw grid
        grid_width_px = self.grid_width * self.block_size
        grid_height_px = self.grid_height * self.block_size
        
        # Draw border
        pygame.draw.rect(surface, BORDER_COLOR, (0, 0, grid_width_px, grid_height_px), 2)
        
        # Draw grid lines
        for x in range(0, grid_width_px + 1, self.block_size):
            pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, grid_height_px), 1)
        for y in range(0, grid_height_px + 1, self.block_size):
            pygame.draw.line(surface, GRID_COLOR, (0, y), (grid_width_px, y), 1)
        
        # Draw placed blocks
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid[y][x] != 0:
                    self.draw_block(surface, x, y, self.grid[y][x])
        
        # Draw current piece
        if self.current_piece:
            for x, y in self.current_piece.get_blocks():
                if y >= 0:  # Only draw visible blocks
                    self.draw_block(surface, x, y, self.current_piece.color)
        
        # Draw sidebar
        sidebar_x = grid_width_px + 10
        
        # Draw next piece preview
        preview_text = self.font.render("Next:", True, TEXT_COLOR)
        surface.blit(preview_text, (sidebar_x, 30))
        
        # Draw the next piece
        if self.next_piece:
            preview_x = sidebar_x + 50
            preview_y = 80
            for x, y in self.next_piece.get_blocks():
                # Adjust position for preview (center the piece)
                adjusted_x = preview_x + (x - self.next_piece.x) * self.block_size // 1.5
                adjusted_y = preview_y + (y - self.next_piece.y) * self.block_size // 1.5
                pygame.draw.rect(surface, self.next_piece.color, 
                                 (adjusted_x, adjusted_y, 
                                  self.block_size // 1.5, self.block_size // 1.5))
        
        # Draw score, level, and lines
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        level_text = self.font.render(f"Level: {self.level}", True, TEXT_COLOR)
        lines_text = self.font.render(f"Lines: {self.lines_cleared}", True, TEXT_COLOR)
        
        surface.blit(score_text, (sidebar_x, 180))
        surface.blit(level_text, (sidebar_x, 210))
        surface.blit(lines_text, (sidebar_x, 240))
        
        # Draw game over or paused text
        if self.game_over:
            game_over_text = self.big_font.render("GAME OVER", True, TEXT_COLOR)
            text_rect = game_over_text.get_rect(center=(grid_width_px // 2, grid_height_px // 2))
            surface.blit(game_over_text, text_rect)
            
            restart_text = self.font.render("Press R to restart", True, TEXT_COLOR)
            restart_rect = restart_text.get_rect(center=(grid_width_px // 2, grid_height_px // 2 + 50))
            surface.blit(restart_text, restart_rect)
        elif self.paused:
            paused_text = self.big_font.render("PAUSED", True, TEXT_COLOR)
            text_rect = paused_text.get_rect(center=(grid_width_px // 2, grid_height_px // 2))
            surface.blit(paused_text, text_rect)
    
    def draw_block(self, surface, x, y, color):
        """Draw a single block at the given grid coordinates."""
        rect = pygame.Rect(
            x * self.block_size + 1,  # +1 to account for grid lines
            y * self.block_size + 1,
            self.block_size - 2,      # -2 to account for grid lines
            self.block_size - 2
        )
        pygame.draw.rect(surface, color, rect)
        # Draw a 3D effect
        pygame.draw.line(surface, self.lighten_color(color), 
                        (rect.left, rect.top), (rect.right, rect.top), 2)
        pygame.draw.line(surface, self.lighten_color(color), 
                        (rect.left, rect.top), (rect.left, rect.bottom), 2)
        pygame.draw.line(surface, self.darken_color(color), 
                        (rect.right, rect.top), (rect.right, rect.bottom), 2)
        pygame.draw.line(surface, self.darken_color(color), 
                        (rect.left, rect.bottom), (rect.right, rect.bottom), 2)
    
    def lighten_color(self, color):
        """Return a lighter version of the given color."""
        r, g, b = color
        return min(255, r + 40), min(255, g + 40), min(255, b + 40)
    
    def darken_color(self, color):
        """Return a darker version of the given color."""
        r, g, b = color
        return max(0, r - 40), max(0, g - 40), max(0, b - 40)
