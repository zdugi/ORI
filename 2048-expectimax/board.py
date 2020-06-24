import numpy as np

dirs = [UP, DOWN, LEFT, RIGHT] = range(4)


def merge_left(matrix):
    for i in range(4):
        for j in range(3):
            if matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0:
                matrix[i][j] *= 2
                matrix[i][j + 1] = 0
    return matrix


def merge_right(matrix):
    for i in reversed(range(4)):
        for j in range(3, 0, -1):
            if matrix[i][j] == matrix[i][j - 1] and matrix[i][j] != 0:
                matrix[i][j] *= 2
                matrix[i][j - 1] = 0
    return matrix


def merge_up(matrix):
    for j in range(4):
        for i in range(3):
            if matrix[i][j] == matrix[i + 1][j] and matrix[i][j] != 0:
                matrix[i][j] *= 2
                matrix[i + 1][j] = 0
    return matrix


def merge_down(matrix):
    for j in reversed(range(4)):
        for i in range(3, 0, -1):
            if matrix[i][j] == matrix[i - 1][j] and matrix[i][j] != 0:
                matrix[i][j] *= 2
                matrix[i - 1][j] = 0
    return matrix


def align_left(matrix, out):
    for i in [0, 1, 2, 3]:
        new_pos = 0
        for j in [0, 1, 2, 3]:
            if matrix[i][j] != 0:
                out[i][new_pos] = matrix[i][j]
                new_pos += 1
    return out


def align_right(matrix, out):
    for i in range(4):
        new_pos = 3
        for j in reversed(range(4)):
            if matrix[i][j] != 0:
                out[i][new_pos] = matrix[i][j]
                new_pos -= 1
    return out


def align_up(matrix, out):
    for j in range(4):
        new_pos = 0
        for i in range(4):
            if matrix[i][j] != 0:
                out[new_pos][j] = matrix[i][j]
                new_pos += 1
    return out


def align_down(matrix, out):
    for j in range(4):
        new_pos = 3
        for i in reversed(range(4)):
            if matrix[i][j] != 0:
                out[new_pos][j] = matrix[i][j]
                new_pos -= 1
    return out


class GameBoard:
    def __init__(self):
        self.grid = np.zeros((4, 4))

    def clone(self):
        grid_copy = GameBoard()
        grid_copy.grid = np.copy(self.grid)
        return grid_copy

    def insert_tile(self, pos, value):
        self.grid[pos[0]][pos[1]] = value

    def get_available_cells(self):
        cells = []
        for x in range(4):
            for y in range(4):
                if self.grid[x][y] == 0:
                    cells.append((x, y))
        return cells

    def get_max_tile(self):
        return np.amax(self.grid)

    def move(self, direction):
        z1 = np.zeros((4, 4))
        z2 = np.zeros((4, 4))

        if direction == UP:
            self.grid = align_up(self.grid, z1)
            self.grid = merge_up(self.grid)
            self.grid = align_up(self.grid, z2)
        if direction == DOWN:
            self.grid = align_down(self.grid, z1)
            self.grid = merge_down(self.grid)
            self.grid = align_down(self.grid, z2)
        if direction == LEFT:
            self.grid = align_left(self.grid, z1)
            self.grid = merge_left(self.grid)
            self.grid = align_left(self.grid, z2)
        if direction == RIGHT:
            self.grid = align_right(self.grid, z1)
            self.grid = merge_right(self.grid)
            self.grid = align_right(self.grid, z2)

    def get_cell_value(self, pos):
        return self.grid[pos[0]][pos[1]]
