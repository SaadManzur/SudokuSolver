import numpy as np
from copy import deepcopy


class Board:

    def __init__(self, data, order):
        self.data = deepcopy(data)
        self.order = order
        self.dimension = order * order
        self.col_costs = np.zeros(self.dimension)
        self.row_costs = np.zeros(self.dimension)
        self.cost = 0
        self.locked = np.zeros((self.dimension, self.dimension), dtype=bool)

    def init_random(self):
        for i in range(0, self.order):
            for j in range(0, self.order):
                available_values = list(range(1, 10))

                for x in range(3):
                    for y in range(3):
                        current_item = self.get_block_item(i, j, x, y)
                        if current_item > 0:
                            self.locked[i*self.order + x, j*self.order + y] = True
                            available_values.remove(current_item)

                np.random.shuffle(available_values)

                count = 0
                for x in range(3):
                    for y in range(3):
                        if not self.is_locked(x, y, i, j):
                            self.set_block_item(i, j, x, y, available_values[count])
                            count += 1

    def get_block(self, i, j):
        return self.data[i * self.order: i * self.order + self.order, j * self.order: j * self.order + self.order]

    def get_block_item(self, block_x, block_y, i, j):
        return self.data[block_x * self.order + i, block_y*self.order + j]

    def get_row(self, i):
        return self.data[i, :]

    def get_col(self, i):
        return self.data[:, i]

    def is_locked(self, i, j, block_x=None, block_y=None):
        if block_x is not None and block_y is not None:
            return self.locked[block_x * self.order + i, block_y * self.order + j]
        else:
            return self.locked[i, j]

    def set_block_item(self, block_x, block_y, i, j, value):
        self.data[block_x * self.order + i, block_y * self.order + j] = value

    def calculate_cost_single(self, arr):
        exists = np.zeros(self.dimension, dtype=bool)

        cost = 0
        for i in arr:
            if not exists[i-1]:
                exists[i-1] = True

        for i in range(1, self.dimension + 1):
            if not exists[i-1]:
                cost += 1

        return cost

    def calculate_row_and_col_cost(self):
        for i in range(self.dimension):
            self.calculate_cost_row(i)
            self.calculate_cost_col(i)

    def calculate_cost_row(self, i):
        self.row_costs[i] = self.calculate_cost_single(self.data[i, :])
        return self.row_costs[i]

    def calculate_cost_col(self, i):
        self.col_costs[i] = self.calculate_cost_single(self.data[:, i])
        return self.col_costs[i]

    def calculate_total_cost(self):
        cost = 0

        for i in range(self.dimension):
            cost += self.row_costs[i]
            cost += self.col_costs[i]

        return cost

    def pick_random(self):
        block_i, block_j = np.random.randint(0, self.order, 2)

        base_x = block_i * self.order
        base_y = block_j * self.order

        while True:
            i1, j1 = np.random.randint(0, self.order, 2)
            i2, j2 = np.random.randint(0, self.order, 2)

            i1, j1 = i1 + base_x, j1 + base_y
            i2, j2 = i2 + base_x, j2 + base_y

            if i1 != i2 or j1 != j2:
                if not self.locked[i1, j1] and not self.locked[i2, j2]:
                    return (i1, j1), (i2, j2)

    def swap(self, i1, j1, i2, j2):
        temp = self.data[i1, j1]
        self.data[i1, j1] = self.data[i2, j2]
        self.data[i2, j2] = temp

    def print_board(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                print(self.data[i, j], end=",")
            print("[" + str(self.row_costs[i]) + "]")

        for i in range(self.dimension):
            print("[" + str(self.col_costs[i]) + "]", end="")

        print(self.cost)

