import numpy as np
from board import Board
from copy import deepcopy


class Solver:

    def __init__(self):
        self.temperature = 99
        self.temperature_after_reheat = 50
        self.reheat_limit = 3000
        self.reheat = 0
        self.reheat_count = 0
        self.cooling_rate = 0.999
        self.start = Board(None, 0)

    def read_file(self, filename):
        data = np.genfromtxt(filename, delimiter=",", dtype=np.int32)

        self.start = Board(data, int(np.sqrt(data.shape[0])))
        self.start.init_random()
        self.start.calculate_row_and_col_cost()
        self.start.cost = self.start.calculate_total_cost()
        self.start.print_board()

    def solve(self):

        for x in range(10000000000):
            if self.start.cost > 0:
                #print(str(self.start.cost) + " " + str(self.start.calculate_total_cost()))
                self.annealing()
            else:
                self.start.print_board()
                print("DONE")
                return

    def update_temperature(self):
        self.temperature *= self.cooling_rate
        self.check_for_reheat()

    def check_for_reheat(self):
        if self.reheat >= self.reheat_limit:
            print("Stuck at local minima. Reheating...")
            self.temperature = self.temperature_after_reheat
            self.reheat = 0
            self.reheat_count += 1

    def annealing(self):

        element1, element2 = self.start.pick_random()

        self.start.swap(element1[0], element1[1], element2[0], element2[1])

        row1_old = self.start.row_costs[element1[0]]
        col1_old = self.start.col_costs[element1[1]]
        row2_old = self.start.row_costs[element2[0]]
        col2_old = self.start.col_costs[element2[1]]

        row1_new = self.start.calculate_cost_row(element1[0])
        col1_new = self.start.calculate_cost_col(element1[1])
        row2_new = self.start.calculate_cost_row(element2[0])
        col2_new = self.start.calculate_cost_col(element2[1])

        cost_diff = row1_new - row1_old
        cost_diff += col1_new - col1_old
        cost_diff += row2_new - row2_old
        cost_diff += col2_new - col2_old

        if cost_diff < 0:
            self.start.cost += cost_diff
            self.reheat = 0
            print("Improvement of cost by: " + str(cost_diff) + " and current cost: ", self.start.cost)
            self.update_temperature()

        else:
            probability_true = self.temperature / 100
            probability_false = 1 - probability_true

            choice = np.random.choice([True, False], 1, p=[probability_true, probability_false])[0]

            if choice:
                self.reheat = 0
                self.start.cost += cost_diff
            else:
                self.reheat += 1
                self.start.swap(element1[0], element1[1], element2[0], element2[1])
                self.start.row_costs[element1[0]] = row1_old
                self.start.row_costs[element2[0]] = row2_old
                self.start.col_costs[element1[1]] = col1_old
                self.start.col_costs[element2[1]] = col2_old

            self.update_temperature()


if __name__ == '__main__':
    solver = Solver()
    solver.read_file("c1.txt")
    solver.solve()