import pygame
import asyncio
import platform

# Sudoku logic class
class Sudoku:
    def __init__(self, board):
        self.board = [row[:] for row in board]
        self.original = [row[:] for row in board]  # Track original puzzle
    
    def is_valid(self, row, col, num):
        for x in range(9):
            if self.board[row][x] == num or self.board[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        return True
    
    def set_value(self, row, col, num):
        if self.original[row][col] == 0:  # Only allow changes to non-original cells
            if num == 0 or self.is_valid(row, col, num):
                self.board[row][col] = num
                return True
        return False

# Pygame game class
class SudokuGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 540, 600  # Extra space for buttons
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sudoku")
        self.cell_size = self.width // 9
        self.selected = None
        self.running = True
        
        # Example puzzle
        self.puzzle = [
            [5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]
        ]
        self.sudoku = Sudoku(self.puzzle)
        self.font = pygame.font.SysFont("arial", 36)
        self.error = False
    
    def draw_grid(self):
        self.screen.fill((255, 255, 255))
        # Draw grid lines
        for i in range(10):
            width = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.cell_size, 0), (i * self.cell_size, self.width), width)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.cell_size), (self.width, i * self.cell_size), width)
        
        # Draw numbers
        for i in range(9):
            for j in range(9):
                if self.sudoku.board[i][j] != 0:
                    color = (0, 0, 0) if self.sudoku.original[i][j] != 0 else (0, 0, 255)
                    if self.error and self.selected == (i, j) and not self.sudoku.is_valid(i, j, self.sudoku.board[i][j]):
                        color = (255, 0, 0)
                    text = self.font.render(str(self.sudoku.board[i][j]), True, color)
                    self.screen.blit(text, (j * self.cell_size + 15, i * self.cell_size + 10))
        
        # Highlight selected cell
        if self.selected:
            row, col = self.selected
            pygame.draw.rect(self.screen, (255, 255, 0), (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 3)
        
        # Draw instructions
        instr_font = pygame.font.SysFont("arial", 20)
        instr_text = instr_font.render("Click cell, press 1-9 to input, 0 to clear", True, (0, 0, 0))
        self.screen.blit(instr_text, (10, self.width + 10))
        
        pygame.display.flip()
    
    def handle_click(self, pos):
        x, y = pos
        if y < self.width:  # Click within grid
            row, col = y // self.cell_size, x // self.cell_size
            self.selected = (row, col)
            self.error = False
    
    def handle_key(self, key):
        if self.selected and key in range(pygame.K_0, pygame.K_9 + 1):
            row, col = self.selected
            num = int(pygame.key.name(key)) if key != pygame.K_0 else 0
            if not self.sudoku.set_value(row, col, num):
                self.error = True
    
    def update_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                self.handle_key(event.key)
        self.draw_grid()
    
    def setup(self):
        self.draw_grid()

async def main():
    game = SudokuGame()
    game.setup()
    while game.running:
        game.update_loop()
        await asyncio.sleep(1.0 / 60)  # 60 FPS

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())