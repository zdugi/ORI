import math
import time
import numpy as np

directions = [UP, DOWN, LEFT, RIGHT] = range(4)
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
        monotonocity = 0

        big_t = np.sum(np.power(grid, 2))
        smoothness -= np.sum(np.abs(grid[::, 0] - grid[::, 1]))
        smoothness -= np.sum(np.abs(grid[::, 1] - grid[::, 2]))
        smoothness -= np.sum(np.abs(grid[::, 2] - grid[::, 3]))
        smoothness -= np.sum(np.abs(grid[0, ::] - grid[1, ::]))
        smoothness -= np.sum(np.abs(grid[1, ::] - grid[2, ::]))
        smoothness -= np.sum(np.abs(grid[2, ::] - grid[3, ::]))

        # vertical = grid[:, 1:] >= grid[:, :-1]
        # horizontal = grid.T[:, 1:] >= grid.T[:, :-1]
        #
        # for i in range(4):
        #     if not np.all(vertical[i, ::]) and np.any(vertical[i, ::]):
        #         monotonocity -= 1
        #     if not np.all(horizontal[i, ::]) and np.any(horizontal[i, ::]):
        #         monotonocity -= 1

        unique, counts = np.unique(grid, return_counts=True)
        occurrences = dict(zip(unique, counts))

        unmerged = 0

        for occurrence in occurrences:
            if occurrences[occurrence] > 1:
                unmerged -= occurrences[occurrence] * occurrence

        empty_w = 100
        max_corner_w = 2
       # monotonocity_w = 100

        utility += empty_w * num_empty
        utility += smoothness
        #utility += monotonocity * monotonocity_w
        utility += np.sqrt(big_t)
        utility += unmerged

        if board.is_max_in_corner():
            utility += max_corner_w * board.get_max_tile()

        #print(smoothness, utility, monotonocity)
        #print(board.current_merges)
        return None, utility

    def value(self, board, depth=0):
        empty_cells = board.get_available_cells()
        num_empty = len(empty_cells)

        if depth % 2 == 0:
            return self.max_value(board, depth)
        else:
            if num_empty >= 6 and depth > 2:
                return self.eval_heuristic(board, num_empty)
            if num_empty >= 0 and depth > 4:
                return self.eval_heuristic(board, num_empty)
            if num_empty == 0:
                return self.max_value(board, depth)

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


