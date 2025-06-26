from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import random
import json
import copy
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the API key from environment variable
PROGRAM_API_KEY = os.getenv("PROGRAM_API_KEY")

# Existing SudokuGenerator class (same as before)
class SudokuGenerator:
    def __init__(self, grid_size, difficulty):
        """Initialize Sudoku with specified grid size and difficulty."""
        self.grid_size = grid_size
        self.block_size = int(grid_size ** 0.5)  # 2 for 4x4, 3 for 9x9, 4 for 16x16
        self.difficulty = difficulty.lower()
        self.board = [[0] * grid_size for _ in range(grid_size)]
        self.valid_sizes = {4: 2, 9: 3, 16: 4}  # Grid size to block size mapping
        if grid_size not in self.valid_sizes:
            raise ValueError("Invalid grid size. Choose 4, 9, or 16.")
        if difficulty.lower() not in ["easy", "medium", "hard"]:
            raise ValueError("Invalid difficulty. Choose easy, medium, or hard.")

    def is_valid(self, row, col, num):
        """Check if placing num at (row, col) is valid."""
        for x in range(self.grid_size):
            if self.board[row][x] == num or self.board[x][col] == num:
                return False
        start_row, start_col = self.block_size * (row // self.block_size), self.block_size * (col // self.block_size)
        for i in range(self.block_size):
            for j in range(self.block_size):
                if self.board[start_row + i][start_col + j] == num:
                    return False
        return True

    def find_empty(self):
        """Find an empty cell (0) on the board."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def solve(self):
        """Solve the Sudoku board using backtracking."""
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty
        nums = list(range(1, self.grid_size + 1))
        random.shuffle(nums)
        for num in nums:
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0
        return False

    def generate_puzzle(self):
        """Generate a Sudoku puzzle with specified difficulty."""
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.solve()
        solution = copy.deepcopy(self.board)
        total_cells = self.grid_size * self.grid_size
        if self.difficulty == "easy":
            clues = int(total_cells * random.uniform(0.5, 0.6))
        elif self.difficulty == "medium":
            clues = int(total_cells * random.uniform(0.3, 0.5))
        else:  # hard
            clues = int(total_cells * random.uniform(0.2, 0.3))
        cells_to_remove = total_cells - clues # removing values
        cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size)]
        random.shuffle(cells)
        for i, j in cells[:cells_to_remove]:
            self.board[i][j] = 0
        return solution

    def to_display_value(self, num):
        """Convert number to display value (e.g., 10->A for 16x16)."""
        if self.grid_size == 16 and num >= 10:
            return chr(ord('A') + (num - 10))  # 10=A, 11=B, ..., 16=G
        return str(num) if num != 0 else "."

    def to_json(self):
        """Generate JSON output with puzzle and solution."""
        solution = self.generate_puzzle()
        puzzle_display = [[self.to_display_value(num) for num in row] for row in self.board]
        solution_display = [[self.to_display_value(num) for num in row] for row in solution]
        return {
            "grid_size": self.grid_size,
            "block_size": self.block_size,
            "difficulty": self.difficulty,
            "puzzle": puzzle_display,
            "solution": solution_display
        }

    # Rest of the Sudoku logic remains the same...

# FastAPI setup
app = FastAPI()

# Pydantic request model for validation
class SudokuRequest(BaseModel):
    grid_size: int
    difficulty: str

@app.post("/generate_sudoku")
async def generate_sudoku(request: SudokuRequest, authorization: str = Header(None)):
    """Generate a Sudoku puzzle and return it as a JSON response."""
    # 1. Validate API key
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")
    
    token = authorization.split(" ")[1]
    if token != PROGRAM_API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized API key.")

    try:
        generator = SudokuGenerator(request.grid_size, request.difficulty)
        puzzle_data = generator.to_json()
        return puzzle_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the Sudoku Generator API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
# uvicorn main:app --reload