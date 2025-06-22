class Sudoku:
    def __init__(self):
        # Initialize empty 9x9 board
        self.board = [[0 for _ in range(9)] for _ in range(9)]
    
    def print_board(self):
        # Print the Sudoku board in a readable format
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - ")
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(self.board[i][j] if self.board[i][j] != 0 else ".", end=" ")
            print()
    
    def is_valid(self, row, col, num):
        # Check if placing num at board[row][col] is valid
        
        # Check row
        for x in range(9):
            if self.board[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if self.board[x][col] == num:
                return False
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def solve(self):
        # Solve the Sudoku puzzle using backtracking
        empty = self.find_empty()
        if not empty:
            return True  # Puzzle is solved
        
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                
                if self.solve():
                    return True
                
                self.board[row][col] = 0  # Backtrack
        
        return False
    
    def find_empty(self):
        # Find an empty cell (value 0) on the board
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def set_board(self, board):
        # Set the board with a given 9x9 list
        if len(board) == 9 and all(len(row) == 9 for row in board):
            self.board = [row[:] for row in board]
        else:
            raise ValueError("Invalid board dimensions")

# Example usage
if __name__ == "__main__":
    # Example puzzle (0 represents empty cells)
    puzzle = [
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
    
    sudoku = Sudoku()
    sudoku.set_board(puzzle)
    print("Initial puzzle:")
    sudoku.print_board()
    
    if sudoku.solve():
        print("\nSolved puzzle:")
        sudoku.print_board()
    else:
        print("\nNo solution exists")