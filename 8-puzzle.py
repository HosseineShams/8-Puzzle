import copy

# Class to represent the puzzle board and its operations
class PuzzleBoard:
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
    
    def print_board(self):
        for row in self.board:
            print(" ".join(map(str, row)))
    
    def is_solvable(self):
        flat_board = [cell for row in self.board for cell in row if cell != 0]
        inversions = sum(1 for i in range(len(flat_board)) for j in range(i + 1, len(flat_board)) if flat_board[i] > flat_board[j])
        return inversions % 2 == 0
    
    def find_zero(self):
        for row_idx, row in enumerate(self.board):
            for col_idx, cell in enumerate(row):
                if cell == 0:
                    return row_idx, col_idx
    
    def is_valid_move(self, move):
        row_idx, col_idx = self.find_zero()
        if move == "up":
            return row_idx > 0
        elif move == "down":
            return row_idx < self.rows - 1
        elif move == "left":
            return col_idx > 0
        elif move == "right":
            return col_idx < self.cols - 1
    
    def make_move(self, move):
        new_board = copy.deepcopy(self.board)
        row_idx, col_idx = self.find_zero()
        if move == "up":
            new_board[row_idx][col_idx], new_board[row_idx - 1][col_idx] = new_board[row_idx - 1][col_idx], new_board[row_idx][col_idx]
        elif move == "down":
            new_board[row_idx][col_idx], new_board[row_idx + 1][col_idx] = new_board[row_idx + 1][col_idx], new_board[row_idx][col_idx]
        elif move == "left":
            new_board[row_idx][col_idx], new_board[row_idx][col_idx - 1] = new_board[row_idx][col_idx - 1], new_board[row_idx][col_idx]
        elif move == "right":
            new_board[row_idx][col_idx], new_board[row_idx][col_idx + 1] = new_board[row_idx][col_idx + 1], new_board[row_idx][col_idx]
        return PuzzleBoard(new_board)

def main():
    initial_board = [[1, 2, 3], [4, 5, 0], [7, 8, 6]]
    puzzle_board = PuzzleBoard(initial_board)
    
    if not puzzle_board.is_solvable():
        print("The starting board is not solvable.")
        return
    
    while True:
        puzzle_board.print_board()
        move = input("Enter a move (up, down, left, right): ")
        if puzzle_board.is_valid_move(move):
            puzzle_board = puzzle_board.make_move(move)
        else:
            print("Invalid move. Try again.")

if __name__ == '__main__':
    main()
