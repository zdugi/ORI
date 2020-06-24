import math
import time
import numpy as np

directions = [UP, DOWN, LEFT, RIGHT] = range(4)
states = [COMPUTER, AGENT, TERMINAL] = range(3)


class Expectimax():
    def get_move(self, board):
        pass

    def eval_heuristic(self, board, num_empty):
        pass

    def value(self, board, depth=0):
        pass

    def max_value(self, board, depth=0):
        pass

    def exp_value(self, board, depth=0):
        pass