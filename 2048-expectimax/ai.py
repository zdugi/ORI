import math
import time
import numpy as np

directions = [UP, DOWN, LEFT, RIGHT] = range(4)
states = [COMPUTER, AGENT, TERMINAL] = range(3)
CHANCE_2 = 0.9
CHANCE_4 = 0.1


def emptiness(x):
    if x > 10:
        return 10000
    elif 6 < x <= 10:
        return 1000
    elif 1 < x <= 6:
        return 100
    else:
        return 10


class Expectimax():
    def get_move(self, board):
        best_move, _ = self.value(board)
        return best_move

    def eval_heuristic(self, board, num_empty):
        grid = board.grid
        utility = 0
        smoothness = 0

        smoothness -= np.sum(np.abs(grid[::, 0] - grid[::, 1]))
        smoothness -= np.sum(np.abs(grid[::, 1] - grid[::, 2]))
        smoothness -= np.sum(np.abs(grid[::, 2] - grid[::, 3]))
        smoothness -= np.sum(np.abs(grid[0, ::] - grid[1, ::]))
        smoothness -= np.sum(np.abs(grid[1, ::] - grid[2, ::]))
        smoothness -= np.sum(np.abs(grid[2, ::] - grid[3, ::]))

        empty_w = emptiness(num_empty)
        max_corner_w = 200

        utility += empty_w * num_empty
        utility += smoothness
        print(smoothness, utility)

        if board.is_max_in_corner() and num_empty >= 4:
            utility += max_corner_w

        return None, utility

    def value(self, board, depth=0):
        empty_cells = board.get_available_cells()
        num_empty = len(empty_cells)

        if depth % 2 == 0:
            if num_empty >= 5 and depth > 1:
                return self.eval_heuristic(board, num_empty)
            if num_empty >= 0 and depth > 3:
                return self.eval_heuristic(board, num_empty)

            return self.max_value(board, depth)
        else:
            return self.exp_value(board, empty_cells, depth)

    def max_value(self, board, depth=0):
        moves = board.get_available_moves()
        moves_boards = []

        for move in moves:
            move_board = board.clone()
            move_board.move(move)
            moves_boards.append((move, move_board))

        max_utility = float('-inf')
        best_direction = None

        for move_board in moves_boards:
            _, utility = self.value(move_board[1], depth + 1)

            if utility >= max_utility:
                max_utility = utility
                best_direction = move_board[0]

        return best_direction, max_utility

    def exp_value(self, board, empty_cells, depth=0):
        possible_tiles = []
        num_empty = len(empty_cells)

        chance_2 = CHANCE_2 * (1 / num_empty)
        chance_4 = CHANCE_4 * (1 / num_empty)

        for empty_cell in empty_cells:
            possible_tiles.append((empty_cell, 2, chance_2))
            possible_tiles.append((empty_cell, 4, chance_4))

        utility_sum = 0

        for tile in possible_tiles:
            tile_board = board.clone()
            tile_board.insert_tile(tile[0], tile[1])

            _, utility = self.value(tile_board, depth + 1)

            utility_sum += utility * tile[2]

        return None, utility_sum


