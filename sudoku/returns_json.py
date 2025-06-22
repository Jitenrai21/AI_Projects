import random
import json
import copy

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

    def find_empty(self):
        """Find an empty cell (0) on the board."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

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
        cells_to_remove = total_cells - clues
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

    def print_grid(self, grid, title):
        """Print the grid in a horizontal, human-readable format."""
        print(f"\n{title}:")
        for i in range(self.grid_size):
            if i % self.block_size == 0 and i != 0:
                print("-" * (self.grid_size * 2 + self.block_size - 1))
            row = []
            for j in range(self.grid_size):
                if j % self.block_size == 0 and j != 0:
                    row.append("|")
                row.append(self.to_display_value(grid[i][j]))
            print(" ".join(row))
        print()

    def to_json(self):
        """Generate JSON output with puzzle and solution."""
        solution = self.generate_puzzle()
        puzzle_display = [[self.to_display_value(num) for num in row] for row in self.board]
        solution_display = [[self.to_display_value(num) for num in row] for row in solution]
        # self.print_grid(self.board, "Puzzle")
        # self.print_grid(solution, "Solution")
        return {
            "grid_size": self.grid_size,
            "block_size": self.block_size,
            "difficulty": self.difficulty,
            "puzzle": puzzle_display,
            "solution": solution_display
        }

def generate_sudoku(grid_size, difficulty):
    """Generate a Sudoku puzzle and return it as JSON string."""
    generator = SudokuGenerator(grid_size, difficulty)
    return json.dumps(generator.to_json(), indent=2)

def main():
    """Main function to get user input and generate puzzle."""
    print("Choose grid size (4 for 4x4, 9 for 9x9, 16 for 16x16):")
    grid_size = int(input())
    print("Choose difficulty (easy, medium, hard):")
    difficulty = input().lower()
    try:
        result = generate_sudoku(grid_size, difficulty)
        print("\nJSON Output:")
        print(result)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()