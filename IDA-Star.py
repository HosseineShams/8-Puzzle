import math

def is_solvable(board):
    """Check if a given 8-puzzle configuration is solvable."""
    size = len(board)
    tiles = [board[i][j] for i in range(size) for j in range(size) if board[i][j] != 0]
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i+1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1

    if size % 2 == 1:
        return inversions % 2 == 0
    else:
        blank_row = [i for i in range(size) for j in range(size) if board[i][j] == 0][0]
        if blank_row % 2 == 0:
            return inversions % 2 == 1
        else:
            return inversions % 2 == 0

def solve_puzzle_ida_star(board, goal, size):
    h = heuristic(board, goal, size)
    bound = h
    g = 0
    move_direction = None
    path = []
    while True:
        result = search(board, goal, size, g, bound, move_direction, path)
        if type(result) == list:
            return result
        bound = result
        path = []
        
def search(board, goal, size, g_cost, bound, move_direction, path):
    h_cost = heuristic(board, goal, size)
    f_cost = g_cost + h_cost
    min_value = math.inf
    solution_dict = {"board": board, "g_cost": g_cost, "h_cost": h_cost, "f_cost": f_cost, "min": min_value, "bound": bound, "direction": move_direction}
    solution_exists = False
    for i in range(len(path)):
        if path[i]["g_cost"] == g_cost:
            path[i] = solution_dict
            solution_exists = True
            break
    if solution_exists == False:
        path.append(solution_dict)
    if f_cost > bound:
        path.pop()
        return f_cost
    if board == goal:
        return path
    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                x = row
                y = col
                break
    for x_value, y_value in [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]:
        if (0 <= x_value < size) and (0 <= y_value < size):
            move_dir = find_direction(x, y, x_value, y_value)
            move_dir_opposite = tuple(map(lambda dir: -1 * dir, move_dir))
            if move_direction != move_dir_opposite:
                new_board = [row[:] for row in board]
                new_board[x][y], new_board[x_value][y_value] = new_board[x_value][y_value], new_board[x][y]
                result = search(new_board, goal, size, g_cost + 1, bound, move_dir, path)
                if type(result) == list:
                    return result
                else:
                    min_value = min(min_value, result)
    return min_value

def heuristic(board, goal, size):
    board_dict = create_dict(board)
    goal_dict = create_dict(goal)
    distance = 0
    for num in range(1, size**2):
        x_dis = abs(goal_dict[num][0] - board_dict[num][0])
        y_dis = abs(goal_dict[num][1] - board_dict[num][1])
        distance += x_dis + y_dis
    return distance

def find_direction(x, y, x_value, y_value):
    if x_value == x+1:
        return (1, 0)
    elif x_value == x-1:
        return (-1, 0)
    elif y_value == y+1:
        return (0, 1)
    elif y_value == y-1:
        return (0, -1)

def create_dict(board):
    board_dict = {}
    for i_index, i in enumerate(board):
        for j_index, j in enumerate(i):
            board_dict[j] = (i_index, j_index)
    return board_dict

def main():
    goal = [
        [1,2,3],
        [4,5,6],
        [7,8,0],
    ]
    print(goal)
    board = []
    for i in range(3):
        row = input(f"Enter values for row {i+1}, separated by spaces: ").split()
        board.append([int(x) for x in row])
    print(board)
    if not is_solvable(board):
        print("This puzzle configuration is not solvable!")
        return
    size = len(board)
    solution = solve_puzzle_ida_star(board, goal, size)
    for state in solution:
        print(state)

if __name__ == "__main__":
    main()
