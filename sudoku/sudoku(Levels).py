import pygame
import asyncio # library for asynchronous programming, used here to manage the game loop at 60 FPS
import platform # to check the execution environment
import random

# Sudoku logic class
class Sudoku:
    def __init__(self, board=None):
        self.board = [[0 for _ in range(9)] for _ in range(9)] if board is None else [row[:] for row in board]
        self.original = [row[:] for row in self.board]
    
    # Checks if placing num at (row, col) follows Sudoku rules.
    def is_valid(self, row, col, num): 
        # Checks for duplicates in the same row and column.
        for x in range(9):
            if self.board[row][x] == num or self.board[x][col] == num:
                return False
        # Checks the 3×3 subgrid.
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        return True
    
    # Sets a number in the cell only if it's not a pre-filled cell and is valid.
    def set_value(self, row, col, num):
        if self.original[row][col] == 0:
            if num == 0 or self.is_valid(row, col, num):
                self.board[row][col] = num
                return True
        return False
    
    # Solves the board using backtracking. Ends when no empty cell remains.
    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        # Randomizes numbers to introduce variability in puzzle generation.
        row, col = empty
        nums = list(range(1, 10))
        random.shuffle(nums)
        # Tries placing a number and recursively attempts to solve the board. If stuck, resets the cell.
        for num in nums:
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0
        return False # Triggers backtracking.
    
    # Finds and returns the next empty cell.
    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    # Creates a full, valid Sudoku board, then removes numbers based on difficulty.
    def generate_puzzle(self, difficulty):
        # Generate a full solution
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve()
        full_board = [row[:] for row in self.board]
        
        # Remove cells based on difficulty
        if difficulty == "easy":
            cells_to_remove = random.randint(40, 50)
        elif difficulty == "medium":
            cells_to_remove = random.randint(30, 40)
        elif difficulty == "hard":
            cells_to_remove = random.randint(20, 30)
        else:
            cells_to_remove = 40
        
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        for i, j in cells[:cells_to_remove]:
            self.board[i][j] = 0
        
        self.original = [row[:] for row in self.board]
        return self.board

# Pygame game class
class SudokuGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 540, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sudoku")
        self.cell_size = self.width // 9
        self.selected = None
        self.running = True
        self.state = "menu"  # menu or game
        self.sudoku = None
        self.font = pygame.font.SysFont("arial", 36)
        self.button_font = pygame.font.SysFont("arial", 24)
        self.error = False
        
        # Button rectangles for difficulty selection
        self.buttons = {
            "easy": pygame.Rect(170, 200, 200, 50),
            "medium": pygame.Rect(170, 270, 200, 50),
            "hard": pygame.Rect(170, 340, 200, 50)
        }
    
    def draw_menu(self):
        self.screen.fill((255, 255, 255))
        title = self.font.render("Select Difficulty", True, (0, 0, 0))
        self.screen.blit(title, (150, 100))
        
        for difficulty, rect in self.buttons.items():
            color = (200, 200, 200)  # Light gray
            pygame.mouse.get_pos()
            pygame.draw.rect(self.screen, color, rect)
            text = self.button_font.render(difficulty.capitalize(), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()
    
    def draw_grid(self):
        self.screen.fill((255, 255, 255))
        for i in range(10):
            width = 4 if i % 3 == 0 else 1  # Thicker lines every 3 rows/columns
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.cell_size, 0), (i * self.cell_size, self.width), width)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.cell_size), (self.width, i * self.cell_size), width)
        
        #Draws the numbers. Blue = user input, black = original, red = invalid entry.
        for i in range(9):
            for j in range(9):
                if self.sudoku.board[i][j] != 0:
                    color = (0, 0, 0) if self.sudoku.original[i][j] != 0 else (0, 0, 255)  # Black for original
                    if self.error and self.selected == (i, j) and not self.sudoku.is_valid(i, j, self.sudoku.board[i][j]):
                        color = (255, 0, 0) # Red for invalid
                    text = self.font.render(str(self.sudoku.board[i][j]), True, color)
                    self.screen.blit(text, (j * self.cell_size + 15, i * self.cell_size + 10))
        
        # Highlights selected cell.
        if self.selected:
            row, col = self.selected
            pygame.draw.rect(self.screen, (255, 255, 0), (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 3)
        
        instr_text = self.button_font.render("Click cell! Enter any digit between 1-9 to input, 0 to clear", True, (0, 0, 0))
        self.screen.blit(instr_text, (10, self.width + 10))
        
        pygame.display.flip()
    
    def handle_menu_click(self, pos):
        for difficulty, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.sudoku = Sudoku()
                self.sudoku.generate_puzzle(difficulty)
                self.state = "game"
                self.draw_grid()
                break
    
    def handle_game_click(self, pos):
        x, y = pos
        if y < self.width:
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
                if self.state == "menu":
                    self.handle_menu_click(event.pos)
                else:
                    self.handle_game_click(event.pos)
            elif event.type == pygame.KEYDOWN and self.state == "game":
                self.handle_key(event.key)
        
        if self.state == "menu":
            self.draw_menu()
        else:
            self.draw_grid()
    
    def setup(self):
        self.draw_menu()

# Main Asynchronous Execution
async def main():
    game = SudokuGame()
    game.setup()
    while game.running:
        game.update_loop()
        await asyncio.sleep(1.0 / 60) # Runs the game at 60 FPS using asyncio.

if platform.system() == "Emscripten": # If running in browser (e.g., via Pyodide/WebAssembly), ensure_future is used.
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())