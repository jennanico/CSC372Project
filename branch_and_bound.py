'''
Branch and bound algorithm for bin packing

Usage:
    branch_and_bound.py [item_input_file] int_weight_limit

    Example usage:
        python branch_and_bound.py dummy_input.txt 50

'''
import sys
import copy
from bisect import insort
import math
from greedy import (compute_greedy)

class BinPackSolver():
    def __init__(self, weight_limit: int, items: list):
        self.weight_limit = weight_limit
        self.items = items

    ## might be able to do a better initial bound
    def get_root(self):
        bins = [[0]]
        return BinPackTN(bins,1,1,len(self.items),self)
    
    def find_solution(self):
        PQ: list[BinPackTN] = [self.get_root()]
        best_node = BinPackTN(PQ[0].bins,PQ[0].item_to_add,PQ[0].bound,PQ[0].bound,self)

        while PQ != []:
            most_promising = PQ.pop()
            for child in most_promising.get_children():
                if child.has_better_value(best_node):
                    best_node = child
                if child.might_be_better_than(best_node):
                    insort(PQ, child)
        return best_node

class BinPackTN():
    def __init__(self,
                 bins: list,
                 item_to_add: int,
                 bins_used: int,
                 bound: int,
                 solver: BinPackSolver):
        self.bins = bins
        self.item_to_add = item_to_add
        self.bins_used = bins_used
        self.bound = bound
        self.solver = solver
    
    def compute_bound(self):
        new_bins = copy.deepcopy(self.bins)
        num_bins = 0
        bin_array = [[]]
        num_bins, bin_array = compute_greedy(new_bins, self.item_to_add, self.solver.items, self.solver.weight_limit)
        #print(math.floor(num_bins / 1.5))
        return math.floor(num_bins / 1.5)
    
    def might_be_better_than(self, other):
        return self.bound <= other.bins_used
    
    def has_better_value(self, other):
        return (self.bins_used <= other.bins_used and 
                self.item_to_add == len(self.solver.items))
    
    def __lt__(self, other):
        return self.might_be_better_than(other)
    
    def get_children(self):
        if self.item_to_add == len(self.solver.items):
            return []
        children = []
        for bin in range(len(self.bins)):
            ##if item fits add to bin - stops us from creating invalid nodes
            if (self.solver.items[self.item_to_add]) + self.bin_capasity(bin) <= self.solver.weight_limit:
                new_bins = copy.deepcopy(self.bins)
                new_bins[bin].append(self.item_to_add)
                child = BinPackTN(new_bins,
                                  self.item_to_add + 1,
                                  self.bins_used,
                                  0,
                                  self.solver)
                child.bound = child.compute_bound()
                children.append(child)
        new_bins = copy.deepcopy(self.bins)
        new_bins.append([])
        new_bins[len(self.bins)].append(self.item_to_add)
        child = BinPackTN(new_bins,
                          self.item_to_add + 1,
                          self.bins_used + 1,
                          0,
                          self.solver)
        child.bound = child.compute_bound()
        children.append(child)
        return children
    
    def bin_capasity(self, bin):
        total_weight = 0
        for item in self.bins[bin]:
            total_weight = total_weight + self.solver.items[item]
        return total_weight

def main():
    input_values = sys.argv[1]
    weight_limit = int(sys.argv[2])
    file_input = open(input_values,'r')
    with open(input_values, 'r') as file:
        items = [int(line.strip()) for line in file]
    file_input.close()
    items.sort(reverse=True)
    BinPack = BinPackSolver(weight_limit, items)
    best_sol = BinPack.find_solution()

    print(best_sol.bins_used)
    for bin in best_sol.bins:
        print (bin)
          
if __name__ == "__main__":
    main()